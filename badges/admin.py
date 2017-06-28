# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Badge
from .models import BadgeEarner

class BadgeAdmin(admin.ModelAdmin):
	list_display = ['title', 'brief']

class BadgeEarnerAdmin(admin.ModelAdmin):
	list_display = ['earner', 'badge', 'status']

admin.site.register(Badge, BadgeAdmin)
admin.site.register(BadgeEarner, BadgeEarnerAdmin)
