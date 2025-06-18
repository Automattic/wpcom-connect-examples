// Replace the TODO values with the values shown on your app's Manage Settings page: https://developer.wordpress.com/apps/
// For more details, see the https://developer.wordpress.com/docs/oauth2/

module.exports = {
  client_id: 1, //TODO
  client_secret: "your-client-secret", //TODO
  login_url: "http://localhost:3000/", //TODO
  redirect_url: "http://localhost:3000/connected", //TODO
  request_token_url: "https://public-api.wordpress.com/oauth2/token",
  authenticate_url: "https://public-api.wordpress.com/oauth2/authenticate"
};
