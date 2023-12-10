from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile


# Create your views here.
def index(request):
    return render(request, 'core/index.html') # render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email exist')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                # create profile for user
                User_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=User_model, id_user=User_model.id)
                new_profile.save()
                return redirect('signup')
                
        else:
            messages.info(request, 'password not matching')
            return redirect('signup')
    else:
        return render(request, 'core/signup.html') # render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # authenticate user
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('signin')
    else:
        return render(request, 'core/signin.html') # render() function takes the request object as its first argument, a template name as its second argument and a dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.