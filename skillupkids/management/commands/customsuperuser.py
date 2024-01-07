from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            superuser = User.objects.create_superuser(
                username='admin',
                email='skillupkidscontact@gmail.com',
                password='skillupkidsid'
            )
            superuser.save()
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser with username "admin" already exists. No new superuser created.'))
