import hashlib

import jwt
import src
import secrets
from datetime import datetime, timedelta, timezone

from src.data_store import data_store
from src.error import AccessError, InputError
from src import config
import re

SECRET = "s9sDjkDJA8"

# Create JWT token, returns this token
def create_token(u_id):
    store = data_store.get()
    
	# Get the next sequential ID to use
    s_id = store['curr_session_id']

    store['sessions'].append(s_id)

	# Increment sequential ID for next session to use
    store['curr_session_id'] += 1

	# Create the JSW token with the user ID and session ID
    token = jwt.encode({'u_id': u_id, 's_id': s_id, 'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=30) }, SECRET, algorithm='HS256')
    
    data_store.set(store)
    return token


def email_is_unique(email):
	store = data_store.get()
	users = store['users']

	for user in users:
		if user['email'] == email:
			return False

	return True

def email_is_valid(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    return True if re.fullmatch(pattern, email) else False

def auth_register(email, password, name_first, name_last):
    
    name_first = name_first.lower()
    name_last = name_last.lower()

	# Check email is valid
    if not email_is_unique(email):
	    raise InputError(description='Email has already been used to register a user')
	
    if not email_is_valid(email):
        raise InputError(description='Email is invalid')

    # Check first and last name is valid
    if not 1 <= len(name_first) <= 50:
        raise InputError(description='First name must be between 1 and 50 characters')
	
    if not 1 <= len(name_last) <= 50:
        raise InputError(description='Last name must be between 1 and 50 characters')

	# Check if password is valid
    if len(password) < 6:
        raise InputError(description='Password must not be less than 6 characters')

	# Add to users list
    store = data_store.get()
    users = store['users'] # List of users, index = id

    u_id = len(users)

    token = create_token(u_id)

    users.append({
		'u_id': u_id,
		'email': email,
		'name_first': name_first,
		'name_last': name_last,
    })

    #Add password to data store
    hashed_pword = hashlib.sha256(password.encode()).hexdigest()
    store['passwords'].append(hashed_pword)
    
    data_store.set(store)

    return {
        'user_id': u_id,
		'token': token,
    }

 
