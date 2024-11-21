# Generated by Django 5.1.1 on 2024-11-16 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_payment_link_payment_session_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="payment_date",
            field=models.DateField(
                default=datetime.datetime.now, verbose_name="дата оплаты"
            ),
        ),
    ]