# Generated by Django 3.1.1 on 2020-09-15 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0007_auto_20200915_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
