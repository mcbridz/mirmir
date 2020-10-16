from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth
from .models import StatusField, SortField, Contact, Product, CarouselSlide, MainPageWarning, MainPageHighlight
import requests
import random
# from django.contrib.auth import login as login_user
import django.contrib.auth
from django.views.generic import CreateView
from .forms import ContactForm


####################################
#         Employee Views           #
####################################

def employee_check(user):
    return user.profile.status.status == 'employee'


@user_passes_test(employee_check)
def employee_main(request):
    print(request)
    return render(request, 'mirmir_app/employee_main.html')


@user_passes_test(employee_check)
def main_page_management(request):
    print(request)
    context = {

    }
    return render(request, 'mirmir_app/main_page_management.html', context)


@user_passes_test(employee_check)
def highlights(request):
    highlights = MainPageHighlight.objects.all()
    highlight_data = []
    for highlight in highlights:
        highlight_data.append({
            'image': highlight.image.url,
            'text': highlight.text,
        })
    return JsonResponse({'highlight_data': highlight_data})


@user_passes_test(employee_check)
def get_warning(request):
    warning = MainPageWarning.objects.get(id=1)
    return JsonResponse({'warning': warning.text, 'shown': warning.show_warning})


@user_passes_test(employee_check)
def get_carousele(request):
    slides = CarouselSlide.objects.all()
    slides_data = []
    for slide in slides:
        slides_data.append({
            'image': slide.image.url,
            'caption_title': slide.caption_title,
            'display_order': slide.display_order,
        })
    return JsonResponse({'slides': slides_data})
####################################
#         Customer Views           #
####################################


def index(request):
    context = {
        'message': 'Hello, world!',
    }
    return render(request, 'mirmir_app/index.html', context)


def main(request):
    meads = Product.objects.filter(is_display_on_website=True)
    slides = CarouselSlide.objects.all()
    warning = MainPageWarning.objects.get(id=1)
    highlights = MainPageHighlight.objects.all()
    context = {
        'meads': meads,
        'slides': slides,
        'warning': warning,
        'highlights': highlights,
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
    if request.method == 'GET':
        form = ContactForm()
        context = {
            'form': form,
            'site_key': settings.RECAPTCHA_SITE_KEY,
        }
        return render(request, 'mirmir_app/register.html', context)
    else:
        print(request.POST)
        secret_key = settings.RECAPTCHA_SECRET_KEY
        data = {
            'response': request.POST['g-recaptcha-response'],
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
        password = request.POST['password']
        password_v = request.POST['password_v']
        if password != password_v:
            message = 'passwords do not match'
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            message = 'user already exists'
        user = User.objects.create_user(
            username, request.POST['email'], password)
        data = request.POST
        new_contact = Contact(
            username=user,
            first_name=data['first_name'],
            last_name=data['last_name'],
            company=data['company'],
            city=data['city'],
            state_code=data['state_code'],
            zip_code=data['zip_code'],
            main_phone=data['main_phone'],
            email=data['email'],
            birthday=data['birthday']
        )
        new_contact.save()
        django.contrib.auth.login(request, user)
        # django.contrib.auth.login(request, user)
        next = request.GET.get('next', reverse('mirmir_app:main'))
        return HttpResponseRedirect(next)


@login_required
def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(reverse('mirmir_app:main'))


def login(request):
    if request.method == 'GET':
        context = {
            'site_key': settings.RECAPTCHA_SITE_KEY,
        }
        return render(request, 'mirmir_app/login.html', context)
    else:
        secret_key = settings.RECAPTCHA_SECRET_KEY
        data = {
            'response': request.POST['g-recaptcha-response'],
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
        print(user.profile.status)
        if user is None:
            message = 'not_found'
        elif user.profile.status.status == 'employee':
            context = {

            }
            django.contrib.auth.login(request, user)
            next = request.GET.get('next', reverse('mirmir_app:employee_main'))
            return HttpResponseRedirect(next)
        else:
            django.contrib.auth.login(request, user)
            next = request.GET.get('next', reverse('mirmir_app:main'))
            return HttpResponseRedirect(next)
