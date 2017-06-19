# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Badge

class BadgeAdmin(admin.ModelAdmin):
	list_display = ['title', 'description']

admin.site.register(Badge, BadgeAdmin)
