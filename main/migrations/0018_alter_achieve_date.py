# Generated by Django 3.2 on 2024-01-06 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20240106_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achieve',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
