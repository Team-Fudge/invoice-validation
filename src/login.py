import hashlib

import jwt
import src
import secrets

from src.data_store import data_store
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
used_details = None
#Checks the users to find a matching email
for item in users:
    if item['email'] == email:
        used_details = item
        break

#Non-existent email raises InputError
if used_details is None:
    raise InputError("Email Does not Exist")