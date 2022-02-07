from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import auth
import json

# Create your views here.

def pageNotExist(request):
    return render(request, 'page_not_exist.html')

def index(request):
    if request.user.is_authenticated:
        return redirect('/books')
    return render(request,'index.html',{})

def login(request):

    if request.method == "POST":
        
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            username = data['sUsername']
            password = data['sPassword']
            
            user = auth.authenticate(request, username=username,password=password)
            
            if user is not None:
                auth.login(request, user)
                return redirect('/books')
            else:
                message = f"user '{username}' or password is not correct"
                return render(request, 'login.html', {'invalid_user': message})

        else:
            return render(request, 'login.html', {'form': form})
    else:
        return render(request, 'login.html', {})
    

def signup(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            firstname = data['sFirstName']
            lastname = data['sLastName']
            username = data['sUsername']
            email = data['sEmail']
            password = data['sPassword']
            password2 = data['sConfirmPassword']

            if password != password2:
                pass            

            user = User.objects.create_user(username,email,password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            auth.login(request, user)
            return redirect('/books')
        else:
            return render(request, 'signup.html',{'form': form})

    else:
        return render(request,'signup.html',{})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('index')