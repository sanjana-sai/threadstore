# Generated by Django 5.0.6 on 2024-06-02 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_basketitems_basket_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketitems',
            name='basket_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cartitems', to='store.basket'),
        ),
    ]
