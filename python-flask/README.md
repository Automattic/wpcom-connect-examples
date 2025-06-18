# WordPress.com Connect Example (Flask)

This is an example Flask application demonstrating how to connect with WordPress.com using OAuth2.

## Setup & Run Instructions

1. **Clone this repository and navigate to the `flask` directory:**
   ```sh
   cd flask
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure your WordPress.com credentials:**
   - Edit `config.py` and set your `client_id` and `client_secret`.

5. **Run the Flask app:**
   ```sh
   python run.py
   ```

6. **Open your browser and visit:**
   [http://localhost:5001/](http://localhost:5001/)

---

**Note:**
- If you change dependencies, re-run the install command.
- If you encounter import errors, ensure your virtual environment is activated and all dependencies are installed.