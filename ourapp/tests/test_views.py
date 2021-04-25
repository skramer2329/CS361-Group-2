from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ourapp.views import Login

from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
#from authentication.utils import generate_token


# Create your tests here.


class BaseTest(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.create_account_url = reverse('create-account')
        self.user = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': 'password',
            'password2': 'password',
            'name': 'fullname'
        }

        return super().setUp()


class LoginTest(BaseTest):
    # note: client comes from the TestCase class
    def test_login_success(self):
        # create a user in database
        self.client.post(self.create_account_url, self.user)

        # gets first user
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url, self.user)
        self.assertEqual(response.status_code, 302)

    def test_cant_login_with_unverified_email(self):
        self.client.post(self.create_account_url, self.user)
        response = self.client.post(self.login_url, self.user)
        self.assertEqual(response.status_code, 401)

    def test_cant_login_with_no_username(self):
        response = self.client.post(self.login_url, {'password': 'passwped', 'username': ''})
        self.assertEqual(response.status_code, 401)

    def test_cant_login_with_no_password(self):
        response = self.client.post(self.login_url, {'username': 'passwped', 'password': ''})
        self.assertEqual(response.status_code, 401)