from lxml import etree
from error import InputError, AccessError
import os 

def verify_wellformedness(invoice_file):
    
    broken_rules = []
    
    if  not os.path.isfile(invoice_file):
        raise InputError("No invoice recieved.")
    
    if os. stat(invoice_file).st_size == 0:
        return {"broken_rules": "The provided file is empty"}
    
    # If invoice is successfully well-formed
    try:
        tree = etree.parse(invoice_file)
        return {"broken_rules": "No broken rules found. Invoice is well-formed!" }
    
    # If errors are present, go through error log file and save it to list
    except etree.XMLSyntaxError as err:
        for error in err.error_log:
            error_line = ("ERROR ON LINE %s: %s" % (error.line, error.message))
            broken_rules.append(error_line)
    
    return {"broken_rules": broken_rules}

if __name__ == "__main__":
    invoice_file = "WF_incorrect.xml"
    print(verify_wellformedness(invoice_file))
