# Generated by Django 4.2.1 on 2023-05-11 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_userprofile_margin_level_userprofile_open_positions"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="referral_code",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
