from django.shortcuts import render, redirect
from .models import Todo
from django.contrib import messages
from django.contrib.auth.models import User, auth
# Create your views here.


def index(request):
    todo_list = Todo.objects.all()
    return render(request, 'index.html', {'todo_list': todo_list})


def register(request):
    if request.method == 'POST':
        entered_username = request.POST['username']
        entered_email = request.POST['email']
        entered_password = request.POST['password']
        confirmed_password = request.POST['confirm_password']
        if entered_password == confirmed_password:
            if User.objects.filter(username=entered_username).exists():
                messages.info(request, 'Username already already exists.')
                return redirect('register')
            elif User.objects.filter(email=entered_email).exists():
                messages.info(request, 'Email Address already exists.')
                return redirect('register')
            else:
                user = User.objects.create(
                    username=entered_username, email=entered_email, password=entered_password)
                user.save()
                return redirect('login')
        else:
            messages.error(request, 'Passwords provided does not match.')
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        entered_username = request.POST['username']
        entered_password = request.POST['password']
        user = auth.authenticate(
            username=entered_username, password=entered_password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials provided')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
