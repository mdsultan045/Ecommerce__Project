from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from . import views
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'users', views.serializerview)

urlpatterns = [
    path('', views.index, name="home"),
    path('contact', views.contact, name="contact"),
    path('signup', views.SignUp, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('cart', views.cart_info, name="cartdtls"),
    path('checkout', views.checkout, name="checkout"),
    path('order', views.Order_Dtls, name="order"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
