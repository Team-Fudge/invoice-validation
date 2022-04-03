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


def verify_peppol_request(token, invoice):
    return requests.post(config.url + 'invoice/verify/peppol', params={
        'token': token
    }, data=invoice)

@pytest.fixture
def user():
	user_data = auth_register_request("user@gmail.com", "password", "first", "last").json()
	return {'u_id': user_data['user_id'], 'token': user_data['token']}

def test_empty_xml_type(user):

    string_xml = open_file_as_string("example_empty.xml")
    data = verify_peppol_request(user['token'], string_xml)
    assert data.status_code == 400
    assert isinstance(data.json(), dict)


def test_incorrect_xml(user):

    string_xml = open_file_as_string("peppol_incorrect.xml")
    data = verify_peppol_request(user['token'], string_xml)
    assert data.status_code == 200
    assert isinstance(data.json(),dict)

def test_correct_xml_type(user):

    string_xml = open_file_as_string("example_good.xml")
    data = verify_peppol_request(user['token'], string_xml)
    assert data.status_code == 200
    assert isinstance(data.json(),dict)