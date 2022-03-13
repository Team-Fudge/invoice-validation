import sys
import signal
from json import dumps
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from src import config

# Errors
from src.error import InputError
from src.error import AccessError

# Functions
import src.schema_validation
from src.verify_syntax import verify_syntax_errors
from src.wellformedness import verify_wellformedness

######################################################

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True

######################################################

# example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

# Wellformedness
@APP.route("/invoice/verify/wellformedness", methods=['GET', 'POST'])
def verify_wellformedness_invoice():
    data = request.data
    resp = verify_wellformedness(data)
    return dumps(resp)

# Syntax
@APP.route("/invoice/verify/syntax", methods=['GET', 'POST'])
def verify_syntax():
    data = request.data
    resp = verify_syntax_errors(data)
    return dumps(
     resp
    )   

# PEPPOL
@APP.route("/invoice/verify/peppol", methods=['GET', 'POST'])
def verify_peppol():
    resp = request.args.get('data')
    return dumps({
        resp
    })

# Schema
@APP.route("/invoice/verify/schema", methods=['GET'])
def verify_schema():
    data = request.args.get('data')
    return dumps({
        # report
    })

#active
@APP.route("/active", methods=['GET'])
def active():
    return dumps({
        'server_active': True,
        'wellformedness_validator_active': True,
        'syntax_validator_active': True,
        'PEPPOL_validator_active': True,
        'schema_validator_active': False,
    })

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
