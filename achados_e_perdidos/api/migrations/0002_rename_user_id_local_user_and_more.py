# Generated by Django 4.1.2 on 2022-10-17 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='local',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='objeto',
            old_name='local_id',
            new_name='local',
        ),
    ]
