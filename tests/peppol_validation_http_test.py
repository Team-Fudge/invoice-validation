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

# def test_empty_xml_file():

#     string_xml = open_file_as_string("tests/empty_xml.xml")
#     data = requests.post(config.url + '/invoice/verify/peppol', data = string_xml)
#     assert data.json() == 0
    
def test_no_currency_code_xml():

    string_xml = open_file_as_string("tests/example_invoice_currency_code.xml")
    data = requests.post(config.url + '/invoice/verify/peppol', data = string_xml)
    json_data = data.json()
    assert data.status_code == 200
    assert json_data == [{'broken_rule': 'PEPPOL - EN16931 - CL007', 'broken_rule_detailed': 'Currency code must be according to ISO 4217:2005'}]
    
def test_incorrect_date_syntax():

    string_xml = open_file_as_string("tests/example_invoice_wrong_date_syntax.xml")
    data = requests.post(config.url + '/invoice/verify/peppol', data = string_xml)
    json_data = data.json()
    assert data.status_code == 200
    assert json_data == [{'broken_rule' : "PEPPOL - EN16931 - F001", "broken_rule_detailed" : "A date MUST be formatted YYYY-MM-DD"}]

def test_no_address_in_xml():

    string_xml = open_file_as_string("tests/example_invoice_no_address.xml")
    data = requests.post(config.url + '/invoice/verify/peppol', data = string_xml)
    json_data = data.json()
    assert data.status_code == 200
    assert json_data == [{'broken_rule' : "PEPPOL - EN16931 - R010", "broken_rule_detailed" : "Buyer electronic address MUST be provided"}]

def test_incorrect_baseamount_percentage_etc_in_xml():

    string_xml = open_file_as_string("tests/example_invoice_invalid_percentage_baseamount.xml")
    data = requests.post(config.url + '/invoice/verify/peppol', data = string_xml)
    json_data = data.json()
    assert data.status_code == 200
    assert json_data == [{'broken_rule' : "PEPPOL - EN16931 - R040", "broken_rule_detailed" : "Allowance/charge amount must equal base amount * percentage/100 if base amount and percentage exists"}]

def test_check_gross_net_amount_in_xml():

    string_xml = open_file_as_string("tests/example_invoice_invalid_gross_net_price.xml")
    data = requests.post(config.url + '/invoice/verify/peppol', data = string_xml)
    json_data = data.json()
    assert data.status_code == 200
    assert json_data == [{'broken_rule' : "PEPPOL - EN16931 - R046", "broken_rule_detailed" : "Item net price MUST equal (Gross price - Allowance amount) when gross price is provided."}]

def test_no_reference_in_xml():

    string_xml = open_file_as_string("tests/example_invoice_no_ref_number.xml")
    data = requests.post(config.url + '/invoice/verify/peppol', data = string_xml)
    json_data = data.json()
    assert data.status_code == 200
    assert json_data == [{'broken_rule' : "PEPPOL - EN16931 - R003", "broken_rule_detailed" : "A buyer reference or purchase order reference MUST be provided"}]

def test_valid_xml():

    string_xml = open_file_as_string("tests/exmaple_invoice.xml")
    data = requests.post(config.url + '/invoice/verify/peppol', data = string_xml)
    json_data = data.json()
    assert data.status_code == 200
    assert json_data == []

