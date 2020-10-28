from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth
from django.core import serializers
from .models import StatusField, SortField, Contact, Product, CarouselSlide, MainPageWarning, MainPageHighlight, Order, OrderType, PaymentStatus, OrderItemQuantity, ShippingStatus, TransactionType
import requests
import random
import django.contrib.auth
from django.views.generic import CreateView
from .forms import ContactForm
from . import utilities
import json
import re


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
def get_open_orders(request):
    #data = serializers.serialize('xml', SomeModel.objects.all(), fields=('name','size'))
    data = Order.get_open_orders()
    return JsonResponse({'data': data})


@user_passes_test(employee_check)
def employee_main(request):
    print(request)
    context = {
        'open_orders': Order.get_open_orders(),
        'shipping_statuses': ShippingStatus.get_shipping_statuses(),
        'order_types': OrderType.get_order_types(),
        'transaction_types': TransactionType.get_transaction_types(),
        'payment_statuses': PaymentStatus.get_payment_statuses(),
    }
    return render(request, 'mirmir_app/employee_main.html', context)


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


@login_required
def profile(request):
    if request.method == 'GET':
        form = ContactForm(instance=request.user.profile)
        orders = request.user.profile.orders.all()
        num_items = []
        context = {
            'form': form,
            'site_key': settings.RECAPTCHA_SITE_KEY,
        }

        # only if user has order history
        if orders:
            for order in orders:
                item_quantities = order.items.all()
                total = 0
                for tup in item_quantities:
                    total += tup.quantity
                num_items.append(total)
            context['orders'] = orders
            context['num_items'] = num_items

        return render(request, 'mirmir_app/profile.html', context)
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
        form = ContactForm(request.POST, request.FILES,
                           instance=request.user.profile)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('mirmir_app:main'))


@login_required
def order_details(request, order_num):
    order = Order.objects.get(order_number=order_num)
    items = order.items.all()
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'mirmir_app/order_details.html', context)

##########################################################
#                       shop views                       #
##########################################################


def shop(request):
    products = Product.objects.filter(is_display_on_website=True)
    print(products)
    context = {
        'products': products
    }
    return render(request, 'mirmir_app/shop.html', context)


def shop_get_product_data(request):
    products = Product.objects.filter(is_display_on_website=True)
    data = []
    for product in products:
        photos = []
        for photo in product.product_photos.all():
            photos.append({
                'display_order': photo.photo_image_number,
                'photo': photo.photo.url
            })
        data.append({
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'teaser': product.description_teaser,
            'date_added': product.date_added,
            'cost': product.SKU_cost_of_good,
            'photos': photos,
            'wine_properties': {
                'size': product.WineProperties_bottle_size_in_ml,
                'alcohol': product.WineProperties_alcohol,
                'pairing': product.WineProperties_food_pairing_notes,
                'tasting': product.WineProperties_tasting_notes
            }
        })
    return JsonResponse({'product_data': data})


def checkout(request):
    context = {
        'site_key': settings.RECAPTCHA_SITE_KEY,
    }
    return render(request, 'mirmir_app/checkout.html', context)


def cart_verification(request):
    context = {
        'site_key': settings.RECAPTCHA_SITE_KEY,
    }
    return render(request, 'mirmir_app/cart_verification.html', context)


def upsert_order(request):
    data = json.loads(request.body)
    print(data)
    # big make for Order
    billing = data['order']['billing']
    shipping = data['order']['shipping']
    # print(billing)
    birthday = billing['birthday']
    birthday = re.split('/', birthday)
    final_birthday = birthday[2] + '-' + birthday[0] + '-' + birthday[1]
    # print(final_birthday)
    ###########################################
    #          get Contact logic here         #
    ###########################################
    order_number = Order.objects.count() + 1
    order = Order(
        order_type=OrderType.objects.get(type_string="website"),
        order_number=order_number,
        shipping_status=ShippingStatus.objects.get(status="no_status"),
        billing_birthdate=final_birthday,
        billing_first_name=billing['first_name'],
        billing_last_name=billing['last_name'],
        billing_company=billing['company'],
        billing_address=billing['address'],
        billing_address2=billing['address2'],
        billing_city=billing['city'],
        billing_state_code=billing['state'],
        billing_zip_code=int(billing['zip_code']),
        billing_email=billing['email'],
        sub_total=data['total'],
        is_pickup=True,
        payment_status=PaymentStatus.objects.get(status='pending'),
        shipping_birthdate=final_birthday,
        shipping_first_name=billing['first_name'],
        shipping_last_name=billing['last_name'],
        shipping_company=billing['company'],
        shipping_address=billing['address'],
        shipping_address2=billing['address2'],
        shipping_city=billing['city'],
        shipping_state_code=billing['state'],
        shipping_zip_code=int(billing['zip_code']),
        transaction_type=TransactionType.objects.get(t_type='order'),
        previous_order_number=0,
    )
    if data['is_gift']:
        birthday = shipping['birthday']
        birthday = re.split('/', birthday)
        final_birthday = birthday[2] + '-' + birthday[0] + '-' + birthday[1]
        order.shipping_first_name = shipping['first_name']
        order.shipping_last_name = shipping['last_name']
        order.shipping_company = shipping['company']
        order.shipping_address = shipping['address']
        order.shipping_address2 = shipping['address2']
        order.shipping_city = shipping['city']
        order.shipping_state_code = shipping['state']
        order.shipping_zip_code = int(shipping['zip_code'])
        order.shipping_birthdate = final_birthday
        order.gift_message = data['order']['gift_message']
    if request.user.is_authenticated:
        contact = request.user.profile
        order.contact = contact
    order.save()
    # make OrderItemQuantity's for each product
    cart = data['cart']
    print('Items in cart:')
    for item in cart:
        print(item['title'])
        product = Product.objects.get(id=item['id'])
        quantity = item['num']
        new_item_quantity = OrderItemQuantity(
            quantity=quantity, product=product, order=order)
        new_item_quantity.save()
    return HttpResponse('Order Complete')
