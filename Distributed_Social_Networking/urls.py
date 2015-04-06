from django.conf.urls import patterns, include, url 
from django.contrib import admin
from SocialNetworkModels import views, api_urls
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

import json

from rest_framework import generics
from SocialNetworkModels.models import Posts, Author, Friends, FriendManager, Follows, FollowManager, FriendManager, Comments
from rest_framework.decorators import api_view

from rest_framework import mixins

from rest_framework import status
from rest_framework.decorators import detail_route
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from RestApi import Api

import logging, logging.config
import sys

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'users', Api.UserViewSet)
router.register(r'author', Api.AuthorViewSet)

router.register(r'allfriends', Api.FriendsViewSet)

router.register(r'follows', Api.FollowViewSet)
router.register(r'post', Api.PostsViewSet)


urlpatterns = patterns('',

    url(r'^service/author/(?P<authorid>.+)/posts/$', csrf_exempt(Api.AuthorPosts.as_view())),
    url(r'^service/author/posts/$', csrf_exempt(Api.GrabPublicPost.as_view())),
    url(r'^service/posts/(?P<postid>.+)/$', csrf_exempt(Api.GrabPostID.as_view())),
    url(r'^service/posts/$', csrf_exempt(Api.GrabPublicPost.as_view())),
    url(r'^service/friendrequest/$', csrf_exempt(Api.FriendRequest.as_view())),

    url(r'^service/foaf/getposts/$', csrf_exempt(Api.GrabFoafPost.as_view())),

    url(r'^service/foaf/(?P<postid>.+)/$', csrf_exempt(Api.FoafPost.as_view())),


    url(r'^service/friends/(?P<username1>.+)/(?P<username2>.+)/$', csrf_exempt(Api.FriendList.as_view())),

    url(r'^service/friends/(?P<username1>.+)/$', csrf_exempt(Api.FriendList.as_view())),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^service/', include(router.urls), name='url_service'),

    url(r'^addforeign/(?P<username>.+)/(?P<id>.+)/$', views.addforeign),

    url(r'^users/$', Api.UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    
    url(r'^$', views.user_login, name = 'user_login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', views.user_login, name = 'user_login'),
    url(r'^logout/', views.user_logout, name = 'user_logout'),
    url(r'^home/', views.home,name='home'),

    url(r'^post/', views.author_post, name ='author_post'),
    url(r'^display/(?P<post_id>[a-zA-Z0-9\-]+)/$',views.display_post,name ='display_post'),
    url(r'^postdelete/(?P<post_id>[a-zA-Z0-9\-]+)/$',views.author_post_delete,name ='author_post_delete'),
    url(r'^postedit/(?P<post_id>[a-zA-Z0-9\-]+)/$',views.author_post_edit,name ='author_post_edit'),
    url(r'^postcomment/(?P<post_id>[a-zA-Z0-9\-]+)/(?P<author>[a-zA-Z0-9\-]+)/$',views.author_post_comment,name ='author_post_comment'),
    url(r'^profile/', views.profile, {'edit': '0'}, name ='profile'),
    url(r'^profile1/', views.profile, {'edit': '1'}, name ='profile'),
    url(r'^profile_post/(?P<user_id>[a-zA-Z0-9\-]+)/$',views.profile_post,{'edit': '2'},name ='profile_post'),
    url(r'^profile_edit/', views.profile_edit, name ='profile_edit'),
    url(r'^register/', views.register, name ='register'),

    url(r'^searchusers/', views.search_users, name ='search_users'),
    url(r'^searchposts/', views.search_posts, name ='search_posts'),

    url(r'^follow/(?P<reciever_pk>\w+)/$', views.follow, name="follow"),
    url(r'^addfriend/(?P<reciever_pk>\w+)/$', views.addfriend, name="addfriend"),
    url(r'^unfollow/(?P<reciever_pk>\w+)/$', views.unfollow, name="unfollow"),
    url(r'^unfriend/(?P<reciever_pk>\w+)/$', views.unfriend, name="unfriend"),
    url(r'^confirmfriend/(?P<reciever_pk>\w+)/$', views.confirmfriend, name="confirmfriend"),

    url(r'^friendrequests/', views.viewfriendrequests, name="viewfriendrequests"),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),

)

