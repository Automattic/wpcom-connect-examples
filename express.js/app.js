var express = require('express');
var app = express();
var request = require('request');

var crypto = require('crypto');
app.use(express.cookieParser());

//TODO: session secret, unique to your application
var session_secret = "FixMeBuildBetterSecretThanThis";

var wpcc_consts = {
	"client_id": 1234, //TODO
	"client_secret": "Your WP.com Secret", //TODO
	"login_url": "http://localhost:3000/", //TODO
	"redirect_url": "http://localhost:3000/connected", //TODO
	"request_token_url": "https://public-api.wordpress.com/oauth2/token",
	"authenticate_url": "https://public-api.wordpress.com/oauth2/authenticate"
}

app.use(express.session({secret: session_secret}));

app.get('/', function(req, res) {
	var state = crypto.createHash('md5').digest("hex");
	req.session.wpcc_state = state;
	
	var params = { 
		"response_type": "code", 
		"client_id": wpcc_consts.client_id, 
		"state": state,
		"redirect_uri": wpcc_consts.redirect_url
	};
	var URLparams = new Array();
	for ( param in params ) {
		URLparams.push( param + '=' + params[param] );
	}
	var wpcc_url = wpcc_consts.authenticate_url + '?' + URLparams.join('&');

	var body = '<html>';
	body += '<body>';
  body += '<h2>Connect to Trafalgar Square</h2>';
	body += '<a href="' + wpcc_url +'"><img src="//s0.wp.com/i/wpcc-button.png" width="231" /></a>';
	body += '</body>';
	body += '</html>';

  res.end(body);
});

app.get('/connected', function(req, res) {
	if ( req.query.code ) {
		if ( ! req.query.state ) {
			res.end( 'Warning! State variable missing after authentication' );
			return;
		}
		if ( req.query.state != req.session.wpcc_state ) {
			res.end( 'Warning! State mismatch. Authentication attempt may have been compromised.' )
			return;
		}

		var post_data = { "form" : {
			"client_id" : wpcc_consts.client_id,
			"redirect_uri" : wpcc_consts.redirect_url,
			"client_secret" : wpcc_consts.client_secret,
			"code" : req.query.code, // The code from the previous request
			"grant_type" : 'authorization_code'
		} };

		request.post(
			wpcc_consts.request_token_url,
			post_data,
			function _callback(error, response, body) {
				if (!error && response.statusCode == 200) {
					//TODO: in real app, store the returned token
		 			res.end('Connected to Trafalgar Square!');
				} else {
		 			res.end('ERROR: ' + body);
				}
			}
		);
	} else {
		//redirect errors or cancelled requests back to login page
		res.writeHead( 303, {
			'Location': wpcc_consts.login_url
		});
		res.end();
	}

});

app.listen(3000);
console.log('Listening on port 3000');
