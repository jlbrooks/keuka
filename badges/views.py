# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from keuka.forms import SignUpForm

from badges.models import Badge

def index(request):
    badges = Badge.objects.all().order_by('title')
    return render(request, 'badges/index.html', {
        'badges': badges,
    })

def badge_detail(request, id):
    try:
        badge = Badge.objects.get(id=id)
    except Badge.DoesNotExist:
        raise Http404('This badge does not exist')
    return render(request, 'badges/badge_detail.html', {
        'badge':badge,
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

