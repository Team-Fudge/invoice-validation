from bs4 import BeautifulSoup
import re
import os

def open_file_as_string(file_name):

    #open & read file
    with open(file_name, 'r') as f:
       data = f.read()

    return data



#file_name should be of type string
#xml_tag should be of type string
def retrieve_tag_value (string_xml, xml_tag):


    data = string_xml

    #extract data from file
    data = BeautifulSoup(data, "xml")

    #
    value = data.find_all(xml_tag)
    if value == []:
        return [None, None]
    for i in range(len(value)):
        value[i] = value[i].get_text()
        if value[i] == "":
            value[i] = None
    return value
 
def check_section_exists(string_xml, tag, index):
    value = retrieve_tag_value(string_xml, tag)[index]
    if value == None:
        return None
    value = value.replace("\n","")
    value = value.replace(" ","")
    return value

def verify_syntax_errors(string_xml):
    disclaimer = "The current version of this microservice can only test syntax errors BR-01 to BR-16"
    
    if len(string_xml) == 0:
        return {"broken_rules": "The provided file is empty", "broken_rules_detailed": "The provided file is empty", "disclaimer": disclaimer}
    
    unchecked = 1
    
    rule_book = {
        "[BR-01]-An Invoice shall have a Specification identifier (BT-24).": retrieve_tag_value (string_xml, "cbc:CustomizationID")[0],
        "[BR-02]-An Invoice shall have an Invoice number (BT-1).": retrieve_tag_value (string_xml, "cbc:ID")[0],
        "[BR-03]-An Invoice shall have an Invoice issue date (BT-2).": retrieve_tag_value (string_xml, "cbc:IssueDate"),
        "[BR-04]-An Invoice shall have an Invoice type code (BT-3).": retrieve_tag_value (string_xml, "cbc:InvoiceTypeCode"),
        "[BR-05]-An Invoice shall have an Invoice currency code (BT-5).": retrieve_tag_value (string_xml, "cbc:DocumentCurrencyCode") ,
        "[BR-06]-An Invoice shall contain the Seller name (BT-27).": retrieve_tag_value(string_xml,"cbc:RegistrationName")[0],
        "[BR-07]-An Invoice shall contain the Buyer name (BT-44).":  retrieve_tag_value(string_xml,"cbc:RegistrationName")[1],
        "[BR-08]-An Invoice shall contain the Seller postal address.": check_section_exists(string_xml, "cac:PostalAddress", 0),
        "[BR-09]-The Seller postal address (BG-5) shall contain a Seller country code (BT-40).": retrieve_tag_value(string_xml,"cbc:IdentificationCode")[0],
        "[BR-10]-An Invoice shall contain the Buyer postal address (BG-8).": check_section_exists(string_xml,"cac:PostalAddress", 1), 
        "[BR-11]-The Buyer postal address shall contain a Buyer country code (BT-55).": retrieve_tag_value(string_xml,"cbc:IdentificationCode")[1],
        "[BR-12]-An Invoice shall have the Sum of Invoice line net amount (BT-106).": retrieve_tag_value(string_xml,"cbc:LineExtensionAmount")[0],
        "[BR-13-AUNZ]-An Invoice shall have the Invoice total amount without Tax (BT-109).": retrieve_tag_value(string_xml,"cbc:TaxExclusiveAmount")[0],
        "[BR-14-AUNZ]-An Invoice shall have the Invoice total amount with Tax (BT-112).": retrieve_tag_value(string_xml,"cbc:TaxInclusiveAmount")[0],
        "[BR-15]-An Invoice shall have the Amount due for payment (BT-115).": retrieve_tag_value(string_xml,"cbc:PayableAmount")[0],
        "[BR-16]-An Invoice shall have at least one Invoice line (BG-25)": check_section_exists(string_xml,"cac:InvoiceLine",0),
        "[BR-17]-The Payee name (BT-59) shall be provided in the Invoice: None, if the Payee (BG-10) is different from the Seller (BG-4)": unchecked,
        "[BR-18]-The Seller tax representative name (BT-62) shall be provided in the Invoice: None, if the Seller (BG-4) has a Seller tax representative party (BG-11)": unchecked,
        "[BR-19]-The Seller tax representative postal address (BG-12) shall be provided in the Invoice: None, if the Seller (BG-4) has a Seller tax representative party (BG-11).": unchecked,
        "[BR-20]-The Seller tax representative postal address (BG-12) shall contain a Tax representative country code (BT-69): None, if the Seller (BG-4) has a Seller tax representative party (BG-11).": unchecked,
        "[BR-21]-Each Invoice line (BG-25) shall have an Invoice line identifier (BT-126).": unchecked,
        "[BR-22]-Each Invoice line (BG-25) shall have an Invoiced quantity (BT-129).": unchecked,
        "[BR-23]-An Invoice line (BG-25) shall have an Invoiced quantity unit of measure code (BT-130).": unchecked,
        "[BR-24]-Each Invoice line (BG-25) shall have an Invoice line net amount (BT-131).": unchecked,
        "[BR-25]-Each Invoice line (BG-25) shall contain the Item name (BT-153).": unchecked,
        "[BR-26]-Each Invoice line (BG-25) shall contain the Item net price (BT-146).": unchecked,
        "[BR-27]-The Item net price (BT-146) shall NOT be negative.": unchecked,
        "[BR-28]-The Item gross price (BT-148) shall NOT be negative.": unchecked,
        "[BR-29]-If both Invoicing period start date (BT-73) and Invoicing period end date (BT-74) are given then the Invoicing period end date (BT-74) shall be later or equal to the Invoicing period start date (BT-73).": unchecked,
        "[BR-30]-If both Invoice line period start date (BT-134) and Invoice line period end date (BT-135) are given then the Invoice line period end date (BT-135) shall be later or equal to the Invoice line period start date (BT-134).": unchecked,
        "[BR-31]-Each Document level allowance (BG-20) shall have a Document level allowance amount (BT-92).": unchecked,
        "[BR-32-AUNZ]-Each Document level allowance (BG-20) shall have a Document level allowance Tax category code (BT-95).": unchecked,
        "[BR-33]-Each Document level allowance (BG-20) shall have a Document level allowance reason (BT-97) or a Document level allowance reason code (BT-98).": unchecked,
        "[BR-36]-Each Document level charge (BG-21) shall have a Document level charge amount (BT-99).": unchecked,
        "[BR-37-AUNZ]-Each Document level charge (BG-21) shall have a Document level charge Tax category code (BT-102).": unchecked,
        "[BR-38]-Each Document level charge (BG-21) shall have a Document level charge reason (BT-104) or a Document level charge reason code (BT-105).": unchecked,  
        "[BR-41]-Each Invoice line allowance (BG-27) shall have an Invoice line allowance amount (BT-136).": unchecked,
        "[BR-42]-Each Invoice line allowance (BG-27) shall have an Invoice line allowance reason (BT-139) or an Invoice line allowance reason code (BT-140).": unchecked,
        "[BR-43]-Each Invoice line charge (BG-28) shall have an Invoice line charge amount (BT-141).": unchecked,
        "[BR-44]-Each Invoice line charge shall have an Invoice line charge reason or an invoice line allowance reason code.": unchecked,
        "[BR-45-AUNZ]-Each Tax subtotal (BG-23) shall have a Tax category taxable amount (BT-116).": unchecked,
        "[BR-46-AUNZ]-Each Tax subtotal (BG-23) shall have a Tax category tax amount (BT-117).": unchecked,
        "[BR-47-AUNZ]-Each Tax subtotal (BG-23) shall be defined through a Tax category code (BT-118).": unchecked,
        "[BR-48-AUNZ]-Each Tax subtotal (BG-23) shall have a Tax category rate (BT-119): None, except if the Invoice is not subject to Tax.": unchecked,
        "[BR-49]-A Payment instruction (BG-16) shall specify the Payment means type code (BT-81).": unchecked,
        "[BR-50]-A Payment account identifier (BT-84) shall be present if Credit transfer (BG-17) information is provided in the Invoice.": unchecked,
        "[BR-51]-The last 4 to 6 digits of the Payment card primary account number (BT-87) shall be present if Payment card information (BG-18) is provided in the Invoice.": unchecked,
        "[BR-52]-Each Additional supporting document (BG-24) shall contain a Supporting document reference (BT-122).": unchecked,  
        "[BR-53-AUNZ]-If the Tax accounting currency code (BT-6) is present: None, then the Invoice total Tax amount in accounting currency (BT-111) shall be provided.": unchecked,
        "[BR-54]-Each Item attribute (BG-32) shall contain an Item attribute name (BT-160) and an Item attribute value (BT-161).": unchecked,
        "[BR-55]-Each Preceding Invoice reference (BG-3) shall contain a Preceding Invoice reference (BT-25).": unchecked,
        "[BR-56-AUNZ]-Each Seller tax representative party (BG-11) shall have a Seller tax representative tax identifier (BT-63).": unchecked,
        "[BR-57]-Each Deliver to address (BG-15) shall contain a Deliver to country code (BT-80).": unchecked,
        "[BR-61]-If the Payment means type code (BT-81) means SEPA credit transfer: None, Local credit transfer or Non-SEPA international credit transfer: None, the Payment account identifier (BT-84) shall be present.": unchecked,
        "[BR-62]-The Seller electronic address (BT-34) shall have a Scheme identifier.": unchecked,
        "[BR-63]-The Buyer electronic address (BT-49) shall have a Scheme identifier.": unchecked,  
        "[BR-64]-The Item standard identifier (BT-157) shall have a Scheme identifier.": unchecked,
        "[BR-65]-The Item classification identifier (BT-158) shall have a Scheme identifier.": unchecked,
        "[BR-66]-An Invoice shall contain maximum one Payment Card account (BG-18)": unchecked,
        "[BR-67]-An Invoice shall contain maximum one Payment Mandate (BG-19)": unchecked,
    }
    broken_rules = []
    broken_rules_detailed = []
    
    #Add disclaimer to be passed into report
    disclaimer = "The current version of this microservice can only test syntax errors BR-01 to BR-16"

    for tag in rule_book:
        if rule_book.get(tag) == None:
            broken_rules.append(tag[1:6])
            broken_rules_detailed.append(tag)
    
    return {"broken_rules": broken_rules, "broken_rules_detailed": broken_rules_detailed, "disclaimer": disclaimer}


def open_and_check_error_for_tests(file_name):
    string_xml = open_file_as_string(file_name)
    return verify_syntax_errors(string_xml)



if __name__ == "__main__":
    
    string_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:cec="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2">
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
</Invoice>'''

    print(verify_syntax_errors(string_xml))

