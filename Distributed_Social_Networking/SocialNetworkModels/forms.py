from django import forms
#from SocialNetworkModels.models import Author,Posts, UserProfile
from django.contrib.auth.models import User
from SocialNetworkModels.models import AuthorProfile



"""
class AuthorForm(forms.ModelForm):
    author_username = forms.CharField(max_length=200, help_text = "Please enter name")
    author_email = forms.CharField(max_length=200, help_text = "Please enter name")
    author_password = forms.CharField(max_length=200, help_text = "Please enter name")

    #view = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model = Author
        fields = ('author_username','author_email','author_password',)
        #exclude = ('registration_date',)
        
class PostsForm(forms.ModelForm):
    post_text = forms.CharField(max_length=200, help_text = "Please enter title of post")
    number_of_Likes =  forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model = Posts
        exclude = ('post_author',)
"""
class AuthorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = AuthorProfile
        fields = ('website', 'picture')


        