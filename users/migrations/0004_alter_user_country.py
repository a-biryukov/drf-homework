# Generated by Django 5.0.7 on 2024-07-20 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_payments_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, help_text='Введите страну', null=True, verbose_name='Страна'),
        ),
    ]
