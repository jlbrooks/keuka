# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
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

# Test views

class BadgesForUserViewTests(TestCase):
    def test_no_badges(self):        
		user = User.objects.create_user(username='john',
			email='jlennon@beatles.com',
			password='glass onion')
		self.client.login(username='john', password='glass onion')

		response = self.client.get(reverse('profile', args=[user.id]))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Nothing!')
		self.assertContains(response, 'No badges waiting approval.')
		self.assertContains(response, 'No earned badges yet.')

    def test_one_badge_started(self):        
		user = User.objects.create_user(username='john',
			email='jlennon@beatles.com',
			password='glass onion')
		self.client.login(username='john', password='glass onion')
		badge = Badge.objects.create(title='Fun Badge')
		badge_earner = BadgeEarner(badge=badge, earner=user)
		badge_earner.save()

		response = self.client.get(reverse('profile', args=[user.id]))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Fun Badge')
		self.assertContains(response, 'No badges waiting approval.')
		self.assertContains(response, 'No earned badges yet.')

    def test_one_badge_for_approval(self):        
		user = User.objects.create_user(username='john',
			email='jlennon@beatles.com',
			password='glass onion')
		self.client.login(username='john', password='glass onion')
		badge = Badge.objects.create(title='Fun Badge')
		badge_earner = BadgeEarner(badge=badge, earner=user)
		badge_earner.save()
		badge_earner.advance_status()

		response = self.client.get(reverse('profile', args=[user.id]))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Fun Badge')
		self.assertContains(response, 'Nothing!')
		self.assertContains(response, 'No earned badges yet.')