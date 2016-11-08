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
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'bookmarkz_app'))

from django.conf.urls import url
from django.contrib import admin
from django.views.static import serve
from django.contrib.auth import views as auth_views
from bookmarkz import views as bookmarkz_views
from bookmarkz_app import views as bookmarkz_app_views

#pathname manipulation
site_media = os.path.join(
  os.path.dirname(__file__),'..', 'site_media'
)

#path is bookmarkz/bookmarkz
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^site_media/(?P<path>.*)$', serve,
     { 'document_root': site_media }),
    # Browsing
    url(r'^$', bookmarkz_app_views.main_page, name='main_page'),
    url(r'^user/(\w+)/$', bookmarkz_app_views.user_page, name='user_page'),
    #url(r'^tag/([^\s]+)/$', tag_page, name='tag_page'),
    url(r'^tag/$', bookmarkz_app_views.tag_cloud_page),
    url(r'^search/$', bookmarkz_app_views.search_page),
    # Session management
    url(r'^accounts/login/$', auth_views.login ),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', bookmarkz_views.logout_page, name='logout'),
    url(r'^register/$', bookmarkz_views.register, name='register'),
    # Account management
    url(r'^save/$', bookmarkz_views.bookmark_save_page, name='bookmark_save'),
]
