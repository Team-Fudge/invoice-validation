import sys
import signal
from json import dumps
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from src import config
from src.peppol_validation import check_reference_number, check_date_syntax, check_currency_Code, check_if_buyer_seller_address_exists, check_xml_empty, check_valid

# Errors
from src.error import InputError
from src.error import AccessError

# Functions
from src.schema_validation import verify_schema
from src.verify_syntax import verify_syntax_errors
from src.wellformedness import verify_wellformedness
from src.helper import compile_report
######################################################

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

APP = Flask(__name__)
CORS(APP)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)




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
    report = compile_report(resp, syntax = True) 
    return dumps(
     report
    )   

# All peppol functions in main will be commented out until either a requirements.txt file
# is made or to sort out dependencies and the form of ubl invoice can be confirmed to be UBL 2.1

# PEPPOL
@APP.route("/invoice/verify/peppol", methods=['GET', 'POST'])
def verify_peppol():

    xml_file = request.data
    broken_ruless = []

    # Validating all Rules
    broken_ruless = check_valid(xml_file)
   
    # Getting rid of all None elements in the broken rules 
    try:
        while True:
            broken_ruless.remove(None)
    except ValueError:
        pass

    dict_broken_rules = {"broken_rules": broken_ruless}
    
    report = compile_report(dict_broken_rules, peppol = True) 
    return dumps(report)


# Schema
@APP.route("/invoice/verify/schema", methods=['GET', 'POST'])
def verify_schema_xml():
    data = request.data
    resp = verify_schema(data)
    report = compile_report(resp, schema = True) 
    return dumps(
     report
    )


# all
@APP.route("/invoice/verify/all", methods=['GET', 'POST'])
def verify_all():
    data = request.data

    resp = verify_wellformedness(data)
    report = compile_report(resp,wellformedness = True)
    
    resp = verify_syntax_errors(data)
    report = compile_report(resp,syntax = True)

    resp = verify_schema(data)
    report = compile_report(resp,schema = True) 

    return dumps(
     report
    )  

#active
@APP.route("/active", methods=['GET'])
def active():
    return dumps({
        'server_active': True,
        'wellformedness_validator_active': True,
        'syntax_validator_active': True,
        'PEPPOL_validator_active': True,
        'schema_validator_active': True,
    })

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(host='0.0.0.0', port=config.port) # Do not edit this port