# Generated by Django 3.1.1 on 2020-09-19 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0012_auto_20200920_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
