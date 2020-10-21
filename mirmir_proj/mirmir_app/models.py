from django.db import models
from django.contrib.auth.models import User


###############################################
#             Contact Models                  #
###############################################
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

###############################################
#               Product Models                #
###############################################


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


class ProductPhoto(models.Model):
    photo = models.ImageField(upload_to='product_images')
    photo_image_number = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='product_photos')

    def __str__(self):
        return str(self.product) + ' photo# ' + str(self.photo_image_number)

###################################################################
#                          Page Models                            #
###################################################################


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


##################################################################
#                         Order Models                           #
##################################################################
class ShippingStatus(models.Model):
    status = models.CharField(max_length=50)
    pretty_status = models.CharField(max_length=50)

    def __str__(self):
        return self.pretty_status


class OrderType(models.Model):
    type_string = models.CharField(max_length=50)
    pretty_type = models.CharField(max_length=50)

    def __str__(self):
        return self.pretty_type


class TransactionType(models.Model):
    t_type = models.CharField(max_length=50)
    pretty_t_type = models.CharField(max_length=50)

    def __str__(self):
        return self.pretty_t_type


class PaymentStatus(models.Model):
    status = models.CharField(max_length=50)
    pretty_status = models.CharField(max_length=50)

    def __str__(self):
        return self.pretty_status


class Order(models.Model):
    contact = models.ForeignKey(
        Contact, on_delete=models.PROTECT, related_name='orders')
    order_type = models.ForeignKey(
        OrderType, on_delete=models.PROTECT, related_name='orders')
    order_number = models.IntegerField()
    order_date = models.DateField(auto_now_add=True)
    shipping_status = models.ForeignKey(
        ShippingStatus, on_delete=models.PROTECT, related_name='orders')
    ################################################
    #            billing=source(meadery)           #
    ################################################
    # employee birthday
    billing_birthdate = models.DateField()
    billing_first_name = models.CharField(max_length=50)
    billing_last_name = models.CharField(max_length=50)
    billing_company = models.CharField(
        max_length=100, default='Mirmir\'s Well Meadery')
    billing_address = models.CharField(max_length=100)
    billing_address2 = models.CharField(max_length=100, blank=True)
    billing_city = models.CharField(max_length=50)
    billing_state_code = models.CharField(max_length=4)
    billing_zip_code = models.IntegerField()
    billing_email = models.EmailField(
        max_length=100, default='mirmirswellmeadery@gmail.com')
    ################################################
    #       shipping=destination(customer)         #
    ################################################
    # customer birthday
    shipping_birthdate = models.DateField()
    shipping_first_name = models.CharField(max_length=50)
    shipping_last_name = models.CharField(max_length=50)
    shipping_company = models.CharField(max_length=100)
    shipping_address = models.CharField(max_length=100)
    shipping_address2 = models.CharField(max_length=100, blank=True)
    shipping_city = models.CharField(max_length=50)
    shipping_state_code = models.CharField(max_length=4)
    shipping_zip_code = models.IntegerField()
    gift_message = models.CharField(max_length=1024, blank=True)
    sub_total = models.FloatField(default=0.0)
    order_notes = models.CharField(max_length=1024, blank=True)
    handling = models.FloatField(default=0.0)
    shipping = models.FloatField(default=0.0)
    tax = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    previous_order_number = models.IntegerField(blank=True)
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.PROTECT, related_name='orders')
    is_pickup = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    shipping_service = models.CharField(max_length=100, blank=True)
    shipping_tracking_number = models.CharField(max_length=200, blank=True)
    payment_status = models.ForeignKey(
        PaymentStatus, on_delete=models.PROTECT, related_name='orders')
    shipping_status = models.ForeignKey(
        ShippingStatus, on_delete=models.PROTECT, related_name='orders')


class OrderItemQuantity(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='order_items')
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items', blank=True)

    def __str__(self):
        return str(self.product) + ': ' + str(self.quantity)
