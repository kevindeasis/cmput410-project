from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client

from SocialNetworkModels.models import Posts, Author, Friends, FriendManager
from django.contrib.auth.models import User

from . import models
import factory

import nose.tools as noto

#testing doesnt use the database for models it creates a new pseudo database!
class UserFactory(factory.Factory):
    class Meta:
        model = models.User

    first_name = 'testuser'
    last_name = 'testlastname'
    is_superuser = False

class SuperFactory(factory.Factory):
    class Meta:
        model = models.User

    first_name = 'superuser'
    last_name = 'superpassword'
    username = 'superpassword'
    password = 'superpassword'

    is_superuser = True

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

class Test_Author_Auth(TestCase):
    client = Client()

    #not saved
    user = UserFactory.build()
    superuser = SuperFactory.build()

    #saved
    #user = UserFactory.create()

    #this guy isnt approved by the server administrator so he shouldnt get a 200
    #this guy isnt registered as an author so he cant get a 200
    def test_noaccess(self):
        response = self.client.post('/home/', {'username': self.user.username, 'password': self.user.password})
        self.assertFalse((self.client.login()))

    def test_noaccess2(self):
        response = self.client.login(username= self.user.username, password = self.user.password)
        self.assertFalse((self.client.login()))

    def test_access(self):
        newclient = Client()

        user = User.objects.create_user('superpassword3', 'email@ems3ail.com', 'superpassword3')
        user.save
        response = newclient.login(username = 'superpassword3', password = 'superpassword3')

        self.assertTrue((response.redirect_chain[0][0]))

    def test_access(self):
        newclient = Client()

        user = User.objects.create_user('superpassword2', 'email2@emsail.com', 'superpassword1')
        user.save
        author = Author()
        author.user = user
        author.save()

        response = self.client.post('/home/', {'username': 'superpassword2', 'password': 'superpassword1'}, follow = True)
        self.assertRedirects(response, 'http://testserver/?next=/home/')

    def test_has_access(self):
        newclient = Client()

        user = User.objects.create_user('2superpassword2', '2email2@emsail.com', '2superpassword1')
        author = Author()
        author.user = user
        author.approved = True
        author.save()
        user.save

        response = self.client.post('/login/', {'username': '2superpassword2', 'password': '2superpassword1'},follow = True)
        self.assertRedirects(response, 'http://testserver/home/')


class Test_User_Auth(TestCase):
    client = Client()

    #not saved
    user = UserFactory.build()
    superuser = SuperFactory.build()

    #this guy isnt approved by the server administrator so he shouldnt get a 200
    #this guy isnt registered as an author so he cant get a 200
    def test_noaccess(self):
        response = self.client.post('/home/', {'username': self.user.username, 'password': self.user.password})
        self.assertFalse((self.client.login()))

    def test_noaccess2(self):
        response = self.client.login(username= self.user.username, password = self.user.password)
        self.assertFalse((self.client.login()))

    #this is the admin so he should be good
    def test_access(self):
        newclient = Client()

        user = User.objects.create_user('superpassword1', 'email@emsail.com', 'superpassword1')
        #user.is_superuser = True
        user.save
        #print user.is_superuser
        response = newclient.login(username = 'superpassword1', password = 'superpassword1')
        self.assertTrue((response))


class Test_Profile(TestCase):
    client = Client()

    # logged in?
    # IMPORTANT: FUNCTION NAME MUST BE setUp !!!
    def setUp(self):
        u = User.objects.create_user(username='myuser1', email='email@emsail.com', password='myuser1')
        u.save()
        author = Author()
        author.user = u
        author.save()
        login = self.client.login(username = 'myuser1', password = 'myuser1')
        self.assertTrue(login)

    # render profile page?
    def test_render_profile(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    # get correct profile data?
    # def test_data_profile()


class Test_Post(TestCase):
    client = Client()

    # logged in?
    # IMPORTANT: FUNCTION NAME MUST BE setUp !!!
    def setUp(self):
        u = User.objects.create_user(username='myuser1', email='email@emsail.com', password='myuser1')
        u.save()
        author = Author()
        author.user = u
        author.save()
        login = self.client.login(username = 'myuser1', password = 'myuser1')
        self.assertTrue(login)

    # render post page?
    def test_render_post(self):
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)


    # render search searchposts page?
    #def test_render_searchposts(self):
        #response = self.client.get('/searchposts/')
        #self.assertEqual(response.status_code, 200)


'''
class Test_Search_User(TestCase):
    client = Client()

    #not saved
    user = UserFactory.build()
    superuser = SuperFactory.build()

    #saved
    #user = UserFactory.create()
'''   

''' 
class Test_Friend(TestCase):
    client = Client()

    #not saved
    user = UserFactory.build()
    superuser = SuperFactory.build()

    #saved
    #user = UserFactory.create()
'''   

    

'''
#tutorials
#https://docs.djangoproject.com/en/1.7/topics/testing/tools/
#http://www.marinamele.com/2014/03/tools-for-testing-in-django-nose.html
#http://factoryboy.readthedocs.org/en/latest/
#http://factoryboy.readthedocs.org/en/latest/
#https://docs.djangoproject.com/fr/1.5/topics/testing/advanced/
'''
