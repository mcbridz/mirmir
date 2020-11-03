from django.db import models
from django.contrib.auth.models import User


###############################################
#             Contact Models                  #
###############################################
class StatusField(models.Model):
    status = models.CharField(max_length=50)
    pretty_status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.pretty_status + str(self.id)


class SortField(models.Model):
    name = models.CharField(max_length=50)
    pretty_name = models.CharField(max_length=50)

    def __str__(self):
        return self.pretty_name


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=255, blank=True)
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
    email_address_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.last_name + ', ' + self.first_name


class EmailConfirmation(models.Model):
    contact = models.ForeignKey(
        Contact, on_delete=models.PROTECT, related_name='email_confirmations')
    code = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_confirmed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.contact.username.username + ' ' + self.code

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
        max_length=255, blank=True)
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

    @staticmethod
    def get_active_products():
        products = Product.objects.filter(is_active=True)
        product_output = []
        for product in products:
            photos = product.product_photos.all()
            photo_data = []
            for photo in photos:
                photo_data.append({
                    "photo": photo.photo.url,
                    "photo_image_number": photo.photo_image_number,
                    "id": photo.id,
                })
            product_output.append({
                "id": product.id,
                "product_type": product.product_type,
                "title": product.title,
                "POSTitle": product.POSTitle,
                "brand": product.brand,
                "subtitle": product.subtitle,
                "action_message": product.action_message,
                "is_active": product.is_active,
                "is_display_on_website": product.is_display_on_website,
                "description": product.description,
                "description_teaser": product.description_teaser,
                # wine_properties
                "date_added": product.date_added.strftime('%m/%d/%Y'),
                "date_modified": '' if product.date_modified is None else product.date_modified.strftime('%m/%d/%Y'),
                # SKU generation using last three digits of year, followed by month and day bottled, followed by the first three letters of the mead name
                "SKU_SKU": product.SKU_SKU,
                "SKU_cost_of_good": product.SKU_cost_of_good,
                "SKU_UPC_code": product.SKU_UPC_code,
                "SKU_unit_description": product.SKU_unit_description,
                "SKU_min_order_qty": product.SKU_min_order_qty,
                "SKU_max_order_qty": product.SKU_max_order_qty,
                "SKU_order_in_multiples_of": product.SKU_order_in_multiples_of,
                "SKU_weight": product.SKU_weight,
                "SKU_is_non_taxable": product.SKU_is_non_taxable,
                "SKU_is_no_shipping_charge": product.SKU_is_no_shipping_charge,
                "SKU_Prices_price_level": product.SKU_Prices_price_level,
                "SKU_Prices_price": product.SKU_Prices_price,
                'SKU_Prices_price_quantity': product.SKU_Prices_price_quantity,
                "SKU_Prices_is_inventory_on": product.SKU_Prices_is_inventory_on,
                "SKU_Prices_Inventory_current_inventory": product.SKU_Prices_Inventory_current_inventory,
                "SKU_Prices_Inventory_inventory_pool": product.SKU_Prices_Inventory_inventory_pool,
                "WineProperties_bottles_in_case": product.WineProperties_bottles_in_case,
                "WineProperties_bottle_size_in_ml": product.WineProperties_bottle_size_in_ml,
                "WineProperties_type": product.WineProperties_type,
                "WineProperties_alcohol": product.WineProperties_alcohol,
                "WineProperties_bottling_date": product.WineProperties_bottling_date,
                "WineProperties_tasting_notes": product.WineProperties_tasting_notes,
                "WineProperties_wine_maker_notes": product.WineProperties_wine_maker_notes,
                "WineProperties_food_pairing_notes": product.WineProperties_food_pairing_notes,
                "product_photos": photo_data,
            })
        return product_output


class ProductPhoto(models.Model):
    photo = models.ImageField(upload_to='product_images')
    photo_image_number = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='product_photos')

    def __str__(self):
        return str(self.product) + ' photo# ' + str(self.photo_image_number)

    class Meta:
        ordering = ['photo_image_number']

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

    @staticmethod
    def get_shipping_statuses():
        statuses = ShippingStatus.objects.all()
        output = []
        for status in statuses:
            output.append({
                'id': status.id,
                'status': status.status,
                'pretty_status': status.pretty_status,
            })
        return output


class OrderType(models.Model):
    type_string = models.CharField(max_length=50)
    pretty_type = models.CharField(max_length=50)

    def __str__(self):
        return self.pretty_type

    @staticmethod
    def get_order_types():
        types = OrderType.objects.all()
        output = []
        for t_type in types:
            output.append({
                'type_string': t_type.type_string,
                'pretty_type': t_type.pretty_type,
                'id': t_type.id,
            })


class TransactionType(models.Model):
    t_type = models.CharField(max_length=50)
    pretty_t_type = models.CharField(max_length=50)

    def __str__(self):
        return self.pretty_t_type

    @staticmethod
    def get_transaction_types():
        t_types = TransactionType.objects.all()
        output = []
        for t_type in t_types:
            output.append({
                't_type': t_type.t_type,
                'pretty_t_type': t_type.pretty_t_type,
                'id': t_type.id,
            })


class PaymentStatus(models.Model):
    status = models.CharField(max_length=50)
    pretty_status = models.CharField(max_length=50)

    def __str__(self):
        return self.pretty_status

    @staticmethod
    def get_payment_statuses():
        payment_statuses = PaymentStatus.objects.all()
        output = []
        for status in payment_statuses:
            output.append({
                'status': status.status,
                'pretty_status': status.pretty_status,
                'id': status.id
            })


class Order(models.Model):
    contact = models.ForeignKey(
        Contact, on_delete=models.PROTECT, related_name='orders', null=True)
    order_type = models.ForeignKey(
        OrderType, on_delete=models.PROTECT, related_name='orders')
    order_number = models.IntegerField()
    order_date = models.DateField(auto_now_add=True)
    shipping_status = models.ForeignKey(
        ShippingStatus, on_delete=models.PROTECT, related_name='orders')
    ################################################
    #            billing=source(customer)           #
    ################################################
    # employee birthday
    billing_birthdate = models.DateField(blank=True)
    billing_first_name = models.CharField(max_length=50)
    billing_last_name = models.CharField(max_length=50)
    billing_company = models.CharField(max_length=100, blank=True)
    billing_address = models.CharField(max_length=100)
    billing_address2 = models.CharField(max_length=100, blank=True)
    billing_city = models.CharField(max_length=50)
    billing_state_code = models.CharField(max_length=4)
    billing_zip_code = models.IntegerField()
    billing_email = models.EmailField(
        max_length=100, default='mirmirswellmeadery@gmail.com')
    ################################################
    #       shipping=destination(customer/gift_recipient)         #
    ################################################
    shipping_birthdate = models.DateField(blank=True)
    shipping_first_name = models.CharField(max_length=50, blank=True)
    shipping_last_name = models.CharField(max_length=50, blank=True)
    shipping_company = models.CharField(max_length=100, blank=True)
    shipping_address = models.CharField(max_length=100, blank=True)
    shipping_address2 = models.CharField(max_length=100, blank=True)
    shipping_city = models.CharField(max_length=50, blank=True)
    shipping_state_code = models.CharField(max_length=4, blank=True)
    shipping_zip_code = models.IntegerField(blank=True)
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

    def __str__(self):
        return self.transaction_type.pretty_t_type + str(self.order_number)

    class Meta:
        ordering = ['-order_date']

    @staticmethod
    def get_open_orders():
        orders = Order.objects.exclude(payment_status__status=[
                                       'cancelled', 'completed'])
        order_output = []
        for order in orders:
            order_output.append({
                "contact": "Guest Checkout" if order.contact is None else order.contact.username.username,
                "order_type": order.order_type.id,
                "order_number": order.order_number,
                "order_date": order.order_date.strftime('%m/%d/%Y'),
                "billing_birthdate": order.billing_birthdate.strftime('%m/%d/%Y'),
                "billing_first_name": order.billing_first_name,
                "billing_last_name": order.billing_last_name,
                "billing_company": order.billing_company,
                "billing_address": order.billing_address,
                "billing_address2": order.billing_address2,
                "billing_city": order.billing_city,
                "billing_state_code": order.billing_state_code,
                "billing_zip_code": order.billing_zip_code,
                "billing_email": order.billing_email,
                "shipping_birthdate": order.shipping_birthdate.strftime('%m/%d/%Y'),
                "shipping_first_name": order.shipping_first_name,
                "shipping_last_name": order.shipping_last_name,
                "shipping_company": order.shipping_company,
                "shipping_address": order.shipping_address,
                "shipping_address2": order.shipping_address2,
                "shipping_city": order.shipping_city,
                "shipping_state_code": order.shipping_state_code,
                "shipping_zip_code": order.shipping_zip_code,
                "gift_message": order.gift_message,
                "sub_total": order.sub_total,
                "order_notes": order.order_notes,
                "handling": order.handling,
                "shipping": order.shipping,
                "tax": order.tax,
                "total": order.total,
                "previous_order_number": order.previous_order_number,
                "transaction_type": order.transaction_type.id,
                "is_pickup": order.is_pickup,
                "is_paid": order.is_paid,
                "shipping_service": order.shipping_service,
                "shipping_tracking_number": order.shipping_tracking_number,
                "payment_status": order.payment_status.id,
                "shipping_status": order.shipping_status.id,
            })
        return order_output


class OrderItemQuantity(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='order_items')
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items', blank=True)

    def __str__(self):
        return str(self.product) + ': ' + str(self.quantity)
