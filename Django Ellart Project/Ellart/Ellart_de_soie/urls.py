"""
URL configuration for Ellart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Ellart_de_soie import views
from Ellart import settings
from django.conf.urls.static import static

admin.site.site_header = "Ellart de Soie"
admin.site.site_title = "Ellart de Soie Admin Portal"
admin.site.index_title = "Welcome to Ellart de Soie Portal"

urlpatterns = [
    path('', views.Home, name='home'),
    path('about/', views.Aboutus, name='about'),
    path('baby/', views.Baby_Store, name='baby_store'),
    path('hair/', views.Hair_Shop, name='hair_shop'),
    # path('login/', views.Login_page, name='login'),
    path('perfumes/', views.Perfumes, name='perfumes'),
    path('mens/', views.Men_Store, name='men_store'),
    # path('register/', views.Register_Page, name='register'),
    path('skin/', views.Skin, name='skin_care'),
    path('women/', views.Women_Store, name='women_store'),
    path('cart/', views.Cart_Page, name='cart'),
    path('pdetails/<int:product_id>/', views.Product_Details, name='product_details'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('products/', views.product_list, name='product_list'),  # List view with filtering, sorting, and searching
    path('sort/<sv>/', views.sort, name='sort'),
    path('cart/', views.Cart_Page, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase-quantity/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('create-order/', views.create_order, name='create_order'),
    path('payment/verify/', views.payment_verify, name='payment_verify'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/<str:order_id>/', views.order_success, name='order_success'),
    path('forgot_password/', views.forgot_password, name='forgot_password'), 
    path('enterotp/', views.enter_otp, name='enter_otp'), 
    path('resetpassword/', views.reset_password, name='reset_password'),
    path('Register/', views.register),
    path('login/', views.user_login, name='login'),
    path('CashOnDelivery/', views.CashOnDelivery, name='CashOnDelivery'),
\

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

