import sys
import pytest
import requests
import json
from src import server
from src import config
from src.error import InputError, AccessError

# XML with correct formatting
data = open("WF_correct.xml", 'r')
string1 = data.read()
string1 = bytes(bytearray(string1, encoding='utf-8'))

# XML with incorrect formatting
data2 = open("WF_incorrect.xml", 'r')
string2 = data2.read()
string2 = bytes(bytearray(string2, encoding='utf-8'))

# Empty string example
string3 = " "

# Register Request

def auth_register_request(email, password, name_first, name_last):
    return requests.post(config.url + 'auth/register', json={
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    })

# Clear Request
def clear_request():
    return requests.delete(config.url + 'clear', params={})

@pytest.fixture(autouse=True)
def clear():
	clear_request()
	pass


def verify_wellformedness_request(token, invoice):
    return requests.post(config.url + 'invoice/verify/wellformedness', params={
        'token': token
    }, data=invoice)

@pytest.fixture
def user():
	user_data = auth_register_request("user@gmail.com", "password", "first", "last").json()
	return {'u_id': user_data['user_id'], 'token': user_data['token']}
    
# Blackbox/HTTP Testing
def test_wellformedness_verify_request_good(user):
    assert verify_wellformedness_request(user['token'], string1).status_code == 200
    assert isinstance(verify_wellformedness_request(user['token'], string1).json(),dict)

def test_wellformedness_verify_request_bad(user):
    assert verify_wellformedness_request(user['token'], string2).status_code == 200
    assert isinstance(verify_wellformedness_request(user['token'], string2).json(),dict)

def test_wellformedness_verify_request_empty(user):
    assert verify_wellformedness_request(user['token'], string3).status_code == 200
    assert isinstance(verify_wellformedness_request(user['token'], string3).json(),dict)

# Whitebox testing
def test_wellformedness_invoice_correct(user):
    assert verify_wellformedness_request(user['token'], string1).status_code == 200
    assert verify_wellformedness_request(user['token'], string1).json() == {'broken_rules': 'No broken rules found. Invoice is well-formed!'}

def test_wellformedness_invoice_wrong(user):
    assert verify_wellformedness_request(user['token'], string2).status_code == 200
    assert verify_wellformedness_request(user['token'], string2).json() =={'broken_rules': ["ERROR ON LINE 23: Failed to parse QName 'cbc:'", 
                                                             'ERROR ON LINE 23: Opening and ending tag mismatch: CityName line 23 and cbc:', 
                                                             'ERROR ON LINE 33: Opening and ending tag mismatch: PartyName line 19 and Party', 
                                                             'ERROR ON LINE 34: Opening and ending tag mismatch: Party line 15 and AccountingSupplierParty', 
                                                             'ERROR ON LINE 101: Opening and ending tag mismatch: AccountingSupplierParty line 14 and Invoice', 
                                                             'ERROR ON LINE 101: Premature end of data in tag Invoice line 2']}
def test_wellformedness_invoive_empty(user):
    assert verify_wellformedness_request(user['token'], string3).status_code == 200
    assert verify_wellformedness_request(user['token'], string3).json() == {"broken_rules":["ERROR ON LINE 1: Start tag expected, '<' not found"]}
