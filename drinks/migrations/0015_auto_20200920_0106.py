# Generated by Django 3.1.1 on 2020-09-20 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0014_auto_20200920_0106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='slug_Customer',
            new_name='slugCustomer',
        ),
    ]
