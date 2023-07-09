from django.urls import path
from . import views 


urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('search/', views.search, name='search'),
    path('laptop/', views.laptop, name='laptop'),
    path('mobile/', views.mobile, name='mobile'),
    path('smart_watch/', views.smart_watch, name='smart_watch'),
    path('washing_machine/', views.washing_machine, name='washing_machine'),
    path('tablet/', views.tablet, name='tablet'),
    path('product/<pk>', views.mobile, name='mobile'),
]