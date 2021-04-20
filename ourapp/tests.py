from django.test import TestCase, Client
from .models import Supervisor
from .models import Instructor

# Create your tests here.


class TestAccountCreation(TestCase):
    def setUp(self):
        self.client = Client()
        self.supervisor = Supervisor(email="test1@uwm.edu", password='pass1', first_name="bob", last_name="smith",
                                     phone_number="(123)456-7890", address="123 Main St, Milwaukee, WI, 53211")
        self.supervisor.save()

        self.instructor = Instructor(email="test2@uwm.edu", password='pass2', first_name="bob", last_name="smith",
                                     phone_number="(123)456-7890", address="123 Main St, Milwaukee, WI, 53211")
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