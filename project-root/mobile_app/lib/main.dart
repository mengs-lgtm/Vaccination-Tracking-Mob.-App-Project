import 'package:flutter/material.dart';
import 'package:mobile_app/screens/dashboard.dart';
import 'package:mobile_app/services/notification_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await NotificationService.init(); // initialize notifications and timezones
  runApp(VaccinationApp());
}

class VaccinationApp extends StatelessWidget {
  const VaccinationApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Vaccination Tracker',
      theme: ThemeData(
        fontFamily: 'NotoSans', // ✅ custom font applied here
        primarySwatch: Colors.blue,
      ),
      home: Dashboard(), // ✅ your main screen
      debugShowCheckedModeBanner: false,
    );
  }
}
