from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test.client import Client

from rest_framework.test import force_authenticate

from django.contrib.auth.models import User
from SocialNetworkModels.models import Posts, Author, Friends, FriendManager, Follows, FollowManager, FriendManager, Comments

from rest_framework.test import APIClient

#factory = APIRequestFactory()

#request = factory.post('/service/', {'title': 'new idea'}, format='json' )


class FirstLayerServiceTest(APITestCase):

    client = Client()

    def test_first_layer(self):
        #url = reverse('url_service')
        response = self.client.get('/service/')
        self.assertEqual(response.status_code, 200)

class AuthorPostTest(APITestCase):

    client = Client()

    def test_author(self):
        response = self.client.get('/service/author/74/posts', follow=True)
        self.assertEqual(response.status_code, 403)

class DeniedAuthenticationTest(APITestCase):

    client = Client()

    def test_author(self):
        response = self.client.get('/service/author/posts/', follow=True)
        self.assertEqual(response.status_code, 403)

class FriendTest(APITestCase):

    factory = APIRequestFactory() # enforce_csrf_checks=True ?

    def test_friend_one(self):
        request = factory.post('/service/friends/67/', {"query": "friends", "author": "9de17f29c12e8f97bcbbd34cc908f1baba40658e", "authors": ["69", "68", "67"]}, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_friend_two(self):
        request = factory.get('/service/friends/67/68/')
        response = view(request)
        self.assertEqual(response.status_code, 200)

class PostIDTest(APITestCase):

    factory = APIRequestFactory() # enforce_csrf_checks=True ?

    def test_post_id_get(self):
        request = factory.get('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a26e/')
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_post_id_post(self):
        request = factory.post('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a268/', {"post_title": "no", "post_id": "c4d924d8-caaf-4470-ad7d-ae0e4714a268", "post_text": "no", "post_author": {"user": 63, "github_username": "jeff", "picture": "http://cs410.cs.ualberta.ca:41071/service/author/63/static/profile_images/gamersky_034origin_067_20131111227AA2.jpg", "approved": true, "author_details": {"url": "http://cs410.cs.ualberta.ca:41071/service/users/63/", "username": "jeff", "email": "jeff@gmail.com", "is_staff": false}}, "visibility": "PUBLIC", "markdown": false}, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_post_id_put(self):
        request = factory.put('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a26e/', {"post_title": "no", "post_id": "c4d924d8-caaf-4470-ad7d-ae0e4714a26e", "post_text": "no", "post_author": {"user": 63, "github_username": "jeff", "picture": "http://cs410.cs.ualberta.ca:41071/service/author/63/static/profile_images/gamersky_034origin_067_20131111227AA2.jpg", "approved": true, "author_details": {"url": "http://cs410.cs.ualberta.ca:41071/service/users/63/", "username": "jeff", "email": "jeff@gmail.com", "is_staff": false}}, "visibility": "PUBLIC", "markdown": false}, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200)

class PostTest(APITestCase):

    factory = APIRequestFactory() # enforce_csrf_checks=True ?

    def test_post_get(self):
        request = factory.get('/service/posts/')
        response = view(request)
        self.assertEqual(response.status_code, 200)

class FriendRequestTest(APITestCase):

    factory = APIRequestFactory() # enforce_csrf_checks=True ?

    def test_fr(self):
        request = factory.post('/service/friendrequest/', {"query":"friendrequest", "author":{"id":"67", "host":"http://127.0.0.1:5454/", "displayname":"1"}, "friend": {"id":"68", "host":"http://127.0.0.1:5454/", "displayname":"2", "url":"http://localhost:9000/service/author/68/"}}, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200)

class AuthorTest(APITestCase):

    factory = APIRequestFactory() # enforce_csrf_checks=True ?

    def test_author(self):
        request = factory.get('/service/author/posts/')
        response = view(request)
        self.assertEqual(response.status_code, 200)

class AuthorIDTest(APITestCase):

    factory = APIRequestFactory() # enforce_csrf_checks=True ?

    def test_author_id(self):
        request = factory.get('/service/author/63/')
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_author_id(self):
        request = factory.get('/service/author/63/posts/')
        response = view(request)
        self.assertEqual(response.status_code, 200)

class FoaFTest(APITestCase):

    factory = APIRequestFactory() # enforce_csrf_checks=True ?

    def test_FoaF(self):
        request = factory.get('/service/foaf/getposts/', {"query":"getpost", "id":"63", "author":{"id":"66", "host":"http://127.0.0.1:5454/", "displayname":"Greg"}, "friends":["67", "68"]}, format='json')
        response = view(request)
        self.assertEqual(response.status_code, 200)

#following types of test to be done
#http://www.django-rest-framework.org/api-guide/testing/

#http://blog.pedesen.de/2013/06/05/Testing-django-rest-framework-API-with-TokenAuthentication/

#https://www.udacity.com/wiki/cs258/all-any




