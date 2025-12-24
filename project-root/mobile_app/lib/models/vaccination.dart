class Vaccination {
  final int id;
  final int userId;
  final String vaccineName;
  final String dateAdministered;
  final String? nextDueDate;

  Vaccination({
    required this.id,
    required this.userId,
    required this.vaccineName,
    required this.dateAdministered,
    this.nextDueDate,
  });

  factory Vaccination.fromJson(Map<String, dynamic> json) {
    return Vaccination(
      id: json['id'],
      userId: json['user_id'],
      vaccineName: json['vaccine_name'],
      dateAdministered: json['date_administered'],
      nextDueDate: json['next_due_date'],
    );
  }
}
