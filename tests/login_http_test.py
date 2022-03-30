'''
Tests for auth functions auth_login
'''
import pytest
from src.login import auth_login
from src.clear import clear

import json
import sys
import requests
from src import config
from src.error import AccessError, InputError

def auth_login_request(email, password):
    return requests.post(config.url + 'auth/login', json={
        'email': email,
        'password': password,
    })

def clear_request():
    return requests.delete(config.url + 'clear', params={})

@pytest.fixture(autouse=True)
def clear():
	clear_request()
	pass

def test_email_dne():
    '''
    #Testing case where email does not exist. Should raise InputError
    '''
    pytest.fixture
    data = auth_login_request("johnsmith@gmail.com", "password")
    assert data.status_code == InputError.code

def test_pwd_incorrect():
    '''
    #Testing case where pwd is incorrect. Should raise InputError
    '''
    pytest.fixture
    user = requests.post(config.url + 'auth/register', json= {'email': 'randomemail@gmail.com', 'password': 'Password2123', 'name_first' : 'Bob', 'name_last' :'Joe'},)
    user_data = user.json()
    login = requests.post(config.url + 'auth/login', json= {'email': 'randomemail@gmail.com', 'password': 'WrongPassword'})

    assert login.status_code == InputError.code
    
def test_login_successful():
    '''
    #Testing case where Login is successful
    '''
    pytest.fixture
    requests.post(config.url + 'auth/register', json= {'email': 'randomemail@gmail.com', 'password': 'Password2123', 'name_first' : 'Bob', 'name_last' :'Joe'},)
    login = requests.post(config.url + 'auth/login', json= {'email': 'randomemail@gmail.com', 'password': 'Password2123'},)
    login_data = login.json()

    assert isinstance(login_data['user_id'], int)
    assert isinstance(login_data['token'], str)
