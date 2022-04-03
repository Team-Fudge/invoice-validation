import 'package:flutter/material.dart';
import 'http_service.dart';
import 'package:flutter_easyloading/flutter_easyloading.dart';

class WellformednessPage extends StatefulWidget {
  const WellformednessPage({Key? key}) : super(key: key);

  @override
  _WellformednessPageState createState() => _WellformednessPageState();
}

class _WellformednessPageState extends State<WellformednessPage> {
  late String xml = "";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(title: const Text('Wellformedness Validator')),
        body: Container(
          margin: const EdgeInsets.symmetric(horizontal: 30, vertical: 20),
          child: ListView(
            children: [
              TextField(
                obscureText: false,
                decoration: InputDecoration(hintText: 'xml'),
                maxLines: null,
                keyboardType: TextInputType.multiline,
                onChanged: (value) {
                  setState(() {
                    xml = value;
                  });
                },
              ),
              InkWell(
                  onTap: () async {
                    print(xml);
                    await HttpService.wellformedness(xml, context);
                  },
                  child: Container(
                    margin: const EdgeInsets.symmetric(
                        horizontal: 20, vertical: 10),
                    child: const Center(
                      child: Text(
                        "Wellformedness",
                        style: TextStyle(
                            fontWeight: FontWeight.bold, color: Colors.white),
                      ),
                    ),
                    height: 50,
                    width: double.infinity,
                    decoration: BoxDecoration(
                        color: Color.fromARGB(255, 0, 80, 121),
                        ),
                  ))
            ],
          ),
        )
      // ignore: avoid_unnecessary_containers
    );
  }
}