from django.contrib import admin
from .models import Contact, StatusField, SortField, Product, CarouselSlide, MainPageWarning, MainPageHighlight, ShippingStatus, OrderType, OrderItemQuantity, TransactionType, PaymentStatus, Order, ProductPhoto

admin.site.register(Contact)
admin.site.register(StatusField)
admin.site.register(SortField)
admin.site.register(Product)
admin.site.register(ProductPhoto)
admin.site.register(CarouselSlide)
admin.site.register(MainPageWarning)
admin.site.register(MainPageHighlight)
admin.site.register(ShippingStatus)
admin.site.register(OrderType)
admin.site.register(OrderItemQuantity)
admin.site.register(TransactionType)
admin.site.register(PaymentStatus)
admin.site.register(Order)
