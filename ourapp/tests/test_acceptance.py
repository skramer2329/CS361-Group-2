from django.test import TestCase, Client
from ourapp.models import MyCourse, Section, MyUser
from django.urls import reverse


# Create your tests here.

class TestLoginSuccess(TestCase):
    monkey = None
    userOne = None

    def setUp(self):
        self.monkey = Client()
        temp = MyUser(email="userOne@uwm.edu", password="userOne")
        temp.save()
        temp2 = MyUser(email="userTwo@uwm.edu", password="userTwo")
        temp2.save()

    def test_correct_user_password_logs_in_successfully(self):
        resp = self.monkey.post("/", {"uname": "userOne@uwm.edu", "password": "userOne"}, follow=True)

    def test_no_such_user_exists(self):
        resp = self.monkey.post("/", {"uname": "userThree@uwm.edu", "password": "userOne"}, follow=True)
        self.assertEqual(resp.context["message"], "The username that you used does not exist. Please retry.",
                         "no failed login when the user didn't exist in database.")

    def test_user_exists_but_invalid_password(self):
        resp = self.monkey.post("/", {"uname": "userTwo@uwm.edu", "password": "WrongPassword"}, follow=True)
        self.assertEqual(resp.context["message"], "The password that you entered is not correct.  Please retry.",
                         "no failed password with wrong password.")

    def test_user_exists_but_valid_password_for_wrong_user_doesnt_log_in(self):
        resp = self.monkey.post("/", {"uname": "userOne@uwm.edu", "password": "userTwo"}, follow=True)
        self.assertEqual(resp.context["message"], "The password that you entered is not correct.  Please retry.",
                         "Log in is successful when wrong user's password is input.  This shouldn't occur.")


class TestAccountCreation(TestCase):
    def setUp(self):
        self.client = Client()
        self.supervisor = MyUser(email="test1@uwm.edu", password='pass1', role='supervisor')
        self.supervisor.save()

        self.instructor = MyUser(email="test2@uwm.edu", password='pass2', role='instructor')
        self.instructor.save()
        self.session = self.client.session
        self.session['name'] = self.supervisor.email
        self.session.save()

    def test_create_new_supervisor(self):
        r = self.client.post("/account/", {"email": "test3@uwm.edu", "password": "pass3", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "(123)456-7890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "supervisor"}, follow=True)

        self.assertIn(MyUser.objects.get(email='test3@uwm.edu'), r.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual(r.context["message"], "Account created successfully")

        # testing a password that was already used
        r = self.client.post("/account/", {"email": "test4@uwm.edu", "password": "pass2", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "(123)456-7890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "supervisor"}, follow=True)
        self.assertIn(MyUser.objects.get(email="test4@uwm.edu"), r.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual(r.context["message"], "Account created successfully")

    def test_create_new_instructor(self):
        r = self.client.post("/account/", {"email": "test5@uwm.edu", "password": "pass5", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "(123)456-7890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "instructor"}, follow=True)

        self.assertIn(MyUser.objects.get(email='test5@uwm.edu'), r.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual(r.context["message"], "Account created successfully")

        # testing a password that was already used
        r = self.client.post("/account/", {"email": "test6@uwm.edu", "password": "pass2", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "(123)456-7890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "instructor"}, follow=True)
        self.assertIn(MyUser.objects.get(email="test6@uwm.edu"), r.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual(r.context["message"], "Account created successfully")

    def test_create_new_ta(self):
        r = self.client.post("/account/", {"email": "test7@uwm.edu", "password": "pass7", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "(123)456-7890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "ta"}, follow=True)

        self.assertIn(MyUser.objects.get(email='test7@uwm.edu'), r.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual(r.context["message"], "Account created successfully")

        # testing a password that was already used
        r = self.client.post("/account/", {"email": "test8@uwm.edu", "password": "pass2", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "(123)456-7890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "ta"}, follow=True)
        self.assertIn(MyUser.objects.get(email="test8@uwm.edu"), r.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual(r.context["message"], "Account created successfully")

    def test_try_creating_existing_supervisor(self):
        r = self.client.post("/account/", {"email": self.instructor.email, "password": "pass3", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "(123)456-7890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "supervisor"}, follow=True)
        self.assertEqual(r.context['message'], "A user with this email has already been created.  Try again.",
                         "there was an attempt to make a new account with an already used unique identifier")

    def test_try_creating_existing_instructor(self):
        r = self.client.post("/account/", {"email": self.instructor.email, "password": "pass3", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "(123)456-7890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "instructor"}, follow=True)
        self.assertEqual(r.context['message'], "A user with this email has already been created.  Try again.",
                         "there was an attempt to make a new account with an already used unique identifier")

    def test_try_creating_existing_ta(self):
        r = self.client.post("/account/", {"email": self.instructor.email, "password": "pass3", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "(123)456-7890",
                                           "address": "123 Main St, Milwaukee, WI, 53211", "role": "ta"}, follow=True)
        self.assertEqual(r.context['message'], "A user with this email has already been created.  Try again.",
                         "there was an attempt to make a new account with an already used unique identifier")


class TestCourseCreation(TestCase):
    def setUp(self):
        self.client = Client()
        self.supervisor = MyUser(email="coursetest1@uwm.edu", password='password1', first_name="steve",
                                 last_name="miller",
                                 phone_number="(123)456-7890", address="123 Main St, Milwaukee, WI, 53211")
        self.supervisor.save()

        self.course = MyCourse(name="Intro to Chemistry", number=102)
        self.course.save()

        self.session1 = self.client.session
        self.session1['email'] = self.supervisor.email
        self.session1.save()

    def test_createNewAccount(self):
        r = self.client.post("/course/create", {"name": "System Programming", "number": 337}, follow=True)
        self.assertIn("System Programming", r.context['courses'], "new course not shown in rendered response")
        self.assertEqual(r.context['message'], "course created")

    def test_courseTaken(self):
        # course name is already used
        r = self.client.post("/course/create", {"name": self.course.name, "number": 103}, follow=True)
        self.assertEqual(r.context['message'], "course name already exists")

        # course number is already used
        r = self.client.post("/course/create", {"name": "Intro to Software Engineering",
                                                "number": self.course.number}, follow=True)
        self.assertEqual(r.context['message'], "course number already exists")


class TestSectionCreation(TestCase):
    client = None
    courseList = None

    def setUp(self):
        self.client = Client()
        self.courseList = {"Math": [1], "Chemistry": [2], "Art": [3]}

        for i in self.courseList.keys():
            temp = MyCourse(name=i, number=self.courseList[i])
            temp.save()
            for j in self.courseList[i]:
                Section(course=temp, number=j)

    def test_add_section_already_exists(self):
        c = self.client.session
        c["number"] = 1
        c.save
        resp = self.client.post("/section/create", {"number": 1}, follow=True)
        self.assertEqual(resp.context['message'], "section number already exists")

    def test_add_section(self):
        c = self.client.session
        temp = MyCourse(name="Calculus", number=4)
        c.save
        resp = self.client.post("/section/create", {"course": temp, "number": 4}, follow=True)
        self.assertEqual(4, resp.context["number"])

    def test_add_when_no_course(self):
        c = self.client.session
        temp = None
        c.save
        resp = self.client.post("/section/create", {"course": temp, "number": 5}, follow=True)
        self.assertEqual(resp.context['message'], "no course exists for this section")