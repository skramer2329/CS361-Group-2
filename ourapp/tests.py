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
        temp2 = MyUser(email="userTwo@uwm.edu",password="userTwo")
        temp2.save()

    def test_correct_user_password_logs_in_successfully(self):
        resp = self.monkey.post("/", {"uname":"userOne@uwm.edu","password":"userOne"}, follow=True)

    def test_no_such_user_exists(self):
        resp = self.monkey.post("/", {"uname":"userThree@uwm.edu", "password":"userOne"}, follow=True)
        self.assertEqual(resp.context["message"], "The username that you used does not exist. Please retry.", "no failed login when the user didn't exist in database.")

    def test_user_exists_but_invalid_password(self):
        resp = self.monkey.post("/", {"uname":"userTwo@uwm.edu", "password":"WrongPassword"}, follow=True)
        self.assertEqual(resp.context["message"], "The password that you entered is not correct.  Please retry.", "no failed password with wrong password.")
    def test_user_exists_but_valid_password_for_wrong_user_doesnt_log_in(self):
        resp = self.monkey.post("/", {"uname":"userOne@uwm.edu", "password":"userTwo"}, follow=True)
        self.assertEqual(resp.context["message"], "The password that you entered is not correct.  Please retry.", "Log in is successful when wrong user's password is input.  This shouldn't occur.")



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
        
class TestCourseCreation(TestCase):
    def setUp(self):
        self.client = Client()
        self.supervisor = MyUser(email="coursetest1@uwm.edu", password='password1', first_name="steve", last_name="miller",
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
