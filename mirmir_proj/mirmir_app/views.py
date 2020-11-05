from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth
from django.core import serializers
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import StatusField, SortField, Contact, Product, CarouselSlide, MainPageWarning, MainPageHighlight, Order, OrderType, PaymentStatus, OrderItemQuantity, ShippingStatus, ProductPhoto, TransactionType, EmailConfirmation
import requests
import random
import django.contrib.auth
from django.views.generic import CreateView
from .forms import ContactForm
from . import utilities
import json
import re
import string
from datetime import datetime

####################################
#         Employee Views           #
####################################


def employee_check(user):
    return user.profile.status.status == 'employee'


@user_passes_test(employee_check)
def send_email(request):
    data = json.loads(request.body)
    print(data)
    status_id = data['email_select_by_status']
    contacts = Contact.objects.filter(status=status_id)
    email_addresses = []
    for contact in contacts:
        email_addresses.append(contact.email)
    email_text = data['email_text']
    body = render_to_string(
        'mirmir_app/employee_email.html', {'email_text': email_text})
    send_mail('News From Mirmir', '', settings.EMAIL_HOST_USER,
              email_addresses, fail_silently=False, html_message=body)
    return JsonResponse({'blank_text': ''})


@user_passes_test(employee_check)
def send_customer_email(request):
    data = json.loads(request.body)
    print(data)
    email_address = data['email_address']
    email_text = data['email_text']
    body = render_to_string(
        'mirmir_app/employee_email.html', {'email_text': email_text})
    send_mail('News About Your Order', '', settings.EMAIL_HOST_USER,
              [email_address], fail_silently=False, html_message=body)
    return JsonResponse({'blank_text': ''})


@user_passes_test(employee_check)
def save_photo(request):
    data = request.POST
    print(data)
    product = Product.objects.get(id=request.POST['product_id'])
    new_num = product.product_photos.count() + 1
    new_photo = ProductPhoto(
        photo=request.FILES['image'], photo_image_number=new_num, product=product)
    new_photo.save()
    return HttpResponse('image saved')


@user_passes_test(employee_check)
def save_product_changes(request):
    product_update = json.loads(request.body)['product']
    type_of_update = json.loads(request.body)['type']
    photo_remove_instructions = json.loads(
        request.body)['photo_remove_instructions']
    if type_of_update == 'update':
        # print(product_update)
        product = Product.objects.get(id=product_update['id'])
        print(product)
        product.title = product_update['title']
        product.subtitle = product_update['subtitle']
        product.action_message = product_update['action_message']
        product.is_active = product_update['is_active']
        product.is_display_on_website = product_update['is_display_on_website']
        product.description = product_update['description']
        product.description_teaser = product_update['description_teaser']
        product.SKU_unit_description = product_update['SKU_unit_description']
        product.SKU_min_order_qty = product_update['SKU_min_order_qty']
        product.SKU_max_order_qty = product_update['SKU_max_order_qty']
        product.SKU_order_in_multiples_of = product_update['SKU_order_in_multiples_of']
        product.SKU_is_non_taxable = product_update['SKU_is_non_taxable']
        product.SKU_is_no_shipping_charge = product_update['SKU_is_no_shipping_charge']
        product.SKU_Prices_price_level = product_update['SKU_Prices_price_level']
        product.SKU_Prices_price = product_update['SKU_Prices_price']
        product.SKU_Prices_price_quantity = product_update['SKU_Prices_price_quantity']
        product.SKU_Prices_is_inventory_on = product_update['SKU_Prices_is_inventory_on']
        product.SKU_Prices_Inventory_current_inventory = product_update[
            'SKU_Prices_Inventory_current_inventory']
        product.SKU_Prices_Inventory_inventory_pool = product_update[
            'SKU_Prices_Inventory_inventory_pool']
        product.WineProperties_tasting_notes = product_update['WineProperties_tasting_notes']
        product.WineProperties_wine_maker_notes = product_update['WineProperties_wine_maker_notes']
        product.WineProperties_food_pairing_notes = product_update[
            'WineProperties_food_pairing_notes']
        for photo_id in photo_remove_instructions:
            tmp_photo = ProductPhoto.objects.get(id=photo_id)
            tmp_photo.delete()
        product.save()
        return HttpResponse(product_update['id'])

    elif type_of_update == 'new':
        print(product_update)
        # bottling_date = re.split('/', product_update['bottling_date'])
        # final_bottling_date = bottling_date[2] + '-' + \
        #     bottling_date[0] + '-' + bottling_date[1]
        new_product = Product(
            product_type=product_update['product_type'],
            title=product_update['title'],
            POSTitle=product_update['POSTitle'],
            brand=product_update['brand'],
            subtitle=product_update['subtitle'],
            action_message=product_update['action_message'],
            is_active=product_update['is_active'],
            is_display_on_website=product_update['is_display_on_website'],
            description=product_update['description'],
            description_teaser=product_update['description_teaser'],
            SKU_SKU=product_update['SKU_SKU'],
            SKU_cost_of_good=product_update['SKU_cost_of_good'],
            SKU_UPC_code=product_update['SKU_UPC_code'],
            SKU_unit_description=product_update['SKU_unit_description'],
            SKU_min_order_qty=product_update['SKU_min_order_qty'],
            SKU_max_order_qty=product_update['SKU_max_order_qty'],
            SKU_order_in_multiples_of=product_update['SKU_order_in_multiples_of'],
            SKU_weight=product_update['SKU_weight'],
            SKU_is_non_taxable=product_update['SKU_is_non_taxable'],
            SKU_is_no_shipping_charge=product_update['SKU_is_no_shipping_charge'],
            SKU_Prices_price_level=product_update['SKU_Prices_price_level'],
            SKU_Prices_price=product_update['SKU_Prices_price'],
            SKU_Prices_price_quantity=product_update['SKU_Prices_price_quantity'],
            SKU_Prices_is_inventory_on=product_update['SKU_Prices_is_inventory_on'],
            SKU_Prices_Inventory_current_inventory=product_update[
                'SKU_Prices_Inventory_current_inventory'],
            SKU_Prices_Inventory_inventory_pool=product_update['SKU_Prices_Inventory_inventory_pool'],
            WineProperties_bottles_in_case=product_update['WineProperties_bottles_in_case'],
            WineProperties_bottle_size_in_ml=product_update['WineProperties_bottle_size_in_ml'],
            WineProperties_type=product_update['WineProperties_type'],
            WineProperties_alcohol=product_update['WineProperties_alcohol'],
            WineProperties_bottling_date=product_update['WineProperties_bottling_date'],
            WineProperties_tasting_notes=product_update['WineProperties_tasting_notes'],
            WineProperties_wine_maker_notes=product_update['WineProperties_wine_maker_notes'],
            WineProperties_food_pairing_notes=product_update['WineProperties_food_pairing_notes']
        )
        new_product.save()
        return HttpResponse(new_product.id)
    else:
        return HttpResponse('error')

    product.save()
    return HttpResponse('Ok')


@user_passes_test(employee_check)
def get_active_products(request):
    data = Product.get_active_products()
    return JsonResponse({'data': data})


@user_passes_test(employee_check)
def get_next_order_number_employee(request):
    return HttpResponse(Order.objects.count() + 1)


@user_passes_test(employee_check)
def save_order_changes(request):
    # print(request.body)
    order_update = json.loads(request.body)['order']
    type_of_update = json.loads(request.body)['type']
    print(order_update)
    # order object update
    if type_of_update == 'update':
        print(order_update['order_number'])
        order = Order.objects.get(order_number=order_update['order_number'])
        order.order_type = OrderType.objects.get(id=order_update['order_type'])
        order.shipping_status = ShippingStatus.objects.get(
            id=order_update['shipping_status'])
        order.billing_first_name = order_update['billing_first_name']
        order.billing_last_name = order_update['billing_last_name']
        order.billing_address = order_update['billing_address']
        order.billing_address2 = order_update['billing_address2']
        order.billing_city = order_update['billing_city']
        order.billing_state_code = order_update['billing_state_code']
        order.billing_zip_code = order_update['billing_zip_code']
        order.billing_email = order_update['billing_email']
        order.sub_total = order_update['sub_total']
        order.is_pickup = order_update['is_pickup']
        order.payment_status = PaymentStatus.objects.get(
            id=order_update['payment_status'])
        order.shipping_first_name = order_update['shipping_first_name']
        order.shipping_last_name = order_update['shipping_last_name']
        order.shipping_address = order_update['shipping_address']
        order.shipping_address2 = order_update['shipping_address2']
        order.shipping_city = order_update['shipping_city']
        order.shipping_state_code = order_update['shipping_state_code']
        order.shipping_zip_code = order_update['shipping_zip_code']
        order.transaction_type = TransactionType.objects.get(
            id=order_update['transaction_type'])
        order.total = order_update['total']
        order.previous_order_number = order_update['previous_order_number']
    elif type_of_update == 'new':
        order = Order(
            order_type=OrderType.objects.get(
                id=order_update['order_type']),
            order_number=order_update['order_number'],
            shipping_status=ShippingStatus.objects.get(
                id=order_update['shipping_status']),
            billing_first_name=order_update['billing_first_name'],
            billing_last_name=order_update['billing_last_name'],
            billing_address=order_update['billing_address'],
            billing_address2=order_update['billing_address2'],
            billing_city=order_update['billing_city'],
            billing_state_code=order_update['billing_state_code'],
            billing_zip_code=order_update['billing_zip_code'],
            billing_email=order_update['billing_email'],
            sub_total=order_update['sub_total'],
            is_pickup=order_update['is_pickup'],
            payment_status=PaymentStatus.objects.get(
                id=order_update['payment_status']),
            shipping_first_name=order_update['shipping_first_name'],
            shipping_last_name=order_update['shipping_last_name'],
            shipping_address=order_update['shipping_address'],
            shipping_address2=order_update['shipping_address2'],
            shipping_city=order_update['shipping_city'],
            shipping_state_code=order_update['shipping_state_code'],
            shipping_zip_code=order_update['shipping_zip_code'],
            transaction_type=TransactionType.objects.get(
                id=order_update['transaction_type']),
            total=order_update['total'],
            previous_order_number=order_update['previous_order_number'],
        )
    else:
        return HttpResponse('Failure')
    order.save()

    return HttpResponse('Ok')


def justify_carousel_ordering():
    slides = CarouselSlide.objects.all()
    i = 1
    for slide in slides:
        slide.display_order = i
        i += 1


@user_passes_test(employee_check)
def get_open_orders(request):
    # data = serializers.serialize('xml', SomeModel.objects.all(), fields=('name','size'))
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


def verified_account(user):
    return user.is_authenticated and user.profile.email_address_confirmed


def index(request):
    context = {
        'message': 'Hello, world!',
    }
    return render(request, 'mirmir_app/index.html', context)


def main(request):
    print(request.user)
    if request.user.username == 'admin':
        return HttpResponseRedirect(reverse('mirmir_app:logout'))
    if request.user.is_authenticated:
        print(request.user.profile.status)
        if request.user.profile.status.status == 'employee':
            return HttpResponseRedirect(reverse('mirmir_app:employee_main'))
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
    if request.method == 'GET':
        context = {

        }
        if request.user.is_authenticated:
            context['is_club_member'] = (
                request.user.profile.status.status == 'club_member')
        print(context)
        return render(request, 'mirmir_app/club.html', context)
    else:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('mirmir_app:login'))
        profile = request.user.profile
        print(request.POST)
        if 'opt_in' in request.POST:
            profile.status = StatusField.objects.get(status='club_member')
        else:
            profile.status = StatusField.objects.get(status='purchaser')
        profile.save()
        return HttpResponseRedirect(reverse('mirmir_app:profile'))


def archive(request):
    context = {

    }
    return render(request, 'mirmir_app/archive.html', context)


def random_code(n):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(n)])


@login_required
def email_sent(request):
    return render(request, 'mirmir_app/email_sent.html')


@login_required
def send_new_code(request):
    # verification = request.user.profile.email_confirmations.objects.all()
    # print(verification)
    # if verification is not None:
    #     verification.delete()
    email_confirmation = EmailConfirmation(
        contact=request.user.profile, code=random_code(10))
    email_confirmation.save()
    body = render_to_string('mirmir_app/email.html', {
        'code': email_confirmation.code, 'domain': 'http://' + request.META['HTTP_HOST']})
    send_mail('Confirm Your Account', '', settings.EMAIL_HOST_USER, [
        request.user.profile.email], fail_silently=False, html_message=body)
    return HttpResponseRedirect(reverse('mirmir_app:email_sent'))


@login_required
def confirm(request):
    code = request.GET.get('code', '')
    if code == '':
        return render(request, 'mirmir_app/profile.html', {})
    email_confirmation = EmailConfirmation.objects.get(code=code)
    print(email_confirmation)
    if email_confirmation is not None:
        email_confirmation.date_confirmed = timezone.now()
        email_confirmation.save()
        contact = email_confirmation.contact
        contact.email_address_confirmed = True
        contact.save()
    return HttpResponseRedirect(reverse('mirmir_app:profile'))


@login_required
def logged_in_password_reset(request):
    email_address = [request.user.profile.email]
    email_confirmation = EmailConfirmation(
        contact=request.user.profile, code=random_code(10))
    email_confirmation.save()
    body = render_to_string('mirmir_app/email_password_reset.html', {
        'code': email_confirmation.code, 'domain': 'http://' + request.META['HTTP_HOST'], 'username': request.user.username})
    send_mail('Change Password Link', '', settings.EMAIL_HOST_USER,
              email_address, fail_silently=False, html_message=body)
    return JsonResponse({'message': 'okay'})


def reset_password_request(request):
    if request.method == 'GET':
        context = {
            'is_there_a_message': False,
            'site_key': settings.RECAPTCHA_SITE_KEY,
        }
        return render(request, 'mirmir_app/reset_password_request.html', context)
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
        if not result_json['success']:
            context = {
                'site_key': settings.RECAPTCHA_SITE_KEY,
                'there_is_a_message': True,
                'message': 'reCAPTCHA v3 unsuccessful'
            }
            return render(request, 'mirmir_app/reset_password_request.html', context)
        if result_json['score'] > 0.5:
            account = None
            if request.POST['username'] != '':
                account = Contact.objects.filter(
                    username__username=request.POST['username']).first()
            elif request.POST['email'] != '' and account is not None:
                account = Contact.objects.filter(
                    email=request.POST['email']).first()
            if account:
                email_address = [account.email]
                email_confirmation = EmailConfirmation(
                    contact=account, code=random_code(10))
                email_confirmation.save()
                body = render_to_string('mirmir_app/email_password_reset.html', {
                    'code': email_confirmation.code, 'domain': 'http://' + request.META['HTTP_HOST'], 'username': account.username.username})
                send_mail('Change Password Link', '', settings.EMAIL_HOST_USER,
                          email_address, fail_silently=False, html_message=body)
                context = {
                    'site_key': settings.RECAPTCHA_SITE_KEY,
                    'there_is_a_message': True,
                    'message': 'Email Sent Successfully'
                }
                return render(request, 'mirmir_app/reset_password_request.html', context)
            else:
                context = {
                    'site_key': settings.RECAPTCHA_SITE_KEY,
                    'there_is_a_message': True,
                    'message': 'Account Not Found'
                }
                return render(request, 'mirmir_app/reset_password_request.html', context)


def change_password(request):
    if request.method == 'GET':
        code = request.GET.get('code', '')
        if code == '':
            return render(request, 'mirmir_app/profile.html', {})
        email_confirmation = EmailConfirmation.objects.get(code=code)
        print(email_confirmation)
        if email_confirmation is not None:
            email_confirmation.date_confirmed = timezone.now()
            email_confirmation.save()
            context = {
                'code': code,
                'site_key': settings.RECAPTCHA_SITE_KEY,
                'is_there_a_message': False,
            }
            return render(request, 'mirmir_app/change_password.html', context)
        else:
            return HttpResponseRedirect(reverse('mirmir_app:reset_password_request'))
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
        code = request.POST['code']
        if not result_json['success']:
            context = {
                'code': code,
                'site_key': settings.RECAPTCHA_SITE_KEY,
                'there_is_a_message': True,
                'message': 'reCAPTCHA v3 unsuccessful'
            }
            return render(request, 'mirmir_app/change_password.html', context)
        if result_json['score'] > 0.5:
            ################################################
            # user login logic here
            password = request.POST['password']
            password_v = request.POST['password_v']
            if password != password_v:
                context = {
                    'code': code,
                    'site_key': settings.RECAPTCHA_SITE_KEY,
                    'there_is_a_message': True,
                    'message': 'Passwords do not match, please try again.'
                }
                return render(request, 'mirmir_app/change_password.html', context)
            else:
                email_confirmation = EmailConfirmation.objects.filter(
                    code=code).first()
                if email_confirmation is not None and email_confirmation.date_confirmed is not None:
                    user = email_confirmation.contact.username
                    user.set_password(password)
                    user.save()
                    django.contrib.auth.login(request, user)
                    return HttpResponseRedirect(reverse('mirmir_app:profile'))
                else:
                    context = {
                        'code': code,
                        'site_key': settings.RECAPTCHA_SITE_KEY,
                        'there_is_a_message': True,
                        'message': 'A database error occurred, contact an administrator.'
                    }
                    return render(request, 'mirmir_app/change_password.html', context)


def register(request):
    if request.method == 'GET':
        form = ContactForm()
        context = {
            'form': form,
            'site_key': settings.RECAPTCHA_SITE_KEY,
            'is_there_a_message': False,
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
        if not result_json['success']:
            context = {
                'site_key': settings.RECAPTCHA_SITE_KEY,
                'there_is_a_message': True,
                'message': 'reCAPTCHA v3 unsuccessful'
            }
            return render(request, 'mirmir_app/register.html', context)
        if result_json['score'] > 0.5:
            ################################################
            # user login logic here
            username = request.POST['username']
            if User.objects.filter(username=username).exists():
                form = ContactForm()
                context = {
                    'form': form,
                    'site_key': settings.RECAPTCHA_SITE_KEY,
                    'is_there_a_message': True,
                    'message': 'Username already exists, please choose another username.',
                }
                return render(request, 'mirmir_app/register.html', context)
            password = request.POST['password']
            password_v = request.POST['password_v']
            if password != password_v:
                context = {
                    'site_key': settings.RECAPTCHA_SITE_KEY,
                    'there_is_a_message': True,
                    'message': 'Passwords do not match, please try again.'
                }
                return render(request, 'mirmir_app/register.html', context)
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
            email_confirmation = EmailConfirmation(
                contact=new_contact, code=random_code(10))
            email_confirmation.save()
            body = render_to_string('mirmir_app/email.html', {
                                    'code': email_confirmation.code, 'domain': 'http://' + request.META['HTTP_HOST']})
            send_mail('Confirm Your Account', '', settings.EMAIL_HOST_USER, [
                      new_contact.email], fail_silently=False, html_message=body)
            django.contrib.auth.login(request, user)
            # django.contrib.auth.login(request, user)
            next = request.GET.get('next', reverse('mirmir_app:profile'))
            return HttpResponseRedirect(next)
        else:
            context = {
                'site_key': settings.RECAPTCHA_SITE_KEY,
                'there_is_a_message': True,
                'message': 'reCAPTCHA v3 suspect, please try again.'
            }
            return render(request, 'mirmir_app/register.html', context)


@login_required
def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(reverse('mirmir_app:main'))


def login(request):
    if request.method == 'GET':
        context = {
            'site_key': settings.RECAPTCHA_SITE_KEY,
            'is_there_a_message': False,
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
        # captcha logic
        if not result_json['success']:
            context = {
                'site_key': settings.RECAPTCHA_SITE_KEY,
                'there_is_a_message': True,
                'message': 'reCAPTCHA v3 unsuccessful'
            }
            return render(request, 'mirmir_app/login.html', context)

        ################################################
        # user login logic here
        username = request.POST['username']
        password = request.POST['password']
        user = django.contrib.auth.authenticate(
            request, username=username, password=password)
        # print(user.profile.status)
        if user is None:
            context = {
                'site_key': settings.RECAPTCHA_SITE_KEY,
                'there_is_a_message': True,
                'message': 'Incorrect username or password, please try again or reset your password.'
            }
            return render(request, 'mirmir_app/login.html', context)
        elif user.profile.status.status == 'employee':
            context = {

            }
            django.contrib.auth.login(request, user)
            next = request.GET.get('next', reverse('mirmir_app:employee_main'))
            return HttpResponseRedirect(next)
        else:
            ###########################################
            # captcha logic
            # test score <=5
            # result_json['score'] = 0.1
            if result_json['score'] <= 0.5:
                context = {
                    'site_key': settings.RECAPTCHA_SITE_KEY,
                    'there_is_a_message': True,
                    'message': 'Are you a robot? Please check your registered email for link.'
                }
                email_address = [user.profile.email]
                email_confirmation = EmailConfirmation(
                    contact=user.profile, code=random_code(10))
                email_confirmation.save()
                body = render_to_string('mirmir_app/two_fa.html', {
                    'code': email_confirmation.code, 'domain': 'http://' + request.META['HTTP_HOST']})
                send_mail('Confirm Your Account', '', settings.EMAIL_HOST_USER,
                          email_address, fail_silently=False, html_message=body)
                return render(request, 'mirmir_app/login.html', context)
            #########################################
            # All tests passed, login user and go on
            django.contrib.auth.login(request, user)
            next = request.GET.get('next', reverse('mirmir_app:main'))
            return HttpResponseRedirect(next)


def confirm_login(request):
    code = request.GET.get('code', '')
    if code == '':
        context = {
            'site_key': settings.RECAPTCHA_SITE_KEY,
            'there_is_a_message': True,
            'message': 'Incorrect code, please try to login again.'
        }
        return render(request, 'mirmir_app/login.html', context)
    email_confirmation = EmailConfirmation.objects.get(code=code)
    # print(email_confirmation)
    if email_confirmation is not None:
        email_confirmation.date_confirmed = timezone.now()
        email_confirmation.save()
        contact = email_confirmation.contact
        django.contrib.auth.login(request, contact.username)
    return HttpResponseRedirect(reverse('mirmir_app:profile'))


@login_required
def profile(request):
    if request.method == 'GET':
        form = ContactForm(instance=request.user.profile)
        orders = request.user.profile.orders.all()
        num_items = []
        context = {
            'form': form,
            'status': request.user.profile.status.pretty_status,
            'email': request.user.profile.email,
            'confirmed': False
        }
        if request.user.profile.email_address_confirmed:
            context['confirmed'] = True
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
        ################################################
        # user login logic here
        form = ContactForm(request.POST, request.FILES,
                           instance=request.user.profile)
        if form.is_valid():
            form.save()
        print(request.POST)
        profile = request.user.profile
        if 'opt_in' in request.POST:
            print('found opt-in')
            profile.status = StatusField.objects.get(
                status='subscriber')
        else:
            print('no opt-in')
            if profile.status.status == 'subscriber':
                print('user is subscriber')
                profile.status = StatusField.objects.get(
                    status='purchaser')
        profile.save()
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


@login_required
def shop(request):
    products = Product.objects.filter(is_display_on_website=True)
    print(products)
    context = {
        'products': products
    }
    return render(request, 'mirmir_app/shop.html', context)


@login_required
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
            'in_stock': (product.SKU_Prices_Inventory_current_inventory > 0),
            'cost': product.SKU_Prices_price,
            'photos': photos,
            'wine_properties': {
                'size': product.WineProperties_bottle_size_in_ml,
                'alcohol': product.WineProperties_alcohol,
                'pairing': product.WineProperties_food_pairing_notes,
                'tasting': product.WineProperties_tasting_notes
            },
            'inventory': product.SKU_Prices_Inventory_current_inventory
        })
    return JsonResponse({'product_data': data})


@user_passes_test(verified_account)
def checkout(request):
    context = {
        'site_key': settings.RECAPTCHA_SITE_KEY,
    }
    return render(request, 'mirmir_app/checkout.html', context)


@user_passes_test(verified_account)
def get_user_data_for_checkout(request):
    user = request.user.profile
    print('company ' + user.company)
    output = {
        'billing': {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'company': user.company,
            'city': user.city,
            'state': user.state_code,
            'zip_code': user.zip_code,
            'email': user.email,
            'birthday': user.birthday.strftime('%m/%d/%Y')
        }
    }
    return JsonResponse(output)


@user_passes_test(verified_account)
def cart_verification(request):
    context = {
        'site_key': settings.RECAPTCHA_SITE_KEY,
    }
    return render(request, 'mirmir_app/cart_verification.html', context)


@user_passes_test(verified_account)
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
    print('order_shipping_company: ' + order.shipping_company)
    print('order_billing_company' + order.billing_company)
    order.save()
    # make OrderItemQuantity's for each product
    num_items = 0
    cart = data['cart']
    print('Items in cart:')
    for item in cart:
        print(item['title'])
        product = Product.objects.get(id=item['id'])
        quantity = int(item['num'])
        num_items += quantity
        new_item_quantity = OrderItemQuantity(
            quantity=quantity, product=product, order=order)
        if product.SKU_Prices_Inventory_current_inventory - quantity < 0:
            order.delete()
            return HttpResponse('inventory_error')
        product.SKU_Prices_Inventory_current_inventory -= quantity
        product.save()
        new_item_quantity.save()
        print('Product Quantity: ' + str(quantity))
        print('Product Price: ' + str(product.SKU_Prices_price))
        print('Current sub total: ' + str(order.sub_total))
    order.total = order.sub_total * \
        (1 + (order.tax / 100)) + order.shipping + order.handling
    order.save()
    # send email receipt
    email_order = {
        'billing_email': order.billing_email,
        'billing_first_name': order.billing_first_name,
        'billing_last_name': order.billing_last_name,
        'order_number': order.order_number,
        'order_date': order.order_date.strftime('%m/%d/%Y'),
        'shipping_first_name': order.shipping_first_name,
        'shipping_last_name ': order.shipping_last_name,
        'shipping_address': order.shipping_address,
        'shipping_address2': order.shipping_address2,
        'shipping_city': order.shipping_city,
        'shipping_state': order.shipping_state_code,
        'total': order.total,
    }
    num_items
    body = render_to_string(
        'mirmir_app/email_receipt.html', {'order': email_order, 'num_items': num_items})
    send_mail('Order Receipt ' + str(order.order_number), '', settings.EMAIL_HOST_USER,
              [order.billing_email], fail_silently=False, html_message=body)
    print('Order total: ' + str(order.total))
    return HttpResponse('Order Complete')
