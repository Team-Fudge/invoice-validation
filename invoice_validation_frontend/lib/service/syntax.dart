import 'package:flutter/material.dart';
import 'http_service.dart';

class RegisterPage extends StatefulWidget {
  const RegisterPage({Key? key}) : super(key: key);

  @override
  _RegisterPageState createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {

  String xml = "";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: const Text('Syntax Validation')),
        body: Container(
          margin: const EdgeInsets.symmetric(horizontal: 30, vertical: 20),
          child: ListView(
            children: [
              TextFormField(
                maxLines: null,
                keyboardType: TextInputType.multiline,
                obscureText: false,
                initialValue: """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:cec="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2">
   <cbc:UBLVersionID>2.1</cbc:UBLVersionID>
   <cbc:CustomizationID></cbc:CustomizationID>
   <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
   <cbc:ID>EBWASP1002</cbc:ID>
   <cbc:IssueDate></cbc:IssueDate>
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
            <cbc:StreetName></cbc:StreetName>
            <cbc:CityName></cbc:CityName>
            <cbc:PostalZone></cbc:PostalZone>
            <cac:Country>
               <cbc:IdentificationCode listAgencyID="6" listID="ISO3166-1:Alpha2">AU</cbc:IdentificationCode>
            </cac:Country>
         </cac:PostalAddress>
         <cac:PartyLegalEntity>
            <cbc:RegistrationName></cbc:RegistrationName>
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
</Invoice>""",
                decoration: InputDecoration(hintText: 'xml'),
                onChanged: (value) {
                  setState(() {
                    xml = value;
                  });
                },
              ),
              
              InkWell(
                  onTap: () async {
                    await HttpService.syntax(xml, context);
                  },
                  child: Container(
                    margin: const EdgeInsets.symmetric(
                        horizontal: 20, vertical: 10),
                    child: const Center(
                      child: Text(
                        "Syntax",
                        style: TextStyle(
                            fontWeight: FontWeight.bold, color: Colors.white),
                      ),
                    ),
                    height: 50,
                    width: double.infinity,
                    decoration: BoxDecoration(
                        color: Color.fromARGB(255, 0, 80, 121),
                        borderRadius: BorderRadius.circular(25)),
                  ))
            ],
          ),
        )
      // ignore: avoid_unnecessary_containers
    );
  }
}