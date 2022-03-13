import sys
import signal
from json import dumps
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import config

# Errors
from error import InputError
from error import AccessError

# Functions
import schema_validation

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
@APP.route("/invoice/verify/wellformedness", methods=['GET'])
def verify_wellformedness():
    data = request.args.get('data')
    return dumps({
        # report
    })

# Syntax
@APP.route("/invoice/verify/syntax", methods=['GET'])
def verify_syntax():
    data = request.args.get('data')
    return dumps({
        # report
    })   

# PEPPOL
@APP.route("/invoice/verify/peppol", methods=['GET'])
def verify_peppol():
    data = request.args.get('data')
    return dumps({
        # report
    })

# Schema
@APP.route("/invoice/verify/schema", methods=['GET'])
def verify_schema():
    data = request.args.get('data')
    return dumps({
        # report
    })

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port