import sys
import pytest
import requests
import json
from src import server
from src import config
from src.error import InputError, AccessError


# JSON DATA to be converted
json_data = {
        "UBLID": 2.1,
        "CustomizationID": "urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0",
        "ProfileID": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0",
        "ID": "EBWASP1002",
        "IssueDate": "2022-02-07",
        "InvoiceCode": 380,
        "Currency": "AUD",
        "BuyerReference": "EBWASP1002",
        "AddDocReference": "ebwasp1002",
        "SupplierID": 80647710156,
         "SupplierStreet": "100 Business Street",
        "SupplierCity": "Dulwich Hill",
        "SupplierPost": 2203,
        "SupplierCountry": "AU",
        "SupplierRegistration": "Ebusiness Software Services Pty Ltd",
        "CustomerStreet": "Suite 132 Level 45",
        "CustomerAddStreet": "999 The Crescent",
        "CustomerCity": "Homebush West",
        "CustomerPost": "2140",
        "CustomerCountry": "AU",
        "CustomerRegistration": "Awolako Enterprises Pty Ltd",
        "PaymentType": 1,
        "PaymentID": "EBWASP1002",
        "PaymentTerms": "As agreed",
        "TaxAmount": 10,
        "TaxableAmount": 100,
        "TaxSubtotalAmount": 10,
        "TaxID": "S",
        "TaxPercent": 10,
        "TaxSchemeID": "GST",
        "LegalLineExtension": 100,
        "TaxExclusiveAmount": 100,
        "TaxInclusiveAmount": 110,
        "PayableRoundingAmount": 0,
        "PayableAmount": 110,
        "InvoiceID": 1,
        "InvoiceQuantity": 500,
        "InvoiceLineExtension": 100,
        "InvoiceName": "Pencils",
        "InvoiceTaxID": 5,
        "InvoiceTaxPercent": 10,
        "InvoiceTaxSchemeID": "GST",
        "InvoicePriceAmount": 0.2,
        "InvoiceBaseQuantity": 1,
        "InvoiceID2": 1,
        "InvoiceQuantity2": 500,
        "InvoiceLineExtension2": 100,
        "InvoiceName2": "Erasers",
        "InvoiceTaxID2": 12345,
        "InvoiceTaxPercent2": 10,
        "InvoiceTaxSchemeID2": "GST",
        "InvoicePriceAmount2": 0.2,
        "InvoiceBaseQuantity2": 1
    }
    
def test_api_creation_request_good():
    data = requests.post(config.url + 'invoice/create', json=json_data)
    assert data.status_code == 200