# Generated by Django 4.2.1 on 2023-06-20 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authsystem', '0012_borrowbook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowbook',
            name='user2',
        ),
    ]