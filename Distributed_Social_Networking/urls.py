from django.conf.urls import patterns, include, url 
from django.contrib import admin
from SocialNetworkModels import views

urlpatterns = patterns('',
    url(r'^$', views.user_login, name = 'user_login'),
    url(r'^login/', views.user_login, name = 'user_login'),
    url(r'^home/', views.home,name='home'), # NEW MAPPING!
    url(r'^post/', views.author_post, name ='author_post'),
    url(r'^profile/', views.profile, name ='profile'),
    url(r'^register/', views.register, name ='register'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', views.user_logout, name = 'user_logout'), # NEW MAPPING!
    url(r'^friend/$', views.friend, name='friend'), # NEW MAPPING!
    url(r'^friend/unfriend/(?P<target_user>\w+)/$', views.unfriend, name='unfriend'), # NEW MAPPING!
    url(r'^friend/befriend/$', views.befriend, name='befriend'), # NEW MAPPING!
)
