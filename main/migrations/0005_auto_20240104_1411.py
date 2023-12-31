# Generated by Django 3.2 on 2024-01-04 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_balls_ball'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='reaction',
        ),
        migrations.AlterField(
            model_name='achieve',
            name='date',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='ended_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='time',
            field=models.IntegerField(default=7, editable=False),
        ),
        migrations.DeleteModel(
            name='Reaction',
        ),
    ]
