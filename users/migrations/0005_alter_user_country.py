# Generated by Django 5.0.7 on 2024-07-20 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, help_text='Введите страну', max_length=100, null=True, verbose_name='Страна'),
        ),
    ]
