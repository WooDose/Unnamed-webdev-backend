# Generated by Django 3.0.6 on 2020-06-03 00:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messages_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='message_date',
        ),
    ]