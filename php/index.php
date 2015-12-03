<?php

require_once dirname( __FILE__ ) . '/defines.php';

// Track a random state value in the session to ensure we're talking to the
// same user after they return
session_start();
$wpcc_state = md5( mt_rand() );
$_SESSION[ 'wpcc_state' ] = $wpcc_state;

// To authenticate the user, we generate a URL including the query parameters
// describing our application. When the visitor clicks this link, they'll be
// presented with a form to grant access to your application.
$url_to = AUTHENTICATE_URL . '?' . http_build_query( array(
	'response_type' => 'code',
	'client_id'     => CLIENT_ID,
	'state'         => $wpcc_state,
	'redirect_uri'  => REDIRECT_URL
) );

echo '<h2>Connect using your WordPress.com account</h2>';
echo '<a href="' . $url_to . '"><img src="//s0.wp.com/i/wpcc-button.png" width="231" /></a>';
