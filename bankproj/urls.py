from django.contrib import admin
from django.urls import path
from bankapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup',views.signup,name='signup'),
    path('userlogin',views.userlogin,name='userlogin'),
    path('home',views.home,name='home'),
    path('details',views.details,name='details'),
    path('deposit',views.deposit,name='deposit'),
    path('withdrawal',views.withdrawal,name='withdrawal'),
    path('userlogout',views.userlogout,name='userlogout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)