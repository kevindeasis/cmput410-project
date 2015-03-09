from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User

from SocialNetworkModels.models import Author

class AuthorMethodTests(TestCase):

	def test_create_author(self):
		usr = User(username='test', password='')
		auth = Author(user=usr, github_username='', picture='')
		auth.save()
		self.assertEqual((auth.user == usr), True)
