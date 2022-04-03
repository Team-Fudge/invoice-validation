import hashlib
import jwt
import secrets
import src

from src.data_store import data_store
from src.error import AccessError, InputError
from src.helper import valid_user_id, valid_token


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