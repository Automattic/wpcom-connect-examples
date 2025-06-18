<?php

// TODO: Replace these with the values shown on your app's Manage Settings page
// Visit: https://developer.wordpress.com/apps/
define('CLIENT_ID', 1);
define('CLIENT_SECRET', 'your-client-secret');
define('LOGIN_URL', 'http://localhost:8000');
define('REDIRECT_URL', 'http://localhost:8000/connected.php');

// You do not need to change these settings
define('REQUEST_TOKEN_URL', 'https://public-api.wordpress.com/oauth2/token');
define('AUTHENTICATE_URL', 'https://public-api.wordpress.com/oauth2/authenticate');

session_start();
