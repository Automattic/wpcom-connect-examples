# WordPress.com Connect Node/Express.js Demo

This is a simple Node.js/Express.js example demonstrating how to implement WordPress.com Connect (OAuth2 authentication) in your application.

## Prerequisites

- Node.js (v14 or higher recommended)
- npm (comes with Node.js)
- A [WordPress.com Developer Application](https://developer.wordpress.com/apps/)

## Setup Instructions

1. **Clone this repository** (if you haven't already):
   ```sh
   git clone https://github.com/Automattic/wpcom-connect-examples.git
   cd wpcom-connect-examples/express.js
   ```

2. **Register a new application** at [WordPress.com Developer Console](https://developer.wordpress.com/apps/):
   - Set the **Redirect URL** to: `http://localhost:3000/connected`
   - Note your **Client ID** and **Client Secret**.

3. **Configure your credentials:**
   - Open `config.js` in this folder.
   - Replace the `client_id`, `client_secret`, `login_url`, and `redirect_url` values with those from your app's settings.
   - Adjust `login_url` and `redirect_url` if you use a different port or domain.

4. **Install dependencies:**
   ```sh
   npm install
   ```

5. **Start the server:**
   ```sh
   npm start
   ```
   - This will serve the demo at [http://localhost:3000](http://localhost:3000)

6. **Test the demo:**
   - Open [http://localhost:3000](http://localhost:3000) in your browser.
   - Click the "Connect with WordPress.com" button.
   - Authorize the app and you should see a "Connected to WordPress.com!" message.

## Notes

- This demo is for educational purposes. In a real application, you should securely store the access token and handle errors appropriately.
- If you change the port or domain, update `login_url` and `redirect_url` in `config.js` and in your WordPress.com app settings.
- You can set a custom session secret by defining the `SESSION_SECRET` environment variable.
- For more details, see the [official documentation](https://developer.wordpress.com/docs/oauth2/).