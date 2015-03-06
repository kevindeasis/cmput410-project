from django.contrib import admin
#from SocialNetworkModels.models import Author, Posts
from SocialNetworkModels.models import AuthorProfile, Posts


# Register your models here.

"""
class PostInline(admin.StackedInline):
    model = Posts
    extra = 5
    

class AuthorAdmin(admin.ModelAdmin):
    #fields = ['author_username','registration_date', 'author_email']
    
    fieldsets = [
        (None,                 {'fields':['author_username']}),
        #('Registration Date',  {'fields':['registration_date']}),
        ('Email',              {'fields':['author_email']}),
    ]
    
   # list_display = ('author_username','registration_date','author_email')
    list_display = ('author_username','author_email')
    
    
    inlines = [PostInline]
    
admin.site.register(Author, AuthorAdmin)"""

class PostInline(admin.StackedInline):
    model = Posts
    fk_name = 'post_author'
    extra = 3

class AuthorAdmin(admin.ModelAdmin):
    inlines = [PostInline]

admin.site.register(AuthorProfile, AuthorAdmin)
admin.site.register(Posts)

#admin.site.register(AuthorProfile)

