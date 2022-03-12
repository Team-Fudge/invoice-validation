from peppol_validation import check_reference_number, check_date_syntax, check_currency_Code, check_if_buyer_seller_address_exists, check_base_amount_and_percentage, check_gross_net_amount, check_xml_empty
from error import InputError
import pytest

def test_empty_file():
    with pytest.raises(InputError):
        check_xml_empty("empty_xml.xml")

def test_refernce_number():
    # No ref number (invalid invoice)
    assert(check_reference_number("example_invoice_no_ref_number.xml") == {'broken_rule' : "PEPPOL - EN16931 - R003", "broken_rule_detailed" : "A buyer reference or purchase order reference MUST be provided"})

def test_date_syntax_number():
    # Incorrect syntax (invalid invoice)
    assert(check_date_syntax("example_invoice_wrong_date_syntax.xml") == {'broken_rule' : "PEPPOL - EN16931 - F001", "broken_rule_detailed" : "A date MUST be formatted YYYY-MM-DD"})

def test_check_currency_Code():
    # Incorrect Currency Code (invalid invoice)
    assert(check_currency_Code("example_invoice_currency_code.xml") == {'broken_rule' : "PEPPOL - EN16931 - CL007", "broken_rule_detailed" : "Currency code must be according to ISO 4217:2005"})

def test_check_if_buyer_seller_address_exists():

    # No buyer or seller adddress (invalid invoice)
    assert(check_if_buyer_seller_address_exists("example_invoice_no_address.xml") == {'broken_rule' : "PEPPOL - EN16931 - R010", "broken_rule_detailed" : "Buyer electronic address MUST be provided"})
    
def test_check_base_amount_and_percentage():

    # Incorrect value of baseamount, percentage or amount (Invalid Invoice)
    assert(check_base_amount_and_percentage("example_invoice_invalid_percentage_baseamount.xml") == {'broken_rule' : "PEPPOL - EN16931 - R040", "broken_rule_detailed" : "Allowance/charge amount must equal base amount * percentage/100 if base amount and percentage exists"})
   
def test_check_gross_net_amount():

    # Incorrect value of Gross amount, allowance amount or netprice (Invalid Invoice)
    assert(check_gross_net_amount("example_invoice_invalid_gross_net_price.xml") == {'broken_rule' : "PEPPOL - EN16931 - R046", "broken_rule_detailed" : "Item net price MUST equal (Gross price - Allowance amount) when gross price is provided."})
    
def test_valid_invoic():
    # Valid invoice
    assert(check_gross_net_amount("exmaple_invoice.xml") == None)