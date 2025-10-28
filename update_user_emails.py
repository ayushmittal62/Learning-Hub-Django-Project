import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from django.contrib.auth.models import User

# Update existing users with email addresses
users_to_update = [
    ('admin1', 'admin1@learninghub.com'),
    ('john', 'john@learninghub.com'),
    ('sarah', 'sarah@learninghub.com'),
]

for username, email in users_to_update:
    try:
        user = User.objects.get(username=username)
        user.email = email
        user.save()
        print(f"✅ Updated {username} with email: {email}")
    except User.DoesNotExist:
        print(f"❌ User {username} not found")

print("\n✅ Email addresses updated successfully!")
