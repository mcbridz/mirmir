from django.contrib import admin
from .models import Contact, StatusField, SortField, Product, CarouselSlide, MainPageWarning, MainPageHighlight

admin.site.register(Contact)
admin.site.register(StatusField)
admin.site.register(SortField)
admin.site.register(Product)
admin.site.register(CarouselSlide)
admin.site.register(MainPageWarning)
admin.site.register(MainPageHighlight)
