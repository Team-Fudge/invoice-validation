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

@pytest.fixture
def user():
	user_data = auth_register_request("user@gmail.com", "password", "first", "last").json()
	return {'u_id': user_data['user_id'], 'token': user_data['token']}

def verify_schema_request(token, invoice):
    header = {'Authorisation': token}
    return requests.post(config.url + 'invoice/verify/schema', headers=header, data=invoice)
    
def test_empty_xml_type(user):
    assert verify_schema_request(user['token'], '''''').status_code == 400
    assert isinstance(verify_schema_request(user['token'], '''''').json(), dict)

def test_incorrect_xml_type(user):
    assert verify_schema_request(user['token'], open_file_as_string("schema_incorrect.xml")).status_code == 200
    assert isinstance(verify_schema_request(user['token'], open_file_as_string("schema_incorrect.xml")).json(),dict)

def test_correct_xml_type(user):
    assert verify_schema_request(user['token'], open_file_as_string("schema_correct.xml")).status_code == 200
    assert isinstance(verify_schema_request(user['token'], open_file_as_string("schema_correct.xml")).json(),dict)
