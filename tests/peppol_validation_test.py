
from src.peppol_validation import check_reference_number, check_date_syntax, check_currency_Code, check_if_buyer_seller_address_exists, check_xml_empty, check_if_one_tax_total_is_provided, check_if_base_quantity_is_positive_number, check_valid, empty_broken_rules
from src.error import InputError
import pytest
from bs4 import BeautifulSoup

def open_file(file_name):

    #open & read file
    with open(file_name, 'r') as f:
       data = f.read()
    return data

def test_empty_file():

    string_xml = open_file("example_empty.xml")
    with pytest.raises(InputError):
        check_xml_empty(string_xml)

def test_refernce_number():

    string_xml = open_file("peppol_incorrect.xml") #parse_xml_file("example_invoice_no_ref_number.xml")
    # No ref number (invalid invoice)
    assert(check_reference_number(string_xml) == {'broken_rule' : "PEPPOL - EN16931 - R003", "broken_rule_detailed" : "A buyer reference or purchase order reference MUST be provided"})

def test_date_syntax_number():
    
    string_xml = open_file("peppol_incorrect.xml")
    # Incorrect syntax (invalid invoice)
    assert(check_date_syntax(string_xml) == {'broken_rule' : "PEPPOL - EN16931 - F001", "broken_rule_detailed" : "A date MUST be formatted YYYY-MM-DD"})
  

def test_check_currency_Code():

    string_xml = open_file("peppol_incorrect.xml")
    # Incorrect Currency Code (invalid invoice)
    assert(check_currency_Code(string_xml) == {'broken_rule' : "PEPPOL - EN16931 - CL007", "broken_rule_detailed" : "Currency code must be according to ISO 4217:2005"})

def test_check_if_buyer_seller_address_exists():

    string_xml = open_file("peppol_incorrect.xml")
    # No buyer or seller adddress (invalid invoice)
    assert(check_if_buyer_seller_address_exists(string_xml) == {'broken_rule' : "PEPPOL - EN16931 - R010", "broken_rule_detailed" : "Buyer electronic address MUST be provided"})


def test_check_if_tax_total_exists():

    string_xml = open_file("peppol_incorrect.xml")
    # No buyer or seller adddress (invalid invoice)
    assert(check_if_one_tax_total_is_provided(string_xml) == {'broken_rule' : "PEPPOL - EN16931 - R053", "broken_rule_detailed" : "Only one tax total with tax subtotals MUST be provided"})

def test_base_quantity_more_than_0():

    string_xml = open_file("peppol_incorrect.xml")
    # No buyer or seller adddress (invalid invoice)
    assert(check_if_base_quantity_is_positive_number(string_xml) == {'broken_rule' : "PEPPOL - EN16931 - R121", "broken_rule_detailed" : "Base quantity MUST be a positive number abover 0"})
    
def test_valid_invoic():

    empty_broken_rules()
    string_xml = open_file("example_good.xml")
    # Valid invoice

    for element in check_valid(string_xml):
        assert element == None
    

