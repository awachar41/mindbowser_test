# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from managers.forms import UserForm, UserFormLogin


def login_view(request):
    login_form = UserFormLogin()
    context = {
        'login_form': login_form
    }
    return render(request, 'login.html', context)


def signup(request):
    signup_form = UserForm(request.POST)
    context = {
        'signup_form': signup_form
    }
    return render(request, 'signup.html', context)


@require_POST
def save_signup(request):
    signup_form = UserForm(request.POST)
    password = request.POST.get('password')
    if signup_form.is_valid():
        instance = signup_form.save(commit=False)
        instance.set_password(password)
        instance.is_manager = True
        instance.save()
        messages.success(request, 'Success! Account Created.')
        return redirect('/')
    else:
        print(signup_form.errors)
        signup_form = UserForm(request.POST)
        context = {
            'signup_form': signup_form
        }
        return render(request, 'signup.html', context)


@csrf_exempt
def user_login(request):
    form = UserFormLogin(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_manager:
                return redirect('/dashboard/')
            else:
                messages.errors(request, 'Opps! Employee login is currently unavailable')
        else:
            messages.success(request, 'Incorrect Username Or Password')
            return redirect('/')
    else:
        print(form.errors)
    messages.error(request, 'Incorrect Username Or Password')
    return redirect('/')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out.')
    return redirect('/')
