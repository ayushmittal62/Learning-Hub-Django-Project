"""
Run this script to create test users:
python manage.py shell < create_users.py
"""

from django.contrib.auth.models import User
from MyFirstProject.models import UserProfile

print("\n=== Creating Test Users ===\n")

# Create Admin User 1
try:
    admin1 = User.objects.create_user(
        username='admin1',
        email='admin1@example.com',
        password='admin123'
    )
    admin1.profile.user_type = 'admin'
    admin1.profile.save()
    print(f"Created: {admin1.username} - Type: {admin1.profile.user_type}")
except Exception as e:
    print(f"Error creating admin1: {e}")

# Create Admin User 2
try:
    admin2 = User.objects.create_user(
        username='sarah',
        email='sarah@example.com',
        password='admin456'
    )
    admin2.profile.user_type = 'admin'
    admin2.profile.save()
    print(f"Created: {admin2.username} - Type: {admin2.profile.user_type}")
except Exception as e:
    print(f"Error creating sarah: {e}")

# Create Regular User 1
try:
    user1 = User.objects.create_user(
        username='john',
        email='john@example.com',
        password='user123'
    )
    print(f"Created: {user1.username} - Type: {user1.profile.user_type}")
except Exception as e:
    print(f"Error creating john: {e}")

# Create Regular User 2
try:
    user2 = User.objects.create_user(
        username='alice',
        email='alice@example.com',
        password='user456'
    )
    print(f"Created: {user2.username} - Type: {user2.profile.user_type}")
except Exception as e:
    print(f"Error creating alice: {e}")

print("\n=== Summary ===")
print(f"Total Users: {User.objects.count()}")
print(f"Total Admin Users: {UserProfile.objects.filter(user_type='admin').count()}")
print(f"Total Regular Users: {UserProfile.objects.filter(user_type='user').count()}")

print("\n=== Login Credentials ===")
print("\nADMIN USERS:")
print("  Username: admin1  | Password: admin123 | Login As: Admin")
print("  Username: sarah   | Password: admin456 | Login As: Admin")
print("\nREGULAR USERS:")
print("  Username: john    | Password: user123  | Login As: User")
print("  Username: alice   | Password: user456  | Login As: User")
print("\nLogin URL: http://localhost:8000/login/")
print("\n=== Done! ===\n")
