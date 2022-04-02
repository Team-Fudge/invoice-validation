from src.schema_validation import verify_schema
from src.error import InputError
import pytest

def open_file_as_string(file_name):

    #open & read file
    with open(file_name, 'r') as f:
       data = f.read()

    return data


# Test Exceptions
def test_output_empty_xml():
    with pytest.raises(InputError):
        verify_schema(open_file_as_string("example_empty.xml"))

# Tests
def test_output():
        assert(isinstance(verify_schema(open_file_as_string("schema_incorrect.xml")), dict))
        assert(isinstance(verify_schema(open_file_as_string("schema_correct.xml")), dict))

# Whitebox Tests
def test_output_correct_xml():
    assert(verify_schema(open_file_as_string("schema_correct.xml")) == {'broken_rules': []})

def test_output_incorrect_xml():
    assert(verify_schema(open_file_as_string("schema_incorrect.xml")) == {'broken_rules': ['Invoice - This element MUST be conveyed as the root element in any instance document based on this Schema expression', 
                                                                                           'cbc:UBLVersionID - Identifies the earliest version of the UBL 2 schema for this document type that defines all of the elements that might be encountered in the current instance.',
                                                                                           'cbc:IssueDate - The date, assigned by the sender, on which this document was issued.']})

def test_output_duplicate_accounting_supplier():
    assert(verify_schema(open_file_as_string("duplicate_accounting_supplier_tag.xml")) == {'broken_rules': ['cac:AccountingSupplierParty - The accounting supplier party.']})