from src.error import InputError
import pytest
import requests
import json
from src import server
from src import config
from src.verify_syntax import verify_syntax_errors

'''
def open_file_as_string(file_name):

    #open & read file
    with open(file_name, 'r') as f:
       data = f.read()

    return data

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


#the below are whiteboard tests

def test_output_wrong_xml(user):
    assert(verify_syntax_errors(user['token'], open_file_as_string("example_broken.xml")) == {'broken_rules': ['BR-01'],
                                                     'broken_rules_detailed': ['[BR-01]-An Invoice shall have a Specification identifier (BT-24).'],
                                                     'disclaimer': 'The current version of this microservice can only test syntax errors BR-01 to BR-16'
                                                     })
def test_output_correct_xml(user):
    assert(verify_syntax_errors(user['token'], open_file_as_string("example_good.xml")) == {"broken_rules": [], "broken_rules_detailed": [], "disclaimer": 'The current version of this microservice can only test syntax errors BR-01 to BR-16'})

def test_output_empty_xml(user):
    with pytest,raises(InputError):
        verify_syntax_errors(user['token'], open_file_as_string("example_empty.xml"))

'''