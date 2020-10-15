from django.contrib import admin
from .models import Contact, StatusField, SortField

admin.site.register(Contact)
admin.site.register(StatusField)
admin.site.register(SortField)
