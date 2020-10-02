# Generated by Django 3.1.1 on 2020-10-02 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0024_auto_20200927_2353'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flutter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.CharField(blank=True, max_length=2000, null=True)),
                ('secret_key', models.CharField(blank=True, max_length=2000, null=True)),
                ('encryption_key', models.CharField(blank=True, max_length=2000, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]