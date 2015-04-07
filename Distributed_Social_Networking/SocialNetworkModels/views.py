from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, redirect,render_to_response
from SocialNetworkModels.models import Posts, Comments, Author, Friends, FriendManager, Follows, FollowManager, FriendManager,Nodes
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

import logging, logging.config
import sys

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)

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
	    node = Nodes.objects.all()
	    receive=[]
	    receive2=[]
	    count = 0
	    if post !=None:
		count =1
	    if node is not None:
		for i in node:
		    #team 6 connection
		    if i.host_url == "http://social-distribution.herokuapp.com" and i.status == True:
			try:
			    response=requests.get(i.host_url+'/api/author/posts',auth=(i.host_name,i.host_password))
			    response=response.json()
			    p = json.loads(json.dumps(response))
			    receive.append(p)

			except:
			    pass
		    #team 3 connection
		    elif i.host_url == "http://cmput410project15.herokuapp.com" and i.status == True:
			try:
			    response=requests.get(i.host_url+'/main/author/posts',auth=(i.host_name,i.host_password))
			    response=response.json()
			    p = json.loads(json.dumps(response))
			    receive2.append(p)

			except:
			    pass
		    else:
			return render(request, 'LandingPage/home.html',{'posts':post, 'user':user, 'FOAF':FOAF,'friends':ourfriend,'lenn':count, 'comments':comments,})
		try:
		    if len(receive)>0 and len(receive2)>0:
			return render(request, 'LandingPage/home.html',{'posts':post, 'user':user, 'FOAF':FOAF,'friends':ourfriend,'lenn':count, 'comments':comments,'getPost':receive[0]['posts'],'getPost2':receive2[0]['posts']})
		    elif len(receive)>0:
			return render(request, 'LandingPage/home.html',{'posts':post, 'user':user, 'FOAF':FOAF,'friends':ourfriend,'lenn':count, 'comments':comments,'getPost':receive[0]['posts']})
		    elif len(receive2)>0:
			return render(request, 'LandingPage/home.html',{'posts':post, 'user':user, 'FOAF':FOAF,'friends':ourfriend,'lenn':count, 'comments':comments,'getPost2':receive2[0]['posts']})
		    else:
			return render(request, 'LandingPage/home.html',{'posts':post, 'user':user, 'FOAF':FOAF,'friends':ourfriend,'lenn':count, 'comments':comments})
		except Author.DoesNotExist:
		    return render(request, 'LandingPage/login.html',{'error': False})
	    try:
		return render(request, 'LandingPage/home.html',{'posts':post, 'user':user, 'FOAF':FOAF,'friends':ourfriend,'lenn':count, 'comments':comments})
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

                metainfo = request.META
                client_host = metainfo['HTTP_HOST']
                client_port = metainfo['SERVER_PORT']


                user=User.objects.create_user(username ,email,password)
                user.save()
                author= Author.objects.create(user=user,github_username=github_username,picture = picture, author_host = client_host, author_url = client_host+('/service/author/')+str(user.pk))
                author.save()

                return redirect('/login')

    return render(request, 'LandingPage/register.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')




@login_required
def addforeign(request, username, id):
    #search for users
    logging.info(username);
    logging.info(id);

    try:
        user=User.objects.create_user(username ,username + '@foreignuser.com',username)
        user.save()
        author= Author.objects.create(user=user,foreign_id = id)
        author.save()
        Friends.friendmanager.mutualFriends(User.objects.get(username = request.user),User.objects.get(username = user.username))
    except:
        pass
    return redirect('/searchusers')


@login_required
def search_users(request):

    #search for users
    if request.method == 'GET':

        if request.user.is_authenticated():

            receive=[]
	    receive3=[]
            try:
                node = Nodes.objects.all()

                if node is not None:
                    for i in node:
                        foreignauthors = {}
			foreignauthors2 = {}
                        if i.host_url == "http://social-distribution.herokuapp.com" and i.status == True:
                            try:
                                response=requests.get(i.host_url+'/api/author',auth=(i.host_name,i.host_password))
                                response=response.json()
                                foreignauthors = json.loads(json.dumps(response))
                                receive.append(foreignauthors)
                            except:
                                pass
			elif i.host_url == "http://cmput410project15.herokuapp.com" and i.status == True:
			    try:
                                response=requests.get(i.host_url+'/main/author/all/',auth=(i.host_name,i.host_password))
                                response=response.json()
                                foreignauthors2 = json.loads(json.dumps(response))
                                receive3.append(foreignauthors2)
                            except:
                                pass
            except Exception, e:
                    pass

        followed = Follows.followManager.getFollowing(request.user)
        allfriends = Friends.friendmanager.getFriends(request.user)
        allpending = Friends.friendmanager.getAll(request.user)

        ourfollows = []
        for afollow in followed:
            ausername = afollow.followed.get_username()
            ourfollows.append('{s}'.format(s=ausername))

        ourfriends = []
        for afriend in allfriends:
            afriendusername = afriend.reciever.get_username()
            ourfriends.append('{s}'.format(s=afriendusername))

        pendingrequests = []
        for apending in allpending:
            afriendusername = apending.reciever.get_username()
            pendingrequests.append('{s}'.format(s=afriendusername))

                #for foreign in foreignauthors:

        authors=Author.objects.all()
        if len(receive)>0:
            recieve2 = []
            for x in json.loads(json.dumps(receive[0]['authors'])):
                logging.info(x["id"])
                logging.info(x["id"])
                logging.info(x["id"])
                logging.info('here')

                #x = json.loads(x)
                #logging.info(x.id)

                if Author.objects.filter(foreign_id = x["id"]).exists():
                    pass
                else:
                    recieve2.append(x)

	    for x in json.loads(json.dumps(receive3[0]['author'])):
                logging.info(x["id"])
                logging.info(x["id"])
                logging.info(x["id"])
                logging.info('here')

                #x = json.loads(x)
                #logging.info(x.id)

                if Author.objects.filter(foreign_id = x["id"]).exists():
                    pass
                else:
                    recieve2.append(x)

            return render(request, 'LandingPage/search_users.html', {'authors': authors, 'followed': ourfollows, 'allfriends': ourfriends,'allpending': pendingrequests, 'username': request.user.username, 'foreignauthors': recieve2})
        else:
            return render(request, 'LandingPage/search_users.html', {'authors': authors, 'followed': ourfollows, 'allfriends': ourfriends,'allpending': pendingrequests, 'username': request.user.username})

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
	    node = Nodes.objects.all()

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
def api_author_post(request):
    data = json.loads(request.body)
    title = data['post_title']
    text = data['post_text']
    pid = data['post_id']
    picture = data['post_author']['picture']
    visibility = data['visibility']
    mark_down = data['markdown']

    post = Posts()
    post.post_author = Author.objects.get(user = request.user)
    post.post_title = title
    post.post_id = pid
    post.post_text = text
    post.visibility = visibility
    post.mark_down= mark_down
    post.image = None
    if picture is not None:
        post.image=picture
    post.save()

@login_required
def api_author_post_edit(request,post_id):
    post = Posts.objects.get(post_id = post_id)
    data = json.loads(request.body)
    title = data['post_title']
    text = data['post_text']
    picture = data['post_author']['picture']
    visibility = data['visibility']
    mark_down = data['markdown']

    post = Posts()
    post.post_author = Author.objects.get(user = request.user)
    post.post_title = title
    post.post_text = text
    post.visibility = visibility
    post.mark_down= mark_down
    post.image = None
    if picture is not None:
        post.image=picture
    post.save()

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
	node = Nodes.objects.all()

	for i in node:
	    #team 6 connection
	    if i.host_url == "http://social-distribution.herokuapp.com" and i.status == True:
		response=requests.get(i.host_url+'/api/posts/%s'%(post_id),auth=(i.host_name,i.host_password))
		if response.status_code == 200 and len(response.text) > 20:
		    #return HttpResponse(json.dumps(response.json()),content_type='text/plain')
		    response=response.json()
		    p = json.loads(json.dumps(response))
		    post =Posts()
		    #post.post_author = None
		    post.post_title = p['title']
		    post.post_text = p['content']
		    post.visibility =p['visibility']
		    post.post_id = post_id
		    post.image = None
		    break
	    #team 3 connection
	    elif i.host_url == "http://cmput410project15.herokuapp.com" and i.status == True:
		response=requests.get(i.host_url+'/main/posts/%s'%(post_id),auth=(i.host_name,i.host_password))
		if response.status_code == 200 and len(response.text) > 20:
		    #return HttpResponse(json.dumps(response.json()),content_type='text/plain')
		    response=response.json()
		    p = json.loads(json.dumps(response))
		    post =Posts()
		    #post.post_author = None
		    post.post_title = p['posts'][0]['title']
		    post.post_text = p['posts'][0]['content']
		    post.visibility = p['posts'][0]['visibility']
		    post.post_id = post_id
		    post.image = None
		    break
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
		node = Nodes.objects.all()

	for i in node:
		#team 6 connection
		if i.host_url == "http://social-distribution.herokuapp.com" and i.status == True:
		    response=requests.get(i.host_url+'/api/author/%s'%(user_id),auth=(i.host_name,i.host_password))
		    if response.status_code == 200 and len(response.text) > 20:
			response=response.json()
			p = json.loads(json.dumps(response))

			response=requests.get(i.host_url+'/api/author/%s/posts'%(user_id),auth=(i.host_name,i.host_password)) 
			response=response.json()
			a = json.loads(json.dumps(response))
			return render(request, 'LandingPage/profile.html',{'username':p['displayname'],'post':a['posts'],'edit':edit})
			break
		#team 3 connection - not currently working - needed to push regardless
		elif i.host_url == "http://cmput410project15.herokuapp.com" and i.status == True:
		    response=requests.get(i.host_url+'/main/author/%s'%(user_id),auth=(i.host_name,i.host_password))
		    if response.status_code == 200 and len(response.text) > 20:
			response=response.json()
			p = json.loads(json.dumps(response))

			response=requests.get(i.host_url+'/main/author/%s/posts'%(user_id),auth=(i.host_name,i.host_password)) 
			response=response.json()
			a = json.loads(json.dumps(response))		
			return render(request, 'LandingPage/profile.html',{'username':p['author'][0]['displayname'],'post':a['posts'],'edit':edit})
			break
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
            request.user.save()
            author.save()
            messages.info(request, "Your profile was updated successfully.")

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
