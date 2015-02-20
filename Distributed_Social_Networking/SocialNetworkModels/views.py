from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from SocialNetworkModels.forms import AuthorForm
 

def index(request):
    return render(request, 'LandingPage/index.html', None)
#    return HttpResponse("Hello, world. You're at the  index.")



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
    return render(request, 'author/add_author.html', {'form': form})