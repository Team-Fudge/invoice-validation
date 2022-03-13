import pytest
import requests
import json
from src import server
from src import config

def test_active():
    isinstance(requests.get(config.url + 'active').json(),dict)