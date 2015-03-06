from django.conf.urls import patterns, include, url
from django.contrib import admin
from SocialNetworkModels import views

urlpatterns = patterns('',
    url(r'^home/', include('SocialNetworkModels.url2')), # NEW MAPPING!
    url(r'^post/', views.author_post, name ='author_post'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', include('SocialNetworkModels.url_logout')), # NEW MAPPING!
    url(r'^$', include('SocialNetworkModels.urls')),
)