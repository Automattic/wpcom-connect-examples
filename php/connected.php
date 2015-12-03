<?php

require_once dirname( __FILE__ ) . '/defines.php';

// If someone visits this page without a `code` value, it's likely they've not 
// been authenticated or declined access, so redirect them to the login page.
if ( ! isset( $_GET[ 'code' ] ) ) {
	header( 'Location: ' . LOGIN_URL );
	die();
}

// We pass an anti-forgery state value when redirecting the visitor, so upon
// arrival here, we verify that the returned value matches our expectations.
session_start();
if ( $_GET[ 'state' ] !== $_SESSION[ 'wpcc_state' ] ) {
	die( 'Warning! State mismatch. Authentication attempt may have been compromised.' );  	
}

// When redirected, a temporary, time-sensitive code will be included as a 
// query parameter. This needs to be exchanged for an authorization token.
$code = $_GET[ 'code' ];

$curl = curl_init( REQUEST_TOKEN_URL );
curl_setopt( $curl, CURLOPT_POST, true );
curl_setopt( $curl, CURLOPT_POSTFIELDS, array(
	'client_id'     => CLIENT_ID,
	'redirect_uri'  => REDIRECT_URL,
	'client_secret' => CLIENT_SECRET,
	'code'          => $code,
	'grant_type'    => 'authorization_code'
) );

curl_setopt( $curl, CURLOPT_RETURNTRANSFER, 1 );
$auth = curl_exec( $curl );

// The JSON response can be decoded to an object containing the access_token 
// that you will use to query the users profile information.
$secret = json_decode( $auth );

// TODO: In a real app, you'll likely want to store the returned token so that
// you can continue to make authenticated requests.
echo 'Connection successful!';
