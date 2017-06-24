# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import markdown

class Badge(models.Model):
    title = models.CharField(max_length=100)
    brief = models.CharField(max_length = 200, default=' ')
    description = models.TextField()
    image = models.ImageField(null=True, upload_to='badge-images/')
    requirements = models.TextField(default='')

    def __str__(self):
        return self.title

    def description_html(self):
        return markdown.markdown(self.description)

    def requirements_html(self):
        return markdown.markdown(self.requirements)
