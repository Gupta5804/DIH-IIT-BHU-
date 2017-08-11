"""por URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from . import views
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from search import views as search_views
from django.conf import settings
from django.conf.urls.static import static
from activities import views as activities_views
urlpatterns = [
    url(r'^$',views.site_redirect),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/',views.home),
    url(r'^accounts/profile_edit/(?P<pk>[\-\w]+)/$', views.edit_user, name='account_update'),
    url(r'^accounts/profile_view/(?P<pk>[\-\w]+)/$',views.get_user, name = 'account_view'),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^profile/(?P<username>[^/]+)/$', views.profile, name='profile'),
    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),
    url(r'', include('events.urls')),
    url(r'^messages/', include('messenger.urls')),
    url(r'^settings/picture/$', views.picture, name='picture'),
    url(r'^settings/upload_picture/$', views.upload_picture,
        name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', views.save_uploaded_picture,
        name='save_uploaded_picture'),
    url(r'^feeds/', include('feeds.urls')),
    url(r'^lan_complain/', include('lan_complain.urls')),
    url(r'^enotices/', include('enotices.urls')),
    url(r'^notifications/$', activities_views.notifications,
        name='notifications'),
    url(r'^notifications/last/$', activities_views.last_notifications,
        name='last_notifications'),
    url(r'^notifications/check/$', activities_views.check_notifications,
        name='check_notifications'),
    url(r'^LostAndFound/', include('lost_found.urls', namespace="laf")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()