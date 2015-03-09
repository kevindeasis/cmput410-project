#from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django_extensions.db.fields import UUIDField


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

#to be implemented
class SiteBlockedAccount(models.Model):
class UserBlockedUser(models.Model):
class Follow(models.Model):
class FriendRequest(models.Model):
class FriendFactory(models.Model):
class InviteEmail(models.Model):

#Required to be default as stated in the user stories
class SiteBlockedAccount(models.Model):
"""

class Author(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    github_username = models.CharField(max_length=128, blank=True)
    picture = models.ImageField(upload_to='static/profile_images/', blank = True)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username


#if you wanna know what this is doing:
#https://godjango.com/51-better-models-through-custom-managers-and-querysets/
#https://docs.djangoproject.com/en/1.6/topics/db/managers/
class FriendManager(models.Manager):

    #call this by Friends.friendmanager.getFriends(authorname)
    def getFriends(self, authorname):
        return self.get_queryset().filter(initiator=authorname)

class FollowManager(models.Manager):

    #call this by Follows.followmanager.getFollowers(authorname)
    def getFollowers(self, followed):
        return self.get_queryset().filter(followed=followed)

    def getFollowing(self, follower):
        return self.get_queryset().filter(follower=follower)

class Follows(models.Model):
    followed = models.ForeignKey(User, related_name='followed')
    follower = models.ForeignKey(User, related_name='follower')

    hide = models.BooleanField(default=False)

    followManager = FollowManager()

    class Meta:
        verbose_name = "Following"
        verbose_name_plural = "Followers"
        unique_together = (('followed', 'follower'),)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        try:
            return "{sender} is followed by {reciever}".format(sender=self.followed, reciever=self.follower)
        except:
            return "{solo} prob has no followers)".format(solo=self.followed)

    def getafollowing(self):
        return self.followed



class Friends(models.Model):
    initiator = models.ForeignKey(User, related_name='initiator')
    reciever = models.ForeignKey(User, related_name='reciever')

    #this can be removed due to the following use case
    sentrequest =  models.BooleanField(default=True)
    approvedrequest = models.BooleanField(default=False)

    fof_private = models.BooleanField(default=False)
    friendmanager = FriendManager()

    class Meta:
        verbose_name = "Friends"
        verbose_name_plural = "Friends"
        unique_together = (('initiator', 'reciever'),)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        try:
            return "{sender} initiated friendship with {reciever}".format(sender=self.initiator, reciever=self.reciever)
        except:
            return "{solo} prob has no friends)".format(solo=self.initiator)


class PostManager(models.Manager):

    def getFriends(self, authorname):
        return self.get_queryset().filter(post_author=authorname)


class Posts(models.Model):
    #create visibility let author choose when they make post
    VISIBILITY=(("PRIVATE","Private"),("PUBLIC","Public"),("FRIENDS","Friends"),("FRIENDSFRIENDS","Friend of a Friend"))
    post_id = UUIDField(primary_key=True, auto=True)
    post_author = models.ForeignKey(Author)
    post_title = models.CharField(max_length = 20)
    post_text = models.CharField(max_length=200)
    visibility = models.CharField(max_length = 10, choices = VISIBILITY,default="PUBLIC")
    image = models.ImageField(upload_to='static/post_images/',blank = True)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.post_author
