# Generated by Django 4.2.1 on 2023-06-19 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0015_closedpositions_fund_cost"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="openpositions",
            name="available_margin",
        ),
        migrations.AddField(
            model_name="openpositions",
            name="liquidation_price",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
