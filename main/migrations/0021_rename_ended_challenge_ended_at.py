# Generated by Django 3.2 on 2024-01-07 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20240107_2024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='challenge',
            old_name='ended',
            new_name='ended_at',
        ),
    ]
