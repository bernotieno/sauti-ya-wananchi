import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create admin user for production deployment'

    def handle(self, *args, **options):
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'admin@sauti.go.ke')
        password = os.getenv('ADMIN_PASSWORD', 'admin123')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                role='admin'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Admin user "{username}" created successfully')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Admin user "{username}" already exists')
            )