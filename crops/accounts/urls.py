from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns =[
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("crop_recommendation",views.crop_recommendation,name="crop_recommendation"),
    path('activate/<uidb64>/<token>',
         views.save_user, name='activate'),
]