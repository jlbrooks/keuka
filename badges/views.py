# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404

from badges.models import Badge

def index(request):
	badges = Badge.objects.all()
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
