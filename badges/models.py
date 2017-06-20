# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import markdown

class Badge(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()

	def __str__(self):
		return self.title

	def description_html(self):
		return markdown.markdown(self.description)

class Requirement(models.Model):
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    title = models.TextField()
    details = models.TextField()
    sequence = models.IntegerField(default=0)

    ordering = ('sequence')

    def __str__(self):
    	return self.title
