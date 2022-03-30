import hashlib

import jwt
import src
import secrets

from src.data_store import data_store
from src.register import create_token
from src.error import AccessError, InputError
from src import config
import re

def auth_login(email, password):

    char_reg = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'

    #Checks the email using the regex passing if valid, raising input error otherwise
    if re.search(char_reg, email):
        pass
    else:
        raise InputError("Invalid Email")


    store = data_store.get()
    users = store['users']
    user_details = None
    #Checks the users to find a matching email
    for item in users:
        if item['email'] == email:
            user_details = item
            break

    #Non-existent email raises InputError
    if user_details is None:
        raise InputError("Email Does not Exist")

    #Checks to see if the password parameter matches with the email associated with it
    user_id = user_details['u_id']
    user_password = store['passwords'][user_id]
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if user_password != password_hash:
        raise InputError("Incorrect Password")

    token = create_token(user_id)
    data_store.set(store)

    return {
            'user_id': user_id,
            'token': token,
        }