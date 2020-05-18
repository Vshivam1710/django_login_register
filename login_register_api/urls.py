"""login_register_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from working import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.my_logout, name='logout'),
    url(r'^register/$', views.Register.as_view(), name='register'),
    url(r'^update_password/$', views.update_password, name='update_password'),
    url(r'^edit_profile/(?P<pk>\d+)/$', views.EditProfile.as_view(), name='edit_profile'),
    url(r'^delete_data/(?P<pk>\d+)/$', views.delete_data, name='delete_data'),
]
