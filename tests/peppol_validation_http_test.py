import pytest
import requests
import json
from src import server
from src import config
from src.error import InputError, AccessError

def open_file_as_string(file_name):
    #open & read file
    with open(file_name, 'r') as f:
       data = f.read()

    return data

def test_empty_xml_type():

    string_xml = open_file_as_string("example_empty.xml")
    data = requests.post(config.url + '/invoice/verify/peppol', data = string_xml)
    assert data.status_code == 400
    assert isinstance(data.json(), dict)

def test_incorrect_xml():

    string_xml = open_file_as_string("peppol_incorrect.xml")
    data = requests.post(config.url + '/invoice/verify/peppol', data = string_xml)
    assert data.status_code == 200
    assert isinstance(data.json(),dict)

def test_correct_xml_type():

    string_xml = open_file_as_string("example_good.xml")
    data = requests.post(config.url + '/invoice/verify/peppol', data = string_xml)
    assert data.status_code == 200
    assert isinstance(data.json(),dict)