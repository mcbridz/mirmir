# Generated by Django 3.1.1 on 2020-10-21 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mirmir_app', '0013_auto_20201020_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_string', models.CharField(max_length=50)),
                ('pretty_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('pretty_status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
                ('pretty_status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_type', models.CharField(max_length=50)),
                ('pretty_t_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItemQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='OrderItems', to='mirmir_app.product')),
            ],
        ),
    ]