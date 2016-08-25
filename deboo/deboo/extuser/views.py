# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import RequestContext
from extuser.forms import UserCreationForm, UserCreationForm2, UserCreationForm1
from extuser.models import ExtUser
from django.http import HttpResponseRedirect

def login(request):
    args = {}
    args.update(csrf(request))
    args['user'] = auth.get_user(request)
    if request.POST:
        username = request.POST.get('email'.encode('ascii','ignore'), '')
        password = request.POST.get('password'.encode('ascii','ignore'), '')
        user = auth.authenticate(email=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/auth/profile/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)

def profile(request, login_user):
    args = {}
    args.update(csrf(request))
    args['user'] = auth.get_user(request)
    args['pr'] = login_user
    args['form'] = UserCreationForm1(request.POST or None, instance=login_user)
    user_profile = ExtUser.objects.filter(login=login_user)
    # Save new/edited student
    if request.method == 'POST':
        form = UserCreationForm2(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/auth/profile/')
    return render_to_response('profile.html', args)





def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    args = {}
    args.update(csrf(request))
    args['user'] = auth.get_user(request)
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(email=newuser_form.cleaned_data['email'], password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html', args)
