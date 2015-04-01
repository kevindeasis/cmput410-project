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

class FirstLayerServiceTest(APITestCase):

    client = Client()

    def test_first_layer(self):
        #url = reverse('url_service')
        response = self.client.get('/service/')
        self.assertEqual(response.status_code, 200)

class DeniedAuthenticationTest(APITestCase):

    client = Client()

    def test_author(self):
        response = self.client.get('/service/author/posts/', follow=True)
        self.assertEqual(response.status_code, 403)


#following types of test to be done
#http://www.django-rest-framework.org/api-guide/testing/

#http://blog.pedesen.de/2013/06/05/Testing-django-rest-framework-API-with-TokenAuthentication/

#https://www.udacity.com/wiki/cs258/all-any




