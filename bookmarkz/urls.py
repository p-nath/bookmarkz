"""bookmarkz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from bookmarkz_app.views import *
from bookmarkz.views import *
from django.contrib.auth import views as auth_views
import os

#pathname manipulation
site_media = os.path.join(
  os.path.dirname(__file__),'../', 'site_media'
)

#path is bookmarkz/bookmarkz
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
     { 'document_root': site_media }),
    # Browsing
    url(r'^$', main_page, name='main_page'),
    url(r'^user/(\w+)/$', user_page, name='user_page'),
    #url(r'^tag/([^\s]+)/$', tag_page, name='tag_page'),
    url(r'^tag/$', tag_cloud_page),
    # Session management
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', logout_page, name='logout'),
    url(r'^register/$', register, name='register'),
    # Account management
    url(r'^save/$', bookmark_save_page, name='bookmark_save'),
]
