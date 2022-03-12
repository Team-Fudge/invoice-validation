import pytest
from make_requests_test import *
from wellformedness import verify_wellformedness


# Whitebox testing
def test_wellformedness_invoice_correct():
    assert(verify_wellformedness("WF_correct.xml") == {'broken_rules': 'No broken rules found. Invoice is well-formed!'} )

def test_wellformedness_invoice_errors():
    assert(verify_wellformedness("WF_incorrect.xml") == {'broken_rules': ["ERROR ON LINE 23: Failed to parse QName 'cbc:'", 'ERROR ON LINE 23: Opening and ending tag mismatch: CityName line 23 and cbc:', 
                                                                       'ERROR ON LINE 33: Opening and ending tag mismatch: PartyName line 19 and Party', 
                                                                       'ERROR ON LINE 34: Opening and ending tag mismatch: Party line 15 and AccountingSupplierParty', 
                                                                       'ERROR ON LINE 101: Opening and ending tag mismatch: AccountingSupplierParty line 14 and Invoice', 
                                                                       'ERROR ON LINE 101: Premature end of data in tag Invoice line 2']})

# Blackbox/HTTP Testing
def test_wellformedness_no_invoice():
    assert  verify_wellformedness().statuscode == 400


