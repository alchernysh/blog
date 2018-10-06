from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import *
from blog.views import get_uid,get_token
from django.contrib.sites.shortcuts import get_current_site
class LoginTest(TestCase):
	def setUp(self):
		test_user = User.objects.create_user(username='testuser', password='12345') 
		test_user.save()
		reg_user = User.objects.create_user(username='reg_user', password='regpass12345')
		reg_user.is_active = False
		reg_user.save()

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

	def test_registration(self):
		reg_user = User.objects.get(username = 'reg_user')
		activate_url = 'activate/'+get_uid(reg_user)+'/'+get_token(reg_user)+'/'
		resp = self.client.get('http://localhost:8000/'+activate_url)
		self.assertEqual(resp.status_code, 200)

