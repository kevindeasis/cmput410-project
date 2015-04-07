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

    client = APIClient(enforce_csrf_checks=True)

    def setUp(self):
        u = User.objects.create_superuser(username='apitest1', email='apitest1@apitest.com', password='apitest1')
        u.save()
        login = self.client.login(username = 'apitest1', password = 'apitest1')
        self.assertTrue(login)

    # test for POST on /service/friends/userid/
    def test_friend_one(self):
        response = self.client.post('/service/friends/67/', {"query": "friends", "author": "9de17f29c12e8f97bcbbd34cc908f1baba40658e", "authors": ["69", "68", "67"]}, format='json')
        self.assertEqual(response.status_code, 200)

    # test for GET on /service/friends/userid1/userid2/
    def test_friend_two(self):
        response = self.client.get('/service/friends/67/68/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()

class FriendTestUnauth(APITestCase):

    client = APIClient()

    # test for un-authenticated client
    def test_friend_one_unauth(self):
        response = self.client.post('/service/friends/67/', {"query": "friends", "author": "9de17f29c12e8f97bcbbd34cc908f1baba40658e", "authors": ["69", "68", "67"]}, format='json')
        self.assertEqual(response.status_code, 403)

    # test for un-authenticated client
    def test_friend_two_unauth(self):
        response = self.client.get('/service/friends/67/68/')
        self.assertEqual(response.status_code, 403)

''' For /service/posts/{ID} API calls '''
class PostIDTest(APITestCase):

    client = APIClient(enforce_csrf_checks=True)

    def setUp(self):
        u = User.objects.create_superuser(username='apitest2', email='apitest2@apitest.com', password='apitest2')
        u.save()
        login = self.client.login(username = 'apitest2', password = 'apitest2')
        self.assertTrue(login)

    # test for GET on /service/posts/postid/
    def test_post_id_get(self):
        response = self.client.get('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a26e/')
        self.assertEqual(response.status_code, 200)

    # test for POST on /service/posts/postid/
    def test_post_id_post(self):
        response = self.client.post('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a268/', {"post_title": "no", "post_id": "c4d924d8-caaf-4470-ad7d-ae0e4714a268", "post_text": "no", "post_author": {"user": 63, "github_username": "jeff", "picture": "http://cs410.cs.ualberta.ca:41071/service/author/63/static/profile_images/gamersky_034origin_067_20131111227AA2.jpg", "approved": True, "author_details": {"url": "http://cs410.cs.ualberta.ca:41071/service/users/63/", "username": "jeff", "email": "jeff@gmail.com", "is_staff": False}}, "visibility": "PUBLIC", "markdown": False}, format='json')
        self.assertEqual(response.status_code, 200)

    # test for PUT on /service/posts/postid/
    def test_post_id_put(self):
        response = self.client.put('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a26e/', {"post_title": "no", "post_id": "c4d924d8-caaf-4470-ad7d-ae0e4714a26e", "post_text": "no", "post_author": {"user": 63, "github_username": "jeff", "picture": "http://cs410.cs.ualberta.ca:41071/service/author/63/static/profile_images/gamersky_034origin_067_20131111227AA2.jpg", "approved": True, "author_details": {"url": "http://cs410.cs.ualberta.ca:41071/service/users/63/", "username": "jeff", "email": "jeff@gmail.com", "is_staff": False}}, "visibility": "PUBLIC", "markdown": False}, format='json')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()

class PostIDTestUnauth(APITestCase):

    client = APIClient()

    # test for un-authenticated client
    def test_post_id_get_unauth(self):
        response = self.client.get('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a26e/')
        self.assertEqual(response.status_code, 403)

    # test for un-authenticated client
    def test_post_id_post_unauth(self):
        response = self.client.post('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a268/', {"post_title": "no", "post_id": "c4d924d8-caaf-4470-ad7d-ae0e4714a268", "post_text": "no", "post_author": {"user": 63, "github_username": "jeff", "picture": "http://cs410.cs.ualberta.ca:41071/service/author/63/static/profile_images/gamersky_034origin_067_20131111227AA2.jpg", "approved": True, "author_details": {"url": "http://cs410.cs.ualberta.ca:41071/service/users/63/", "username": "jeff", "email": "jeff@gmail.com", "is_staff": False}}, "visibility": "PUBLIC", "markdown": False}, format='json')
        self.assertEqual(response.status_code, 403)

    # test for un-authenticated client
    def test_post_id_put_unauth(self):
        response = self.client.put('/service/posts/c4d924d8-caaf-4470-ad7d-ae0e4714a26e/', {"post_title": "no", "post_id": "c4d924d8-caaf-4470-ad7d-ae0e4714a26e", "post_text": "no", "post_author": {"user": 63, "github_username": "jeff", "picture": "http://cs410.cs.ualberta.ca:41071/service/author/63/static/profile_images/gamersky_034origin_067_20131111227AA2.jpg", "approved": True, "author_details": {"url": "http://cs410.cs.ualberta.ca:41071/service/users/63/", "username": "jeff", "email": "jeff@gmail.com", "is_staff": False}}, "visibility": "PUBLIC", "markdown": False}, format='json')
        self.assertEqual(response.status_code, 403)

''' For /service/posts/ API calls '''
class PostTest(APITestCase):

    client = APIClient(enforce_csrf_checks=True)

    def setUp(self):
        u = User.objects.create_superuser(username='apitest3', email='apitest3@apitest.com', password='apitest3')
        u.save()
        login = self.client.login(username = 'apitest3', password = 'apitest3')
        self.assertTrue(login)

    # test for GET on /service/posts/
    def test_post_get(self):
        response = self.client.get('/service/posts/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()

class PostTestUnauth(APITestCase):

    client = APIClient()

    # test for un-authenticated client
    def test_post_get_unauth(self):
        response = self.client.get('/service/posts/')
        self.assertEqual(response.status_code, 403)

''' For /service/friendrequest/ API calls '''
class FriendRequestTest(APITestCase):

    client = APIClient(enforce_csrf_checks=True)

    def setUp(self):
        u = User.objects.create_superuser(username='apitest4', email='apitest4@apitest.com', password='apitest4')
        u.save()
        login = self.client.login(username = 'apitest4', password = 'apitest4')
        self.assertTrue(login)

    # test for POST on /service/friendrequest/
    def test_fr(self):
        response = self.client.post('/service/friendrequest/', {"query":"friendrequest", "author":{"id":"67", "host":"http://127.0.0.1:5454/", "displayname":"1"}, "friend": {"id":"68", "host":"http://127.0.0.1:5454/", "displayname":"2", "url":"http://localhost:9000/service/author/68/"}}, format='json')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()

class FriendRequestTestUnauth(APITestCase):

    client = APIClient()

    # test for un-authenticated client
    def test_fr_unauth(self):
        response = self.client.post('/service/friendrequest/', {"query":"friendrequest", "author":{"id":"67", "host":"http://127.0.0.1:5454/", "displayname":"1"}, "friend": {"id":"68", "host":"http://127.0.0.1:5454/", "displayname":"2", "url":"http://localhost:9000/service/author/68/"}}, format='json')
        self.assertEqual(response.status_code, 403)

''' For /service/author/ API calls '''
class AuthorTest(APITestCase):

    client = APIClient(enforce_csrf_checks=True)

    def setUp(self):
        u = User.objects.create_superuser(username='apitest5', email='apitest5@apitest.com', password='apitest5')
        u.save()
        login = self.client.login(username = 'apitest5', password = 'apitest5')
        self.assertTrue(login)

    # test for GET on /service/author/posts/
    def test_author(self):
        response = self.client.get('/service/author/posts/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()

class AuthorTestUnauth(APITestCase):

    client = APIClient()

    # test for un-authenticated client
    def test_author_unauth(self):
        response = self.client.get('/service/author/posts/')
        self.assertEqual(response.status_code, 403)

''' For /service/author/{ID} API calls '''
class AuthorIDTest(APITestCase):

    client = APIClient(enforce_csrf_checks=True)

    def setUp(self):
        u = User.objects.create_superuser(username='apitest6', email='apitest6@apitest.com', password='apitest6')
        u.save()
        login = self.client.login(username = 'apitest6', password = 'apitest6')
        self.assertTrue(login)

    # test for GET on /service/author/userid/
    def test_author_id(self):
        response = self.client.get('/service/author/63/')
        self.assertEqual(response.status_code, 404)

    # test for GET on /service/author/userid/posts/
    def test_author_id_posts(self):
        response = self.client.get('/service/author/63/posts/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()

class AuthorIDTestUnauth(APITestCase):

    client = APIClient()

    # test for un-authenticated client
    def test_author_id_unauth(self):
        response = self.client.get('/service/author/63/')
        self.assertEqual(response.status_code, 404)

    # test for un-authenticated client
    def test_author_id_posts_unauth(self):
        response = self.client.get('/service/author/63/posts/')
        self.assertEqual(response.status_code, 403)

''' For /service/foaf/ API calls '''
class FoaFTest(APITestCase):

    client = APIClient(enforce_csrf_checks=True)

    def setUp(self):
        u = User.objects.create_superuser(username='apitest7', email='apitest7@apitest.com', password='apitest7')
        u.save()
        login = self.client.login(username = 'apitest7', password = 'apitest7')
        self.assertTrue(login)

    # test for GET on /service/foaf/getposts/
    def test_FoaF(self):
        response = self.client.get('/service/foaf/getposts/', {"query":"getpost", "id":"63", "author":{"id":"66", "host":"http://127.0.0.1:5454/", "displayname":"Greg"}, "friends":["67", "68"]}, format='json')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()

class FoaFTestUnauth(APITestCase):

    client = APIClient()

    # test for un-authenticated client
    def test_FoaF_unauth(self):
        response = self.client.get('/service/foaf/getposts/', {"query":"getpost", "id":"63", "author":{"id":"66", "host":"http://127.0.0.1:5454/", "displayname":"Greg"}, "friends":["67", "68"]}, format='json')
        self.assertEqual(response.status_code, 403)

#following types of test to be done
#http://www.django-rest-framework.org/api-guide/testing/

#http://blog.pedesen.de/2013/06/05/Testing-django-rest-framework-API-with-TokenAuthentication/

#https://www.udacity.com/wiki/cs258/all-any




