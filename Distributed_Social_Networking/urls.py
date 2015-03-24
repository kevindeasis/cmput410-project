from django.conf.urls import patterns, include, url 
from django.contrib import admin
from SocialNetworkModels import views
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

import json

from rest_framework import generics
from SocialNetworkModels.models import Posts, Author, Friends, FriendManager, Follows, FollowManager, FriendManager
from rest_framework.decorators import api_view


from rest_framework import mixins

from rest_framework import status
from rest_framework.decorators import detail_route
from django.http import HttpResponse, HttpResponseRedirect

from django.views.decorators.csrf import csrf_exempt

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



# http://www.django-rest-framework.org/#tutorial

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    author_details = UserSerializer(source='user')

    class Meta:
        model = Author
        fields = ('user', 'github_username', 'picture', 'approved', 'author_details')

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class FriendsSerializer(serializers.HyperlinkedModelSerializer):

    friends = serializers.CharField(source='approvedrequest')

    class Meta:
        model = Friends
        fields = ('initiator', 'reciever', 'fof_private', 'friend_private', 'own_private', 'remote_private', 'friends')

class FriendsViewSet(viewsets.ModelViewSet):
    queryset = Friends.friendmanager.all()
    serializer_class = FriendsSerializer

class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friends.friendmanager.all()
    serializer_class = FriendsSerializer

    def get_queryset(self):
        user1 = self.kwargs['username1']
        user2 = self.kwargs['username2']
        return Friends.friendmanager.get_api_friends(user1, user2)

#http://stackoverflow.com/questions/14824807/adding-root-element-to-json-response-django-rest-framework
class CustomFriendRenderer(JSONRenderer):
    queryset = Friends.friendmanager.all()
    serializer_class = FriendsSerializer

    def render(self, data, accepted_media_type=None, renderer_context= None):
        #data = {'query':'friends',data}
        jsondata = {}
        jsondata['query']='friends'
        jsondata['authors']= []
        jsondata['authors'].append(data[0]["initiator"])
        jsondata['authors'].append(data[0]["reciever"])
        jsondata['friends']=data[0]["friends"]

        return super(CustomFriendRenderer, self).render(jsondata, accepted_media_type, renderer_context)



class CustomFriendsViewSet(viewsets.ModelViewSet):
    renderer_classes = (CustomFriendRenderer, )
    queryset = Friends.friendmanager.all()
    serializer_class = FriendsSerializer

    def get_queryset(self):
        user1 = self.kwargs['username1']
        user2 = self.kwargs['username2']
        return Friends.friendmanager.get_api_friends(user1, user2)


class FindFriendsSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.CharField(source='initiator')
    friends = serializers.CharField(source='reciever')

    class Meta:
        model = Friends
        fields = ('author', 'friends')

class FriendList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):


    queryset = Friends.friendmanager.all()
    serializer_class = FindFriendsSerializer


    def get(self, request, *args, **kwargs):

        logging.info(request.GET.get('username'))
        #logging.info(request.GET['username'])



        user1 = self.kwargs['username1']
        #return Friends.friendmanager.getAll(user1)
        return HttpResponse(user1)
    #http://django-rest-framework.readthedocs.org/en/latest/tutorial/3-class-based-views.html
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        user1 = self.kwargs['username1']

        data = json.loads(request.body)
        #logging.info(request.POST['username'])
        #logging.info(type(data))
        #logging.info((data['query']))
        #logging.info((data['author']))

        #logging.info(type(data['authors']))

        #OK THIS WORKS
        friendslist = []
        ourfriendlist = Friends.friendmanager.getAll(User.objects.get(pk=user1))
        for y in ourfriendlist:
            friendslist.append(y.reciever.pk)
        logging.info(friendslist)

        returnlist = []
        for x in range(len(data['authors'])):
            #logging.info(type(int(data['authors'][x][0])))
            #logging.info(data['authors'][x][0] in friendslist)
            #logging.info(type(data['authors'][x]))
            #logging.info(type(friendslist[0]))

            if int(data['authors'][x]) in friendslist:
                returnlist.append(data['authors'][x])

        jsonresponse = {}
        jsonresponse['query'] = 'friends'
        jsonresponse['author'] = user1
        jsonresponse['friends'] = returnlist

        logging.info(jsonresponse)

        #logging.info((data['authors'][0]))
        #this is a list
        #logging.info((data['authors']))
        #logging.info((data['']))

        #logging.info((type(user1)))
        #logging.info(((user1)))

        #logging.info(User.objects.get(pk=user1))
        #logging.info(User.objects.get(pk=user1).username)


        #logging.info(Friends.friendmanager.getAll(User.objects.get(pk=user1)))

        #obviously returns a list
        #return HttpResponse(Friends.friendmanager.getAll(User.objects.get(pk=user1)))

        #this is Friends but get the attribute titled reciever
        #return HttpResponse(Friends.friendmanager.getAll(User.objects.get(pk=user1))[0].reciever)
        return HttpResponse(json.dumps(jsonresponse), content_type = 'application/json')

        #return HttpResponse(Friends.friendmanager.getAll(User.objects.get(pk=user1)))


class FollowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Follows
        fields = ('followed', 'follower', 'hide')

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follows.followManager.all()
    serializer_class = FollowSerializer

class PostsSerializer(serializers.HyperlinkedModelSerializer):
    #http://stackoverflow.com/questions/17066074/modelserializer-using-model-property
    post_author = AuthorSerializer(required=True)
    #post_author = AuthorSerializer(read_only=True)

    class Meta:
        model = Posts
        fields = ('post_title', 'post_id', 'post_text', 'post_author')
        #    id = serializers.CharField(read_only=True)


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

class AuthorPostsSerializer(serializers.HyperlinkedModelSerializer):
    #http://stackoverflow.com/questions/17066074/modelserializer-using-model-property

    class Meta:
        model = Posts
        fields = ('post_id', 'post_author', 'post_title', 'post_text', 'VISIBILITY', 'image', 'mark_down' )

class AuthorPosts(viewsets.ModelViewSet):
    serializer_class = AuthorPostsSerializer



# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'author', AuthorViewSet)

#router.register(r'friends', FriendsViewSet)
#router.register(r'friends/(?P<username1>.+)/(?P<username2>.+)/$', CustomFriendsViewSet )

#router.register(r'friends/(?P<username1>.+)/$', FriendList.as_view() )



router.register(r'follows', FollowViewSet)
router.register(r'post', PostsViewSet)


urlpatterns = patterns('',
    url(r'^service/friends/(?P<username1>.+)/(?P<username2>.+)/$', CustomFriendsViewSet.as_view({'get': 'list', 'post': 'list'})),

    url(r'^service/friends/(?P<username1>.+)/$', csrf_exempt(FriendList.as_view())),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^service/', include(router.urls)),

    url(r'^users/$', UserViewSet.as_view({'get': 'list', 'post': 'create'})),

    url(r'^$', views.user_login, name = 'user_login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', views.user_login, name = 'user_login'),
    url(r'^logout/', views.user_logout, name = 'user_logout'), # NEW MAPPING!

    url(r'^home/', views.home,name='home'), # NEW MAPPING!

    url(r'^post/', views.author_post, name ='author_post'),
    url(r'^display/(?P<post_id>[a-zA-Z0-9\-]+)/$',views.display_post,name ='display_post'),
    url(r'^postdelete/(?P<post_id>[a-zA-Z0-9\-]+)/$',views.author_post_delete,name ='author_post_delete'),
    url(r'^postedit/(?P<post_id>[a-zA-Z0-9\-]+)/$',views.author_post_edit,name ='author_post_edit'),
    url(r'^postcomment/(?P<post_id>[a-zA-Z0-9\-]+)/$',views.author_post_comment,name ='author_post_comment'),
    url(r'^profile/', views.profile, {'edit': '0'}, name ='profile'),
    url(r'^profile1/', views.profile, {'edit': '1'}, name ='profile'),
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

