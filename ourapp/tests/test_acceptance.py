from django.test import TestCase, Client
from ourapp.models import MyCourse, MySection, MyUser
from django.urls import reverse


# Create your tests here.

class TestLoginSuccess(TestCase):

    # NOTE: an error is occuring because the supervisor is not being saved for some reason?

    def setUp(self):
        self.client = Client()
        self.supervisor = MyUser(first_name="supervisor", last_name="super", email="testsupervisor@uwm.edu", password="supervisor",
                                                address="123 straight st", phone_number="1234567890", role="supervisor")
        self.supervisor.save()

        self.emptyUserEmail = MyUser(first_name="supervisor", last_name="super", email="", password="supervisor",
                                                address="123 straight st", phone_number="1234567890", role="supervisor")
        self.emptyUserEmail.save()
        self.instructor = MyUser(first_name="instructor", last_name="instruct", email="instructor@uwm.edu",
                                                password="instructor",
                                                address="123 corner st", phone_number="7777777", role="instructor")
        self.ta = MyUser.objects.create(first_name="ta", last_name="assist", email="ta@uwm.edu",
                                                password="ta", address="123 round st", phone_number="1234567890", role="ta")

    def test_correct_user_password_logs_in_successfully(self):

        response = self.client.post("/", {"email": self.supervisor.email, "password": self.supervisor.password}, follow=True)
        #expected, actual
        self.assertEqual("Valid", response.context["message"])


    def test_no_such_user_exists(self):
        response = self.client.post("/", {"email": self.emptyUserEmail.email, "password": self.supervisor.password}, follow=True)
        self.assertEqual("The username that you used does not exist. Please retry.", response.context["message"])

    def test_user_exists_but_invalid_password(self):
        response = self.client.post("/", {"email": self.supervisor.email, "password": "WrongPassword"}, follow=True)
        self.assertEqual("The password that you entered is not correct.  Please retry.", response.context["message"])

    def test_user_exists_but_valid_password_for_wrong_user_doesnt_log_in(self):
        response = self.client.post("/", {"email": self.supervisor.email, "password": self.instructor.password}, follow=True)
        self.assertEqual("The password that you entered is not correct.  Please retry.", response.context["message"])


class TestAccountCreation(TestCase):
    def setUp(self):
        self.client = Client()
        self.super = MyUser(first_name="supervisor", last_name="super", email="test1@uwm.edu", password="pass1",
                                                address="123 straight st", phone_number="1234567890", role="supervisor")
        self.super.save()

        self.instructor = MyUser(first_name="instructor", last_name="super", email="test2@uwm.edu",
                                 password='pass2',address="123 straight st", phone_number="1234567890", role='instructor')
        self.instructor.save()
        self.ta = MyUser(first_name="ta", last_name="super", email="test3@uwm.edu",
                                 password='pass3', address="123 straight st", phone_number="1234567890",
                                 role='ta')
        self.ta.save()

    def test_create_new_supervisor(self):
        response = self.client.post("/account/", {"first_name": "bill", "last_name": "johnson", "email": "newsupervisor@uwm.edu", "password": "pass3",
                                            "phone_number": "1234567890", "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "supervisor"}, follow=True)

        self.assertIn(MyUser.objects.get(email='newsupervisor@uwm.edu'), response.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual("Account created successfully", response.context["message"])

        # testing a password that was already used
        r = self.client.post("/account/", {"email": "test4@uwm.edu", "password": "pass2", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "1234567890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "supervisor"}, follow=True)
        self.assertIn(MyUser.objects.get(email="test4@uwm.edu"), r.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual("Account created successfully", r.context["message"])

    def test_create_new_instructor(self):
        r = self.client.post("/account/", {"email": "newinstructor@uwm.edu", "password": "pass5", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "1234567890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "instructor"}, follow=True)

        self.assertIn(MyUser.objects.get(email='newinstructor@uwm.edu'), r.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual("Account created successfully", r.context["message"])

        # testing a password that was already used
        r = self.client.post("/account/", {"email": "test6@uwm.edu", "password": "pass2", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "1234567890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "instructor"}, follow=True)
        self.assertIn(MyUser.objects.get(email="test6@uwm.edu"), r.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual("Account created successfully", r.context["message"])

    def test_create_new_ta(self):
        r = self.client.post("/account/", {"email": "newta@uwm.edu", "password": "pass7", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "1234567890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "ta"}, follow=True)

        self.assertIn(MyUser.objects.get(email='newta@uwm.edu'), r.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual("Account created successfully", r.context["message"])

        # testing a password that was already used
        r = self.client.post("/account/", {"email": "test8@uwm.edu", "password": "pass2", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "1234567890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "ta"}, follow=True)
        self.assertIn(MyUser.objects.get(email="test8@uwm.edu"), r.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual("Account created successfully", r.context["message"])

    def test_try_creating_existing_supervisor(self):
        r = self.client.post("/account/", {"email": self.super.email, "password": "pass1", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "1234567890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "supervisor"}, follow=True)
        self.assertEqual("A user with this email has already been created.  Try again.", r.context['message'])

    def test_try_creating_existing_instructor(self):
        r = self.client.post("/account/", {"email": self.instructor.email, "password": "pass3", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "1234567890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "instructor"}, follow=True)
        self.assertEqual("A user with this email has already been created.  Try again.", r.context['message'])

    def test_try_creating_existing_ta(self):
        r = self.client.post("/account/", {"email": self.ta.email, "password": "pass3", "first_name": "bill",
                                           "last_name": "johnson", "phone_number": "1234567890",
                                           "address": "123 Main St, Milwaukee, WI, 53211", "role": "ta"}, follow=True)
        self.assertEqual("A user with this email has already been created.  Try again.", r.context['message'])


class TestCourseCreation(TestCase):
    def setUp(self):
        self.client = Client()
        self.supervisor = MyUser(email="coursetest1@uwm.edu", password='password1', first_name="steve",
                                 last_name="miller",
                                 phone_number="(123)456-7890", address="123 Main St, Milwaukee, WI, 53211", role="supervisor")
        self.supervisor.save()

        self.course = MyCourse(name="Intro to Chemistry", number=102)
        self.course.save()

        self.session1 = self.client.session
        self.session1['email'] = self.supervisor.email
        self.session1.save()

    def test_createNewCourse(self):
        r = self.client.post("/course/create", {"name": "System Programming", "number": 337}, follow=True)
        #self.assertIn("System Programming", r.context["name"], "new course not shown in rendered response")
        self.assertEqual("course created", r.context['message'])

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
                MySection(course=temp, number=j)

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