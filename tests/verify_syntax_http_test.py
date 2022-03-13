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

# The tests below are whitebox 
def test_empty_xml():
    assert verify_syntax_request('''''').status_code == 200
    assert verify_syntax_request('''''').json() == {'broken_rules': 'The provided file is empty', 'broken_rules_detailed': 'The provided file is empty', 'disclaimer': 'The current version of this microservice can only test syntax errors BR-01 to BR-16'}

def test_bad_xml():
    assert verify_syntax_request(open_file_as_string("example_broken.xml")).status_code == 200
    assert verify_syntax_request(open_file_as_string("example_broken.xml")).json() ==  {'broken_rules': ['BR-01'],
                                                     'broken_rules_detailed': ['[BR-01]-An Invoice shall have a Specification identifier (BT-24).'],
                                                     'disclaimer': 'The current version of this microservice can only test syntax errors BR-01 to BR-16'
                                                     }
def test_good_xml():
    assert verify_syntax_request(open_file_as_string("example_good.xml")).status_code == 200
    assert verify_syntax_request(open_file_as_string("example_good.xml")).json() ==  {"broken_rules": [], "broken_rules_detailed": [], "disclaimer": 'The current version of this microservice can only test syntax errors BR-01 to BR-16'}