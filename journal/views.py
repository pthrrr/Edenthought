from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import messages

from django.contrib.auth.models import auth
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.conf import settings

from . forms import CreateUserForm
from . forms import LoginForm
from . forms import ThoughtForm
from . forms import UpdateUserForm
from . forms import UpdateProfileForm

from . models import Thought
from . models import Profile


def homepage(request):
    return render(request, 'journal/index.html')

def register(request):
    form = CreateUserForm
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            current_user = form.save(commit=False)
            form.save()

            send_mail("Welcome to Thought Journal",
                      "Hello " + current_user.username + ",\n\nThank you for registering at Thought Journal!",
                        settings.EMAIL_HOST_USER, [current_user.email], fail_silently=True)
            profile = Profile.objects.create(user=current_user)

            messages.success(request, 'User created successfully!')
            return redirect('my_login')
    
    context = {'RegistrationForm': form}
    return render(request, 'journal/register.html', context) 

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    
    context = {'LoginForm': form}
    return render(request, 'journal/my-login.html', context)

def user_logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='my_login')
def dashboard(request):
    profile_pic = Profile.objects.get(user=request.user)
    context = {'profile_pic': profile_pic}
    return render(request, 'journal/dashboard.html', context)

@login_required(login_url='my_login')
def create_thought(request):
    form = ThoughtForm()
    if request.method == 'POST':
        form = ThoughtForm(request.POST)
        if form.is_valid():
            thought = form.save(commit=False)   # wait to assign user
            thought.user = request.user         # before saving, assign the user
            thought.save()                      # save to DB
            return redirect('my_thoughts')
    context = {'CreateThoughtForm': form}
    return render(request, 'journal/create-thought.html', context)

@login_required(login_url='my_login')
def my_thoughts(request):
    user_id = request.user.id
    thoughts = Thought.objects.all().filter(user=user_id)
    context = {'thoughts': thoughts}
    return render(request, 'journal/my-thoughts.html', context)

@login_required(login_url='my_login')
def upadate_thought(request, pk):
    try:
        thought = Thought.objects.get(id=pk, user=request.user)
    except:
        return redirect('my_thoughts')
    form = ThoughtForm(instance=thought)
    if request.method == 'POST':
        form = ThoughtForm(request.POST, instance=thought)
        if form.is_valid():
            form.save()
            return redirect('my_thoughts')
    context = {'UpdateThought': form}
    return render(request, 'journal/update-thought.html', context)

@login_required(login_url='my_login')
def delete_thought(request, pk):
    try:
        thought = Thought.objects.get(id=pk, user=request.user)
    except:
        return redirect('my_thoughts')
    if request.method == 'POST':
        thought.delete()
        return redirect('my_thoughts')
    return render(request, 'journal/delete-thought.html')
    
@login_required(login_url='my_login')
def profile_management(request):
    form = UpdateUserForm(instance=request.user)
    profile = Profile.objects.get(user=request.user)
    form2 = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        form2 = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        if form2.is_valid():
            form2.save()
            return redirect('dashboard')
    context = {'UserUpdateForm': form, 'ProfileUpdateForm': form2}
    return render(request, 'journal/profile-management.html', context)

@login_required(login_url='my_login')
def delete_account(request):
    if request.method == 'POST':
        deleteUser = User.objects.get(id=request.user.id)
        deleteUser.delete()
        return redirect('homepage')
    return render(request, 'journal/delete-account.html')