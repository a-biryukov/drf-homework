# Generated by Django 5.0.7 on 2024-07-13 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_payments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='payment_amount',
            field=models.IntegerField(verbose_name='Сумма оплаты'),
        ),
    ]
