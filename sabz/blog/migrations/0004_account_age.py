# Generated by Django 5.0.7 on 2024-08-20 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_account_address_alter_account_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='age',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]