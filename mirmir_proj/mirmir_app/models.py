from django.db import models
from django.contrib.auth.models import User


class StatusField(models.Model):
    status = models.CharField(max_length=50)
    pretty_status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.pretty_status


class SortField(models.Model):
    name = models.CharField(max_length=50)
    pretty_name = models.CharField(max_length=50)

    def __str__(self):
        return self.pretty_name


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state_code = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=50, blank=True, null=True)
    main_phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100)
    username = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateField()
    status = models.ForeignKey(
        StatusField, on_delete=models.PROTECT, related_name='profile', default=2)

    def __str__(self):
        return self.last_name + ', ' + self.first_name


class Product(models.Model):
    product_type = models.CharField(max_length=50, default='Product')
    title = models.CharField(max_length=255)
    POSTitle = models.CharField(max_length=50)
    brand = models.CharField(max_length=255, default='Mirmir\'s Well Meadery')
    subtitle = models.CharField(max_length=50, blank=True, null=True)
    action_message = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_display_on_website = models.BooleanField(default=True)
    description = models.TextField()
    description_teaser = models.CharField(
        max_length=255, blank=True, null=True)
    # wine_properties
    date_added = models.DateField(auto_now_add=True)
    date_modified = models.DateField(blank=True, null=True)
    # SKU generation using last three digits of year, followed by month and day bottled, followed by the first three letters of the mead name
    SKU_SKU = models.CharField(max_length=50)
    SKU_cost_of_good = models.FloatField()
    SKU_UPC_code = models.CharField(max_length=255)
    SKU_unit_description = models.CharField(max_length=255)
    SKU_min_order_qty = models.IntegerField()
    SKU_max_order_qty = models.IntegerField()
    SKU_order_in_multiples_of = models.IntegerField()
    SKU_weight = models.IntegerField()
    SKU_is_non_taxable = models.BooleanField(default=False)
    SKU_is_no_shipping_charge = models.BooleanField(default=False)

    SKU_Prices_price_level = models.CharField(max_length=50)
    SKU_Prices_price = models.FloatField()
    SKU_Prices_price_quantity = models.IntegerField()
    SKU_Prices_is_inventory_on = models.BooleanField(default=True)

    SKU_Prices_Inventory_current_inventory = models.IntegerField()
    SKU_Prices_Inventory_inventory_pool = models.IntegerField()

    WineProperties_bottles_in_case = models.IntegerField(blank=True, null=True)
    WineProperties_bottle_size_in_ml = models.IntegerField()
    WineProperties_type = models.CharField(
        max_length=50, blank=True, null=True)
    WineProperties_alcohol = models.CharField(max_length=255)
    WineProperties_bottling_date = models.DateField()
    WineProperties_tasting_notes = models.TextField(blank=True, null=True)
    WineProperties_wine_maker_notes = models.TextField(blank=True, null=True)
    WineProperties_food_pairing_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class CarouselSlide(models.Model):
    image = models.ImageField(
        upload_to='carousel_images', null=True, blank=True)
    caption_title = models.CharField(max_length=100, null=True, blank=True)
    caption = models.CharField(max_length=100, null=True, blank=True)
    display_order = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return str(self.display_order) + ': ' + self.caption


class MainPageWarning(models.Model):
    text = models.CharField(max_length=255)
    show_warning = models.BooleanField(default=False)


class MainPageHighlight(models.Model):
    image = models.ImageField(
        upload_to='highlight_images', null=True, blank=True)
    text = models.TextField(null=True, blank=True)

##############################################
# Investigate abstracting Main Page Elements into a two element table of 'key': JSON to hold data
##############################################
