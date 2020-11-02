from django.forms import ModelForm, TextInput, DateField, DateInput
from django import forms
from .models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        # fields = '__all__'
        exclude = ['username', 'status', 'email_address_confirmed']
        widgets = {
            'birthday': TextInput(attrs={'type': 'date'})
        }


# date_field = forms.DateField(
#     widget=forms.TextInput(
#         attrs={'type': 'date'}
#     )
# )
