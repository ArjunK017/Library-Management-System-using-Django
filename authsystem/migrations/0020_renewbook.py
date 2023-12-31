# Generated by Django 4.2.1 on 2023-06-21 04:10

import authsystem.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authsystem', '0019_remove_reservedbook_user_reservedbook_user2_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RenewBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentid', models.CharField(max_length=20)),
                ('book1', models.CharField(max_length=20)),
                ('issuedate', models.DateField(auto_now=True)),
                ('expirydate', models.DateField(default=authsystem.models.expiry)),
                ('user2', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
