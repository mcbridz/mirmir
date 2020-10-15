from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth
from .models import StatusField, SortField, Contact
import requests
import random
# from django.contrib.auth import login as login_user
import django.contrib.auth

#


#


def index(request):
    context = {
        'message': 'Hello, world!',
    }
    return render(request, 'mirmir_app/index.html', context)


def main(request):
    context = {

    }
    return render(request, 'mirmir_app/main.html', context)


def about(request):
    context = {

    }
    return render(request, 'mirmir_app/about.html', context)


def club(request):
    context = {

    }
    return render(request, 'mirmir_app/club.html', context)


def archive(request):
    context = {

    }
    return render(request, 'mirmir_app/archive.html', context)


def register(request):
    context = {

    }
    return render(request, 'mirmir_app/register.html', context)


def login(request):
    if request.method == 'GET':
        context = {
            'site_key': settings.RECAPTCHA_SITE_KEY,
        }
        return render(request, 'mirmir_app/login.html', context)
    else:
        secret_key = settings.RECAPTCHA_SECRET_KEY
        data = {
            'response': request.POST['g-captcha-response'],
            'secret': secret_key,
        }
        resp = requests.post(
            'https://www.google.com/recaptcha/api/siteverify', data=data)
        result_json = resp.json()
        print(result_json)
        ################################################
        # need captcha logic
        ################################################
        # user login logic here
        username = request.POST['username']
        password = request.POST['password']
        user = django.contrib.auth.authenticate(
            request, username=username, password=password)

        if user is None:
            message = 'not_found'
        else:
            django.contrib.auth.login(request, user)
            next = request.GET.get('next', reverse('mirmir_app:main'))
            return HttpResponseRedirect(next)
