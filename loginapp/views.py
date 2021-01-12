from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'index.html')


def register(request):
    print(request.POST)
    # code for  registration
    errors = User.objects.register_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the blog to be updated, make the changes, and save
        hash_browns = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(hash_browns)
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_browns
        )
        print(user)
        # redirect to a success route
        request.session['uuid'] = user.id
        return redirect('/success')



def login(request):
    print(request.POST)
    # code for  registration
    errors = User.objects.login_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the blog to be updated, make the changes, and save
        user = User.objects.get(email=request.POST['email'])
        print(user)
        # redirect to a success route
        request.session['uuid'] = user.id
        return redirect('/success')


def success(request):
    if 'uuid' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['uuid'])
    }
    return render(request, 'success.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')
