# Generated by Django 5.1 on 2024-09-02 17:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cricketers", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cricketer",
            old_name="average",
            new_name="odi_average",
        ),
        migrations.RenameField(
            model_name="cricketer",
            old_name="catches",
            new_name="odi_catches",
        ),
        migrations.RenameField(
            model_name="cricketer",
            old_name="matches",
            new_name="odi_matches",
        ),
        migrations.RenameField(
            model_name="cricketer",
            old_name="runs",
            new_name="odi_runs",
        ),
        migrations.RenameField(
            model_name="cricketer",
            old_name="strike_rate",
            new_name="odi_strike_rate",
        ),
    ]