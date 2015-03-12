from django.conf.urls import patterns, include, url 
from django.contrib import admin
from SocialNetworkModels import views
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import generics
from SocialNetworkModels.models import Posts, Author, Friends, FriendManager, Follows, FollowManager, FriendManager


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
#class UserViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def get_queryset(self):
        user = self.kwargs['username']

        return User.objects.filter(username=user)

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('user', 'github_username', 'picture', 'approved')

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class FriendsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Friends
        fields = ('initiator', 'reciever', 'fof_private', 'friend_private', 'own_private', 'remote_private')

class FriendsViewSet(viewsets.ModelViewSet):
    queryset = Friends.friendmanager.all()
    serializer_class = FriendsSerializer

class FollowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Follows
        fields = ('followed', 'follower', 'hide')

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follows.followManager.all()
    serializer_class = FollowSerializer

class PostsSerializer(serializers.HyperlinkedModelSerializer):
    #http://stackoverflow.com/questions/17066074/modelserializer-using-model-property
    class Meta:
        model = Posts
        fields = ('post_id', 'post_author', 'post_title', 'post_text', 'VISIBILITY', 'image', 'mark_down' )
        #    id = serializers.CharField(read_only=True)


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

class AuthorPostsSerializer(serializers.HyperlinkedModelSerializer):
    #http://stackoverflow.com/questions/17066074/modelserializer-using-model-property

    #def posts(self, obj):
    #    return "http://127.0.0.1:8000/users/%d/tickets" % obj.id


    class Meta:
        model = Posts
        fields = ('post_id', 'post_author', 'post_title', 'post_text', 'VISIBILITY', 'image', 'mark_down' )

class AuthorPosts(viewsets.ModelViewSet):
    #username = serializers.SerializerMethodField('get_username')

    #queryset = Posts.objects.get_queryset().filter(post_author=authorname)
    serializer_class = AuthorPostsSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()

#router.register(r'service/(?P<pk>[0-9]+)/', AuthorPosts)

router.register(r'users', UserViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'friends', FriendsViewSet)
router.register(r'follows', FollowViewSet)
router.register(r'post', PostsViewSet)
#router.register(r'service/author//(?P<username>.+)/posts/$', AuthorPosts)



urlpatterns = patterns('',


    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^service/', include(router.urls)),

    #
    #url(r'^rest/', ListCreateAPIView.as_view(model=User)),
    url(r'^users/(?P<username>.+)/$', UserViewSet.as_view({'get': 'list', 'post': 'create'})),



    url(r'^$', views.user_login, name = 'user_login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', views.user_login, name = 'user_login'),
    url(r'^logout/', views.user_logout, name = 'user_logout'), # NEW MAPPING!

    url(r'^home/', views.home,name='home'), # NEW MAPPING!

    url(r'^post/', views.author_post, name ='author_post'),
    url(r'^display/(?P<post_id>[a-zA-Z0-9\-]+)/$',views.display_post,name ='display_post'),
    url(r'^postdelete/(?P<post_id>[a-zA-Z0-9\-]+)/$',views.author_post_delete,name ='author_post_delete'),
    url(r'^postedit/(?P<post_id>[a-zA-Z0-9\-]+)/$',views.author_post_edit,name ='author_post_edit'),
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

    url(r'^testaddfriend/(?P<reciever_pk>\w+)/$', views.testaddfriend, name="testaddfriend"),

    url(r'^friendrequests/', views.viewfriendrequests, name="viewfriendrequests"),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),

)

