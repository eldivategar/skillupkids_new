# Generated by Django 4.2.6 on 2023-11-09 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_testimonial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylist',
            name='price',
            field=models.DecimalField(decimal_places=2, default='', max_digits=10),
        ),
    ]
