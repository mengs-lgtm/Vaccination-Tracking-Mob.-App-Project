import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/vaccination.dart';

class ApiService {
  static const String baseUrl = "http://10.0.2.2:8000"; // Android emulator

  Future<List<Vaccination>> fetchVaccinations() async {
    final response = await http.get(Uri.parse("$baseUrl/vaccinations"));
    if (response.statusCode == 200) {
      final List data = json.decode(response.body);
      return data.map((e) => Vaccination.fromJson(e)).toList();
    } else {
      throw Exception("Failed to load vaccinations");
    }
  }

  Future<void> addVaccination(Map<String, dynamic> payload) async {
    final response = await http.post(
      Uri.parse("$baseUrl/vaccinations"),
      headers: {"Content-Type": "application/json"},
      body: json.encode(payload),
    );
    if (response.statusCode != 201) {
      throw Exception("Failed to add vaccination");
    }
  }
}

Future<List<Vaccination>> fetchUpcomingVaccinations({
  int withinDays = 30,
}) async {
  final response = await http.get(
    Uri.parse("$baseUrl/vaccinations/upcoming?within_days=$withinDays"),
  );
  if (response.statusCode == 200) {
    final List data = json.decode(response.body);
    return data.map((e) => Vaccination.fromJson(e)).toList();
  } else {
    throw Exception("Failed to load upcoming vaccinations");
  }
}
