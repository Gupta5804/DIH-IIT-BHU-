from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', list_item, name="list"),
    url(r'^lost/(?P<id>\d+)/$', detail_lost, name="detail_l"),
    url(r'found/(?P<id>\d+)/$',detail_found,name="detail_f"),
    url(r'ReportLost/$', report_lost, name="lost"),
    url(r'^(?P<id>\d+)/edit$', edit_lost, name="edit"),
    url(r'^(?P<id>\d+)/delete/$', delete_item),
    url(r'ReportFound/$', report_found, name="found"),
]