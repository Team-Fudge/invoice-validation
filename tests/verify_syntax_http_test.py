import pytest
import requests
import json
from src import server
from src import config
from src.error import InputError, AccessError

def open_file_as_string(file_name):
    #open & read file
    with open(file_name, 'r') as f:
       data = f.read()

    return data


def verify_syntax_request(invoice):
    headers = {'Content-Type': 'application/xml'}
    return requests.post(config.url + 'invoice/verify/syntax', data = invoice, headers = headers)

def test_empty_xml_type():
    assert verify_syntax_request('''''').status_code == 200
    assert isinstance(verify_syntax_request('''''').json(), dict)

def test_bad_xml_type():
    assert verify_syntax_request(open_file_as_string("example_broken.xml")).status_code == 200
    assert isinstance(verify_syntax_request(open_file_as_string("example_broken.xml")).json(),dict)

def test_good_xml_type():
    assert verify_syntax_request(open_file_as_string("example_good.xml")).status_code == 200
    assert isinstance(verify_syntax_request(open_file_as_string("example_good.xml")).json(),dict)
