from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group

from Alexandrians.forms import *

def init(request):
    context={}

    return render(request,"Alexandrians/landing.html",context)

def register(request):
    context={}

    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect(reverse('landing'))
       
        else:
            context['errors'] = user_form.errors
    
    else:
        user_form = UserForm()

    context['user_form'] = user_form

    return render(request,"Alexandrians/register.html",context)

def log_in(request):
    context={}
    context['disabled'] = False
    context['invalid'] = False

    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user:

                if user.is_active:
                    login(request, user)
                    return redirect(reverse('landing'))
                
                else:
                    context['disabled'] = True
            
            else:
                context['invalid'] = True

    return render(request,"Alexandrians/log-in.html",context)

def admin_accounts(request):
    context={}

    if request.method == 'POST':
        user_form = BoardForm(request.POST)
        key = request.POST.dict().get('key')

        if user_form.is_valid() and key in board_tokens:
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            group = Group.objects.get(name='board')
            user.groups.add(group)

            login(request, user)
            return redirect(reverse('landing'))
       
        else:
            context['errors'] = user_form.errors

            if not key in board_tokens:
                user_form.add_error('key', 'Invalid key')
    
    else:
        user_form = BoardForm()

    context['user_form'] = user_form
    return render(request,"Alexandrians/admin-accounts.html",context)