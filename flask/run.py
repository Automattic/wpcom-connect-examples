# Example WordPress.com Connect

from flask import Flask
app = Flask(__name__)

from flask import request
from flask import make_response
from flask import abort, redirect, url_for
import urllib
import md5
import random
import string
import requests

wpcc_consts = {
    "client_id": 1234, #TODO
    "client_secret": "Your WP.com secret", #TODO
    "login_url": "http://localhost:5000/", #TODO
    "redirect_url": "http://localhost:5000/connected", #TODO
    "request_token_url": "https://public-api.wordpress.com/oauth2/token",
    "authenticate_url": "https://public-api.wordpress.com/oauth2/authenticate"
}

@app.route("/")
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(30))
    params = { 
        "response_type": "code", 
        "client_id": wpcc_consts['client_id'], 
        "state": state,
        "redirect_uri": wpcc_consts['redirect_url']
    }
    wpcc_url = wpcc_consts['authenticate_url'] + '?' + urllib.urlencode(params)
    resp = make_response(
        '<html><body><h2>Connect to Trafalgar Square</h2><p>' + state + '</p><a href="' + 
        wpcc_url +
        '"><img src="//s0.wp.com/i/wpcc-button.png" width="231" /></a></body></html>'
    )

    resp.set_cookie('wpcc_state', state)
    return resp

@app.route("/connected")
def connected():
    code = request.args.get( 'code' )

    if not code:
        return redirect(url_for('login'))

    state = request.args.get( 'state' )
    if not state:
        return 'Warning! State variable missing after authentication'

    wpcc_state = request.cookies.get( 'wpcc_state' )
    if state != wpcc_state:
        return 'Warning! State mismatch. Authentication attempt may have been compromised. ' + wpcc_state

    payload = {
        "client_id" : wpcc_consts['client_id'],
        "redirect_uri" : wpcc_consts['redirect_url'],
        "client_secret" : wpcc_consts['client_secret'],
        "code" : code, #The code from the previous request
        "grant_type" : 'authorization_code'
    }
    r = requests.post(wpcc_consts['request_token_url'], data=payload)
    if 200 == r.status_code:
        #TODO: in real app, store the returned token
        return 'Connected to Trafalgar Square!'

    return 'Error: ' + r.text


if __name__ == "__main__":
    app.debug = True
    app.run()

