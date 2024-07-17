# Generated by Django 5.0.6 on 2024-05-29 15:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_created=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BasketItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_order_placed', models.BooleanField(default=False)),
                ('basket_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.basket')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('delivery_address', models.CharField(max_length=200)),
                ('excepted_delivery_date', models.DateField(null=True)),
                ('payment_method', models.CharField(choices=[('cod', 'cod'), ('online', 'online')], default='cod', max_length=200)),
                ('order_id', models.CharField(max_length=200, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('order_confirmed', 'order_confirmed'), ('dispatched', 'dispatched'), ('in_transit', 'in_transit'), ('delivered', 'delivered'), ('cancelled', 'cancelled')], default='order_confirmed', max_length=200)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('basket_item_object', models.ManyToManyField(to='store.basketitems')),
                ('user_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myorders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.PositiveIntegerField()),
                ('image', models.ImageField(default='product_images/default.jpg', null=True, upload_to='productimages')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('brand_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.brand')),
                ('category_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category')),
                ('size_object', models.ManyToManyField(null=True, to='store.size')),
                ('tag_object', models.ManyToManyField(null=True, to='store.tag')),
            ],
        ),
        migrations.AddField(
            model_name='basketitems',
            name='product_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.AddField(
            model_name='basketitems',
            name='size_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.size'),
        ),
    ]
