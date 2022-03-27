
# Datastore class for database implementation
# Layout for Datastore class taken from 1531?

initial_object = {
    
    # User contains: u_id, email, name_first, name_last
    'users': [],
    # List of passwords, indexed by ID
    'passwords': []
}


class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()