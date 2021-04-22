from django.test import TestCase, Client
from .models import Supervisor, Instructor, Ta, Course, Section, User
from django.urls import reverse


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
        
cclass TestCourseCreation(TestCase):
    def setUp(self):
        self.client = Client()
        self.supervisor = Supervisor(email="coursetest1@uwm.edu", password='password1', first_name="steve", last_name="miller",
                                     phone_number="(123)456-7890", address="123 Main St, Milwaukee, WI, 53211")
        self.supervisor.save()

        self.course = Course(name="Intro to Chemistry",number=102)
        self.course.save()

        self.session1 = self.client.session
        self.session1['email'] = self.supervisor.email
        self.session1.save()

    def test_createNewAccount(self):
        r = self.client.post("/course/create",{"name":"System Programming","number":337},follow=True)
        self.assertIn("System Programming",r.context['courses'],"new course not shown in rendered response")
        self.assertEqual(r.context['message'],"course created")

    def test_courseTaken(self):
        # course name is already used
        r = self.client.post("/course/create",{"name":self.course.name,"number":103},follow=True)
        self.assertEqual(r.context['message'],"course name already exists")

        # course number is already used
        r = self.client.post("/course/create",{"name":"Intro to Software Engineering",
                                               "number":self.course.number},follow=True)
        self.assertEqual(r.context['message'],"course number already exists")
