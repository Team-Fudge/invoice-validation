from src.verify_syntax import open_and_check_error_for_tests, verify_syntax_errors
import pytest


def open_file_as_string(file_name):

    #open & read file
    with open(file_name, 'r') as f:
       data = f.read()

    return data



def test_output_type_wrong_xml():
        assert(isinstance(verify_syntax_errors(open_file_as_string("example_broken.xml")), dict))

#the below are whiteboard tests

def test_output_wrong_xml():
    assert(verify_syntax_errors(open_file_as_string("example_broken.xml")) == {'broken_rules': ['BR-01'],
                                                     'broken_rules_detailed': ['[BR-01]-An Invoice shall have a Specification identifier (BT-24).'],
                                                     'disclaimer': 'The current version of this microservice can only test syntax errors BR-01 to BR-16'
                                                     })
def test_output_correct_xml():
    assert(verify_syntax_errors(open_file_as_string("example_good.xml")) == {"broken_rules": [], "broken_rules_detailed": [], "disclaimer": 'The current version of this microservice can only test syntax errors BR-01 to BR-16'})

def test_output_empty_xml():
    assert(verify_syntax_errors(open_file_as_string("example_empty.xml")) == {'broken_rules': 'The provided file is empty', 'broken_rules_detailed': 'The provided file is empty', 'disclaimer': 'The current version of this microservice can only test syntax errors BR-01 to BR-16'})
