# Generated by Django 3.1.1 on 2020-09-20 22:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drinks', '0016_product_full_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='allModels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(default=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='drinks.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='drinks.order')),
                ('orderitems', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='drinks.orderitem')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='drinks.product')),
                ('ship', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='drinks.shippingaddress')),
            ],
        ),
    ]
