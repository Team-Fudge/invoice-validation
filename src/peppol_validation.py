
import sys
from bs4 import BeautifulSoup
import datetime
from src.error import InputError, AccessError
from src.helper import valid_token, valid_user_id

broken_rules = []
currency_codes = ['aed', 'afn', 'all', 'amd', 'ang', 'aoa', 'ars', 'aud', 'awg', 'azn', 'bam', 'bbd', 
                'bdt', 'bgn', 'bhd', 'bif', 'bmd', 'bnd', 'bob', 'bov', 'brl', 'bsd', 'btn', 'bwp', 'byn', 'bzd', 'cad', 'cdf', 
                'che', 'chf', 'chw', 'clf', 'clp', 'cny', 'cop', 'cou', 'crc', 'cuc', 'cup', 'cve', 'czk', 'djf', 'dkk', 'dop', 
                'dzd', 'egp', 'ern', 'etb', 'eur', 'fjd', 'fkp', 'gbp', 'gel', 'ghs', 'gip', 'gmd', 'gnf', 'gtq', 'gyd', 'hkd', 
                'hnl', 'hrk', 'htg', 'huf', 'idr', 'ils', 'inr', 'iqd', 'irr', 'isk', 'jmd', 'jod', 'jpy', 'kes', 'kgs', 'khr', 
                'kmf', 'kpw', 'krw', 'kwd', 'kyd', 'kzt', 'lak', 'lbp', 'lkr', 'lrd', 'lsl', 'lyd', 'mad', 'mdl', 'mga', 'mkd', 
                'mmk', 'mnt', 'mop', 'mru', 'mur', 'mvr', 'mwk', 'mxn', 'mxv', 'myr', 'mzn', 'nad', 'ngn', 'nio', 'nok', 'npr', 
                'nzd', 'omr', 'pab', 'pen', 'pgk', 'php', 'pkr', 'pln', 'pyg', 'qar', 'ron', 'rsd', 'rub', 'rwf', 'sar', 'sbd', 
                'scr', 'sdg', 'sek', 'sgd', 'shp', 'sll', 'sos', 'srd', 'ssp', 'stn', 'svc', 'syp', 'szl', 'thb', 'tjs', 'tmt', 
                'tnd', 'top', 'try', 'ttd', 'twd', 'tzs', 'uah', 'ugx', 'usd', 'usn', 'uyi', 'uyu', 'uyw', 'uzs', 'ved', 'ves', 
                'vnd', 'vuv', 'wst', 'xaf', 'xcd', 'xof', 'xpf', 'yer', 'zar', 'zmw', 'zwl']

# Checks if the date format is in YYYY-MM-DD
def date_time_check_format(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Checks is xml is empty
def check_xml_empty(string_xml):

    data = BeautifulSoup(string_xml, "lxml")
    ret = data.get_text() #parse_xml_file(file_name).get_text()

    if (ret == ""): #if file is empty
        raise InputError(description = 'XML isnt valid because it is empty') 


# Checking if order refernce, billeer order and payment reference exists (PEPPOL - EN16931 - R003)
def check_reference_number(string_xml):

    # bs_content = parse_xml_file(file_name)
    bs_content = BeautifulSoup(string_xml, "xml")

    buyer_reference = bs_content.find_all("BuyerReference")
    purchase_reference = bs_content.find_all("PurchaseReference")

    if buyer_reference == [] and purchase_reference == []:
        broken_rule =  {'broken_rule' : "PEPPOL - EN16931 - R003", "broken_rule_detailed" : "A buyer reference or purchase order reference MUST be provided"}
        broken_rules.append(broken_rule)
        return broken_rule

    return None

# Checking if date syntax is correct (PEPPOL - EN16931 - F001)
def check_date_syntax(string_xml):

    # bs_content = parse_xml_file(file_name)
    bs_content = BeautifulSoup(string_xml, "xml")

    date_result = bs_content.find_all("IssueDate")
    date_result_flag = True

    # check if tags named date are in form YYYY-MM-DD 
    for date in date_result:
        if date_time_check_format(date.string) == False:
            date_result_flag = False

    if date_result_flag == False:
        broken_rule = {'broken_rule' : "PEPPOL - EN16931 - F001", "broken_rule_detailed" : "A date MUST be formatted YYYY-MM-DD"}
        broken_rules.append(broken_rule)
        return broken_rule

    return None

# Checking if currency code is valid (PEPPOL - EN16931 - CL007)
def check_currency_Code(string_xml): #check this

    # bs_content = parse_xml_file(file_name)
    bs_content = BeautifulSoup(string_xml, "xml")

    Currency_result = bs_content.find_all("DocumentCurrencyCode")
    currency_code = Currency_result[0].string
    currency_code = str(currency_code).lower()

    if currency_code not in currency_codes:
        broken_rule = {'broken_rule' : "PEPPOL - EN16931 - CL007", "broken_rule_detailed" : "Currency code must be according to ISO 4217:2005"}
        broken_rules.append(broken_rule)
        return broken_rule

    return None

# Checking if buyer seller address exists (PEPPOL - EN16931 - R010 and PEPPOL - EN16931 - R020)
def check_if_buyer_seller_address_exists(string_xml):

    # bs_content = parse_xml_file(file_name)
    bs_content = BeautifulSoup(string_xml, "xml")
    PostalAddress_result = bs_content.find_all("PostalAddress")
    print(PostalAddress_result)

    if PostalAddress_result == []: 
        broken_rule = {'broken_rule' : "PEPPOL - EN16931 - R010", "broken_rule_detailed" : "Buyer electronic address MUST be provided"}
        broken_rules.append(broken_rule)
        return broken_rule
            
    return None

# Checking if only one tax total is provided (PEPPOL - EN16931 - R053)

def check_if_one_tax_total_is_provided(string_xml):

    # bs_content = parse_xml_file(file_name)
    bs_content = BeautifulSoup(string_xml, "xml")
    taxtotal_result = bs_content.find_all("TaxTotal")
    taxsubtotal_result = bs_content.find_all("TaxSubtotal")

    if taxtotal_result == [] or taxsubtotal_result == []:
        broken_rule = {'broken_rule' : "PEPPOL - EN16931 - R053", "broken_rule_detailed" : "Only one tax total with tax subtotals MUST be provided"}
        broken_rules.append(broken_rule)
        return broken_rule
            
    return None

#  Checking if Base quantity MUST be a positive number abover 0
def check_if_base_quantity_is_positive_number(string_xml):

    # bs_content = parse_xml_file(file_name)
    bs_content = BeautifulSoup(string_xml, "xml")
    basequantity_result = bs_content.find_all("BaseQuantity")

    basequantity_val = basequantity_result[0].string
    float_basequantity = float(basequantity_val)

    if float_basequantity < 0: 
        broken_rule = {'broken_rule' : "PEPPOL - EN16931 - R121", "broken_rule_detailed" : "Base quantity MUST be a positive number abover 0"}
        broken_rules.append(broken_rule)
        return broken_rule
            
    return None

def check_valid(token, string_xml):
    
    if not valid_token(token):
        raise AccessError(description='Invalid token')
    
    global broken_rules
    broken_rules = []

    check_xml_empty(string_xml)
    check_reference_number(string_xml)
    check_date_syntax(string_xml)
    check_currency_Code(string_xml)
    check_if_buyer_seller_address_exists(string_xml)
    check_if_one_tax_total_is_provided(string_xml)
    check_if_base_quantity_is_positive_number(string_xml)

    return broken_rules

def empty_broken_rules():
    global broken_rules
    broken_rules = []

if __name__ == "__main__":
    invoice_file = "empty_xml.xml"
    check_xml_empty(invoice_file)

    


