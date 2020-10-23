from django.urls import path
from . import views
from django.conf import settings

app_name = 'mirmir_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('main/', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('mead_club/', views.club, name='club'),
    path('archive/', views.archive, name='archive'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('employee_main/', views.employee_main, name='employee_main'),
    path('main_page_management/', views.main_page_management,
         name='main_page_management'),
    path('highlights/', views.highlights, name='highlights'),
    path('get_warning/', views.get_warning, name='get_warning'),
    path('get_carousele/', views.get_carousele, name='get_carousele'),
    path('save_slide/', views.save_slide, name='save_slide'),
    path('save_highlight/', views.save_highlight, name='save_highlight'),
    path('save_warning/', views.save_warning, name='save_warning'),
    path('add_new_slide/', views.add_new_slide, name='add_new_slide'),
    path('execute_delete/', views.execute_delete, name='execute_delete'),
    path('save_new_highlight/', views.save_new_highlight,
         name='save_new_highlight'),
    path('profile/', views.profile, name='profile'),
    path('shop/', views.shop, name='shop'),
    path('shop_get_product_data/', views.shop_get_product_data,
         name='shop_get_product_data'),
    path('checkout/', views.checkout, name='checkout'),
]
