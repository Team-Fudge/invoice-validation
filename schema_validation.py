'''
Jasmine Wong 2021
'''

from error import InputError
from error import AccessError
import xmlschema
#from invoice_validation import schema_rules
#import example_invoice.xml

def schema_validation(invoice):
    schema = xmlschema.XMLSchema('schema_rules.xsd')
    validation_error_iterator = schema.iter_errors(invoice)
    errors = list()
    for idx, validation_error in enumerate(validation_error_iterator, start=1):
        err = validation_error.__str__()
        errors.append(err)
        print(err)
    return errors

# test functionality
if __name__ == "__main__":
    schema_validation('example_invoice.xml')