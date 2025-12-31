import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/notification_service.dart';

class AddVaccination extends StatefulWidget {
  @override
  _AddVaccinationState createState() => _AddVaccinationState();
}

class _AddVaccinationState extends State<AddVaccination> {
  final _formKey = GlobalKey<FormState>();
  final ApiService apiService = ApiService();

  String vaccineName = "";
  String dateAdministered = "";
  String? nextDueDate;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Add Vaccination")),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                decoration: InputDecoration(labelText: "Vaccine Name"),
                onSaved: (val) => vaccineName = val!,
              ),
              TextFormField(
                decoration: InputDecoration(
                  labelText: "Date Administered (YYYY-MM-DD)",
                ),
                onSaved: (val) => dateAdministered = val!,
              ),
              TextFormField(
                decoration: InputDecoration(
                  labelText: "Next Due Date (YYYY-MM-DD)",
                ),
                onSaved: (val) => nextDueDate = val,
              ),
              SizedBox(height: 20),
              ElevatedButton(
                child: Text("Save"),
                onPressed: () async {
                  _formKey.currentState!.save();
                  await apiService.addVaccination({
                    "user_id": 1,
                    "vaccine_name": vaccineName,
                    "date_administered": dateAdministered,
                    "next_due_date": nextDueDate,
                  });

                  // Schedule notification if nextDueDate is provided
                  if (nextDueDate != null && nextDueDate!.isNotEmpty) {
                    DateTime dueDate = DateTime.parse(nextDueDate!);
                    await NotificationService.scheduleNotification(
                      id: DateTime.now().millisecondsSinceEpoch ~/ 1000,
                      title: "Upcoming Vaccination",
                      body: "${vaccineName} is due on $nextDueDate",
                      scheduledDate: dueDate.subtract(
                        Duration(days: 1),
                      ), // remind 1 day before
                    );
                  }

                  Navigator.pop(context);
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
