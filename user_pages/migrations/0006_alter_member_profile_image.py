# Generated by Django 4.2.6 on 2023-10-31 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_pages', '0005_alter_member_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profile_image',
            field=models.ImageField(blank=True, default='member/avatar-profile.jpg', null=True, upload_to='member/'),
        ),
    ]