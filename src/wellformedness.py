from lxml import etree
from lxml.etree import fromstring
from error import InputError, AccessError

def verify_wellformedness(invoice_file):

    if not invoice_file:
        raise InputError("No invoice provided")
    
    broken_rules = []
    
    if len(invoice_file)== 0:
        return {"broken_rules": "The provided file is empty"}
    
    # If invoice is successfully well-formed
    # Format of invoice will be a string
    try:
        tree = etree.fromstring(invoice_file)
        return {"broken_rules": "No broken rules found. Invoice is well-formed!" }
    
    # If errors are present, go through error log file and save it to list
    except etree.XMLSyntaxError as err:
        for error in err.error_log:
            error_line = ("ERROR ON LINE %s: %s" % (error.line, error.message))
            broken_rules.append(error_line)
    
    return {"broken_rules": broken_rules}
