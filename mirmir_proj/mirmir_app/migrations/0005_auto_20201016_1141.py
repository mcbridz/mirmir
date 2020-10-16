# Generated by Django 3.1.1 on 2020-10-16 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mirmir_app', '0004_auto_20201015_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(
                    default='Product', max_length=50)),
                ('title', models.CharField(max_length=255)),
                ('POSTitle', models.CharField(max_length=50)),
                ('brand', models.CharField(
                    default="Mirmir's Well Meadery", max_length=255)),
                ('subtitle', models.CharField(blank=True, max_length=50, null=True)),
                ('action_message', models.CharField(
                    blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_display_on_website', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('description_teaser', models.CharField(
                    blank=True, max_length=255, null=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(blank=True, null=True)),
                ('SKU_SKU', models.CharField(max_length=50)),
                ('SKU_cost_of_good', models.FloatField()),
                ('SKU_UPC_code', models.CharField(max_length=255)),
                ('SKU_unit_description', models.CharField(max_length=255)),
                ('SKU_min_order_qty', models.IntegerField()),
                ('SKU_max_order_qty', models.IntegerField()),
                ('SKU_order_in_multiples_of', models.IntegerField()),
                ('SKU_weight', models.IntegerField()),
                ('SKU_is_non_taxable', models.BooleanField(default=False)),
                ('SKU_is_no_shipping_charge', models.BooleanField(default=False)),
                ('SKU_Prices_price_level', models.CharField(max_length=50)),
                ('SKU_Prices_price', models.FloatField()),
                ('SKU_Prices_price_quantity', models.IntegerField()),
                ('SKU_Prices_is_inventory_on', models.BooleanField(default=True)),
                ('SKU_Prices_Inventory_current_inventory', models.IntegerField()),
                ('SKU_Prices_Inventory_inventory_pool', models.IntegerField()),
                ('WineProperties_bottles_in_case',
                 models.IntegerField(blank=True, null=True)),
                ('WineProperties_bottle_size_in_ml', models.IntegerField()),
                ('WineProperties_type', models.CharField(
                    blank=True, max_length=50, null=True)),
                ('WineProperties_alcohol', models.CharField(max_length=255)),
                ('WineProperties_bottling_date', models.DateField()),
                ('WineProperties_tasting_notes',
                 models.TextField(blank=True, null=True)),
                ('WineProperties_wine_maker_notes',
                 models.TextField(blank=True, null=True)),
                ('WineProperties_food_pairing_notes',
                 models.TextField(blank=True, null=True)),
            ],
        ),
    ]