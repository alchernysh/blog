# -*- coding: utf-8 -*-
from django.test import LiveServerTestCase,TestCase
from selenium import webdriver
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import *
from blog.views import get_uid,get_token
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait

port = 8000

class AccountTestCase(LiveServerTestCase):
    port = port

    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='12345',email = 'email@dom.org') 
        test_user.save()

        user_unconfirmed = User.objects.create_user(username='user_unconfirmed', password='12345',email = 'email@dom.com') 
        user_unconfirmed.save()
        user_unconfirmed.is_active = False

        self.selenium = webdriver.Chrome()
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()
    
    def test_registration(self):
        self.selenium.get("http://localhost:8000/signup/")
        email = 'test@domain.org'
        self.selenium.find_element_by_id('id_email').send_keys(email)
        self.selenium.find_element_by_id('id_password1').send_keys('123')
        self.selenium.find_element_by_id('id_password2').send_keys('123')
        self.selenium.find_element_by_id('submit').click()
        self.selenium.implicitly_wait(2)
        text = u'На Ваш электронный адрес отправлено письмо с сылкой для подтверждения регистрации. Перейдите по ссылке, чтобы завершить регистрацию.'
        self.assertEquals(text,self.selenium.find_element_by_xpath("/html/body/p").text)
        reg_user = User.objects.get(email = email)
        self.assertEquals(reg_user.username,email)
        self.assertFalse(reg_user.is_active)
        
    def test_email_confirmation(self):
        user_unconfirmed = User.objects.get(username = 'user_unconfirmed')
        activate_url = 'activate/'+get_uid(user_unconfirmed)+'/'+get_token(user_unconfirmed)+'/'
        self.selenium.get('http://localhost:8000/'+activate_url)
        self.selenium.implicitly_wait(2)
        self.assertTrue(user_unconfirmed.is_active)

    def test_login(self):
        self.selenium.get("http://localhost:8000")
        self.assertEquals("http://localhost:8000/login/?next=/", self.selenium.current_url)
        self.selenium.find_element_by_id('id_email').send_keys('email@dom.org')
        self.selenium.find_element_by_id('id_password').send_keys('12345')
        self.selenium.find_element_by_id('submit').click()
        self.assertEquals("http://localhost:8000/", self.selenium.current_url)

    def test_changing_password_part1(self):
        self.selenium.get("http://localhost:8000/email_confirmation/")
        self.selenium.find_element_by_id('id_email').send_keys('email@dom.org')
        self.selenium.find_element_by_id('submit').click()
        text = u'На Ваш электронный адрес отправлено письмо с cсылкой для смены пароля.'
        self.assertEquals(text,self.selenium.find_element_by_xpath("/html/body/p").text)

    def test_changing_password_part2(self):
        test_user = User.objects.get(username = 'testuser')
        change_password = 'change_password/'+get_uid(test_user)+'/'+get_token(test_user)+'/'
        self.selenium.get("http://localhost:8000/"+change_password)
        self.selenium.find_element_by_id('id_password1').send_keys('12345')
        self.selenium.find_element_by_id('id_password2').send_keys('12345')
        self.selenium.find_element_by_id('submit').click()
        test_user = authenticate(username='testuser', password='12345')
        self.assertTrue(test_user != None)



