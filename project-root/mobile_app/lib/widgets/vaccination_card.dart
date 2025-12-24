import 'package:flutter/material.dart';
import '../models/vaccination.dart';

class VaccinationCard extends StatelessWidget {
  final Vaccination vaccination;

  VaccinationCard({required this.vaccination});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.all(8),
      child: ListTile(
        title: Text(vaccination.vaccineName),
        subtitle: Text(
          "Administered: ${vaccination.dateAdministered}\n"
          "Next Due: ${vaccination.nextDueDate ?? 'N/A'}",
        ),
        leading: Icon(Icons.medical_services, color: Colors.blue),
      ),
    );
  }
}
