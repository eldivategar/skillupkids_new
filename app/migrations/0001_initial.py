# Generated by Django 4.2.6 on 2024-07-05 16:24

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityList',
            fields=[
                ('activity_id', models.AutoField(primary_key=True, serialize=False)),
                ('activity_name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('day', models.TextField(default='')),
                ('price', models.DecimalField(decimal_places=3, default='', max_digits=10)),
                ('duration', models.IntegerField(default='')),
                ('age', models.TextField(default='')),
                ('description', models.TextField(default='')),
                ('sub_description', models.TextField(default='')),
                ('learning_method', models.TextField(default='')),
                ('benefit', models.TextField(blank=True, default='', null=True)),
                ('requirements', models.TextField(blank=True, default='', null=True)),
                ('additional_information', models.TextField(blank=True, default='', null=True)),
                ('activity_image', models.ImageField(blank=True, default='activity/default-activity.jpg', null=True, upload_to='activity/')),
                ('activity_status', models.CharField(choices=[('pending', 'Pending'), ('terbit', 'Terbit'), ('ditolak', 'Ditolak')], default='pending', max_length=10)),
                ('message_status', models.TextField(blank=True, default='', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('blog_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, default='blog/default-blog.jpg', null=True, upload_to='blog/')),
                ('tag', models.CharField(default='', max_length=50)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('cust_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('number', models.CharField(max_length=13, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('address', models.TextField(blank=True, default='', null=True)),
                ('profile_image', models.ImageField(blank=True, default='member/avatar-profile_n68t05.jpg', null=True, upload_to='member/')),
                ('is_verified', models.BooleanField(default=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mitra',
            fields=[
                ('mitra_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('number', models.CharField(max_length=13, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('city', models.CharField(default='', max_length=50)),
                ('description', models.TextField()),
                ('start_time', models.TimeField(default='00:00:00')),
                ('end_time', models.TimeField(default='00:00:00')),
                ('twitter_site', models.URLField(blank=True, default='')),
                ('fb_site', models.URLField(blank=True, default='')),
                ('ig_site', models.URLField(blank=True, default='')),
                ('linkedin_site', models.URLField(blank=True, default='')),
                ('yt_site', models.URLField(blank=True, default='')),
                ('profile_image', models.ImageField(blank=True, default='mitra/default-logo_sicqfg.png', null=True, upload_to='mitra/')),
                ('is_verified', models.BooleanField(default=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.CharField(editable=False, max_length=20, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(null=True)),
                ('is_free', models.BooleanField(choices=[(True, True), (False, False)], default=False)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Menunggu Pembayaran', 'Menunggu Pembayaran'), ('Sukses', 'Sukses'), ('Lunas', 'Lunas'), ('Gagal', 'Gagal'), ('Refund', 'Refund'), ('Kadaluwarsa', 'Kadaluwarsa'), ('Dibatalkan', 'Dibatalkan')], default='Menunggu Pembayaran', max_length=50)),
                ('message_status', models.TextField(blank=True, default='')),
                ('total_price', models.DecimalField(decimal_places=3, default=0, max_digits=10)),
                ('payment_method', models.CharField(choices=[('Transfer Bank', 'Transfer Bank'), ('OVO', 'OVO'), ('GoPay', 'GoPay'), ('LinkAja', 'LinkAja'), ('Dana', 'Dana'), ('ShopeePay', 'ShopeePay'), ('Alfamart', 'Alfamart'), ('Indomaret', 'Indomaret')], default='Transfer Bank', max_length=50)),
                ('expired_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('token', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_transaction', to='app.activitylist')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_transaction', to='app.member', to_field='uuid')),
                ('mitra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mitra_transaction', to='app.mitra', to_field='uuid')),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('testimonial_id', models.AutoField(primary_key=True, serialize=False)),
                ('testimonial', models.TextField(default='')),
                ('rating', models.IntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_testimonial', to='app.activitylist')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_testimonial', to='app.member', to_field='uuid')),
            ],
        ),
        migrations.AddField(
            model_name='activitylist',
            name='mitra_activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mitra_activity', to='app.mitra', to_field='uuid'),
        ),
    ]
