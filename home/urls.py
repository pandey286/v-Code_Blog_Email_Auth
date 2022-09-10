from re import search
from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
   path('',views.home, name='home'),
   path('contact', views.contact, name='home'),
   path('about', views.about, name='about'),
   path('search', views.search, name='search'),
   path('signup', views.handleSignup, name='handleSignup'),
   path('login', views.handleLogin, name='handleLogin'),
   path('rnpassword', views.handlernpassword, name='handlernpassword'),
   path('logout', views.handleLogout, name='handleLogout')
]
