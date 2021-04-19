from django.test import TestCase, Client
from models import User
# Create your tests here.

class TestLoginSuccess(TestCase):
    monkey = None
    userOne = None

    def setUp(self):
        self.monkey = Client()
        temp = User(username="userOne",password="userOne")
        temp.save()

    def test_correct_user_password_logs_in_successfully(self):
        resp = self.monkey.post("/", {"name":"userOne","password":"userOne"}, follow=True)

