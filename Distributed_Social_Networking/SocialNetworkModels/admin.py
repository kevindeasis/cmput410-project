from django.contrib import admin
#from SocialNetworkModels.models import Author, Posts
from SocialNetworkModels.models import Author, Posts, Friends, FriendManager, Follows, FollowManager, FriendManager,Nodes
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class AuthorInLine(admin.StackedInline):
    model = Author
    list_display = ('approved')

class UserAdmin(admin.ModelAdmin):
    inlines = [AuthorInLine]
    list_display = ('username', 'email', 'first_name', 'last_name', 'approved')

    def approved(self, obj):
        return obj.post_author.approved
    approved.admin_order_field = 'approved'
    approved.boolean = True

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Author)
admin.site.register(Follows)
admin.site.register(Posts)
admin.site.register(Friends)
admin.site.register(Nodes)
