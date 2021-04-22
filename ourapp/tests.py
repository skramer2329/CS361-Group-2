from django.test import TestCase, Client
from .models import Course, Section, MyUser
from django.urls import reverse


# Create your tests here.

class TestLoginSuccess(TestCase):
    monkey = None
    userOne = None

    def setUp(self):
        self.monkey = Client()
        temp = MyUser(email="userOne@uwm.edu",password="userOne")
        temp.save()

    def test_correct_user_password_logs_in_successfully(self):
        resp = self.monkey.post("/", {"uname":"userOne@uwm.edu","password":"userOne"}, follow=True)

class TestAccountCreation(TestCase):
    def setUp(self):
        self.client = Client()
        self.supervisor = MyUser(email="test1@uwm.edu", password='pass1', role='supervisor')
        self.supervisor.save()

        self.instructor = MyUser(email="test2@uwm.edu", password='pass2', role='instructor')
        self.instructor.save()
        self.session = self.client.session
        self.session['email'] = self.supervisor.email
        self.session.save()

    def test_create_new_user(self):
        r = self.client.post("/account/create", {"email": "test3@uwm.edu", "password": "pass3", "first_name": "bill",
        "last_name": "johnson", "phone_number": "(123)456-7890", "address": "123 Main St, Milwaukee, WI, 53211"}, follow=True)

        # at this point we'd go back to the main accounts page where all the accounts are displayed
        self.assertIn("test3@uwm.edu", r.context['accounts'], "new account not showing up in rendered response")
        self.assertEqual(r.context["message"], "account created successfully")

        # testing a password that was already used
        r = self.client.post("/account/create", {"email": "test4@uwm.edu", "password": "pass2", "first_name": "bill",
            "last_name": "johnson", "phone_number": "(123)456-7890", "address": "123 Main St, Milwaukee, WI, 53211"}, follow=True)
        self.assertIn("test4@uwm.edu", r.context['accounts'], "new account not showing up in rendered response")
        self.assertEqual(r.context["message"], "account created successfully")

    def test_try_creating_existing_user(self):
        r = self.client.post("/account/create", {"email": self.instructor.email, "password": "pass3", "first_name": "bill",
            "last_name": "johnson", "phone_number": "(123)456-7890", "address": "123 Main St, Milwaukee, WI, 53211"}, follow=True)
        self.assertEqual(r.context['message'], "account already exists", "there was an attempt to make a new account"
                                                                         "with an already used unique identifier")
