from django import forms
from SocialNetworkModels.models import Author,Posts


class AuthorForm(forms.ModelForm):
    author_username = forms.CharField(max_length=128, help_text = "Please enter name")

    author_email = forms.CharField(max_length=128, help_text = "Please enter name")

    author_password = forms.CharField(max_length=128, help_text = "Please enter name")

    #view = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model = Author
        fields = ('author_username','author_email','author_password',)
        exclude = ('registration_date',)
        
class PostsForm(forms.ModelForm):
    post_text = forms.CharField(max_length=128, help_text = "Please enter title of post")
    number_of_Likes =  forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    
    class Meta:
        model = Posts
        exclude = ('post_author',)
        
        