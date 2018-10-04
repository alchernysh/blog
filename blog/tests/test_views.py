from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import *

class LoginTest(TestCase):
	def setUp(self):
		test_user = User.objects.create_user(username='testuser', password='12345') 
		test_user.save()

	def test_redirect_if_not_logged_in(self):
		resp = self.client.get(reverse('index'))
		self.assertRedirects(resp, '/login/?next=/')

	def test_logged_in_uses_correct_template(self):
		login = self.client.login(username='testuser', password='12345')
		resp = self.client.get(reverse('index'))
		self.assertEqual(str(resp.context['user']),'testuser')
		self.assertEqual(resp.status_code, 200)
		self.assertTemplateUsed(resp, 'index.html')

	def test_logout(self):
		login = self.client.login(username='testuser', password='12345')
		self.client.get(reverse('logout'))
		resp = self.client.get(reverse('index'))
		self.assertEqual(resp.status_code, 302)
		self.assertRedirects(resp, '/login/?next=/')