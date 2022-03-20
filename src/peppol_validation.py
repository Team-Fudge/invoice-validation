'''
import sys
from bs4 import BeautifulSoup
import datetime
import iso4217
from src.error import InputError, AccessError

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
    bs_content = BeautifulSoup(string_xml, "lxml")

    order_ref_result = bs_content.find_all("orderreference")
    biller_ref_result = bs_content.find_all("billersorderreference")
    payment_ref_result = bs_content.find_all("paymentreference")

    if order_ref_result == [] or biller_ref_result == [] or payment_ref_result == []:
        return {'broken_rule' : "PEPPOL - EN16931 - R003", "broken_rule_detailed" : "A buyer reference or purchase order reference MUST be provided"}

    return None

# Checking if date syntax is correct (PEPPOL - EN16931 - F001)
def check_date_syntax(string_xml):

    # bs_content = parse_xml_file(file_name)
    bs_content = BeautifulSoup(string_xml, "lxml")

    date_result = bs_content.find_all("date")
    invoice_date_result = bs_content.find_all("invoicedate")
    ref_date_result = bs_content.find_all("referencedate")
    
    date_result_flag = True
    invoice_date_result_flag = True
    ref_date_result_flag = True

    # check if tags named date are in form YYYY-MM-DD 
    for date in date_result:
        if date_time_check_format(date.get_text()) == False:
            date_result_flag = False

    # check if tags named invoice date are in form YYYY-MM-DD 
    for date in invoice_date_result:
        if date_time_check_format(date.get_text()) == False:
            invoice_date_result_flag = False
        

    # check if tags named refernce date are in form YYYY-MM-DD 
    for date in ref_date_result:
        if date_time_check_format(date.get_text()) == False:
            ref_date_result_flag == False

    if date_result_flag == False or invoice_date_result_flag == False or ref_date_result_flag == False:
        return {'broken_rule' : "PEPPOL - EN16931 - F001", "broken_rule_detailed" : "A date MUST be formatted YYYY-MM-DD"}

    return None

# Checking if currency code is valid (PEPPOL - EN16931 - CL007)
def check_currency_Code(string_xml):

    # bs_content = parse_xml_file(file_name)
    bs_content = BeautifulSoup(string_xml, "lxml")

    Currency_result = bs_content.find_all("invoice")
    currency_code = Currency_result[0]["invoicecurrency"]
    currency_code = currency_code.lower()

    if currency_code not in dir(iso4217.Currency):
        return {'broken_rule' : "PEPPOL - EN16931 - CL007", "broken_rule_detailed" : "Currency code must be according to ISO 4217:2005"}

    return None

# Checking if buyer seller address exists (PEPPOL - EN16931 - R010 and PEPPOL - EN16931 - R020)
def check_if_buyer_seller_address_exists(string_xml):

    # bs_content = parse_xml_file(file_name)
    bs_content = BeautifulSoup(string_xml, "lxml")
    InvoiceRecipient_result = bs_content.find_all("invoicerecipient")
    Biller_result = bs_content.find_all("biller")

    for tag in  InvoiceRecipient_result:
        str_tag = str(tag)
        if "<address>" not in str_tag:
            return {'broken_rule' : "PEPPOL - EN16931 - R010", "broken_rule_detailed" : "Buyer electronic address MUST be provided"}
            
    for tag in  Biller_result:
        str_tag = str(tag)
        if "<address>" not in str_tag:
            return {'broken_rule' : "PEPPOL - EN16931 - R020", "broken_rule_detailed" : "Seller electronic address MUST be provided"}

    return None

# Checking if base amount and percentage and amount have the correct relationship (PEPPOL - EN16931 - R040)
def check_base_amount_and_percentage(string_xml):

    # bs_content = parse_xml_file(file_name)
    bs_content = BeautifulSoup(string_xml, "lxml")
    all_base_amounts = bs_content.find_all("baseamount")
    all_percentage = bs_content.find_all("percentage")
    all_amounts = bs_content.find_all("amount")

    for index in range(len(all_base_amounts)):

        int_all_base_amounts = float("{:.2f}".format(float(all_base_amounts[index].get_text()))) # getting base amount
        int_all_percentage = float(list(all_base_amounts[index].next_siblings)[1].get_text()) # getting percentage
        int_all_amounts = float(list(all_base_amounts[index].next_siblings)[3].get_text()) # getting percentage

        if float("{:.2f}".format(int_all_base_amounts * (int_all_percentage/100))) != int_all_amounts: # checking peppol rule
            return {'broken_rule' : "PEPPOL - EN16931 - R040", "broken_rule_detailed" : "Allowance/charge amount must equal base amount * percentage/100 if base amount and percentage exists"} 

    return None

# Checking if gross_amount - prepaid_amount = payable_amount  (PEPPOL - EN16931 - R046)
def check_gross_net_amount(string_xml):

    # bs_content = parse_xml_file(file_name)
    bs_content = BeautifulSoup(string_xml, "lxml")
    gross_amount = bs_content.find("totalgrossamount")
    prepaid_amount = bs_content.find("prepaidamount")
    payable_amount = bs_content.find("payableamount")

    int_gross_amount = float(gross_amount.get_text())
    int_prepaid_amount = float(prepaid_amount.get_text())
    int_payable_amount = float(payable_amount.get_text())

    if (int_gross_amount - int_prepaid_amount != int_payable_amount):
        return {'broken_rule' : "PEPPOL - EN16931 - R046", "broken_rule_detailed" : "Item net price MUST equal (Gross price - Allowance amount) when gross price is provided."} 

    return None 


if __name__ == "__main__":
    invoice_file = "empty_xml.xml"
    check_xml_empty(invoice_file)

    

'''
