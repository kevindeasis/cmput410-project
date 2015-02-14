from django.conf.urls import patterns, url

from SocialNetworkModels import views

urlpatterns = patterns('SocialNetworkModels.views',
    url(r'^$', 'index', name='index'),
)