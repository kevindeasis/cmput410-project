from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^add_author/', include('SocialNetworkModels.url2')), # NEW MAPPING!                   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('SocialNetworkModels.urls')),
    
)