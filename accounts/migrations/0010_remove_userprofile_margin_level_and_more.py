# Generated by Django 4.2.1 on 2023-06-16 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0009_openpositions_closedpositions"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="margin_level",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="open_positions",
        ),
        migrations.AddField(
            model_name="closedpositions",
            name="leverage",
            field=models.DecimalField(decimal_places=2, default=20.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name="openpositions",
            name="leverage",
            field=models.DecimalField(decimal_places=2, default=20.0, max_digits=8),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="leverage",
            field=models.FloatField(default=20.0),
        ),
    ]
