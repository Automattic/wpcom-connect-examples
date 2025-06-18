# Example WordPress.com Connect

import requests
import string
import random
import hashlib
import urllib.parse
from flask import abort, redirect, url_for
from flask import make_response
from flask import request
from flask import Flask
from config import wpcc_consts
app = Flask(__name__)


@app.route("/")
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(30))
    params = {
        "response_type": "code",
        "client_id": wpcc_consts['client_id'],
        "state": state,
        "redirect_uri": wpcc_consts['redirect_url']
    }
    wpcc_url = wpcc_consts['authenticate_url'] + \
        '?' + urllib.parse.urlencode(params)
    resp = make_response(
        '<html><body><h2>Connect to WordPress.com</h2><a href="' +
        wpcc_url +
        '"><img src="//s0.wp.com/i/wpcc-button.png" width="231" /></a></body></html>'
    )

    resp.set_cookie('wpcc_state', state)
    return resp


@app.route("/connected")
def connected():
    app.logger.info("Connected page accessed")
    code = request.args.get('code')

    if not code:
        return redirect(url_for('login'))

    state = request.args.get('state')
    if not state:
        app.logger.warning('State parameter missing in callback URL')
        return 'Warning! State variable missing after authentication'

    wpcc_state = request.cookies.get('wpcc_state')
    if not wpcc_state:
        app.logger.warning('wpcc_state cookie missing')
        return 'Warning! State cookie missing. Authentication attempt may have been compromised.'

    if state != wpcc_state:
        app.logger.warning(
            'State mismatch: received %s, expected %s', state, wpcc_state)
        return 'Warning! State mismatch. Authentication attempt may have been compromised.'

    # Optionally, clear the state cookie after use
    payload = {
        "client_id": wpcc_consts['client_id'],
        "redirect_uri": wpcc_consts['redirect_url'],
        "client_secret": wpcc_consts['client_secret'],
        "code": code,  # The code from the previous request
        "grant_type": 'authorization_code'
    }
    r = requests.post(wpcc_consts['request_token_url'], data=payload)
    if 200 == r.status_code:
        token_data = r.json()
        access_token = token_data.get('access_token', 'No token found')
        resp = make_response(
            f'<html><body><h2>Connected to WordPress.com!</h2><p><strong>Access Token:</strong> {access_token}</p></body></html>')
        resp.set_cookie('wpcc_state', '', expires=0)
        return resp

    return 'Error: ' + r.text


if __name__ == "__main__":
    app.debug = True
    app.run(host='localhost', port=5001)
