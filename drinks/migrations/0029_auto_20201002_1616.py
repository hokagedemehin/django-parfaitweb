# Generated by Django 3.1.1 on 2020-10-02 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0028_auto_20201002_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Pend', 'Pending'), ('Out For Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], default='Pend', max_length=100, null=True),
        ),
    ]
