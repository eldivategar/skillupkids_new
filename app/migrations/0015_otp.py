# Generated by Django 4.2.6 on 2024-07-10 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_featuredactivity'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
            ],
        ),
    ]
