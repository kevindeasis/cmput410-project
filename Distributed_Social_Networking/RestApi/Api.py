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

        user1 = self.kwargs['username1']
        return HttpResponse(json.dumps(jsonresponse), content_type = 'application/json')

    #http://django-rest-framework.readthedocs.org/en/latest/tutorial/3-class-based-views.html
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        user1 = self.kwargs['username1']

        data = json.loads(request.body)

        friendslist = []
        ourfriendlist = Friends.friendmanager.getAll(User.objects.get(pk=user1))
        for y in ourfriendlist:
            friendslist.append(y.reciever.pk)
        logging.info(friendslist)

        returnlist = []

        for x in range(len(data['authors'])):
            if int(data['authors'][x]) in friendslist:
                returnlist.append(data['authors'][x])

        jsonresponse = {}
        jsonresponse['query'] = 'friends'
        jsonresponse['author'] = user1
        jsonresponse['friends'] = returnlist

        logging.info(jsonresponse)

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

    class Meta:
        model = Posts
        fields = ('post_title', 'post_id', 'post_text', 'post_author')

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

                jsoncommentauthoroject["id"] = ""
                jsoncommentauthoroject["hostname"] = ""
                jsoncommentauthoroject["displayname"] = ""

                jsoncommentobject["author"]=jsoncommentauthoroject
                jsoncommentobject["comment"]=""
                jsoncommentobject["pubDate"]=""
                jsoncommentobject["guid"]=""

                commentarray.append(jsoncommentobject)
            '''
            setofcomments = obtaincomment(x.post_id)
            for z in commentarray:
                jsoncommentobject = {}


            #Comments.objects.filter()
            #ourfriendlist = Friends.friendmanager.getAll(User.objects.get(pk=user1))


            jsoncommentobject = {}
            jsoncommentauthoroject = {}

            jsoncommentauthoroject["id"] = "commentauthorid"
            jsoncommentauthoroject["hostname"] = "commentauthor urlhost"
            jsoncommentauthoroject["displayname"] = "commentauthor username"

            jsoncommentobject["author"]=jsoncommentauthoroject
            jsoncommentobject["comment"]="author"
            jsoncommentobject["pubDate"]="author"
            jsoncommentobject["guid"]="author"

            commentarray.append(jsoncommentobject)'''

            jsonpostobject["comments"]=commentarray

            postarray.append(jsonpostobject)

        jsonresponse = {}
        jsonresponse['posts'] = postarray

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

        jsonresponse = {}
        jsonresponse['posts'] = postarray

        return HttpResponse(json.dumps(jsonresponse), content_type = 'application/json')

    #http://django-rest-framework.readthedocs.org/en/latest/tutorial/3-class-based-views.html
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        postid = data['post_id']

        try:
            post = Posts.objects.get(post_id=postid)
        except DoesNotExist:
            views.author_post(request)

        return HttpResponse(json.dumps({}), content_type = 'application/json')

    @csrf_exempt
    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)

        postid = data['post_id']

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

            jsoncommentauthoroject["id"] = ""
            jsoncommentauthoroject["hostname"] = ""
            jsoncommentauthoroject["displayname"] = ""

            jsoncommentobject["author"]=jsoncommentauthoroject
            jsoncommentobject["comment"]=""
            jsoncommentobject["pubDate"]=""
            jsoncommentobject["guid"]=""


            commentarray.append(jsoncommentobject)

            jsonpostobject["comments"]=commentarray

            postarray.append(jsonpostobject)

        jsonresponse = {}
        jsonresponse['posts'] = postarray

        return HttpResponse(json.dumps(jsonresponse), content_type = 'application/json')
