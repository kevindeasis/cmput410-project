import os
import django

def populate():

    # populate User
    alluser = {
        'Marry': add_user('Marry','marry@mail.com','marry'),
        'Kate': add_user('Kate','kate@mail.com','kate'),
        'Tom': add_user('Tom','tom@mail.com','tom'),
        'John': add_user('John','john@mail.com','john'),
    }
    
    # populate Author
    allauthor = {
        'Marry': add_author(alluser['Marry'],'marrygit'),
        'Kate': add_author(alluser['Kate'],'kategit'),
        'Tom': add_author(alluser['Tom'],'tomgit'),
        'John': add_author(alluser['John'],'johngit'),
    }

    # populate Friend
    add_friend(allauthor['Marry'], allauthor['Kate'])
    add_friend(allauthor['Marry'], allauthor['Tom'])
    add_friend(allauthor['Kate'], allauthor['Tom'])
    add_friend(allauthor['Tom'], allauthor['Kate'])
    add_friend(allauthor['Tom'], allauthor['John'])

def add_user(username, email, password):
    user = User.objects.create_user(username ,email,password)
    user.save()
    return user

def add_author(user, github_username):
    author = Author.objects.create(user=user, github_username=github_username)
    author.save()
    return author
  
def add_friend(author, friend):
    author.friends.add(friend)    

# Start execution here!
if __name__ == '__main__':
    print "Starting Django population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Distributed_Social_Networking.settings')
    django.setup()
    from SocialNetworkModels.models import Author, Posts
    from django.contrib.auth.models import User
    populate()
