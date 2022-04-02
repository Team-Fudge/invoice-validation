from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from src.error import InputError, AccessError
import re
import os

def check_root(string_xml):
	root = ET.fromstring(string_xml)
	if root.tag == '{urn:oasis:names:specification:ubl:schema:xsd:Invoice-2}Invoice':
		return 1
	return None

def check_no_more_than_one(string_xml, tag):
    data = BeautifulSoup(string_xml, "xml")

    el_list = data.find_all(tag)
    
    if len(el_list) <= 1:
        return 1
    return None

def check_only_one(string_xml, tag):
    data = BeautifulSoup(string_xml, "xml")

    el_list = data.find_all(tag)
    
    if len(el_list) == 1:
        return 1
    return None

def check_min_one(string_xml, tag):
    data = BeautifulSoup(string_xml, "xml")

    el_list = data.find_all(tag)
    
    if len(el_list) >= 1:
        return 1
    return None

def verify_schema(string_xml):
    
    if len(string_xml) == 0:
        raise InputError("No file recieved")
    
    
    rule_book = {
        "Invoice - This element MUST be conveyed as the root element in any instance document based on this Schema expression": check_root(string_xml),
		"cbc:UBLVersionID - Identifies the earliest version of the UBL 2 schema for this document type that defines all of the elements that might be encountered in the current instance.": check_no_more_than_one(string_xml, 'cbc:UBLVersionID'),
		"cbc:CustomizationID - Identifies a user-defined customization of UBL for a specific use.": check_no_more_than_one(string_xml, 'cbc:CustomizationID'),
		"cbc:ProfileID - Identifies a user-defined profile of the customization of UBL being used.": check_no_more_than_one(string_xml, 'cbc:ProfileID'),
		"cbc:ProfileExecutionID - Identifies an instance of executing a profile, to associate all transactions in a collaboration.": check_no_more_than_one(string_xml, 'cbc:ProfileExecutionID'),
        "cbc:ID - An identifier for this document, assigned by the sender.": check_min_one(string_xml, 'cbc:ID'),
        "cbc:CopyIndicator - Indicates whether this document is a copy (true) or not (false).": check_no_more_than_one(string_xml, 'cbc:CopyIndicator'),
        "cbc:UUID - A universally unique identifier for an instance of this document.": check_no_more_than_one(string_xml, 'cbc:UUID'),
        "cbc:IssueDate - The date, assigned by the sender, on which this document was issued.": check_min_one(string_xml, 'cbc:IssueDate'),
        "cbc:IssueTime - The time, assigned by the sender, at which this document was issued.": check_no_more_than_one(string_xml, 'cbc:IssueTime'),
        "cbc:DueDate - The date on which Invoice is due.": check_no_more_than_one(string_xml, 'cbc:DueDate'),
        "cbc:InvoiceTypeCode - A code signifying the type of the Invoice.": check_no_more_than_one(string_xml, 'cbc:InvoiceTypeCode'),
        "cbc:TaxPointDate - The date of the Invoice, used to indicate the point at which tax becomes applicable.": check_no_more_than_one(string_xml, 'cbc:TaxPointDate'),
        "cbc:DocumentCurrencyCode - A code signifying the default currency for this document.": check_no_more_than_one(string_xml, 'cbc:DocumentCurrencyCode'),
        "cbc:TaxCurrencyCode - A code signifying the currency used for tax amounts in the Invoice.": check_no_more_than_one(string_xml, 'cbc:TaxCurrencyCode'),
        "cbc:PricingCurrencyCode - A code signifying the currency used for prices in the Invoice.": check_no_more_than_one(string_xml, 'cbc:PricingCurrencyCode'),
        "cbc:PaymentCurrencyCode - A code signifying the currency used for payment in the Invoice.": check_no_more_than_one(string_xml, 'cbc:PaymentCurrencyCode'),
        "cbc:PaymentAlternativeCurrencyCode - A code signifying the alternative currency used for payment in the Invoice.": check_no_more_than_one(string_xml, 'cbc:PaymentAlternativeCurrencyCode'),
        "cbc:AccountingCostCode - The buyer's accounting code, applied to the Invoice as a whole.": check_no_more_than_one(string_xml, 'cbc:AccountingCostCode'),
        "cbc:LineCountNumeric - The number of lines in the document.": check_no_more_than_one(string_xml, 'cbc:LineCountNumeric'),
        "cac:OrderReference - A reference to the Order with which this Invoice is associated.": check_no_more_than_one(string_xml, 'cac:OrderReference'),
        "cac:AccountingSupplierParty - The accounting supplier party.": check_only_one(string_xml, 'cac:AccountingSupplierParty'),
        "cac:AccountingCustomerParty - The accounting customer party.": check_only_one(string_xml, 'cac:AccountingCustomerParty'),
        "cac:PayeeParty - The payee.": check_no_more_than_one(string_xml, 'cac:PayeeParty'),
        "cac:BuyerCustomerParty - The buyer.": check_no_more_than_one(string_xml, 'cac:BuyerCustomerParty'),
        "cac:SellerSupplierParty - The seller.": check_no_more_than_one(string_xml, 'cac:SellerSupplierParty'),
        "cac:TaxRepresentativeParty - The tax representative.": check_no_more_than_one(string_xml, 'cac:TaxRepresentativeParty'),
        "cac:DeliveryTerms - A set of delivery terms associated with this document.": check_no_more_than_one(string_xml, 'cac:DeliveryTerms'),
        "cac:TaxExchangeRate - The exchange rate between the document currency and the tax currency.": check_no_more_than_one(string_xml, 'cac:TaxExchangeRate'),
        "cac:PricingExchangeRate - The exchange rate between the document currency and the pricing currency.": check_no_more_than_one(string_xml, 'cac:PricingExchangeRate'),
        "cac:PaymentExchangeRate - The exchange rate between the document currency and the payment currency.": check_no_more_than_one(string_xml, 'cac:PaymentExchangeRate'),
        "cac:PaymentAlternativeExchangeRate - The exchange rate between the document currency and the payment alternative currency.": check_no_more_than_one(string_xml, 'cac:PaymentAlternativeExchangeRate'),
        "cac:LegalMonetaryTotal - The total amount payable on the Invoice, including Allowances, Charges, and Taxes.": check_only_one(string_xml, 'cac:LegalMonetaryTotal'),
        "cac:InvoiceLine - A line describing an invoice item.": check_min_one(string_xml, 'cac:InvoiceLine')
        
    }
    broken_rules = []
    

    for tag in rule_book:
        if rule_book.get(tag) == None:
            broken_rules.append(tag)
    
    return {"broken_rules": broken_rules}
