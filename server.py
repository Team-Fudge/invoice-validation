import sys
import signal
from json import dumps
from flask import Flask, request, send_from_directory
from error import ###


# invoice/verify
@APP.route("/invoice/verify", methods=['GET'])
def verify():
    data = request.args.get('###')
    return dumps(###)
    