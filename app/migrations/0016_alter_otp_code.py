# Generated by Django 4.2.6 on 2024-07-10 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='code',
            field=models.CharField(max_length=4),
        ),
    ]