# Generated by Django 5.1.1 on 2024-10-20 19:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_payment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="payment_date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 10, 20, 19, 41, 48, 553735, tzinfo=datetime.timezone.utc
                ),
                verbose_name="дата оплаты",
            ),
        ),
    ]