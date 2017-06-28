# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime 
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import markdown

BADGE_DIR = 'badge-images/'

class Badge(models.Model):
    
    title = models.CharField(max_length=100)
    brief = models.CharField(max_length = 200, default=' ')
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, upload_to=BADGE_DIR)
    requirements = models.TextField(default='')

    # users = models.ManyToManyField(BadgeUser, through='BadgeEarner')


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


class BadgeUser(User):
    class Meta:
        proxy = True

    def can_increment_progress(self, badge):
        try:
            earner = BadgeEarner.objects.get(earner_id = self.id, badge_id = badge.id)
            # We could prevent from moving to `earned` here
            return True
        except BadgeEarner.DoesNotExist:
            # Ensure that we meet the pre-reqs to start a badge
            for prereq in badge.prereqs.all():
                try:
                    req_earner = BadgeEarner.objects.get(earner_id = self.id, badge_id = prereq.required_badge.id)
                    if not BadgeEarner.status_geq(req_earner.status, prereq.min_badge_status):
                        return False
                except BadgeEarner.DoesNotExist:
                    return False
            return True

    # Prereq: Must call can_increment_progress first
    def increment_progress(self, badge):
        try:
            earner = BadgeEarner.objects.get(earner_id = self.id, badge_id = badge.id)
            earner.advance_status()
        except BadgeEarner.DoesNotExist:
            earner = BadgeEarner(
                earner = self,
                badge = badge
            )
            earner.save()
        
        return earner

    def action_text(self, badge):
        try:
            earner = BadgeEarner.objects.get(earner_id = self.id, badge_id = badge.id)
        except BadgeEarner.DoesNotExist:
            return 'Start Earning'

        if earner.status == BadgeEarner.STARTED:
            return 'Submit For Approval'

        return ''

    def started_badges(self):
        return BadgeEarner.objects.filter(earner_id = self.id, status = BadgeEarner.STARTED)

    def pending_badges(self):
        return BadgeEarner.objects.filter(earner_id = self.id, status = BadgeEarner.NEEDS_APPROVAL)

    def earned_badges(self):
        return BadgeEarner.objects.filter(earner_id = self.id, status = BadgeEarner.EARNED)



class BadgeEarner(models.Model):
    STARTED = 0
    NEEDS_APPROVAL = 1
    EARNED = 2
    STATUS_CHOICES = (
        (STARTED, 'Started'),
        (NEEDS_APPROVAL, 'Needs Approval'),
        (EARNED, 'Earned'),
    )

    earner = models.ForeignKey(BadgeUser, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    date_started = models.DateField(default=datetime.now, blank=True, null=True)
    date_submitted_for_approval = models.DateField(blank=True, null=True)
    date_earned = models.DateField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STARTED)

    def advance_status(self):
        if self.status == BadgeEarner.STARTED:
            self.status = BadgeEarner.NEEDS_APPROVAL
            self.date_submitted_for_approval = timezone.now()
        elif self.status == BadgeEarner.NEEDS_APPROVAL:
            self.status = BadgeEarner.EARNED
            self.date_earned = timezone.now()
        self.save()

    # Compares two statuses, returning whether the first is further along than or equal to the second
    @classmethod
    def status_geq(cls,a,b):
        return a >= b

    class Meta:
        unique_together = ('earner', 'badge')


class BadgePrerequisite(models.Model):
    badge = models.ForeignKey(Badge, related_name='prereqs')
    required_badge = models.ForeignKey(Badge, related_name='required_for_set')
    min_badge_status = models.IntegerField(choices=BadgeEarner.STATUS_CHOICES, default=BadgeEarner.EARNED)

