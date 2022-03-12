import sys
import signal
from json import dumps
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import config
import peppol_validation

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
    xml_file = request.args.get('data')

    broken_rules = []

    # Validating all Rules
    broken_rules.append(check_reference_number(xml_file))
    broken_rules.append(check_date_syntax(xml_file))
    broken_rules.append(check_currency_Code(xml_file))
    broken_rules.append(check_if_buyer_seller_address_exists(xml_file))
    broken_rules.append(check_base_amount_and_percentage(xml_file))
    broken_rules.append(check_gross_net_amount(xml_file))

    # Getting rid of all None elements in the broken rules 
    try:
        while True:
            broken_rules.remove(None)
    except ValueError:
        pass

    return dumps({broken_rules})

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