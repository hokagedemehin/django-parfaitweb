# Generated by Django 3.1.1 on 2020-09-23 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0022_auto_20200923_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='profile_default.jpg', null=True, upload_to=''),
        ),
    ]
