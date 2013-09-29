<?php

require_once "defines.php";

$wpcc_state = md5( mt_rand() );
session_start();
$_SESSION[ 'wpcc_state' ] = $wpcc_state;
 
$params = array(
  'response_type' => 'code',
  'client_id' => CLIENT_ID,
  'state' => $wpcc_state,
  'redirect_uri' => REDIRECT_URL
);
 
$url_to = AUTHENTICATE_URL .'?'. http_build_query( $params );

echo "<h2>Connect to Trafalgar Square</h2>";
echo '<a href="' . $url_to . '"><img src="//s0.wp.com/i/wpcc-button.png" width="231" /></a>';

