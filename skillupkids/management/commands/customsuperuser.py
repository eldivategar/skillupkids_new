from django.contrib.auth.models import User

superuser = User.objects.create_superuser(
    username='admin',
    email='skillupkidscontact@gmail.com',
    password='skillupkidsid'
)
superuser.save()