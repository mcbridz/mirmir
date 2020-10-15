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
    company = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state_code = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    main_phone = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    username = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateField()
    status = models.ForeignKey(
        StatusField, on_delete=models.PROTECT, related_name='profile', null=True, blank=True)
