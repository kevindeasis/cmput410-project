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

def obtaincomment(id):
    return Comments.objects.filter(post_id=id)

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

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Friends.friendmanager.all()
    serializer_class = FindFriendsSerializer


    def get(self, request, *args, **kwargs):
        user1 = self.kwargs['username1']
        user2 = self.kwargs['username2']
        allusers = []
        allusers.append(user1)
        allusers.append(user2)

        isfriends = False

        jsonresponse = {}
        jsonresponse['query'] = 'friends'
        jsonresponse['author'] = allusers

        arefriends = len(Friends.friendmanager.get_api_friends(user1, user2))

        if arefriends>0:
            isfriends = True

        jsonresponse['friends'] = isfriends

        logging.info(arefriends)
        #logging.info(request.GET.get('username'))
        #logging.info(request.GET['username'])



        user1 = self.kwargs['username1']
        #return Friends.friendmanager.getAll(user1)
        return HttpResponse(json.dumps(jsonresponse), content_type = 'application/json')

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

class AuthorPosts(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = AuthorPostsSerializer

    #queryset = Posts.objects.filter(post_author=Author)
    #serializer_class = FindFriendsSerializer


    def get(self, request, *args, **kwargs):
        user1 = self.kwargs['authorid']
        theauthor = Author.objects.get(user=User.objects.get(pk=user1))
        allposts = Posts.objects.filter(post_author=theauthor)

        authorid = user1
        authorhost = 'somehosturl'
        authordisplayname = theauthor.user.username
        authorurl = 'someurl'

        postarray = []
        for x in allposts:
            jsonpostobject = {}
            jsonpostobject["title"] = x.post_title
            jsonpostobject["source"] = x.post_title
            jsonpostobject["origin"] = x.post_title
            jsonpostobject["description"] = x.post_title
            jsonpostobject["content-type"] = x.post_title
            jsonpostobject["content"] = x.post_title

            jsonauthorobject = {}
            jsonauthorobject["id"] = authorid
            jsonauthorobject["host"] = authorhost
            jsonauthorobject["displayname"] = authordisplayname
            jsonauthorobject["url"] = authorurl

            jsonpostobject["author"]=jsonauthorobject

            commentarray = []
            #obviously there will be a for loop here

            jsoncommentobject = {}
            jsoncommentauthoroject = {}

            jsoncommentauthoroject["id"] = "commentauthorid"
            jsoncommentauthoroject["hostname"] = "commentauthor urlhost"
            jsoncommentauthoroject["displayname"] = "commentauthor username"

            jsoncommentobject["author"]=jsoncommentauthoroject
            jsoncommentobject["comment"]="author"
            jsoncommentobject["pubDate"]="author"
            jsoncommentobject["guid"]="author"


            commentarray.append(jsoncommentobject)

            jsonpostobject["comments"]=commentarray

            postarray.append(jsonpostobject)
            #logging.info(x.post_title)
            #logging.info(x.post_author.user.username)
            #logging.info(x.post_text)



        #logging.info(allposts)
        jsonresponse = {}
        jsonresponse['posts'] = postarray
        #jsonresponse['query'] = 'friends'
        #jsonresponse['author'] = allusers

        #arefriends = len(Friends.friendmanager.get_api_friends(user1, user2))

        #if arefriends>0:
        #    isfriends = True

        #jsonresponse['friends'] = isfriends

        #logging.info(arefriends)
        #logging.info(request.GET.get('username'))
        #logging.info(request.GET['username'])



        #user1 = self.kwargs['username1']
        #return Friends.friendmanager.getAll(user1)
        return HttpResponse(json.dumps(jsonresponse), content_type = 'application/json')



class FriendRequest(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Friends.friendmanager.all()
    serializer_class = FindFriendsSerializer


    def get(self, request, *args, **kwargs):
        data = json.loads(request.body)

        authorid = data['author']['id']
        authorhost = data['author']['host']
        authordisplayname = data['author']['displayname']

        friendid = data['friend']['id']
        friendhost = data['friend']['host']
        frienddisplayname = data['friend']['displayname']
        friendurl = data['friend']['url']

        logging.info(authorid)
        logging.info(authorhost)
        logging.info(friendid)
        logging.info(friendhost)

        Friends.friendmanager.mutualFriends(User.objects.get(pk = authorid),User.objects.get(pk = friendid))

        return HttpResponse(json.dumps({}), content_type = 'application/json')

    #http://django-rest-framework.readthedocs.org/en/latest/tutorial/3-class-based-views.html
    @csrf_exempt
    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)

        authorid = data['author']['id']
        authorhost = data['author']['host']
        authordisplayname = data['author']['displayname']

        friendid = data['friend']['id']
        friendhost = data['friend']['host']
        frienddisplayname = data['friend']['displayname']
        friendurl = data['friend']['url']

        logging.info(authorid)
        logging.info(authorhost)
        logging.info(friendid)
        logging.info(friendhost)

        Friends.friendmanager.mutualFriends(User.objects.get(pk = authorid),User.objects.get(pk = friendid))

        return HttpResponse(json.dumps({}), content_type = 'application/json')

class GrabPostID(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = AuthorPostsSerializer

    def get(self, request, *args, **kwargs):
        postid = self.kwargs['postid']

        logging.info(obtaincomment(postid).exists())

        #theauthor = Author.objects.get(user=User.objects.get(pk=user1))
        apost = Posts.objects.get(post_id=postid)
        allposts = [apost]

        postauthor = apost.post_author.user
        authorid = postauthor.pk
        authorhost = 'somehosturl'
        authordisplayname = postauthor.username
        authorurl = 'someurl'

        postarray = []
        for x in allposts:

            jsonpostobject = {}
            jsonpostobject["title"] = x.post_title
            jsonpostobject["source"] = x.post_title
            jsonpostobject["origin"] = x.post_title
            jsonpostobject["description"] = x.post_title
            jsonpostobject["content-type"] = x.post_title
            jsonpostobject["content"] = x.post_title

            jsonauthorobject = {}
            jsonauthorobject["id"] = authorid
            jsonauthorobject["host"] = authorhost
            jsonauthorobject["displayname"] = authordisplayname
            jsonauthorobject["url"] = authorurl

            jsonpostobject["author"]=jsonauthorobject

            commentarray = []
            #obviously there will be a for loop here



            #comments_exists=obtaincomment(x.post_id).exists()
            #logging.info(comments_exists)

            if obtaincomment(x.post_id).exists():
                for q in obtaincomment(x.post_id):
                    jsoncommentobject = {}
                    jsoncommentauthoroject = {}

                    jsoncommentauthoroject["id"] = User.objects.get(username=q.comment_author).pk
                    jsoncommentauthoroject["hostname"] = "commentauthor urlhost"
                    jsoncommentauthoroject["displayname"] = User.objects.get(username=q.comment_author).username

                    jsoncommentobject["author"]=jsoncommentauthoroject
                    jsoncommentobject["comment"]=q.comment_text
                    jsoncommentobject["pubDate"]="somedate"
                    jsoncommentobject["guid"]=q.post_id

                    commentarray.append(jsoncommentobject)


            else:


                jsoncommentobject = {}
                jsoncommentauthoroject = {}

                jsoncommentauthoroject["id"] = "commentauthorid"
                jsoncommentauthoroject["hostname"] = "commentauthor urlhost"
                jsoncommentauthoroject["displayname"] = "commentauthor username"

                jsoncommentobject["author"]=jsoncommentauthoroject
                jsoncommentobject["comment"]="author"
                jsoncommentobject["pubDate"]="author"
                jsoncommentobject["guid"]="author"


                commentarray.append(jsoncommentobject)

            jsonpostobject["comments"]=commentarray

            postarray.append(jsonpostobject)

        #logging.info(allposts)
        jsonresponse = {}
        jsonresponse['posts'] = postarray

        return HttpResponse(json.dumps(jsonresponse), content_type = 'application/json')

    #http://django-rest-framework.readthedocs.org/en/latest/tutorial/3-class-based-views.html
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        #logging.info(authorid)
        #logging.info(authorhost)
        #logging.info(friendid)
        #logging.info(friendhost)

        #posttitle = data['post_title']
        postid = data['post_id']
        #posttext = data['post_text']

        #user1 = data['post_author']['user']
        #github_username = data['post_author']['github_username']
        #picture = data['post_author']['picture']
        #approved = data['post_author']['approved']

        #url2 = data['post_author']['author_details']['url']
        #username = data['post_author']['author_details']['username']
        #email = data['post_author']['author_details']['email']
        #isstaff = data['post_author']['author_details']['is_staff']

        try:
            post = Posts.objects.get(post_id=postid)
        except DoesNotExist:
            views.author_post(request)

        return HttpResponse(json.dumps({}), content_type = 'application/json')

    @csrf_exempt
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)

        #logging.info(authorid)
        #logging.info(authorhost)
        #logging.info(friendid)
        #logging.info(friendhost)

        #posttitle = data['post_title']
        postid = data['post_id']
        #posttext = data['post_text']

        #user1 = data['post_author']['user']
        #github_username = data['post_author']['github_username']
        #picture = data['post_author']['picture']
        #approved = data['post_author']['approved']

        #url2 = data['post_author']['author_details']['url']
        #username = data['post_author']['author_details']['username']
        #email = data['post_author']['author_details']['email']
        #isstaff = data['post_author']['author_details']['is_staff']

        try:
            post = Posts.objects.get(post_id=postid)
        except DoesNotExist:
            views.author_post(request)
        else:
            views.author_post_edit(request, postid)

        return HttpResponse(json.dumps({}), content_type = 'application/json')


class GrabPublicPost(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = AuthorPostsSerializer

    def get(self, request, *args, **kwargs):
        allposts = Posts.objects.all()


        postarray = []
        for x in allposts:

            #apost = Posts.objects.get(post_id=postid)
            #allposts = [apost]

            postauthor = x.post_author.user
            authorid = postauthor.pk
            authorhost = 'somehosturl'
            authordisplayname = postauthor.username
            authorurl = 'someurl'

            jsonpostobject = {}
            jsonpostobject["title"] = x.post_title
            jsonpostobject["source"] = x.post_title
            jsonpostobject["origin"] = x.post_title
            jsonpostobject["description"] = x.post_title
            jsonpostobject["content-type"] = x.post_title
            jsonpostobject["content"] = x.post_title

            jsonauthorobject = {}
            jsonauthorobject["id"] = authorid
            jsonauthorobject["host"] = authorhost
            jsonauthorobject["displayname"] = authordisplayname
            jsonauthorobject["url"] = authorurl

            jsonpostobject["author"]=jsonauthorobject

            commentarray = []
            #obviously there will be a for loop here

            jsoncommentobject = {}
            jsoncommentauthoroject = {}

            jsoncommentauthoroject["id"] = "commentauthorid"
            jsoncommentauthoroject["hostname"] = "commentauthor urlhost"
            jsoncommentauthoroject["displayname"] = "commentauthor username"

            jsoncommentobject["author"]=jsoncommentauthoroject
            jsoncommentobject["comment"]="author"
            jsoncommentobject["pubDate"]="author"
            jsoncommentobject["guid"]="author"


            commentarray.append(jsoncommentobject)

            jsonpostobject["comments"]=commentarray

            postarray.append(jsonpostobject)

        jsonresponse = {}
        jsonresponse['posts'] = postarray

        return HttpResponse(json.dumps(jsonresponse), content_type = 'application/json')



class GrabFoafPost(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = AuthorPostsSerializer

    def get(self, request, *args, **kwargs):

        logging.info('ei')


        data = json.loads(request.body)

        logging.info(data)

        requester_id = data['author']['id']
        requester_host = data['author']['host']
        requester_displayname = data['author']['displayname']

        user1 = data['id']

        mutual_friends_list = data['friends']

        theauthor = Author.objects.get(user=User.objects.get(pk=user1))
        allposts = Posts.objects.filter(post_author=theauthor)

        authorid = data['id']
        authorhost = 'somehosturl'
        authordisplayname = theauthor.user.username
        authorurl = 'someurl'

        cangetpost = False

        returnlist = []
        for x in range(len(data['friends'])):
            data['friends'][x]


            '''
            Ok you need info from the other group otherwise you cant do this
            '''


        postarray = []
        for x in allposts:
            jsonpostobject = {}
            jsonpostobject["title"] = x.post_title
            jsonpostobject["source"] = x.post_title
            jsonpostobject["origin"] = x.post_title
            jsonpostobject["description"] = x.post_title
            jsonpostobject["content-type"] = x.post_title
            jsonpostobject["content"] = x.post_title

            jsonauthorobject = {}
            jsonauthorobject["id"] = authorid
            jsonauthorobject["host"] = authorhost
            jsonauthorobject["displayname"] = authordisplayname
            jsonauthorobject["url"] = authorurl

            jsonpostobject["author"]=jsonauthorobject

            commentarray = []
            #obviously there will be a for loop here

            jsoncommentobject = {}
            jsoncommentauthoroject = {}

            jsoncommentauthoroject["id"] = "commentauthorid"
            jsoncommentauthoroject["hostname"] = "commentauthor urlhost"
            jsoncommentauthoroject["displayname"] = "commentauthor username"

            jsoncommentobject["author"]=jsoncommentauthoroject
            jsoncommentobject["comment"]="author"
            jsoncommentobject["pubDate"]="author"
            jsoncommentobject["guid"]="author"


            commentarray.append(jsoncommentobject)

            jsonpostobject["comments"]=commentarray

            postarray.append(jsonpostobject)

        jsonresponse = {}
        jsonresponse['posts'] = postarray

        return HttpResponse(json.dumps(jsonresponse), content_type = 'application/json')



# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'author', AuthorViewSet)

router.register(r'allfriends', FriendsViewSet)
#router.register(r'friends/(?P<username1>.+)/(?P<username2>.+)/$', CustomFriendsViewSet )

#router.register(r'friends/(?P<username1>.+)/$', FriendList.as_view() )



router.register(r'follows', FollowViewSet)
router.register(r'post', PostsViewSet)



urlpatterns = patterns('',
    #url(r'^service/friends/(?P<username1>.+)/(?P<username2>.+)/$', CustomFriendsViewSet.as_view({'get': 'list', 'post': 'list'})),

    url(r'^service/author/(?P<authorid>.+)/posts/$', csrf_exempt(AuthorPosts.as_view())),
    url(r'^service/author/posts/$', csrf_exempt(GrabPublicPost.as_view())),
    url(r'^service/posts/(?P<postid>.+)/$', csrf_exempt(GrabPostID.as_view())),
    url(r'^service/posts/$', csrf_exempt(GrabPublicPost.as_view())),
    url(r'^service/friendrequest/$', csrf_exempt(FriendRequest.as_view())),

    url(r'^service/foaf/getposts/$', csrf_exempt(GrabFoafPost.as_view())),


    url(r'^service/friends/(?P<username1>.+)/(?P<username2>.+)/$', csrf_exempt(FriendList.as_view())),

    url(r'^service/friends/(?P<username1>.+)/$', csrf_exempt(FriendList.as_view())),


    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^service/', include(router.urls)),
    
    url(r'^users/$', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    
    url(r'^$', views.user_login, name = 'user_login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', views.user_login, name = 'user_login'),
    url(r'^logout/', views.user_logout, name = 'user_logout'), # NEW MAPPING!
    #url(r'^api/', include('api_urls')),
    url(r'^home/', views.home,name='home'), # NEW MAPPING!

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

