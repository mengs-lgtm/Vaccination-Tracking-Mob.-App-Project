import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/vaccination.dart';

class ApiService {
  // Base URL for your FastAPI backend
  static const String baseUrl = "http://10.10.14.243:8000"; // chrome
  // For physical device testing, replace with your computer's local IP (e.g., http://192.168.x.x:8000)

  /// Fetch all vaccination records
  Future<List<Vaccination>> fetchVaccinations() async {
    final response = await http.get(Uri.parse("$baseUrl/vaccinations"));
    if (response.statusCode == 200) {
      final List data = json.decode(response.body);
      return data.map((e) => Vaccination.fromJson(e)).toList();
    } else {
      throw Exception("Failed to load vaccinations");
    }
  }

  /// Add a new vaccination record
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

  /// Fetch upcoming vaccinations within a given number of days
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
}
