# Generated by Django 4.2.6 on 2024-07-06 07:53

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_activitylist_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitylist',
            name='price',
            field=djmoney.models.fields.MoneyField(decimal_places=3, default_currency='IDR', max_digits=10),
        ),
    ]
