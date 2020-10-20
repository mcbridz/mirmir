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
import django.contrib.auth
from django.views.generic import CreateView
from .forms import ContactForm
import json


####################################
#         Employee Views           #
####################################
def justify_carousel_ordering():
    slides = CarouselSlide.objects.all()
    i = 1
    for slide in slides:
        slide.display_order = i
        i += 1


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
            'id': highlight.id,
        })
    return JsonResponse({'highlight_data': highlight_data})


@user_passes_test(employee_check)
def get_warning(request):
    warning = MainPageWarning.objects.get(id=1)
    return JsonResponse({'warning': warning.text, 'shown': warning.show_warning, 'id': 1})


@user_passes_test(employee_check)
def get_carousele(request):
    slides = CarouselSlide.objects.all()
    slides_data = []
    for slide in slides:
        slides_data.append({
            'image': slide.image.url if slide.image.url else '',
            'caption_title': slide.caption_title,
            'caption': slide.caption,
            'display_order': slide.display_order,
            'id': slide.id,
        })
    return JsonResponse({'slides': slides_data})


def get_next_order_number(group):
    return group.count() + 1


@user_passes_test(employee_check)
def add_new_slide(request):
    print(request.POST)
    print(request.FILES)
    slides = CarouselSlide.objects.all()
    new_order_num = get_next_order_number(slides)
    slide_data = request.POST
    new_slide = CarouselSlide(
        caption=slide_data['caption'],
        caption_title=slide_data['caption_title'],
        display_order=new_order_num,
    )
    if request.FILES.get('image', False):
        image = request.FILES['image']
        new_slide.image = image
    new_slide.save()
    return get_carousele(request)


@user_passes_test(employee_check)
def save_slide(request):
    print(request.POST)
    print(request.FILES)
    slide_text_data = request.POST['slide_data']
    print(slide_text_data)
    slide_text_data = json.loads(slide_text_data)
    tmp_id = slide_text_data['id']
    print(tmp_id)
    slide = CarouselSlide.objects.get(id=tmp_id)
    slide.caption_title = slide_text_data['caption_title']
    slide.caption = slide_text_data['caption']
    slide.display_order = slide_text_data['display_order']
    if request.FILES.get('image', False):
        image = request.FILES['image']
        slide.image = image
    slide.save()

    return HttpResponse('exiting save_slide view')


@user_passes_test(employee_check)
def save_highlight(request):
    print(request.POST)
    print(request.FILES)
    highlight_text_data = json.loads(request.POST['highlight_data'])
    tmp_id = highlight_text_data['id']
    highlight = MainPageHighlight.objects.get(id=tmp_id)
    highlight.text = highlight_text_data['text']
    if request.FILES.get('image', False):
        image = request.FILES['image']
        highlight.image = image
    highlight.save()

    return HttpResponse('exiting save_slide view')


@user_passes_test(employee_check)
def save_warning(request):
    print(request)
    print(request.body)
    warning_data = json.loads(request.body)
    warning = MainPageWarning.objects.get(id=1)
    warning.text = warning_data['text']
    warning.show_warning = warning_data['shown']
    warning.save()
    return HttpResponse('exiting save_warning view')


@user_passes_test(employee_check)
def execute_delete(request):
    data = json.loads(request.body)
    print(data)
    # if/else for slide or highlight, include JSON response of updated object list
    if data['type'] == 'slide':
        slide = CarouselSlide.objects.get(id=data['id'])
        slide.delete()
        return get_carousele(request)
    else:
        highlight = MainPageHighlight.objects.get(id=data['id'])
        highlight.delete()
        return highlights(request)
    return HttpResponse('exiting execute_delete with no changes')


@user_passes_test(employee_check)
def save_new_highlight(request):
    data = request.POST
    print(data)
    text = data['text']
    new_highlight = MainPageHighlight(text=text, image=request.FILES['image'])
    new_highlight.save()
    return highlights(request)

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
