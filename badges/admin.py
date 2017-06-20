# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Badge
from .models import Requirement

class BadgeAdmin(admin.ModelAdmin):
	list_display = ['title', 'description']

class RequirementAdmin(admin.ModelAdmin):
	list_display = ['badge', 'title']

admin.site.register(Badge, BadgeAdmin)
admin.site.register(Requirement, RequirementAdmin)