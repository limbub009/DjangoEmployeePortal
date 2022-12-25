from django.http.response import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone


from hobbies.forms import LoginForm, SignUpForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('signed_in')
    else:
        if request.method == "POST":
            user = authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password'],
            )
            if user is not None:
                login(request, user)
                request.session['username'] = user.username
                return redirect('signed_in')
            else:
                return HttpResponseForbidden("Invalid credentials")


    return render(request, "hobbies/login_page.html", {
        "title": "Login Page",
        "h1": "Login Page",
        'form': LoginForm(),
    })

def logout_view(request):
        logout(request)
        return redirect('login_page')


def sign_up_view(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            request.session['username'] = user.username
            return redirect('signed_in')
    return render(request, "hobbies/sign_up.html", {
        "title": "Sign Up Page",
        "h1": "Sign Up Page",
        'form': form,
    })

def signed_in_view(request):

    if request.user.is_authenticated:
        return render(request, "hobbies/signed_in.html", {
            "title": "Profile Page",
            "h1": "Profile Page",
        })
    else:
        return redirect('login_page')

def similar_users_view(request):
    if request.user.is_authenticated:
        return render(request, "hobbies/similar_users.html", {
            "title": "Similar users",
            "h1": "Similar users",
        })
    else:
        return redirect('login_page')

def friend_request_view(request):
    if request.user.is_authenticated:
        return render(request, "hobbies/friend_request.html", {
            "title": "Friend Requests",
            "h1": "Friend Requests",
        })
    else:
        return redirect('login_page')

# List all the existing users on the system.
def search_users_view(request):
    if request.user.is_authenticated:
        #users = User.objects.all()'users': users
        context = {"title": "Search"}
        return render(request, 'hobbies/search.html', context)
    else:
        return redirect('login_page')
