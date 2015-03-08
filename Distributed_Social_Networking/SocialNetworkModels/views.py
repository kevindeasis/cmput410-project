from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, redirect,render_to_response
from SocialNetworkModels.models import Posts, Author
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

        user = authenticate(username=username, password=password)
        if user!=None:
            login(request, user)                
            return redirect('/home')
        else:
            error = True
        return render(request, 'LandingPage/login.html',{'error': error})
    elif request.method == 'GET':
        if request.user.is_authenticated():
            return render(request, 'LandingPage/login.html',{'error': error})
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
    


def register(request):
    context= RequestContext(request)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        github_username= request.POST.get('github')
        
        
        if 'picture' in request.FILES:
            picture = request.FILES['picture']
        
        if len(User.objects.filter(username =username))>0:
            return render(request, 'LandingPage/register.html',{'username':'username already exist'})
        else:
            if username != None and password != None:
                user=User.objects.create_user(username ,email,password)
                user.save()
                author= Author.objects.create(user=user,github_username=github_username )
                author.save()
                return redirect('/login')

    return render(request, 'LandingPage/register.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def author_post(request):
    if request.method =='POST':
        
        if post_form.is_valid():
            post = post_form.save()
            return render(request, 'LandingPage/home.html')
        else:
            print post_form.errors
    else:
        post_form = PostsForm()
        
    return render(request, 'LandingPage/post.html', {'post_form': post_form})
        
@login_required
def profile(request):
    if request.user.is_authenticated():
        if request.method =='GET':
            author = Author()
            author.user = request.user
            username = author.user.username
            email = author.user.email
            github_username=author.github_username
            return HttpResponse(github_username)
    return render(request, 'LandingPage/profile.html',{'username':username, 'email':email,'github_username' :github_username})

@login_required   
def friend(request):
#    if request.method == 'GET':
    if request.user.is_authenticated():
        author = Author.objects.filter(user=request.user)[0]
        friends = author.friends.all()
        return render(request, 'LandingPage/friend.html', {'friends':friends})
    return render(request, 'LandingPage/login.html',{'error': False})


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
