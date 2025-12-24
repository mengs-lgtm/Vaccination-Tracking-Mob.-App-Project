import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/vaccination.dart';
import '../widgets/vaccination_card.dart';

class Dashboard extends StatefulWidget {
  @override
  _DashboardState createState() => _DashboardState();
}

class _DashboardState extends State<Dashboard> {
  final ApiService apiService = ApiService();
  late Future<List<Vaccination>> vaccinations;
  late Future<List<Vaccination>> upcomingVaccinations;

  @override
  void initState() {
    super.initState();
    vaccinations = apiService.fetchVaccinations();
    upcomingVaccinations = apiService.fetchUpcomingVaccinations(withinDays: 30);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Vaccination Tracker")),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Upcoming Reminders Section
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "Upcoming Reminders",
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
            ),
            FutureBuilder<List<Vaccination>>(
              future: upcomingVaccinations,
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  if (snapshot.data!.isEmpty) {
                    return Center(child: Text("No upcoming vaccinations"));
                  }
                  return Column(
                    children: snapshot.data!
                        .map((v) => VaccinationCard(vaccination: v))
                        .toList(),
                  );
                } else if (snapshot.hasError) {
                  return Center(child: Text("Error: ${snapshot.error}"));
                }
                return Center(child: CircularProgressIndicator());
              },
            ),

            Divider(),

            // All Vaccinations Section
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "All Vaccinations",
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
            ),
            FutureBuilder<List<Vaccination>>(
              future: vaccinations,
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  return Column(
                    children: snapshot.data!
                        .map((v) => VaccinationCard(vaccination: v))
                        .toList(),
                  );
                } else if (snapshot.hasError) {
                  return Center(child: Text("Error: ${snapshot.error}"));
                }
                return Center(child: CircularProgressIndicator());
              },
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
        onPressed: () => Navigator.pushNamed(context, "/add"),
      ),
    );
  }
}
