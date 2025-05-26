from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Create a superuser without prompt if not exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "saxena")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "mratyunjay.saxena.cs2@gmail.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "1234")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser \"{username}\" already exists.'))
