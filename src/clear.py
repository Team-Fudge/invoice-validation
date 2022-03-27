from src.data_store import data_store
import os
from shutil import rmtree

def clear():

    store = data_store.get()
    store['users'] = []
    store['passwords'] = []
    data_store.set(store)
    
    return {}