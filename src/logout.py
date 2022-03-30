import hashlib
import jwt
import secrets
import src

from src.data_store import data_store
from src.error import AccessError, InputError

def valid_user_id(u_id):
    store = data_store.get()
    return any(u['u_id'] == u_id for u in store['users'])

def valid_token(token):
    store = data_store.get()
    sessions = store['sessions']

    try:
        decoded_jwt = jwt.decode(token, src.register.SECRET, algorithms=['HS256']) 
    except Exception:
        print("Could not decode token")
        return False

    u_id = decoded_jwt['u_id']
    s_id = decoded_jwt['s_id']
    

    # Is the user valid?
    if not valid_user_id(u_id):
        print(f"Invalid UID {u_id}")
        return False
    
    # Is the session valid?
    return any(s == s_id for s in sessions)


def auth_logout(token):

	store = data_store.get()
	sessions = store['sessions']

	if not valid_token(token):
		raise AccessError(description='Invalid token')
	
	# Find the session ID associated with the token, and delete it
	s_id = jwt.decode(token, src.register.SECRET, algorithms=['HS256'])['s_id']
	sessions.remove(s_id)

	data_store.set(store)
	
	return {}