from django.db import models

# Create your models here.
from django.db import models

#   We can refactor these classes into their own files later
#   These are models that can be accessible for the administrators
#   Check: https://docs.djangoproject.com/en/1.7/intro/tutorial01/


class Author(models.Model):
    author_username = models.CharField(max_length=200)
    author_email = models.CharField(max_length=200)
    author_password = models.CharField(max_length=200)
    registration_date = models.DateTimeField('date registered')
    
    def __str__(self):
        return self.author_username


class Posts(models.Model):
    post_author = models.ForeignKey(Author)
    post_text = models.CharField(max_length=200)
    number_of_Likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.post_text
    