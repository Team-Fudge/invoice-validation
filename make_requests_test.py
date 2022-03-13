import json
from flask.globals import request
import requests
import config

def  wellformedness_verify_request(invoice):
    return requests.post(config.url + '/invoice/verify/wellformedness', data={
        


    })
