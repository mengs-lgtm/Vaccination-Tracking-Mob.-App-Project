class User {
  final int id;
  final String fullName;
  final String profileType;

  User({required this.id, required this.fullName, required this.profileType});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      fullName: json['full_name'],
      profileType: json['profile_type'],
    );
  }
}
