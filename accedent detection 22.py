import 'dart:async';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class AccidentDetectionScreen extends StatefulWidget {
  @override
  _AccidentDetectionScreenState createState() => _AccidentDetectionScreenState();
}

class _AccidentDetectionScreenState extends State<AccidentDetectionScreen> {
  final FirebaseFirestore db = FirebaseFirestore.instance;
  final Random random = Random();
  Timer? timer;
  String status = "Monitoring...";

  @override
  void initState() {
    super.initState();
    // Run detection every 5 seconds
    timer = Timer.periodic(Duration(seconds: 5), (_) => detectAccident());
  }

  void detectAccident() async {
    double impactForce = random.nextDouble() * 10; // g-force
    int heartRate = 40 + random.nextInt(80);       // bpm

    if (impactForce > 7 || heartRate < 45) {
      setState(() {
        status = "⚠️ Accident Detected!";
      });

      await db.collection("accidents").add({
        "location": {"lat": 12.95, "lon": 77.60},
        "heartRate": heartRate,
        "impactForce": impactForce,
        "timestamp": DateTime.now().toIso8601String(),
      });
    } else {
      setState(() {
        status = "✅ Normal: Impact=$impactForce g, HR=$heartRate bpm";
      });
    }
  }

  @override
  void dispose() {
    timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Accident Detection")),
      body: Center(child: Text(status, style: TextStyle(fontSize: 18))),
    );
  }
}
