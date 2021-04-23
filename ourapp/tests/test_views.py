from django.test import TestCase, Client
from django.urls import reverse
from ourapp.models import MyUser, MyCourse, Section
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.course_url = reverse('course')
        self.account_url = reverse('account')
        self.create_account_url = reverse('create-account')

    def test_login_GET(self):
        response = self.client.get(reverse(self.login_url))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ourapp/login.html')

    def test_login_POST(self):
        pass

    def test_course_GET(self):
        response = self.client.get(self.course_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ourapp/course.html')

    def test_course_POST(self):
        pass

    def test_account_GET(self):
        response = self.client.get(self.account_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ourapp/account.html')

    def test_account_create_account_redirect_correctly(self):
        pass

    def test_create_account_GET(self):
        response = self.client.get(self.create_account_url)

        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, '')

    def test_create_account_POST(self):
        pass
