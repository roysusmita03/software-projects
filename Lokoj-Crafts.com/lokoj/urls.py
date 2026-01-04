"""
URL configuration for lokoj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from shop import views
from django.conf.urls.static import static
from django.conf import settings  # এই লাইনটি যোগ করুন
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.SignUpPage, name='SignUpPage'),  # Signup Page as the default page
    path('login/', views.LoginPage, name='LoginPage'),  # Login Page
    path('home/', views.index, name='index'),  # Home Page
    path('product/<int:id>/', views.productdetail, name='product detail'),
    path('history/', views.historyofhandicrafts, name='history'),
    path('logout/', views.logout_view, name='logout_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart-count/', views.cart_count, name='cart_count'),
    path('cart/', views.cart, name='cart'),
    path('payment/', views.payment, name='payment'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    #path('artisan/<int:artisan_id>/', views.artisan_detail, name='artisan_detail'),
    path('artisan/<int:artisan_id>/', views.artisan_detail, name='artisan_detail'),
    path('rate-artisan/', views.rate_artisan, name='rate_artisan'),
    path('rate-artisan/', views.rate_artisan, name='rate_artisan'),
    path('about/', views.aboutus, name='aboutus'),

    #path('artisan/<int:artisan_id>/', views.artisan_detail, name='artisan_detail'),
    #path('artisans/', views.artisan_list, name='artisan_list'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
