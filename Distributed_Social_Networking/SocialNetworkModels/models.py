
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django_extensions.db.fields import UUIDField

#   We can refactor these classes into their own files later
class Author(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    github_username = models.CharField(max_length=128, blank=True)
    picture = models.ImageField(upload_to='static/profile_images/', blank = True)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.username

class FriendManager(models.Manager):

    #call this by Friends.friendmanager.getFriends(authorname)
    #everything is mutual
    def getFriends(self, authorname):
        return self.get_queryset().filter(initiator=authorname)

class FollowManager(models.Manager):

    #call this by Follows.followmanager.getFollowers(authorname)
    def getFollowers(self, followed):
        #returns the followers of the arguement
        return self.get_queryset().filter(followed=followed)

    def getFollowing(self, follower):
        #returns the argument is following
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
    def getafollower(self):
        return self.follower

#should really be a friend requrest
class Friends(models.Model):
    initiator = models.ForeignKey(User, related_name='initiator')
    reciever = models.ForeignKey(User, related_name='reciever')

    #this can be removed due to the following use case
    sentrequest =  models.BooleanField(default=False)
    approvedrequest = models.BooleanField(default=False)

    fof_private = models.BooleanField(default=False)
    friend_private = models.BooleanField(default=False)
    own_private = models.BooleanField(default=False)
    remote_private = models.BooleanField(default=False)

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
    VISIBILITY=(("PRIVATE","Private"),("PUBLIC","Public"),("FRIENDS","Friends"),("FOAF","Friend of a Friend"))
    post_id = UUIDField(primary_key=True, auto=True)
    post_author = models.ForeignKey(Author)
    post_title = models.CharField(max_length = 20)
    post_text = models.CharField(max_length=200)
    visibility = models.CharField(max_length = 10, choices = VISIBILITY,default="PUBLIC")
    image = models.ImageField(upload_to='static/post_images/',blank = True)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.post_title


#Tutorials
#if you wanna know what this is doing:
#https://godjango.com/51-better-models-through-custom-managers-and-querysets/
#https://docs.djangoproject.com/en/1.6/topics/db/managers/