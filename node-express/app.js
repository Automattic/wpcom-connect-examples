require('dotenv').config();
const express = require('express');
const request = require('request');
const cookieParser = require('cookie-parser');
const session = require('express-session');
const crypto = require('crypto');
const wpcc_consts = require('./config.js');

const app = express();
const session_secret = process.env.SESSION_SECRET || 'FixMeBuildBetterSecretThanThis';

app.use(cookieParser());
app.use(
  session({
    secret: session_secret,
    resave: false,
    saveUninitialized: true,
    cookie: { httpOnly: true, secure: false }, // Set secure: true if using HTTPS
  })
);

// Helper to build query string
function buildQuery(params) {
  return Object.entries(params)
    .map(([key, val]) => `${encodeURIComponent(key)}=${encodeURIComponent(val)}`)
    .join('&');
}

app.get('/', (req, res) => {
  // Generate a cryptographically secure random state
  const state = crypto.randomBytes(16).toString('hex');
  req.session.wpcc_state = state;

  const params = {
    response_type: 'code',
    client_id: wpcc_consts.client_id,
    state,
    redirect_uri: wpcc_consts.redirect_url,
  };
  const wpcc_url = `${wpcc_consts.authenticate_url}?${buildQuery(params)}`;

  const body = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Connect to WordPress.com</title>
</head>
<body>
  <h2>Connect to WordPress.com</h2>
  <a href="${wpcc_url}"><img src="//s0.wp.com/i/wpcc-button.png" width="231" alt="Connect with WordPress.com" /></a>
</body>
</html>`;

  res.status(200).send(body);
});

app.get('/connected', (req, res) => {
  const { code, state } = req.query;
  if (code) {
    if (!state) {
      res.status(400).send('Warning! State variable missing after authentication');
      return;
    }
    if (state !== req.session.wpcc_state) {
      res.status(400).send('Warning! State mismatch. Authentication attempt may have been compromised.');
      return;
    }

    const post_data = {
      form: {
        client_id: wpcc_consts.client_id,
        redirect_uri: wpcc_consts.redirect_url,
        client_secret: wpcc_consts.client_secret,
        code,
        grant_type: 'authorization_code',
      },
    };

    request.post(
      wpcc_consts.request_token_url,
      post_data,
      (error, response, body) => {
        if (!error && response.statusCode === 200) {
          // TODO: In a real app, store the returned token securely
          const secret = JSON.parse(body);
          const html = `Access Token: <mark><code>${secret.access_token}</code></mark><br>
This token can be used to request more info about the user to the endpoint: <a href="https://developer.wordpress.com/docs/api/1.1/get/me" target="_blank">https://developer.wordpress.com/docs/api/1.1/get/me</a><br>
Connection successful!`;
          res.status(200).send(html);
        } else {
          // Avoid leaking sensitive info in production
          res.status(response ? response.statusCode : 500).send('ERROR: ' + (body || error.message));
        }
      }
    );
  } else {
    // Redirect errors or cancelled requests back to login page
    res.redirect(303, wpcc_consts.login_url);
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});
