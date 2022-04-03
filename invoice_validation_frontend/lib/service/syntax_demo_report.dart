// ignore_for_file: prefer_const_constructors

import 'dart:convert';

import 'package:flutter/material.dart';

class syntaxDemoReport extends StatefulWidget {
  var responseData;
  var string;
  syntaxDemoReport({Key? key, this.responseData }) : super(key: key);

  @override
  _syntaxDemoReportState createState() => _syntaxDemoReportState();
}

class _syntaxDemoReportState extends State<syntaxDemoReport> {

  @override
  Widget build(BuildContext context) {
    final Map<String, dynamic> responsesorted = json.decode(widget.responseData.body);
    var date = DateTime.now().toString();

    return Scaffold(

      appBar: AppBar(
        title: Text("Report"),
      ),
      body: Center(

        child:
        Padding( padding: EdgeInsets.all(40.0) , child: 
          ListView(
            children: [
              Text(
                  "Syntax Report",
                  style: TextStyle(
                      fontWeight: FontWeight.bold , color: Colors.black, fontSize: 40),
                ),
              SizedBox(height: 5,),
              Text(
                  "This report was generated on: " + date,
                  style: TextStyle(
                      fontWeight: FontWeight.w100 , color: Colors.black, fontSize: 15),
                ),
              Text(
                  "Tests:",
                  style: TextStyle(
                      fontWeight: FontWeight.bold , color: Colors.black, fontSize: 30),
                ),
              Text(
                  "   Wellformedness: Previously tested \n   Syntax: Currently tested\n   Peppol: Not checked\n   Schema: Not checked",
                  style: TextStyle(
                      fontWeight: FontWeight.w100 , color: Color.fromARGB(255, 99, 99, 99), fontSize: 20),
                ),
              SizedBox(height: 10,),
              Text(
                  "Syntax Test Results:",
                  style: TextStyle(
                      fontWeight: FontWeight.bold , color: Colors.black, fontSize: 30),
                ),
              Text(
                  "Broken Rules:",
                  style: TextStyle(
                      fontWeight: FontWeight.bold , color: Colors.black, fontSize: 20),
                ),
              Text(
                  "   BR-01\n   BR-06",
                  style: TextStyle(
                      fontWeight: FontWeight.w100 , color: Color.fromARGB(255, 99, 99, 99), fontSize: 20),
                ),
              Text(
                  "Explanation of Rules Broken:",
                  style: TextStyle(
                      fontWeight: FontWeight.bold , color: Colors.black, fontSize: 20),
                ),
              Text(
                  "   [BR-01]-An Invoice shall have a Specification identifier (BT-24).\n   [BR-06]-An Invoice shall contain the Seller name (BT-27).",
                  style: TextStyle(
                      fontWeight: FontWeight.w100 , color: Color.fromARGB(255, 99, 99, 99), fontSize: 20),
                ),
              SizedBox(height: 10,),
              Text(
                  "Disclaimer:",
                  style: TextStyle(
                      fontWeight: FontWeight.bold , color: Colors.black, fontSize: 20),
                ),            
              Text(
                  "The current version of this microservice can only test syntax errors BR-01 to BR-16",
                  style: TextStyle(
                      fontWeight: FontWeight.w100 , color: Colors.black, fontSize: 15),
                ),
            ],
          ),   
        ),
      ),
    );
  }
}