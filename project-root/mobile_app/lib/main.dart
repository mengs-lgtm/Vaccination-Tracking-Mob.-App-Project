import 'package:flutter/material.dart';
import 'screens/dashboard.dart';
import 'screens/add_vaccination.dart';
import 'services/notification_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await NotificationService.init(); // initialize notifications
  runApp(VaccinationApp());
}

class VaccinationApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Vaccination Tracker",
      theme: ThemeData(primarySwatch: Colors.blue),
      initialRoute: "/",
      routes: {
        "/": (context) => Dashboard(),
        "/add": (context) => AddVaccination(),
      },
    );
  }
}
