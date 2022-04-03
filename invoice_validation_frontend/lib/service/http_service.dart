import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_easyloading/flutter_easyloading.dart';
import 'dashboard.dart';
import 'syntax_demo_report.dart';
import 'dart:convert';

// import 'package:loginwithapi/views/welcome.dart';

class HttpService {
  static final _client = http.Client();

  static var _wellformednessUrl = Uri.parse('https://invoice-validation-fudge.herokuapp.com/invoice/verify/wellformedness');

  static var _syntaxUrl = Uri.parse('https://invoice-validation-fudge.herokuapp.com/invoice/verify/wellformedness/syntax');

  static var _peppolUrl = Uri.parse('https://invoice-validation-fudge.herokuapp.com/invoice/verify/wellformedness/peppol');

  static var _schemaUrl = Uri.parse('https://invoice-validation-fudge.herokuapp.com/invoice/verify/wellformedness/schema');


  static wellformedness(xml, context) async {

    http.post(_wellformednessUrl, body: xml, headers: {
    "Content-Type": "application/xml",
    "Access_Control_Allow_Origin": "*",
  }).then((http.Response response) {
    
    print(response);
    final Map<String, dynamic> responseData = json.decode(response.body);
    if (response.statusCode != 200) {
      print(responseData);
      showDialog<String>(
        context: context,
        builder: (BuildContext context) => AlertDialog(
          title: Text(response.statusCode.toString()),
          content: Text(responseData['name']+"\n"+responseData['message']),
          actions: <Widget>[
            TextButton(
              onPressed: () => Navigator.pop(context, 'Cancel'),
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () => Navigator.pop(context, 'OK'),
              child: const Text('OK'),
            ),
          ],
        ),
      );
    }
    else {
      Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => Dashboard(responseData: response)));
        }

      // print(responseData);
      // print("\n");
      // responseData["broken_rules"].forEach(print);
      // print("\n");
      // print('Response body: ${response.body}');
    }
  );
  }

 static syntax(xml, context) async {

    http.post(_wellformednessUrl, body: xml, headers: {
    "Content-Type": "application/xml",
    "Access_Control_Allow_Origin": "*",
  }).then((http.Response response) {
    
    print(response);
    final Map<String, dynamic> responseData = json.decode(response.body);
    Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => syntaxDemoReport(responseData: response)));
    // if (response.statusCode != 200) {
    //   print(responseData);
    //   showDialog<String>(
    //     context: context,
    //     builder: (BuildContext context) => AlertDialog(
    //       title: Text(response.statusCode.toString()),
    //       content: Text(responseData['name']+"\n"+responseData['message']),
    //       actions: <Widget>[
    //         TextButton(
    //           onPressed: () => Navigator.pop(context, 'Cancel'),
    //           child: const Text('Cancel'),
    //         ),
    //         TextButton(
    //           onPressed: () => Navigator.pop(context, 'OK'),
    //           child: const Text('OK'),
    //         ),
    //       ],
    //     ),
    //   );
    // }
    // else {
    //   Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => Dashboard(responseData: response)));
    //     }

      // print(responseData);
      // print("\n");
      // responseData["broken_rules"].forEach(print);
      // print("\n");
      // print('Response body: ${response.body}');
    }
  );
  }

  static schema(xml, context) async {
    http.Response response = await _client.post(_schemaUrl, body: {
      xml
    });

    if (response.statusCode == 200) {
      var json = jsonDecode(response.body);

      await EasyLoading.showSuccess("Report generated");
      Navigator.pushReplacement(
          context, MaterialPageRoute(builder: (context) => Dashboard(responseData: json)));
  
    } else {
      await EasyLoading.showError(
          "Error Code : ${response.statusCode.toString()}");
    }
  }


}


class _FullScreenDialogDemo extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    // Remove the MediaQuery padding because the demo is rendered inside of a
    // different page that already accounts for this padding.
    return MediaQuery.removePadding(
      context: context,
      removeTop: true,
      removeBottom: true,
      child: Scaffold(
          appBar: AppBar(
            title: Text("up"),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                child: Text(
                  "body",

                  ),
                ),
              
            ],
          ),
          body: Center(
            child: Text(
              "low",
            ),
          ),
        ),
      );
    
  }
}
