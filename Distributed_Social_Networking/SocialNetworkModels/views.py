from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, redirect,render_to_response
from SocialNetworkModels.models import Posts, Author, Friends, FriendManager
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


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

                elif u.author.approved:
                    login(request, user)
                    return redirect('/home')
                else:
                    return render(request, 'LandingPage/login.html',{'error': 'not approved'})
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
            try:
                return render(request, 'LandingPage/home.html')
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
                return render(request, 'LandingPage/search_users.html',{'authors': authors})
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
def add_friend(request, reciever_pk):
    #search for users
    if request.user.is_authenticated():
        try:
                #this needs to be paginated later
                #friend = Friends.friendmanager.getFriends(user.username)
            friend = Friends()
            friend.initiator = User.objects.get(username = request.user)
            friend.reciever = User.objects.get(pk = reciever_pk)
            friend.save()
            return redirect('/searchusers')



        except Author.DoesNotExist:
            return redirect('/searchusers')
    else:
        return redirect('/home')







@login_required
def author_post(request):
    if request.method =='POST':
        title = request.POST.get('post_title')
        text = request.POST.get('post_text')
        visibility = request.POST.get('visibility')
        picture = request.FILES.get('picture')        
        #post =Posts.objects.create(post_author = request.user.username, 
                                  #psot_title = title, post_text= text,visibility= visibility)
        post = Posts()
        post.post_author = Author.objects.get(user = request.user)
        post.post_title = title
        post.post_text = text
        post.visibility = visibility
        if picture is not None:
            post.image=picture
        post.save()
        return redirect('/home')
    else:
        return render(request, 'LandingPage/post.html')
        
    return render(request, 'LandingPage/post.html')

@login_required
def profile(request):
    if request.user.is_authenticated():
        if request.method =='GET':
            author = Author.objects.get(user =request.user)
            username = author.user.username
            email = author.user.email
            github_username=author.github_username
            picture = author.picture
            return render(request, 'LandingPage/profile.html',{'username':username, 'email':email,'github_username' :github_username,'picture':picture})
    return render(request, 'LandingPage/profile.html')
"""
    form = AuthorForm()

        #context = RequestContext(request)
    try:
        if request.method == 'POST':
            username = request.POST.get("username","")
            password = request.POST.get("password","")



            #l = Link.objects.get_or_create(title=title, url=url)[0]

            #for atag in tags.split():
             #   t = Tag.objects.get_or_create(name=atag)[0]
             #   l.tags.add(t)
    except:
            return render(request, 'author/add_author.html', {'form': form})

            #return redirect(index)


    return render(request, 'author/add_author.html', {'form': form})

    #return redirect(index)

#    return render(request, 'LandingPage/index.html', None)
#    return HttpResponse("Hello, world. You're at the  index.")"""



"""

def add_author(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = AuthorForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = AuthorForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'author/add_author.html', {'form': form})"""
