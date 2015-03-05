#from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


#   We can refactor these classes into their own files later
#   These are models that can be accessible for the administrators
#   Check: https://docs.djangoproject.com/en/1.7/intro/tutorial01/

"""
class Author(models.Model):
    author_username = models.CharField(max_length=200)
    author_email = models.CharField(max_length=200)
    author_password = models.CharField(max_length=200)
    #registration_date = models.DateTimeField('date registered')
    
    #def __str__(self):
    #    return self.author_username
    
    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.author_username
    """


class AuthorProfile(models.Model):
    user = models.OneToOneField(User)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank = True)

    def __unicode__(self):
        return self.user.username


class Posts(models.Model):
    post_author = models.ForeignKey(AuthorProfile, related_name='post_author')
    post_reciever = models.ForeignKey(AuthorProfile, related_name='post_reciever')
    post_text = models.CharField(max_length=200)
    number_of_Likes = models.IntegerField(default=0)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.post_author


    
    