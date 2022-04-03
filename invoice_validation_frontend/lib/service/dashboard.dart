import 'dart:convert';

import 'package:flutter/material.dart';

class Dashboard extends StatefulWidget {
  var responseData;
  var string;
  Dashboard({Key? key, this.responseData }) : super(key: key);

  @override
  _DashboardState createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {

  @override
  Widget build(BuildContext context) {
    final Map<String, dynamic> responsesorted = json.decode(widget.responseData.body);

    return Scaffold(

      appBar: AppBar(
        title: Text("Report"),
      ),
      body: Center(

        child: Text(responsesorted['broken_rules'][1]),
      ),
    );
  }
}