# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Badge
from .models import BadgeEarner
from .models import BadgeUser
from .models import BadgePrerequisite


class BadgeModelTests(TestCase):

	def test_badge_without_image_has_default(self):
		"""
	    partly to just learn about testing, checking some basic defaults
	    on our badges, such as we should always have a default image attached.
	    """
		badge = Badge(title='No Image')
		self.assertEqual(badge.image_url()[-3:], 'png')

class BadgeEarnerTests(TestCase):

	def test_badge_advancement_status(self):
		badge = Badge.objects.create(title='Badge')
		user = User.objects.create_user(username='john',
                                 email='jlennon@beatles.com',
                                 password='glass onion')

		badge_earner = BadgeEarner(badge=badge, earner=user)
		self.assertIs(badge_earner.status, BadgeEarner.STARTED)
		badge_earner.advance_status()
		self.assertIs(badge_earner.status, BadgeEarner.NEEDS_APPROVAL)
		badge_earner.advance_status()
		self.assertIs(badge_earner.status, BadgeEarner.EARNED)

class BadgePrerequsiteTests(TestCase):
	def test_can_increment_when_no_prereq(self):
		badge = Badge.objects.create(title='Badge')
		user = User.objects.create_user(username='john',
                                 email='jlennon@beatles.com',
                                 password='glass onion')
		bu = BadgeUser.objects.get(pk=user.id)
		self.assertIs(bu.can_increment_progress(badge), True)
