from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client

from SocialNetworkModels.models import Posts, Author, Friends, FriendManager
from django.contrib.auth.models import User

import factory
#http://factoryboy.readthedocs.org/en/latest/

import nose.tools as noto


class Test_URL(TestCase):
    client = Client()

    #index page
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

#home page not 200
    def test_home(self):
        resp = self.client.get('/home/')
        self.assertEqual(resp.status_code, 302)


class Test_Authorization(TestCase):

    client = Client()
    #this is index page
    def test_admin_login(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

    #this is denied authentication
    def test_not_admin(self):
        response = self.client.post('/admin/')
        self.assertEqual(response.status_code, 302)


    #this is checking authorization and authentication
    def test_admin_access(self):
        response = self.client.post('/admin/', {'username': 'admin', 'password': 'admin'},follow=True)
        self.assertEqual(response.status_code, 200)

    #this is checking authorization and authentication
    def test_no_access(self):
        response = self.client.post('/admin/', {'username': 'abc', 'password': 'def'})
        assert response.status_code is not 200

    #this is checking authorization and authentication
    def test_invalid_access(self):
        response = self.client.post('/admin/', {'username': 'admin', 'password': 'qrs#'})
        assert response.status_code is not 200

class Test_Login(TestCase):

    client = Client()
    #this is checking authorization and authentication
    def test_no_access(self):
        response = self.client.post('/home/', {'username': 'admin', 'password': 'admin'}, follow=True)
        self.assertEqual(response.status_code, 200)



'''
#tutorials
#https://docs.djangoproject.com/en/1.7/topics/testing/tools/
#http://www.marinamele.com/2014/03/tools-for-testing-in-django-nose.html
#http://factoryboy.readthedocs.org/en/latest/

FUTURE IMPLEMENTATION
#https://docs.djangoproject.com/fr/1.5/topics/testing/advanced/
#for our rest interface
class AuthorFactory(factory.DjangoModelFactory):
    FATORY_FOR = Author
    user = user...

class UserFactory(factory.Factory):
    class Meta:
        model = models.first

    first_name = 'testuser'
    last_name = 'testlastname'
    admin = False'''
