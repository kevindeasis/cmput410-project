from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^home/', include('SocialNetworkModels.url2')), # NEW MAPPING!
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', include('SocialNetworkModels.url_logout')), # NEW MAPPING!
    url(r'^$', include('SocialNetworkModels.urls')),
)