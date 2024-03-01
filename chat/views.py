from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *

@login_required(login_url='/login/')
def home(request):
    return render(request, 'chat/home.html')

def dashboard(request):
    if request.user.is_authenticated:
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'chat/dashboard.html', { 'users': users})
    else:
        return redirect("login")
    
def generate_room_name(user1_id, user2_id):
    if user1_id < user2_id:
        return f"{user1_id}_{user2_id}"
    else:
        return f"{user2_id}_{user1_id}"

def chat(request, room_name):
    if request.user.is_authenticated:
        obj = User.objects.get(pk=1)
        message_list = Message.objects.filter(sender=request.user, receiver=obj)
        return render(request, 'chat/chat-message.html', { 'message_list': message_list, 'room_name': room_name})
    else:
        return redirect("login")

def user_signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('dashboard')  # Redirect to home page after successful signup
        else:
            form = UserCreationForm()
        return render(request, 'chat/signup.html', {'form': form})
    else:
        return redirect('dashboard')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')  # Redirect to home page after successful login
        else:
            form = AuthenticationForm()
        return render(request, 'chat/login.html', {'form': form})
    else:
        return redirect('dashboard')

def user_logout(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout