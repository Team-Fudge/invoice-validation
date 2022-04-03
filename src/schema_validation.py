from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from src.error import InputError, AccessError
import re
import os
from src.helper import valid_token, valid_user_id

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

def verify_schema(token, string_xml):
    
    if not valid_token(token):
        raise AccessError(description='Invalid token')
    
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


def open_and_check_error_for_tests(file_name):
    string_xml = open_file_as_string(file_name)
    return verify_schema(string_xml)



if __name__ == "__main__":
    
    string_xml_1 = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Incorrect xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:cec="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2">
   <cbc:UBLVersionID>2.1</cbc:UBLVersionID>
   <cbc:CustomizationID></cbc:CustomizationID>
   <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
   <cbc:ID>EBWASP1002</cbc:ID>
   <cbc:IssueDate>2022-02-07</cbc:IssueDate>
   <cbc:InvoiceTypeCode listAgencyID="6" listID="UNCL1001">380</cbc:InvoiceTypeCode>
   <cbc:DocumentCurrencyCode listAgencyID="6" listID="ISO4217">AUD</cbc:DocumentCurrencyCode>
   <cbc:BuyerReference>EBWASP1002</cbc:BuyerReference>
   <cac:AdditionalDocumentReference>
      <cbc:ID>ebwasp1002</cbc:ID>
   </cac:AdditionalDocumentReference>
   <cac:AccountingSupplierParty>
      <cac:Party>
         <cac:PartyIdentification>
            <cbc:ID schemeAgencyID="ZZZ" schemeID="0151">80647710156</cbc:ID>
         </cac:PartyIdentification>
         <cac:PartyName>
            <cbc:Name>Ebusiness Software Services Pty Ltd</cbc:Name>
         </cac:PartyName>
         <cac:PostalAddress>
            <cbc:StreetName>100 Business St</cbc:StreetName>
            <cbc:CityName>Dulwich Hill</cbc:CityName>
            <cbc:PostalZone>2203</cbc:PostalZone>
            <cac:Country>
               <cbc:IdentificationCode listAgencyID="6" listID="ISO3166-1:Alpha2">AU</cbc:IdentificationCode>
            </cac:Country>
         </cac:PostalAddress>
         <cac:PartyLegalEntity>
            <cbc:RegistrationName>Ebusiness Software Services Pty Ltd</cbc:RegistrationName>
            <cbc:CompanyID schemeAgencyID="ZZZ" schemeID="0151">80647710156</cbc:CompanyID>
         </cac:PartyLegalEntity>
      </cac:Party>
   </cac:AccountingSupplierParty>
   <cac:AccountingCustomerParty>
      <cac:Party>
         <cac:PartyName>
            <cbc:Name>Awolako Enterprises Pty Ltd</cbc:Name>
         </cac:PartyName>
         <cac:PostalAddress>
            <cbc:StreetName>Suite 123 Level 45</cbc:StreetName>
            <cbc:AdditionalStreetName>999 The Crescent</cbc:AdditionalStreetName>
            <cbc:CityName>Homebush West</cbc:CityName>
            <cbc:PostalZone>2140</cbc:PostalZone>
            <cac:Country>
               <cbc:IdentificationCode listAgencyID="6" listID="ISO3166-1:Alpha2">AU</cbc:IdentificationCode>
            </cac:Country>
         </cac:PostalAddress>
         <cac:PartyLegalEntity>
            <cbc:RegistrationName>Awolako Enterprises Pty Ltd</cbc:RegistrationName>
         </cac:PartyLegalEntity>
      </cac:Party>
   </cac:AccountingCustomerParty>
   <cac:PaymentMeans>
      <cbc:PaymentMeansCode listAgencyID="6" listID="UNCL4461">1</cbc:PaymentMeansCode>
      <cbc:PaymentID>EBWASP1002</cbc:PaymentID>
   </cac:PaymentMeans>
   <cac:PaymentTerms>
      <cbc:Note>As agreed</cbc:Note>
   </cac:PaymentTerms>
   <cac:TaxTotal>
      <cbc:TaxAmount currencyID="AUD">10.00</cbc:TaxAmount>
      <cac:TaxSubtotal>
         <cbc:TaxableAmount currencyID="AUD">100.00</cbc:TaxableAmount>
         <cbc:TaxAmount currencyID="AUD">10.00</cbc:TaxAmount>
         <cac:TaxCategory>
            <cbc:ID schemeAgencyID="6" schemeID="UNCL5305">S</cbc:ID>
            <cbc:Percent>10.0</cbc:Percent>
            <cac:TaxScheme>
               <cbc:ID schemeAgencyID="6" schemeID="UN/ECE 5153">GST</cbc:ID>
            </cac:TaxScheme>
         </cac:TaxCategory>
      </cac:TaxSubtotal>
   </cac:TaxTotal>
   <cac:LegalMonetaryTotal>
      <cbc:LineExtensionAmount currencyID="AUD">100.00</cbc:LineExtensionAmount>
      <cbc:TaxExclusiveAmount currencyID="AUD">100.00</cbc:TaxExclusiveAmount>
      <cbc:TaxInclusiveAmount currencyID="AUD">110.00</cbc:TaxInclusiveAmount>
      <cbc:PayableRoundingAmount currencyID="AUD">0.00</cbc:PayableRoundingAmount>
      <cbc:PayableAmount currencyID="AUD">110.00</cbc:PayableAmount>
   </cac:LegalMonetaryTotal>
   <cac:InvoiceLine>
      <cbc:ID>1</cbc:ID>
      <cbc:InvoicedQuantity unitCode="C62" unitCodeListID="UNECERec20">500.0</cbc:InvoicedQuantity>
      <cbc:LineExtensionAmount currencyID="AUD">100.00</cbc:LineExtensionAmount>
      <cac:Item>
         <cbc:Name>pencils</cbc:Name>
         <cac:ClassifiedTaxCategory>
            <cbc:ID schemeAgencyID="6" schemeID="UNCL5305">S</cbc:ID>
            <cbc:Percent>10.0</cbc:Percent>
            <cac:TaxScheme>
               <cbc:ID schemeAgencyID="6" schemeID="UN/ECE 5153">GST</cbc:ID>
            </cac:TaxScheme>
         </cac:ClassifiedTaxCategory>
      </cac:Item>
      <cac:Price>
         <cbc:PriceAmount currencyID="AUD">0.20</cbc:PriceAmount>
         <cbc:BaseQuantity unitCode="C62" unitCodeListID="UNECERec20">1.0</cbc:BaseQuantity>
      </cac:Price>
   </cac:InvoiceLine>
</Incorrect>'''

string_xml_2 = '''<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
    xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
    xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
    <cbc:CustomizationID>urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0</cbc:CustomizationID>
    <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
    <cbc:ID>Invoice01</cbc:ID>
    <cbc:IssueDate>2019-07-29</cbc:IssueDate>
    <cbc:DueDate>2019-08-30</cbc:DueDate>
    <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
    <cbc:Note>Tax invoice</cbc:Note>
    <cbc:DocumentCurrencyCode>AUD</cbc:DocumentCurrencyCode>
    <cbc:AccountingCost>4025:123:4343</cbc:AccountingCost>
    <cbc:BuyerReference>0150abc</cbc:BuyerReference>
    <cac:InvoicePeriod>
       <cbc:StartDate>2019-06-01</cbc:StartDate>
       <cbc:EndDate>2019-07-30</cbc:EndDate>
    </cac:InvoicePeriod>
    <cac:OrderReference>
       <cbc:ID>PurchaseOrderReference</cbc:ID>
		<cbc:SalesOrderID>12345678</cbc:SalesOrderID>
    </cac:OrderReference>
    <cac:BillingReference>
       <cac:InvoiceDocumentReference>
           <cbc:ID>PrecedingInvoiceReference</cbc:ID>
           <cbc:IssueDate>2019-05-30</cbc:IssueDate>
       </cac:InvoiceDocumentReference>
    </cac:BillingReference>
    <cac:DespatchDocumentReference>
       <cbc:ID>DDR-REF</cbc:ID>
    </cac:DespatchDocumentReference>
    <cac:ReceiptDocumentReference>
       <cbc:ID>RD-REF</cbc:ID>
    </cac:ReceiptDocumentReference>
    <cac:OriginatorDocumentReference>
       <cbc:ID>OD-REF</cbc:ID>
    </cac:OriginatorDocumentReference>
    <cac:ContractDocumentReference>
       <cbc:ID>CD-REF</cbc:ID>
    </cac:ContractDocumentReference>
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cbc:EndpointID schemeID="0151">47555222000</cbc:EndpointID>
            <cac:PartyIdentification>
                <cbc:ID>47555222000</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name>Supplier Trading Name Ltd</cbc:Name>
            </cac:PartyName>
            <cac:PostalAddress>
                <cbc:StreetName>Main street 1</cbc:StreetName>
                <cbc:AdditionalStreetName>Postbox 123</cbc:AdditionalStreetName>
                <cbc:CityName>Harrison</cbc:CityName>
                <cbc:PostalZone>2912</cbc:PostalZone>
                <cac:Country>
                    <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyTaxScheme>
                <cbc:CompanyID>47555222000</cbc:CompanyID>
                <cac:TaxScheme>
                    <cbc:ID>GST</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>Supplier Official Name Ltd</cbc:RegistrationName>
                <cbc:CompanyID  schemeID="0151">47555222000</cbc:CompanyID>
                <cbc:CompanyLegalForm>Partnership</cbc:CompanyLegalForm>
            </cac:PartyLegalEntity>

            <cac:Contact>
                <cbc:Name>Ronald MacDonald</cbc:Name>
                <cbc:Telephone>Mobile 0430123456</cbc:Telephone>
                <cbc:ElectronicMail>ronald.macdonald@qualitygoods.com.au</cbc:ElectronicMail>
            </cac:Contact>
        </cac:Party>
    </cac:AccountingSupplierParty>

    <cac:AccountingCustomerParty>
        <cac:Party>
            <cbc:EndpointID schemeID="0151">91888222000</cbc:EndpointID>
            <cac:PartyIdentification>
                <cbc:ID schemeID="0151">91888222000</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name>Trotters Trading Co Ltd</cbc:Name>
            </cac:PartyName>
            <cac:PostalAddress>
                <cbc:StreetName>100 Queen Street</cbc:StreetName>
                <cbc:AdditionalStreetName>Po box 878</cbc:AdditionalStreetName>
                <cbc:CityName>Sydney</cbc:CityName>
                <cbc:PostalZone>2000</cbc:PostalZone>
                <cac:Country>
                    <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyTaxScheme>
                <cbc:CompanyID>91888222000</cbc:CompanyID>
                <cac:TaxScheme>
                    <cbc:ID>GST</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>Buyer Official Name</cbc:RegistrationName>
                <cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID>
            </cac:PartyLegalEntity>
            <cac:Contact>
                <cbc:Name>Lisa Johnson</cbc:Name>
                <cbc:Telephone>0261234567</cbc:Telephone>
                <cbc:ElectronicMail>lj@buyer.com.au</cbc:ElectronicMail>
            </cac:Contact>
        </cac:Party>
    </cac:AccountingCustomerParty>

    <cac:PayeeParty>
       <cac:PartyIdentification>
           <cbc:ID>91888222000</cbc:ID>
       </cac:PartyIdentification>
       <cac:PartyName>
           <cbc:Name>Mr Anderson</cbc:Name>
       </cac:PartyName>

       <cac:PartyLegalEntity>
           <cbc:CompanyID schemeID="0151">91888222000</cbc:CompanyID>
       </cac:PartyLegalEntity>    
    </cac:PayeeParty>

    <cac:TaxRepresentativeParty>
       <cac:PartyName>
           <cbc:Name>Mr Wilson</cbc:Name>
       </cac:PartyName>
       <cac:PostalAddress>
           <cbc:StreetName>16 Stout Street</cbc:StreetName>
           <cbc:AdditionalStreetName>Po box 878</cbc:AdditionalStreetName>
           <cbc:CityName>Sydney</cbc:CityName>
           <cbc:PostalZone>2000</cbc:PostalZone>
           <cbc:CountrySubentity>NSW</cbc:CountrySubentity>
           <cac:AddressLine>
               <cbc:Line>Unit 1</cbc:Line>
           </cac:AddressLine>
           <cac:Country>
                    <cbc:IdentificationCode>AU</cbc:IdentificationCode>
           </cac:Country>
      </cac:PostalAddress>
           <cac:PartyTaxScheme>
                <cbc:CompanyID>91888222000</cbc:CompanyID>
                <cac:TaxScheme>
                    <cbc:ID>GST</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme> 
    </cac:TaxRepresentativeParty>


    <cac:Delivery>
        <cbc:ActualDeliveryDate>2019-07-01</cbc:ActualDeliveryDate>
        <cac:DeliveryLocation>
            <cbc:ID schemeID="0151">91888222000</cbc:ID>
            <cac:Address>
                <cbc:StreetName>Delivery street 2</cbc:StreetName>
                <cbc:AdditionalStreetName>Building 56</cbc:AdditionalStreetName>
                <cbc:CityName>Sydney</cbc:CityName>
                <cbc:PostalZone>2000</cbc:PostalZone>
                <cbc:CountrySubentity>NSW</cbc:CountrySubentity>
                <cac:AddressLine>
                    <cbc:Line>Unit 1</cbc:Line>
                </cac:AddressLine>
                <cac:Country>
                    <cbc:IdentificationCode>AU</cbc:IdentificationCode>
                </cac:Country>
            </cac:Address>
        </cac:DeliveryLocation>
        <cac:DeliveryParty>
            <cac:PartyName>
                <cbc:Name>Delivery party Name</cbc:Name>
            </cac:PartyName>
        </cac:DeliveryParty>
    </cac:Delivery>
    <cac:PaymentMeans>
        <cbc:PaymentMeansCode name="Credit transfer">30</cbc:PaymentMeansCode>
        <cbc:PaymentID>PaymentReferenceText</cbc:PaymentID>
        <cac:PayeeFinancialAccount>
            <cbc:ID>AccountNumber</cbc:ID>
            <cbc:Name>AccountName</cbc:Name>
            <cac:FinancialInstitutionBranch>
                <cbc:ID>BSB Number</cbc:ID>
            </cac:FinancialInstitutionBranch>
        </cac:PayeeFinancialAccount>  
    </cac:PaymentMeans>
    <cac:PaymentTerms>
        <cbc:Note>Payment within 30 days</cbc:Note>
    </cac:PaymentTerms>
    <cac:AllowanceCharge>
        <cbc:ChargeIndicator>true</cbc:ChargeIndicator>
        <cbc:AllowanceChargeReasonCode>SAA</cbc:AllowanceChargeReasonCode>
        <cbc:AllowanceChargeReason>Shipping and Handling</cbc:AllowanceChargeReason>
        <cbc:MultiplierFactorNumeric>0</cbc:MultiplierFactorNumeric>
        <cbc:Amount currencyID="AUD">0</cbc:Amount>
        <cbc:BaseAmount currencyID="AUD">0</cbc:BaseAmount>
        <cac:TaxCategory>
            <cbc:ID>S</cbc:ID>
            <cbc:Percent>10</cbc:Percent>
            <cac:TaxScheme>
                <cbc:ID>GST</cbc:ID>
            </cac:TaxScheme>
        </cac:TaxCategory>
    </cac:AllowanceCharge>


    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="AUD">148.74</cbc:TaxAmount>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="AUD">1487.40</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="AUD">148.74</cbc:TaxAmount>
            <cac:TaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>10</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>GST</cbc:ID>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
    </cac:TaxTotal>



    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID="AUD">1487.40</cbc:LineExtensionAmount>
        <cbc:TaxExclusiveAmount currencyID="AUD">1487.40</cbc:TaxExclusiveAmount>
        <cbc:TaxInclusiveAmount currencyID="AUD">1636.14</cbc:TaxInclusiveAmount>
        <cbc:ChargeTotalAmount currencyID="AUD">0.00</cbc:ChargeTotalAmount>
        <cbc:PrepaidAmount currencyID="AUD">0.00</cbc:PrepaidAmount>
        <cbc:PayableAmount currencyID="AUD">1636.14</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>
 

    <cac:InvoiceLine>
       <cbc:ID>1</cbc:ID>
       <cbc:Note>Texts Giving More Info about the Invoice Line</cbc:Note>
       <cbc:InvoicedQuantity unitCode="E99">10</cbc:InvoicedQuantity>
       <cbc:LineExtensionAmount currencyID= "AUD">299.90</cbc:LineExtensionAmount>
           <cbc:AccountingCost>Consulting Fees</cbc:AccountingCost>
           <cac:InvoicePeriod>
           <cbc:StartDate>2019-06-01</cbc:StartDate> 
           <cbc:EndDate>2019-07-30</cbc:EndDate> 
       </cac:InvoicePeriod>
       <cac:OrderLineReference>
            <cbc:LineID>123</cbc:LineID>
       </cac:OrderLineReference>
       <cac:DocumentReference>
            <cbc:ID schemeID="HWB">9000074677</cbc:ID>
            <cbc:DocumentTypeCode>130</cbc:DocumentTypeCode> 
       </cac:DocumentReference>

    <cac:Item>
        <cbc:Description>Widgets True and Fair</cbc:Description>
           <cbc:Name>True-Widgets</cbc:Name>
           <cac:BuyersItemIdentification>
              <cbc:ID>W659590</cbc:ID>
           </cac:BuyersItemIdentification>
           <cac:SellersItemIdentification>
              <cbc:ID>WG546767</cbc:ID>
           </cac:SellersItemIdentification>
           <cac:StandardItemIdentification>
              <cbc:ID  schemeID="0002">WG546767</cbc:ID>
           </cac:StandardItemIdentification>
            <cac:OriginCountry>
                <cbc:IdentificationCode>AU</cbc:IdentificationCode>
            </cac:OriginCountry>
            <cac:CommodityClassification>
                <cbc:ItemClassificationCode listID="SRV">09348023</cbc:ItemClassificationCode>
            </cac:CommodityClassification>
            <cac:ClassifiedTaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>10</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>GST</cbc:ID>
                </cac:TaxScheme>
            </cac:ClassifiedTaxCategory>
        </cac:Item>

       <cac:Price>
           <cbc:PriceAmount currencyID="AUD">29.99</cbc:PriceAmount>
           <cac:AllowanceCharge>
              <cbc:ChargeIndicator>false</cbc:ChargeIndicator>
              <cbc:Amount currencyID="AUD">0.00</cbc:Amount>
              <cbc:BaseAmount currencyID="AUD">29.99</cbc:BaseAmount>
           </cac:AllowanceCharge>
       </cac:Price>

    </cac:InvoiceLine>


   <cac:InvoiceLine>
      <cbc:ID>2</cbc:ID>
      <cbc:InvoicedQuantity unitCode="DAY">2</cbc:InvoicedQuantity>
      <cbc:LineExtensionAmount currencyID="AUD">1000</cbc:LineExtensionAmount>
      <cac:OrderLineReference>
          <cbc:LineID>123</cbc:LineID>
      </cac:OrderLineReference>
      <cac:Item>
          <cbc:Description>Description 2</cbc:Description>
          <cbc:Name>item name 2</cbc:Name>
          <cac:StandardItemIdentification>
              <cbc:ID schemeID="0151">21382183120983</cbc:ID>
          </cac:StandardItemIdentification>
          <cac:OriginCountry>
              <cbc:IdentificationCode>NO</cbc:IdentificationCode>
          </cac:OriginCountry>
          <cac:CommodityClassification>
              <cbc:ItemClassificationCode listID="SRV">09348023</cbc:ItemClassificationCode>
          </cac:CommodityClassification>
          <cac:ClassifiedTaxCategory>
              <cbc:ID>S</cbc:ID>
              <cbc:Percent>10</cbc:Percent>
              <cac:TaxScheme>
                  <cbc:ID>GST</cbc:ID>
              </cac:TaxScheme>
          </cac:ClassifiedTaxCategory>
      </cac:Item>
      <cac:Price>
          <cbc:PriceAmount currencyID="AUD">500</cbc:PriceAmount>
      </cac:Price>
   </cac:InvoiceLine>




<cac:InvoiceLine>
       <cbc:ID>3</cbc:ID>
       <cbc:Note>Invoice Line Description</cbc:Note>
       <cbc:InvoicedQuantity unitCode="M66">25</cbc:InvoicedQuantity>
       <cbc:LineExtensionAmount currencyID= "AUD">187.50</cbc:LineExtensionAmount>
           <cbc:AccountingCost>Consulting Fees</cbc:AccountingCost>
           <cac:InvoicePeriod>
           <cbc:StartDate>2019-06-01</cbc:StartDate> 
           <cbc:EndDate>2019-07-30</cbc:EndDate> 
       </cac:InvoicePeriod>
       <cac:OrderLineReference>
            <cbc:LineID>123</cbc:LineID>
       </cac:OrderLineReference>
       <cac:DocumentReference>
            <cbc:ID schemeID="HWB">9000074677</cbc:ID>
            <cbc:DocumentTypeCode>130</cbc:DocumentTypeCode> 
       </cac:DocumentReference>

    <cac:Item>
        <cbc:Description>Widgets True and Fair</cbc:Description>
           <cbc:Name>True-Widgets</cbc:Name>
           <cac:BuyersItemIdentification>
              <cbc:ID>W659590</cbc:ID>
           </cac:BuyersItemIdentification>
           <cac:SellersItemIdentification>
              <cbc:ID>WG546767</cbc:ID>
           </cac:SellersItemIdentification>
           <cac:StandardItemIdentification>
              <cbc:ID  schemeID="0151">WG546767</cbc:ID>
           </cac:StandardItemIdentification>
            <cac:OriginCountry>
                <cbc:IdentificationCode>AU</cbc:IdentificationCode>
            </cac:OriginCountry>
            <cac:CommodityClassification>
                <cbc:ItemClassificationCode listID="SRV">09348023</cbc:ItemClassificationCode>
            </cac:CommodityClassification>
            <cac:ClassifiedTaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>10</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>GST</cbc:ID>
                </cac:TaxScheme>
            </cac:ClassifiedTaxCategory>
        </cac:Item>

       <cac:Price>
           <cbc:PriceAmount currencyID="AUD">7.50</cbc:PriceAmount>
           <cac:AllowanceCharge>
              <cbc:ChargeIndicator>false</cbc:ChargeIndicator>
              <cbc:Amount currencyID="AUD">0.00</cbc:Amount>
              <cbc:BaseAmount currencyID="AUD">7.50</cbc:BaseAmount>
           </cac:AllowanceCharge>
       </cac:Price>

    </cac:InvoiceLine>


</Invoice>'''

# print(verify_schema(string_xml_1))

