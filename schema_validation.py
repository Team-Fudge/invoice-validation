'''
Jasmine Wong 2022
'''

import xmlschema
from error import AccessError, InputError

def schema_validation(invoice):
    
    #schema = xmlschema.XMLSchema('schema_rules.xsd')
    schema_file = open('schema_rules.xsd')
    schema = xmlschema.XMLSchema(schema_file)
    validation_error_iterator = schema.iter_errors(invoice)
    errors = list()
    for idx, validation_error in enumerate(validation_error_iterator, start=1):
        err = validation_error.__str__()
        errors.append(err)
        print(err)
    return errors
    
if __name__ == "__main__":
    schema_validation('invoice_sample.xml')