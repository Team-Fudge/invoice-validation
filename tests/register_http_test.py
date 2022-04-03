import pytest
import json
from flask.globals import request
import requests
from src import config

def auth_register_request(email, password, name_first, name_last):
    return requests.post(config.url + 'auth/register', json={
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last
    })

def clear_request():
    return requests.delete(config.url + 'clear', params={})

@pytest.fixture(autouse=True)
def clear():
	clear_request()
	pass


def auth_login_request(email, password):
    return requests.post(config.url + 'auth/login', json={
        'email': email,
        'password': password,
    })
    
def test_valid_register():
	register = auth_register_request("user@gmail.com", "password", "firstname", "lastname").json()
	login = auth_login_request("user@gmail.com", "password").json()
	assert register['user_id'] == login['user_id']
	assert register['token'] != login['token']

def test_user_token_unique():
    
    used_tokens = set()

    data = auth_register_request("user1@mail.com", "password", "firstname", "lastname").json()
    assert data['token'] not in used_tokens
    used_tokens.add(data['token'])

    data = auth_register_request("user2@mail.com", "password", "firstname", "lastname").json()
    assert data['token'] not in used_tokens
    used_tokens.add(data['token'])

    data = auth_register_request("user3@mail.com", "password", "firstname", "lastname").json()
    assert data['token'] not in used_tokens
    used_tokens.add(data['token'])

def test_user_id():

    # Set created for used ids
    used_ids = set()
    
    data = auth_register_request("user1@gmail.com", "password12", "firstname", "lastname").json()
    assert data['user_id'] not in used_ids
    used_ids.add(data['user_id'])

    data = auth_register_request("user2@gmail.com", "password123", "firstname", "lastname").json()
    assert data['user_id'] not in used_ids
    used_ids.add(data['user_id'])

# Valid registration
def test_valid_registration():
    assert auth_register_request("user3@gmail.com", "password", "firstname", "lastname").status_code == 200
    
# invalid registrations

def test_invalid_email():
    assert auth_register_request("12324", "password", "firstname", "lastname").status_code == 400
    assert auth_register_request("user@gmail", "password", "firstname", "lastname").status_code == 400
    assert auth_register_request("@gmail", "password", "firstname", "lastname").status_code == 400
    assert auth_register_request("!!!!.com", "password", "firstname", "lastname").status_code == 400
    assert auth_register_request("@gmail.com.", "password", "firstname", "lastname").status_code == 400

def test_password_too_short():
	assert auth_register_request("user3@gmail.com", "", "firstname", "lastname").status_code == 400
	assert auth_register_request("user4@gmail.com", "123", "firstname", "lastname").status_code == 400

def test_first_name_empty():
	assert auth_register_request("firstname@mail.com", "password", "", "lastname").status_code == 400

def test_first_name_too_long():
	assert auth_register_request("firstname@mail.com", "password", "firstname" * 30, "lastname").status_code == 400

def test_last_name_empty():
	assert auth_register_request("firstname@mail.com", "password", "firstname", "").status_code == 400

def test_last_name_too_long():
	assert auth_register_request("firstname@mail.com", "password", "firstname", "lastname" * 30).status_code == 400