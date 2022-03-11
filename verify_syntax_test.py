from verify_syntax import identify_errors
from error import InputError
import pytest
def test_no_real_file():
    with pytest.raises(InputError):
        identify_errors("invalid")

def test_output_type_wrong_xml():
        assert(isinstance(identify_errors("example_broken.xml"), dict))

#the below are whiteboard tests

def test_output_wrong_xml():
    assert(identify_errors("example_broken.xml") == {'broken_rules': ['BR-01'],
                                                     'broken_rules_detailed': ['[BR-01]-An Invoice shall have a Specification identifier (BT-24).'],
                                                     'disclaimer': 'The current version of this microservice can only test syntax errors BR-01 to BR-16'
                                                     })
def test_output_correct_xml():
    assert(identify_errors("example_good.xml") == {"broken_rules": [], "broken_rules_detailed": [], "disclaimer": 'The current version of this microservice can only test syntax errors BR-01 to BR-16'})

def test_output_empty_xml():
    assert(identify_errors("example_empty.xml") == {'broken_rules': 'The provided file is empty', 'broken_rules_detailed': 'The provided file is empty', 'disclaimer': 'The current version of this microservice can only test syntax errors BR-01 to BR-16'})