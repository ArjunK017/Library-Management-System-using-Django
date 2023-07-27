# Generated by Django 4.2.1 on 2023-06-20 12:47

import authsystem.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authsystem', '0011_addbook_is_reserved'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentid', models.CharField(max_length=20)),
                ('book1', models.CharField(max_length=20)),
                ('issuedate', models.DateField(auto_now=True)),
                ('expirydate', models.DateField(default=authsystem.models.expiry)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
