# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404, HttpResponseBadRequest
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from keuka.forms import SignUpForm

from badges.models import Badge
from badges.models import BadgeUser

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

    context = {
        'badge': badge,
        'action_text': '',
    }

    if request.user.is_authenticated:
        user = BadgeUser.objects.get(pk=request.user.id)
        context['action_text'] = user.action_text(badge)

    return render(request, 'badges/badge_detail.html', context)

def badges_for_user(request):
    if request.user.is_authenticated():
        user = BadgeUser.objects.get(pk=request.user.id)
        return render(request, 'badges/badges_for_user.html', {
            'started_badges': user.started_badges(),
            'pending_badges': user.pending_badges(),
            'earned_badges': user.earned_badges(),
        })
    else:
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})

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

def increment_progress(request, id):
    try:
        badge = Badge.objects.get(id=id)
    except Badge.DoesNotExist:
        raise Http404('This badge does not exist')
    if request.user.is_authenticated():
        user = BadgeUser.objects.get(pk=request.user.id)
        if user.can_increment_progress(badge):
            user.increment_progress(badge)
        return redirect('badge_detail', id=badge.id)
    else:
        raise HttpResponseBadRequest('Must be logged in to work on a badge')

