from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, redirect,render_to_response
from SocialNetworkModels.models import Posts, Comments, Author, Friends, FriendManager, Follows, FollowManager, FriendManager
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from urlparse import urlparse
from django.db import IntegrityError
from django.contrib import messages
import requests
#from django.core.serializers.json import DjangoJSONEncoder
#from django.core import serializers

import json

#user login page
def user_login(request):
    #test if user can successfully login
    error =False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(username=username, password=password)
            u = User.objects.get(username=username)
            if user!=None:
                if u.username == 'admin':
                    login(request, user)
                    return redirect('/home')
                elif u.post_author.approved:
                    login(request, user)
                    return redirect('/home')
                else:
                    return render(request, 'LandingPage/login.html',{'error': 'Please wait for approval'})
            else:
                error = True
                return render(request, 'LandingPage/login.html',{'error': error})
        except:
            error = True
            return render(request, 'LandingPage/login.html',{'error': error})
    elif request.method == 'GET':
        if request.user.is_authenticated():
            return redirect('/home')
        else:
            return render(request, 'LandingPage/login.html',{'error': error})

    else:
        return render(request, 'LandingPage/login.html',{'error': error})
    
#home page, display after user login successfully
@login_required   
def home(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            user = request.user
            post = Posts.objects.all()
            ourfriend=[]
            FOAF=[]
            allfriends =Friends.friendmanager.getFriends(request.user)
            #get friend of user
            for afriend in allfriends:
                ourfriend.append(afriend.reciever.get_username())
                friendOfFriend =Friends.friendmanager.getAll(afriend)
                for friend in friendOfFriend:
                    if friend.reciever.get_username() not in FOAF and friend.reciever.get_username() != request.user:
                        FOAF.append(friend.reciever.get_username())
            print ourfriend, FOAF 
	    comments = Comments.objects.all()   
            #friends = Friends.objects.all()
            #return HttpResponse(len(post))
            count = 0
	    if post !=None:
		count =1
	    receive=[]
	    try:
		response=requests.get('http://social-distribution.herokuapp.com/api/author/posts',auth=('team7','cs410.cs.ualberta.ca:team6'))
		#return HttpResponse(json.dumps(response.json()),content_type='text/plain')
		response=response.json()
		p = json.loads(json.dumps(response))
	    except:
		return render(request, 'LandingPage/home.html',{'posts':post, 'user':user, 'FOAF':FOAF,'friends':ourfriend,'lenn':count, 'comments':comments,})
            try:
                return render(request, 'LandingPage/home.html',{'posts':post, 'user':user, 'FOAF':FOAF,'friends':ourfriend,'lenn':count, 'comments':comments,'getPost':p['posts']})
            except Author.DoesNotExist:
                return render(request, 'LandingPage/login.html',{'error': False})   
    elif request.method =='POST':
        return render(request, 'LandingPage/home.html')


def register(request):
    context= RequestContext(request)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        github_username= request.POST.get('github')
        picture = request.FILES.get('picture')
        
        if len(User.objects.filter(username =username))>0:
            return render(request, 'LandingPage/register.html',{'username':'username already exist'})
        else:
            if username != None and password != None:
                user=User.objects.create_user(username ,email,password)
                user.save()
                author= Author.objects.create(user=user,github_username=github_username,picture = picture )
                author.save()
                return redirect('/login')

    return render(request, 'LandingPage/register.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def search_users(request):
    #search for users
    if request.method == 'GET':
        if request.user.is_authenticated():
            try:
                #this needs to be paginated later
                authors = Author.objects.all()

                foreignauthors = {}

                # try 2: always throws exception
                # response=response.json() keeps raising exception
                try:
                    response=requests.get('http://social-distribution.herokuapp.com/api/author/',auth=('team7','cs410.cs.ualberta.ca:team6'))
                    response=response.json()
                except Exception, e:
                    pass
                else:
                    foreignauthors = json.loads(json.dumps(response))

                # try 1: should work?
                #response=requests.get('http://social-distribution.herokuapp.com/api/author/',auth=('team7','cs410.cs.ualberta.ca:team6'))
                #response=response.json()
                #foreignauthors = json.loads(json.dumps(response))

                #follows = Follows()
                followed = Follows.followManager.getFollowing(request.user)
                allfriends = Friends.friendmanager.getFriends(request.user)
                allpending = Friends.friendmanager.getAll(request.user)



                #if this got turned into a json, can do client side
                ourfollows = []
                for afollow in followed:
                    ausername = afollow.followed.get_username()
                    ourfollows.append('{s}'.format(s=ausername))

                #find the user/authors friends
                ourfriends = []
                for afriend in allfriends:
                    afriendusername = afriend.reciever.get_username()
                    ourfriends.append('{s}'.format(s=afriendusername))

                pendingrequests = []
                for apending in allpending:
                    afriendusername = apending.reciever.get_username()
                    pendingrequests.append('{s}'.format(s=afriendusername))

                return render(request, 'LandingPage/search_users.html', {'authors': authors, 'followed': ourfollows, 'allfriends': ourfriends,'allpending': pendingrequests, 'username': request.user.username, 'foreignauthors': foreignauthors})
            except Author.DoesNotExist:
                return redirect('/login')
    else:
        return redirect('/login')



@login_required
def search_posts(request):
    #search for users
    if request.method == 'GET':
        if request.user.is_authenticated():
            try:
                #this needs to be paginated later
                posts = Posts.objects.all()
                return render(request, 'LandingPage/search_users.html',{'posts': posts})
            except Author.DoesNotExist:
                return redirect('/login')
    else:
        return redirect('/login')

@login_required
def follow(request, reciever_pk):
    #actually right now your adding following
    #search for users
    if request.user.is_authenticated():
        try:

            #follows = Follows()
            #mainuser = User.objects.get(username = request.user)
            #tobefollowed = User.objects.get(pk = reciever_pk)
            #follows.save()
            #Follows.followManager.create(followed=tobefollowed, follower=mainuser)


            if(Follows.followManager.isFollowing(User.objects.get(pk = reciever_pk), User.objects.get(username = request.user))):
                Follows.followManager.get(followed=User.objects.get(pk = reciever_pk),follower=User.objects.get(username=request.user)).delete()

            Follows.followManager.create(followed=User.objects.get(pk = reciever_pk),follower=User.objects.get(username=request.user))

            try:
                previousfollowed = Follows.followManager.getFollowers(request.user)
                previousfollower = User.objects.get(pk = reciever_pk).username
                #following = Follows.followManager.getFollowing(previousfollower)

                ausername = ''
                test = False
                for afollow in previousfollowed:
                    ausername = afollow.getafollower
                    busername = User.objects.get(username = ausername).username
                    #return HttpResponse(previousfollower == busername)
                    if(previousfollower == busername):
                        test = True
                        break

                if (test == True):
                    friend = Friends()
                    friend.initiator = User.objects.get(username = request.user)
                    friend.reciever = User.objects.get(pk = reciever_pk)
                    friend.save()

                return redirect('/searchusers')
            except:
                return redirect('/searchusers')

            return redirect('/searchusers')

        except Author.DoesNotExist:
            return redirect('/searchusers')
    else:
        return redirect('/home')

@login_required
def unfriend(request, reciever_pk):
    #return HttpResponse(request.user) utf?

    #try:
    Follows.followManager.mutualFollow(User.objects.get(username = request.user), User.objects.get(username = reciever_pk))

    inst = Friends.friendmanager.get(initiator=User.objects.get(username = request.user),reciever=User.objects.get(username = reciever_pk))
    inst2 = Friends.friendmanager.get(initiator=User.objects.get(username = reciever_pk),reciever=User.objects.get(username = request.user))
    inst.delete()
    inst2.delete()
    return redirect('/home')

@login_required
def unfollow(request, reciever_pk):
    if request.user.is_authenticated():
        try:
            follows = Follows.followManager.get(follower=User.objects.get(username = request.user),followed = User.objects.get(pk = reciever_pk))
            follows.delete()
            return redirect('/searchusers')

        except Author.DoesNotExist:
            return redirect('/searchusers')
    else:
        return redirect('/home')

@login_required
def addfriend(request, reciever_pk):
    try:
        Friends.friendmanager.mutualFriends(User.objects.get(username = request.user),User.objects.get(pk = reciever_pk))
    except:
        return redirect('/searchusers')
    return redirect('/searchusers')


@login_required
def confirmfriend(request, reciever_pk):
    #return HttpResponse(request.user) utf?

    #try:
    Follows.followManager.mutualFollow(User.objects.get(username = request.user), User.objects.get(username = reciever_pk))

    inst = Friends.friendmanager.get(initiator=User.objects.get(username = request.user),reciever=User.objects.get(username = reciever_pk))
    inst2 = Friends.friendmanager.get(initiator=User.objects.get(username = reciever_pk),reciever=User.objects.get(username = request.user))
    inst.delete()
    inst2.delete()
    Friends.friendmanager.addFriend(User.objects.get(username = request.user),User.objects.get(username = reciever_pk))
    #except:
    #    return redirect('/xhz')
    return redirect('/searchusers')

@login_required
def viewfriendrequests(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            try:

                #Youll need to move mutual follow here
                allfriends = Friends.friendmanager.getRequests(request.user)

                #find the user/authors requests
                ourfriends = []
                for afriend in allfriends:
                    afriendusername = afriend.reciever.get_username()
                    ourfriends.append('{s}'.format(s=afriendusername))

                return render(request, 'LandingPage/confirmfriendrequest.html', {'allfriendrequest': ourfriends, 'username': request.user.username})
            except Author.DoesNotExist:
                return redirect('/login')
    else:
        return redirect('/login')

'''
@login_required
def testaddfriend(request, reciever_pk):
    try:
        Friends.friendmanager.mutualFriends(User.objects.get(username = request.user),User.objects.get(pk = reciever_pk))
    except:
        return redirect('/searchusers')
    return redirect('/searchusers')'''


@login_required
def author_post(request):
    if request.method =='POST':
        title = request.POST.get('post_title')
        text = request.POST.get('post_text')
        visibility = request.POST.get('visibility')
        picture = request.FILES.get('picture')     
	mark_down = request.POST.get('markdown')   
        #post =Posts.objects.create(post_author = request.user.username, 
                                  #psot_title = title, post_text= text,visibility= visibility)
        post = Posts()
        post.post_author = Author.objects.get(user = request.user)
        post.post_title = title
        post.post_text = text
        post.visibility = visibility
        post.image = None
        if picture is not None:
            post.image=picture

        if mark_down is not None:
            post.mark_down= True
        post.save()
        return redirect('/home')
    else:
        return render(request, 'LandingPage/post.html')
        
    return render(request, 'LandingPage/post.html')


@login_required
def author_post_comment(request, post_id, author):
    if request.method =='POST':
        comment_text = request.POST.get('comment')
        #post =Posts.objects.create(post_author = request.user.username, 
                                  #psot_title = title, post_text= text,visibility= visibility)
        comment = Comments()
        
        comment.post_id = post_id
        comment.comment_author = author
        comment.comment_text = comment_text

        comment.save()
        return redirect('/home')
    else:
	return redirect('/home')
        
    return render(request, '/home')



@login_required
def author_post_delete(request,post_id):
    user = request.user
    try:
	post = Posts.objects.get(post_id = post_id)
    except:
	response=requests.get('http://social-distribution.herokuapp.com/api/posts/%s'%(post_id),auth=('team7','cs410.cs.ualberta.ca:team6')) 
	#return HttpResponse(json.dumps(response.json()),content_type='text/plain')
	response=response.json()
	p = json.loads(json.dumps(response))
	post =Posts()
	#post.post_author = None
	post.post_title  = p['title']
	post.post_text = p['content']
	post.visibility =p['visibility']
	post.post_id = post_id
	post.image = None	
	context = 'you have no permissions to delete this post'
	return render(request, 'LandingPage/display.html',{'message':context,'post':post})
    conText = ''
   
    if user.post_author !=post.post_author:
        context = 'you have no permissions to delete this post'
        return render(request, 'LandingPage/display.html',{'message':context,'post':post})
    else:
        post.delete()
        return redirect('/home')

@login_required
def display_post(request,post_id):
    try:
	post = Posts.objects.get(post_id = post_id)
    except:
	response=requests.get('http://social-distribution.herokuapp.com/api/posts/%s'%(post_id),auth=('team7','cs410.cs.ualberta.ca:team6')) 
	#return HttpResponse(json.dumps(response.json()),content_type='text/plain')
	response=response.json()
	p = json.loads(json.dumps(response))
	post =Posts()
	#post.post_author = None
	post.post_title  = p['title']
	post.post_text = p['content']
	post.visibility =p['visibility']
	post.post_id = post_id
	post.image = None
    return render(request,'LandingPage/display.html',{'post':post})
    
@login_required
def author_post_edit(request,post_id):
    if request.method =="GET":
        user = request.user
	try:
	    post = Posts.objects.get(post_id = post_id)
	except:
	    response=requests.get('http://social-distribution.herokuapp.com/api/posts/%s'%(post_id),auth=('team7','cs410.cs.ualberta.ca:team6')) 
	    #return HttpResponse(json.dumps(response.json()),content_type='text/plain')
	    response=response.json()
	    p = json.loads(json.dumps(response))
	    post =Posts()
	    #post.post_author = None
	    post.post_title  = p['title']
	    post.post_text = p['content']
	    post.visibility =p['visibility']
	    post.post_id = post_id
	    post.image = None		    
	    context = 'you have no permissions to edit this post'
	    return render(request, 'LandingPage/display.html',{'message':context,'post':post})	    
        conText = ''
        if user.post_author !=post.post_author:
            context = 'you have no permissions to edit this post'
            return render(request, 'LandingPage/display.html',{'message':context,'post':post})
        else:
            return render(request, 'LandingPage/post.html',{'edit':'1','post':post})
    elif request.method =="POST":
        post = Posts.objects.get(post_id = post_id)
        post.post_title = request.POST.get('post_title')
        post.post_text = request.POST.get('post_text')
        post.visibility = request.POST.get('visibility')
        image = request.FILES.get('picture')
	mark_down = request.POST.get('markdown')
        if image is not None:
            post.image=image

	if mark_down is not None:
	    post.mark_down = True
	else:
	    post.mark_down = False
	
        post.save()
    return render(request, 'LandingPage/display.html',{'post':post})
        
        

@login_required
def profile(request,edit):
    if request.user.is_authenticated():
        if request.method =='GET':
            author = Author.objects.get(user =request.user)
            username = author.user.username
            email = author.user.email
            github_username=author.github_username
            picture = author.picture
	    post = Posts.objects.all()
            return render(request, 'LandingPage/profile.html',{'username':username, 'email':email,'github_username' :github_username,'picture':picture,'posts':post,'edit':edit})
    return render(request, 'LandingPage/profile.html')

@login_required
def profile_post(request,user_id,edit):
    if request.user.is_authenticated():
        if request.method =='GET':
	    try:
		user1 = User.objects.get(username = user_id)
		author = Author.objects.get(user = user1)
		username = author.user.username
		email = author.user.email
		github_username=author.github_username
		picture = author.picture
		post = Posts.objects.all()
		return render(request, 'LandingPage/profile.html',{'username':username, 'email':email,'github_username' :github_username,'picture':picture,'posts':post,'edit':edit})
	    except:
		response=requests.get('http://social-distribution.herokuapp.com/api/author/%s'%(user_id),auth=('team7','cs410.cs.ualberta.ca:team6')) 
		#return HttpResponse(json.dumps(response.json()),content_type='text/plain')
		response=response.json()
		p = json.loads(json.dumps(response))
		
		
		response=requests.get('http://social-distribution.herokuapp.com/api/author/%s/posts'%(user_id),auth=('team7','cs410.cs.ualberta.ca:team6')) 
		#return HttpResponse(json.dumps(response.json()),content_type='text/plain')
		response=response.json()
		a = json.loads(json.dumps(response))		
		return render(request, 'LandingPage/profile.html',{'username':p['displayname'],'post':a['posts'],'edit':edit})
    return render(request, 'LandingPage/profile.html')

@login_required
def profile_edit(request):
    '''
    This view is used to edit the profile for the currently logged in user
    '''
    context = RequestContext(request)
    
    if request.method == "POST":
        author = request.user.post_author
        username = request.POST.get('username')
        email = request.POST.get('email')
        github_username = request.POST.get('github_username')	
        picture = request.FILES.get('picture')

        if username is not None and username != '':
            request.user.username = username

        if email is not None and email != '':
            request.user.email = email

        # Update: also set the github account:
        if github_username is not None:
            author.github_username = github_username

        if picture is not None:
            author.picture = picture

        try:
            # Save the User first
            request.user.save()
            # Save the Author last
            author.save()

            # Add a success flash message
            messages.info(request, "Your profile was updated successfully.")

            # Send the user to the profile screen
            return redirect('/home')
        except IntegrityError, e:
            if "username" in e.message:
                # Add the username error
                messages.error(request, "Username is already taken.")
            elif "email" in e.message:
                # Add the email error
                messages.error(request, "An account is associated to that email.")
            else:
                # Add the generic error
                messages.error(request, e.message)
        except Exception, e:
            # Add the generic error
            messages.error(request, e.message)

    return render_to_response('main/profile.html', {}, context)
