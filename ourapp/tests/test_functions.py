from django.test import TestCase, Client
from ourapp.models import MyCourse, Section, MyUser
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from ourapp.helper_methods import login
from django.contrib.auth.models import User
from django.conf import settings
from importlib import import_module
from ourapp.views import View


class TestCanLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                            last_name='johnson', address='123 main st.', phone_number='123', role='ta')
        self.user1.save()

        self.user2 = MyUser.objects.create(email='user2@uwm.edu', password='password2', first_name='joe',
                        last_name='johnson', address='123 main st.', phone_number='123',role='ta')

    def test_valid_email(self):
        self.assertTrue(canLogin('user1@uwm.edu', 'password1'), "canLogin function "
                                        "should allow login to occur when data is stored")

        self.assertFalse(canLogin('user1@uwm.edu', 'password2'), "canLogin function "
                            "should return false with wrong password, even if email is correct")

    def test_invalid_email(self):
        self.assertFalse(canLogin('user3@uwm.edu', 'password3'), "canLogin function "
                                "did not reject the case with an unused email and unused password")

        self.assertFalse(canLogin('user3@uwm.edu', 'password2'), "canLogin function did "
                        "not reject the case with an unused email and password for another user")


class LoginFunction(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                                           last_name='johnson', address='123 main st.', phone_number='123', role='ta')
        self.user1.save()

        self.user2 = MyUser.objects.create(email='user2@uwm.edu', password='password2', first_name='joe',
                                           last_name='johnson', address='123 main st.', phone_number='123',
                                           role='supervisor')
        self.user2.save()

        self.user3 = MyUser.objects.create(email='user3@uwm.edu', password='password3', first_name='joe',
                                           last_name='johnson', address='123 main st.', phone_number='123',
                                           role='instructor')
        self.user3.save()


    def test_login(self):
        request = HttpRequest()
        user = User.objects.create_user(username='Saby', password='secret', email='sabyawesome@uwm.edu',
                        first_name='Sabrina', last_name='kramer')
        request.user = user

        self.assertEqual(login(request, 'user1@uwm.edu', 'password1'), redirect("/course/", request))

