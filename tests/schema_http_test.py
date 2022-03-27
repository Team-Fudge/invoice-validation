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

def verify_schema_request(invoice):
    headers = {'Content-Type': 'application/xml'}
    return requests.post(config.url + 'invoice/verify/schema', data = invoice, headers = headers)

def test_empty_xml_type():
    assert verify_schema_request('''''').status_code == 400
    assert isinstance(verify_schema_request('''''').json(), dict)

def test_incorrect_xml_type():
    assert verify_schema_request(open_file_as_string("schema_incorrect.xml")).status_code == 200
    assert isinstance(verify_schema_request(open_file_as_string("schema_incorrect.xml")).json(),dict)

def test_correct_xml_type():
    assert verify_schema_request(open_file_as_string("schema_correct.xml")).status_code == 200
    assert isinstance(verify_schema_request(open_file_as_string("schema_correct.xml")).json(),dict)
