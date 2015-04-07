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

factory = APIRequestFactory() # enforce_csrf_checks=True ?

#request = factory.post('/service/', {'title': 'new idea'}, format='json' )

''' For base /service/ API calls '''
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

''' For /service/friends/ API calls '''
class FriendTest(APITestCase):

    # test for POST on /service/friends/userid/
    def test_friend_one(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='admin', password='admin')
        response = self.client.post('/service/friends/67/', {"query": "friends", "author": "9de17f29c12e8f97bcbbd34cc908f1baba40658e", "authors": ["69", "68", "67"]}, format='json')
        self.assertEqual(response.status_code, 200)
        client.logout()

    # test for GET on /service/friends/userid1/userid2/
    def test_friend_two(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='admin', password='admin')
        response = self.client.get('/service/friends/67/68/')
        self.assertEqual(response.status_code, 200)
        client.logout()

    # test for un-authenticated client
    def test_friend_one_unauth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = self.client.post('/service/friends/67/', {"query": "friends", "author": "9de17f29c12e8f97bcbbd34cc908f1baba40658e", "authors": ["69", "68", "67"]}, format='json')
        self.assertEqual(response.status_code, 403)

    # test for un-authenticated client
    def test_friend_two_unauth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = self.client.get('/service/friends/67/68/')
        self.assertEqual(response.status_code, 403)

''' For /service/posts/{ID} API calls '''
class PostIDTest(APITestCase):

    # test for GET on /service/posts/postid/
    def test_post_id_get(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='admin', password='admin')
        response = self.client.get('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a26e/')
        self.assertEqual(response.status_code, 200)
        client.logout()

    # test for POST on /service/posts/postid/
    def test_post_id_post(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='admin', password='admin')
        response = self.client.post('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a268/', {"post_title": "no", "post_id": "c4d924d8-caaf-4470-ad7d-ae0e4714a268", "post_text": "no", "post_author": {"user": 63, "github_username": "jeff", "picture": "http://cs410.cs.ualberta.ca:41071/service/author/63/static/profile_images/gamersky_034origin_067_20131111227AA2.jpg", "approved": True, "author_details": {"url": "http://cs410.cs.ualberta.ca:41071/service/users/63/", "username": "jeff", "email": "jeff@gmail.com", "is_staff": False}}, "visibility": "PUBLIC", "markdown": False}, format='json')
        self.assertEqual(response.status_code, 200)
        client.logout()

    # test for PUT on /service/posts/postid/
    def test_post_id_put(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='admin', password='admin')
        response = self.client.put('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a26e/', {"post_title": "no", "post_id": "c4d924d8-caaf-4470-ad7d-ae0e4714a26e", "post_text": "no", "post_author": {"user": 63, "github_username": "jeff", "picture": "http://cs410.cs.ualberta.ca:41071/service/author/63/static/profile_images/gamersky_034origin_067_20131111227AA2.jpg", "approved": True, "author_details": {"url": "http://cs410.cs.ualberta.ca:41071/service/users/63/", "username": "jeff", "email": "jeff@gmail.com", "is_staff": False}}, "visibility": "PUBLIC", "markdown": False}, format='json')
        self.assertEqual(response.status_code, 200)
        client.logout()

    # test for un-authenticated client
    def test_post_id_get_unauth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = self.client.get('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a26e/')
        self.assertEqual(response.status_code, 403)

    # test for un-authenticated client
    def test_post_id_post_unauth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = self.client.post('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a268/', {"post_title": "no", "post_id": "c4d924d8-caaf-4470-ad7d-ae0e4714a268", "post_text": "no", "post_author": {"user": 63, "github_username": "jeff", "picture": "http://cs410.cs.ualberta.ca:41071/service/author/63/static/profile_images/gamersky_034origin_067_20131111227AA2.jpg", "approved": True, "author_details": {"url": "http://cs410.cs.ualberta.ca:41071/service/users/63/", "username": "jeff", "email": "jeff@gmail.com", "is_staff": False}}, "visibility": "PUBLIC", "markdown": False}, format='json')
        self.assertEqual(response.status_code, 403)

    # test for un-authenticated client
    def test_post_id_put_unauth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = self.client.put('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a26e/', {"post_title": "no", "post_id": "c4d924d8-caaf-4470-ad7d-ae0e4714a26e", "post_text": "no", "post_author": {"user": 63, "github_username": "jeff", "picture": "http://cs410.cs.ualberta.ca:41071/service/author/63/static/profile_images/gamersky_034origin_067_20131111227AA2.jpg", "approved": True, "author_details": {"url": "http://cs410.cs.ualberta.ca:41071/service/users/63/", "username": "jeff", "email": "jeff@gmail.com", "is_staff": False}}, "visibility": "PUBLIC", "markdown": False}, format='json')
        self.assertEqual(response.status_code, 403)

''' For /service/posts/ API calls '''
class PostTest(APITestCase):

    # test for GET on /service/posts/
    def test_post_get(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='admin', password='admin')
        response = self.client.get('/service/posts/')
        self.assertEqual(response.status_code, 200)
        client.logout()

    # test for un-authenticated client
    def test_post_get_unauth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = self.client.get('/service/posts/')
        self.assertEqual(response.status_code, 403)

''' For /service/friendrequest/ API calls '''
class FriendRequestTest(APITestCase):

    # test for POST on /service/friendrequest/
    def test_fr(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='admin', password='admin')
        response = self.client.post('/service/friendrequest/', {"query":"friendrequest", "author":{"id":"67", "host":"http://127.0.0.1:5454/", "displayname":"1"}, "friend": {"id":"68", "host":"http://127.0.0.1:5454/", "displayname":"2", "url":"http://localhost:9000/service/author/68/"}}, format='json')
        self.assertEqual(response.status_code, 200)
        client.logout()

    # test for un-authenticated client
    def test_fr_unauth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = self.client.post('/service/friendrequest/', {"query":"friendrequest", "author":{"id":"67", "host":"http://127.0.0.1:5454/", "displayname":"1"}, "friend": {"id":"68", "host":"http://127.0.0.1:5454/", "displayname":"2", "url":"http://localhost:9000/service/author/68/"}}, format='json')
        self.assertEqual(response.status_code, 403)

''' For /service/author/ API calls '''
class AuthorTest(APITestCase):

    # test for GET on /service/author/posts/
    def test_author(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='admin', password='admin')
        response = self.client.get('/service/author/posts/')
        self.assertEqual(response.status_code, 200)
        client.logout()

    # test for un-authenticated client
    def test_author_unauth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = self.client.get('/service/author/posts/')
        self.assertEqual(response.status_code, 403)

''' For /service/author/{ID} API calls '''
class AuthorIDTest(APITestCase):

    # test for GET on /service/author/userid/
    def test_author_id(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='admin', password='admin')
        response = self.client.get('/service/author/63/')
        self.assertEqual(response.status_code, 200)
        client.logout()

    # test for GET on /service/author/userid/posts/
    def test_author_id_posts(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='admin', password='admin')
        response = self.client.get('/service/author/63/posts/')
        self.assertEqual(response.status_code, 200)
        client.logout()

    # test for un-authenticated client
    def test_author_id_unauth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = self.client.get('/service/author/63/')
        self.assertEqual(response.status_code, 404)

    # test for un-authenticated client
    def test_author_id_posts_unauth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = self.client.get('/service/author/63/posts/')
        self.assertEqual(response.status_code, 403)

''' For /service/foaf/ API calls '''
class FoaFTest(APITestCase):

    # test for GET on /service/foaf/getposts/
    def test_FoaF(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username='admin', password='admin')
        response = self.client.get('/service/foaf/getposts/', {"query":"getpost", "id":"63", "author":{"id":"66", "host":"http://127.0.0.1:5454/", "displayname":"Greg"}, "friends":["67", "68"]}, format='json')
        self.assertEqual(response.status_code, 200)
        client.logout()

    # test for un-authenticated client
    def test_FoaF_unauth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = self.client.get('/service/foaf/getposts/', {"query":"getpost", "id":"63", "author":{"id":"66", "host":"http://127.0.0.1:5454/", "displayname":"Greg"}, "friends":["67", "68"]}, format='json')
        self.assertEqual(response.status_code, 403)

#following types of test to be done
#http://www.django-rest-framework.org/api-guide/testing/

#http://blog.pedesen.de/2013/06/05/Testing-django-rest-framework-API-with-TokenAuthentication/

#https://www.udacity.com/wiki/cs258/all-any




