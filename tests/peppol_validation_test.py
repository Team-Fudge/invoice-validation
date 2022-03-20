'''
from src.peppol_validation import check_reference_number, check_date_syntax, check_currency_Code, check_if_buyer_seller_address_exists, check_base_amount_and_percentage, check_gross_net_amount, check_xml_empty
from src.error import InputError
import pytest
from bs4 import BeautifulSoup

def open_file(file_name):

    #open & read file
    with open(file_name, 'r') as f:
       data = f.read()
    return data

def test_empty_file():

    string_xml = open_file("tests/empty_xml.xml")
    with pytest.raises(InputError):
        check_xml_empty(string_xml)

def test_refernce_number():

    string_xml = open_file("tests/example_invoice_no_ref_number.xml") #parse_xml_file("example_invoice_no_ref_number.xml")
    # No ref number (invalid invoice)
    assert(check_reference_number(string_xml) == {'broken_rule' : "PEPPOL - EN16931 - R003", "broken_rule_detailed" : "A buyer reference or purchase order reference MUST be provided"})

def test_date_syntax_number():
    
    string_xml = open_file("tests/example_invoice_wrong_date_syntax.xml")
    # Incorrect syntax (invalid invoice)
    assert(check_date_syntax(string_xml) == {'broken_rule' : "PEPPOL - EN16931 - F001", "broken_rule_detailed" : "A date MUST be formatted YYYY-MM-DD"})

def test_check_currency_Code():

    string_xml = open_file("tests/example_invoice_currency_code.xml")
    # Incorrect Currency Code (invalid invoice)
    assert(check_currency_Code(string_xml) == {'broken_rule' : "PEPPOL - EN16931 - CL007", "broken_rule_detailed" : "Currency code must be according to ISO 4217:2005"})

def test_check_if_buyer_seller_address_exists():

    string_xml = open_file("tests/example_invoice_no_address.xml")
    # No buyer or seller adddress (invalid invoice)
    assert(check_if_buyer_seller_address_exists(string_xml) == {'broken_rule' : "PEPPOL - EN16931 - R010", "broken_rule_detailed" : "Buyer electronic address MUST be provided"})
    
def test_check_base_amount_and_percentage():

    string_xml = open_file("tests/example_invoice_invalid_percentage_baseamount.xml")
    # Incorrect value of baseamount, percentage or amount (Invalid Invoice)
    assert(check_base_amount_and_percentage(string_xml) == {'broken_rule' : "PEPPOL - EN16931 - R040", "broken_rule_detailed" : "Allowance/charge amount must equal base amount * percentage/100 if base amount and percentage exists"})
   
def test_check_gross_net_amount():

    string_xml = open_file("tests/example_invoice_invalid_gross_net_price.xml")
    # Incorrect value of Gross amount, allowance amount or netprice (Invalid Invoice)
    assert(check_gross_net_amount(string_xml) == {'broken_rule' : "PEPPOL - EN16931 - R046", "broken_rule_detailed" : "Item net price MUST equal (Gross price - Allowance amount) when gross price is provided."})
    
def test_valid_invoic():

    string_xml = open_file("tests/exmaple_invoice.xml")
    # Valid invoice
    assert(check_gross_net_amount(string_xml) == None)

'''