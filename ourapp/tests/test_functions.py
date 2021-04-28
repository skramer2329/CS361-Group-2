from django.test import TestCase, Client
from ourapp.models import MyCourse, MySection, MyUser
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from ourapp.helper_methods import login
from django.contrib.auth.models import User
from django.conf import settings
from importlib import import_module
from ourapp.helper_methods import login, get_user, validate_course_number, create_course, \
    validate_section_number, create_section


class TestCanLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                            last_name='johnson', address='123 main st.', phone_number='123', role='ta')
        self.user1.save()

        self.user2 = MyUser.objects.create(email='user2@uwm.edu', password='password2', first_name='joe',
                        last_name='johnson', address='123 main st.', phone_number='123',role='ta')

    def test_valid_email(self):
        self.assertTrue(can_login('user1@uwm.edu', 'password1'), "canLogin function "
                                        "should allow login to occur when data is stored")

        self.assertFalse(can_login('user1@uwm.edu', 'password2'), "canLogin function "
                            "should return false with wrong password, even if email is correct")

    def test_invalid_email(self):
        self.assertFalse(can_login('user3@uwm.edu', 'password3'), "canLogin function "
                                "did not reject the case with an unused email and unused password")

        self.assertFalse(can_login('user3@uwm.edu', 'password2'), "canLogin function did "
                        "not reject the case with an unused email and password for another user")


class TestLoginFunction(TestCase):
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


    def test_login_supervisor(self):
        self.assertEqual(login('user2@uwm.edu', 'password2'), "Valid")
        self.assertEqual(login('user2@uwm.edu', 'password1'), "The password that you entered is not correct.  Please retry.")
        self.assertEqual(login('user2@uwm.edu', 'NobodyPassword'),
                         "The password that you entered is not correct.  Please retry.")

    def test_login_instructor(self):
        self.assertEqual(login('user3@uwm.edu', 'password3'), "Valid")
        self.assertEqual(login('user3@uwm.edu', 'password2'),
                         "The password that you entered is not correct.  Please retry.")
        self.assertEqual(login('user3@uwm.edu', 'NobodyPassword'),
                         "The password that you entered is not correct.  Please retry.")

    def test_login_ta(self):
        self.assertEqual(login('user1@uwm.edu', 'password1'), "Valid")
        self.assertEqual(login('user1@uwm.edu', 'password2'),
                         "The password that you entered is not correct.  Please retry.")
        self.assertEqual(login('user1@uwm.edu', 'NobodyPassword'),
                         "The password that you entered is not correct.  Please retry.")

    def test_login_nobody(self):
        self.assertEqual(login('user4@uwm.edu', 'password1'), "The username that you used does not exist. Please retry.")
        self.assertEqual(login('user4@uwm.edu', 'NobodyPassword'),
                         "The username that you used does not exist. Please retry.")


class TestGetUser(TestCase):
    def setUp(self):
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

    def test_get_user_from_supervisor(self):
        self.assertEqual(get_user('user2@uwm.edu'), self.user2, msg="Incorrect user object was obtained from the email")

    def test_get_user_from_instructor(self):
        self.assertEqual(get_user('user3@uwm.edu'), self.user3, msg="Incorrect user object was obtained from the email")

    def test_get_user_from_ta(self):
        self.assertEqual(get_user('user1@uwm.edu'), self.user1, msg="Incorrect user object was obtained from the email")

    def test_get_user_doesnt_exist(self):
        self.assertIsNone(get_user('user4@uwm.edu'), msg="Nonexistent user should yield a None return type")


class TestCourseInput(TestCase):

    def test_course_validation_good(self):
        self.assertTrue(validate_course_number(123))

    def test_course_validation_too_long(self):
        self.assertFalse(validate_course_number(1234))

    def test_course_validation_too_short(self):
        self.assertFalse(validate_course_number(12))


class TestCourseCreation(TestCase):
    def setUp(self):
        self.course1 = MyCourse(name="System Programming", number=337)
        self.course1.save()

    def create_course_number_used(self):
        self.assertEqual(create_course("New Course", 337),"A course with this number has already been created.  Try again.")

    def create_course_number_unused(self):
        a = MyCourse(name='Course1', number=123)
        self.assertEqual(create_course('Course1', 123), a)

    def create_course_number_big(self):
        self.assertEqual(create_course("Course2", 37), "The course number is not 3 digits long.  Try again.")

    def create_course_number_small(self):
        self.assertEqual(create_course("Course2", 5678), "The course number is not 3 digits long.  Try again.")

class TestSectionInput(TestCase):

    def test_course_validation_good(self):
        self.assertTrue(validate_section_number(901))

    def test_course_validation_too_long(self):
        self.assertFalse(validate_section_number(90))

    def test_course_validation_too_short(self):
        self.assertFalse(validate_section_number(8012))

class TestSectionCreation(TestCase):
    def setUp(self):
        self.course1 = MyCourse(name="System Programming", number=337)
        self.course1.save()

        self.section1 = MySection(course=self.course1, number=901)
        self.section1.save()

    def create_section_number_used(self):
        self.assertEqual(create_section(self.course1, 901), "A section with this number within this course has already been created.  Try again.")

    def create_section_number_unused(self):
        a = MySection(course=self.course1, number=801)
        self.assertEqual(create_section(self.course1, 801), a)

    def create_section_number_big(self):
        self.assertEqual(create_section(self.course1, 8098), "The section number is not 3 digits long.  Try again.")

    def create_section_number_small(self):
        self.assertEqual(create_section(self.course1, 83), "The section number is not 3 digits long.  Try again.")