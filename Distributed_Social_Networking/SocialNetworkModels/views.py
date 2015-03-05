from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
#from SocialNetworkModels.forms import AuthorForm, UserForm, UserProfileForm
from SocialNetworkModels.forms import AuthorProfileForm, AuthorForm

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:

                login(request, user)
                return render(request, 'LandingPage/home.html')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    elif request.method == 'GET':
        if request.user.is_authenticated():
            return render(request, 'LandingPage/home.html')
        else:
            return redirect('../')



    else:
        return redirect('../')


def index(request):
    registered = False

    if request.method == 'POST':
        user_form = AuthorForm(data=request.POST)
        profile_form = AuthorProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = AuthorForm()
        profile_form = AuthorProfileForm()

    return render(request, 'LandingPage/index.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

@login_required
def user_logout(request):
    logout(request)
    return redirect('../../')



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