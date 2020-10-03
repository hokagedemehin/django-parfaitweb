# Generated by Django 3.1.1 on 2020-10-02 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0033_auto_20201002_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], default='Pending', max_length=100, null=True),
        ),
    ]