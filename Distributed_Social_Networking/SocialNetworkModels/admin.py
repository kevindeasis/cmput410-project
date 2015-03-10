from django.contrib import admin
#from SocialNetworkModels.models import Author, Posts
from SocialNetworkModels.models import Author, Posts, Friends, FriendManager, Follows, FollowManager, FriendManager

admin.site.register(Follows)
admin.site.register(Author)
admin.site.register(Posts)
admin.site.register(Friends)