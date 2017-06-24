# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
import markdown

BADGE_DIR = 'badge-images/'

class Badge(models.Model):
    
    title = models.CharField(max_length=100)
    brief = models.CharField(max_length = 200, default=' ')
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, upload_to=BADGE_DIR)
    requirements = models.TextField(default='')

    def __str__(self):
        return self.title

    def image_url(self):
        MEDIA_URL = getattr(settings, "MEDIA_URL", None)
        if self.image:
            return self.image.url
        else:
            return MEDIA_URL + BADGE_DIR + 'blank.png'

    def description_html(self):
        return markdown.markdown(self.description)

    def requirements_html(self):
        return markdown.markdown(self.requirements)
