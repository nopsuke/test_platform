# Generated by Django 4.2.1 on 2023-05-10 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_userprofile_leverage_alter_userprofile_balance"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="margin_level",
            field=models.FloatField(default=100.0),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="open_positions",
            field=models.JSONField(default=dict),
        ),
    ]
