import 'package:flutter/material.dart';
import 'wellformedness.dart';
import 'syntax.dart';

class WelcomePage extends StatefulWidget {
  const WelcomePage({Key? key}) : super(key: key);

  @override
  _WelcomePageState createState() => _WelcomePageState();
}

class _WelcomePageState extends State<WelcomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Container(
        margin: const EdgeInsets.symmetric(horizontal: 30),
        decoration: BoxDecoration(borderRadius: BorderRadius.circular(20)),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            
             Container(
                  margin:
                  const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  child: const Center(
                    child: Text(
                      "Validation Options",
                      style: TextStyle(
                          fontWeight: FontWeight.w100 , color: Color.fromARGB(255, 99, 99, 99), fontSize: 50),
                    ),
                  ),
                ),

            SizedBox(height: 10),
            InkWell(
                onTap: () {
                  Navigator.push(context,
                      MaterialPageRoute(builder: (context) => WellformednessPage()));
                },
                child: Container(
                  margin:
                  const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  child: const Center(
                    child: Text(
                      "Wellformedness [error demonstration]",
                      style: TextStyle(
                          fontWeight: FontWeight.bold, color: Colors.white),
                    ),
                  ),
                  height: 50,
                  width: double.infinity,
                  decoration: BoxDecoration(
                      color: Color.fromARGB(255, 0, 80, 121),
                      ),
                )),
            InkWell(
                onTap: () {
                  Navigator.push(context,
                      MaterialPageRoute(builder: (context) => RegisterPage()));
                },
                child: Container(
                  margin:
                  const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  child: const Center(
                    child: Text(
                      "Syntax [demonstration route]",
                      style: TextStyle(
                          fontWeight: FontWeight.bold, color: Colors.white),
                    ),
                  ),
                  height: 50,
                  width: double.infinity,
                  decoration: BoxDecoration(
                      color: Color.fromARGB(255, 0, 80, 121),
                      ),
                )),
              InkWell(
                onTap: () {
                  Navigator.push(context,
                      MaterialPageRoute(builder: (context) => WellformednessPage()));
                },
                child: Container(
                  margin:
                  const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  child: const Center(
                    child: Text(
                      "Peppol [work in progress]",
                      style: TextStyle(
                          fontWeight: FontWeight.bold, color: Colors.white),
                    ),
                  ),
                  height: 50,
                  width: double.infinity,
                  decoration: BoxDecoration(
                      color: Color.fromARGB(255, 0, 80, 121),
                      ),
                )),
              InkWell(
                onTap: () {
                  Navigator.push(context,
                      MaterialPageRoute(builder: (context) => WellformednessPage()));
                },
                child: Container(
                  margin:
                  const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  child: const Center(
                    child: Text(
                      "Schema [work in progress]",
                      style: TextStyle(
                          fontWeight: FontWeight.bold, color: Colors.white),
                    ),
                  ),
                  height: 50,
                  width: double.infinity,
                  decoration: BoxDecoration(
                      color: Color.fromARGB(255, 0, 80, 121),
                      ),
                )),
              InkWell(
                onTap: () {
                  Navigator.push(context,
                      MaterialPageRoute(builder: (context) => WellformednessPage()));
                },
                child: Container(
                  margin:
                  const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                  child: const Center(
                    child: Text(
                      "Run All Tests [work in progress]",
                      style: TextStyle(
                          fontWeight: FontWeight.bold, color: Colors.white),
                    ),
                  ),
                  height: 50,
                  width: double.infinity,
                  decoration: BoxDecoration(
                      color: Color.fromARGB(255, 0, 80, 121),
                      ),
                )),
          ],
        ),
      ),
    );
  }
}