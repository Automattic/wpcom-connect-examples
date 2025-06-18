# WordPress.com Connect PHP Demo

This is a simple PHP example demonstrating how to implement WordPress.com Connect (OAuth2 authentication) in your application.

## Prerequisites

- PHP 7.0 or higher
- A local web server (e.g., [PHP built-in server](https://www.php.net/manual/en/features.commandline.webserver.php), Apache, or Nginx)
- A [WordPress.com Developer Application](https://developer.wordpress.com/apps/)

## Setup Instructions

1. **Clone this repository** (if you haven't already):
   ```sh
   git clone https://github.com/Automattic/wpcom-connect-examples.git
   cd wpcom-connect-examples/php
   ```

2. **Register a new application** at [WordPress.com Developer Console](https://developer.wordpress.com/apps/):
   - Set the **Redirect URL** to: `http://localhost:8000/connected.php`
   - Note your **Client ID** and **Client Secret**.

3. **Configure your credentials:**
   - Open `config.php` in this folder.
   - Replace the values for `CLIENT_ID` and `CLIENT_SECRET` with those from your app's settings.
   - Adjust `LOGIN_URL` and `REDIRECT_URL` if you use a different port or domain.

4. **Start the PHP built-in server:**
   ```sh
   php -S localhost:8000
   ```
   - This will serve the demo at [http://localhost:8000](http://localhost:8000)

5. **Test the demo:**
   - Open [http://localhost:8000/index.php](http://localhost:8000/index.php) in your browser.
   - Click the "Connect using your WordPress.com account" button.
   - Authorize the app and you should see a "Connection successful!" message.

## Notes

- This demo is for educational purposes. In a real application, you should securely store the access token and handle errors appropriately.
- If you change the port or domain, update `LOGIN_URL` and `REDIRECT_URL` in `config.php` and in your WordPress.com app settings.
- For more details, see the [official documentation](https://developer.wordpress.com/docs/oauth2/). 