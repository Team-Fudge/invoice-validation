from src.data_store import data_store
import os
from shutil import rmtree

def clear():

    store = data_store.get()
    store['users'] = []
    store['passwords'] = []
    store['sessions'] = []
    store['curr_session_id'] = 0
    data_store.set(store)
    
    return {}