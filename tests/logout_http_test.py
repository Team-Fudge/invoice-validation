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

def auth_logout_request(token):
    return requests.post(config.url + 'auth/logout', json={
        'token': token
    })

def clear_request():
    return requests.delete(config.url + 'clear', params={})

@pytest.fixture(autouse=True)
def clear():
	clear_request()
 
@pytest.fixture
def user():
	user_data = auth_register_request("user@gmail.com", "password", "first", "last").json()
	return {'u_id': user_data['user_id'], 'token': user_data['token']}

# Test Correct Logout
def test_logout_correct(user):
	assert auth_logout_request(user['token']).status_code == 200

# Test Logout with wrong tokens
def test_logout_wrong_token():
	assert auth_logout_request("RANDOM").status_code == 403

def test_logout_changed_token(user):
	assert auth_logout_request(user['token'] + 'a').status_code == 403

# Incorrect Logout Procedure

def test_logout_twice(user):
	assert auth_logout_request(user['token']).status_code == 200
	assert auth_logout_request(user['token']).status_code == 403

# Multiple Logout with Users
def test_logout_multiple_users():
	user1 = auth_register_request("user1@gmail.com", "password", "first", "last").json()['token']
	user2 = auth_register_request("user2@gmail.com", "password", "first", "last").json()['token']
	user3 = auth_register_request("user3@gmail.com", "password", "first", "last").json()['token']
	
	assert auth_logout_request(user1).status_code == 200	
	assert auth_logout_request(user2).status_code == 200
	assert auth_logout_request(user3).status_code == 200
