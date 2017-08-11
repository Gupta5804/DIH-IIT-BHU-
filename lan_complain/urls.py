from django.conf.urls import url

from lan_complain import views

urlpatterns = [
    url(r'^$', views.questions, name='questions'),
    url(r'^answered/$', views.answered, name='answered'),
    url(r'^unanswered/$', views.unanswered, name='unanswered'),
    url(r'^all/$', views.all, name='all'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^favorite/$', views.favorite, name='favorite'),
    url(r'^answer/$', views.answer, name='answer'),
    url(r'^answer/accept/$', views.accept, name='accept'),
    url(r'^answer/vote/$', views.vote, name='vote'),
    url(r'^(?P<pk>[\-\w]+)/$', views.question, name='question'),
]
