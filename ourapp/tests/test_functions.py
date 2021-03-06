from django.test import TestCase, Client
from ourapp.models import MyCourse, MySection, MyUser
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from ourapp.helper_methods import login, ValidTeacherForSection
from django.contrib.auth.models import User
from django.conf import settings
from importlib import import_module

from ourapp.helper_methods import login, get_user, validate_course_number, create_course, \
    validate_section_number, create_section, ValidateDeleteAccount

from ourapp.helper_methods import CreateAccountsFunction, valid_email_format, valid_phone_number


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

    def test_login_email_with_space(self):
        with self.assertRaises(TypeError, msg = "The login() function must take an email as its first parameter"):
            login("instructor@uwm. edu", "password")

    def test_login_email_without_at_symbol(self):
        with self.assertRaises(TypeError, msg = "The login() function must take an email as its first parameter"):
            login("instructoruwm.edu", "password")

    def test_login_email_integer_as_email(self):
        with self.assertRaises(TypeError, msg = "The login() function must take an email as its first parameter"):
            login(123, "password")

    def test_login_email_too_many_arguments(self):
        with self.assertRaises(TypeError, msg = "The login() function must take 2 parameters"):
            login(123, "password", "string")

    def test_login_email_one_argument(self):
        with self.assertRaises(TypeError, msg = "The login() function must take 2 parameters"):
            login("email@uwm.edu")

    def test_login_email_no_arguments(self):
        with self.assertRaises(TypeError, msg = "The login() function must take 2 parameters"):
            login()


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

    def test_get_user_email_with_space(self):
        with self.assertRaises(TypeError, msg = "The get_user() function must take an email as its only parameter"):
            get_user("instructor@uwm. edu")

    def test_get_user_without_at_symbol(self):
        with self.assertRaises(TypeError, msg = "The ger_user() function must take an email as its only parameter"):
            get_user("instructoruwm.edu")

    def test_get_user_integer_as_email(self):
        with self.assertRaises(TypeError, msg = "The get_user() function must take an email as its only parameter"):
            get_user(123)

    def test_get_user_no_arguments(self):
        with self.assertRaises(TypeError, msg = "The get_user() function must take an email parameter"):
            get_user()

    def test_get_user_too_many_arguments(self):
        with self.assertRaises(TypeError, msg="The get_user() function must only take one email parameter"):
            get_user("email@uwm.edu", "string2")


class TestCourseInput(TestCase):

    def test_course_validation_good(self):
        self.assertTrue(validate_course_number(123))

    def test_course_validation_too_long(self):
        self.assertFalse(validate_course_number(1234))

    def test_course_validation_too_short(self):
        self.assertFalse(validate_course_number(12))

    def test_course_validation_not_integer(self):
        with self.assertRaises(TypeError, msg = "There must be an integer input to the validate_course_number() function"):
            validate_course_number("string")

    def test_course_validation_no_arguments(self):
        with self.assertRaises(TypeError, msg = "There must be an integer input to the validate_course_number() function"):
            validate_course_number()

    def test_course_validation_too_many_arguments(self):
        with self.assertRaises(TypeError,
                               msg="There must be only one integer input to the validate_course_number() function"):
            validate_course_number(123, 123)


class TestCourseCreation(TestCase):
    def setUp(self):
        self.course1 = MyCourse(name="System Programming", number=337)
        self.course1.save()

    def test_create_course_number_used(self):
        self.assertIsInstance(create_course("New Course", 337), MyCourse)

    def test_create_course_number_unused(self):
        self.assertIsInstance(create_course("Course1", 123), MyCourse)

    def test_create_course_number_big(self):
        self.assertEqual(create_course("Course2", 37), "The course number is not 3 digits long.  Try again.")

    def test_create_course_number_small(self):
        self.assertEqual(create_course("Course2", 5678), "The course number is not 3 digits long.  Try again.")

    def test_create_course_name_not_string(self):
        with self.assertRaises(TypeError, msg= "The first parameter in the create_course() function must be a string"):
            create_course(123, 123)

    def test_create_course_number_not_int(self):
        with self.assertRaises(TypeError, msg= "The second parameter in the create_course() function must be an int"):
            create_course("name of course", "second parameter")

    def test_create_course_not_enough_args(self):
        with self.assertRaises(TypeError, msg= "The create_course() function must take 2 parameters"):
            create_course("name of course")

    def test_create_course_too_many_args(self):
        with self.assertRaises(TypeError, msg= "The create_course() function must take 2 parameters"):
            create_course("name of course", 123, "arg3")

class TestSectionInput(TestCase):

    def test_course_validation_good(self):
        self.assertTrue(validate_section_number(901))

    def test_course_validation_too_long(self):
        self.assertFalse(validate_section_number(90))

    def test_course_validation_too_short(self):
        self.assertFalse(validate_section_number(8012))

    def test_course_validation_not_int(self):
        with self.assertRaises(TypeError, msg= "The validate_section_number() function must take an integer parameter"):
            validate_section_number("course_num")

    def test_course_validation_too_many_args(self):
        with self.assertRaises(TypeError, msg= "The validate_section_number() function must take only one integer parameter"):
            validate_section_number(123, "course_num")

    def test_course_validation_not_enough_args(self):
        with self.assertRaises(TypeError, msg= "The validate_section_number() function must take an integer parameter"):
            validate_section_number()

class TestSectionCreation(TestCase):
    def setUp(self):
        self.course1 = MyCourse(name="System Programming", number=337)
        self.course1.save()

        self.section1 = MySection(course=self.course1, number=901)
        self.section1.save()

    def test_create_section_number_used(self):
        self.assertEqual(create_section(self.course1, 901), "A section with this number within this course has already been created.  Try again.")

    def test_create_section_number_unused(self):
        self.assertIsInstance(create_section(self.course1, 801), MySection)

    def test_create_section_number_big(self):
        self.assertEqual(create_section(self.course1, 8098), "The section number is not 3 digits long.  Try again.")

    def test_create_section_number_small(self):
        self.assertEqual(create_section(self.course1, 83), "The section number is not 3 digits long.  Try again.")

    def test_create_section_first_param_not_course(self):
        with self.assertRaises(TypeError, msg= "The create_section() function must take a course object as its first argument"):
            create_section("hello", 83)

    def test_create_section_second_param_not_int(self):
        with self.assertRaises(TypeError, msg= "The create_section() function must take an integer as its second argument"):
            create_section(self.course1, "string")

    def test_create_section_too_many_args(self):
        with self.assertRaises(TypeError, msg="The create_section() function must take two arguments"):
            create_section(self.course1, 456, "third")

    def test_create_section_not_enough_args(self):
        with self.assertRaises(TypeError, msg="The create_section() function must take two arguments"):
            create_section(self.course1)

class TestValidInputForAccountCreation(TestCase):
    email1 = None
    email2 = None
    email3 = None
    email4 = None
    phonenumber1 = None
    phonenumber2 = None

    def setUp(self):
        self.email1 = "testuwm.edu"
        self.email2 = "test @uwm.edu"
        self.email3 = "test uwm.edu"
        self.email4 = "test@uwm.edu"
        self.phonenumber1 = "414alphabet"
        self.phonenumber2 = "4144144114"


    def test_valid_email_format_no_at_in_email_address(self):
        self.assertEqual(valid_email_format(self.email1), "Email does not contain @.", msg="Email not containing at symbol should fail validation.")

    def test_valid_email_format_space_in_email_address(self):
        self.assertEqual(valid_email_format(self.email2), "Email should not contain a space.", msg="Email cannot contain a space.")

    def test_valid_email_format_space_in_email_and_no_at(self):
        self.assertEqual(valid_email_format(self.email3), "Email does not contain @.", msg="Email containing both a space and not containing an @ symbol should warn about the @.")

    def test_valid_email_format_valid_email(self):
        self.assertEqual(valid_email_format(self.email4), "Valid", msg="Valid email format returns valid message.")

    def test_valid_email_format_not_string(self):
        with self.assertRaises(TypeError, msg= "The valid_email_format() function must take the email as a string for input"):
            valid_email_format(123)

    def test_valid_email_format_no_args(self):
        with self.assertRaises(TypeError, msg= "The valid_email_format() function must take an email as a string for input"):
            valid_email_format()

    def test_valid_email_too_many_args(self):
        with self.assertRaises(TypeError, msg= "The valid_email_format() function must take an email as a string for input"):
            valid_email_format(self.email1, "another")

    def test_valid_phone_number_invalid_phone_number(self):
        self.assertFalse(valid_phone_number(self.phonenumber1), msg="phone number containing letters should not be valid phone number")

    def test_valid_phone_number_valid_phone_number(self):
        self.assertTrue(valid_phone_number(self.phonenumber2), msg="valid phone number should pass test valid phone number.")

    def test_CreateAccountsFunction_at_missing_in_email_no_space_valid_phone_number(self):
        self.assertEqual(CreateAccountsFunction(self.email1, self.phonenumber2) , "Email format must contain '@' symbol.", msg="should return no at message.")

    def test_CreateAccountsFunction_at_missing_in_email_space_valid_phone_number(self):
        self.assertEqual(CreateAccountsFunction(self.email3, self.phonenumber2), "Email format must contain '@' symbol.", msg="should return no at message.")

    def test_CreateAccountsFunction_at_missing_in_email_no_space_invalid_phone_number(self):
        self.assertEqual(CreateAccountsFunction(self.email1, self.phonenumber1), "Email format must contain '@' symbol.", msg="should return no at message.")

    def test_CreateAccountsFunction_at_missing_in_email_space_invalid_phone_number(self):
        self.assertEqual(CreateAccountsFunction(self.email3, self.phonenumber1), "Email format must contain '@' symbol.", msg="should return no at message.")

    def test_CreateAccountsFunction_at_space_valid_phone_number(self):
        self.assertEqual(CreateAccountsFunction(self.email2, self.phonenumber2), "Email should not contain a space.", msg="should return no should not contain space message.")

    def test_CreateAccountsFunction_at_space_invalid_valid_phone_number(self):
        self.assertEqual(CreateAccountsFunction(self.email2, self.phonenumber1), "Email should not contain a space.", msg="should return no should not contain space message.")

    def test_CreateAccountsFunction_at_no_space_invalid_phone_number(self):
        self.assertEqual(CreateAccountsFunction(self.email4, self.phonenumber1), "Phone number must be all digits.  Do not type hyphens.", msg="should return phone number criteria.")

    def test_CreateAccountsFunction_at_missing_in_email_no_space_valid_phone_number(self):
        self.assertEqual(CreateAccountsFunction(self.email4, self.phonenumber2), "Valid", msg="should have been valid data.")


class TestValidTeacherForSection(TestCase):

    def setUp(self):
        self.user1 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                                          last_name='johnson', address='123 main st.', phone_number='123', role='supervisor')
        self.user1.save()

        self.user2 = MyUser.objects.create(email='user2@uwm.edu', password='password2', first_name='joe',
                                           last_name='johnson', address='123 main st.', phone_number='123',
                                           role='instructor')
        self.user2.save()

        self.user3 = MyUser.objects.create(email='user3@uwm.edu', password='password3', first_name='joe',
                                           last_name='johnson', address='123 main st.', phone_number='123',
                                           role='ta')
        self.user3.save()

        self.user4 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                                           last_name='johnson', address='123 main st.', phone_number='123',
                                           role='')
        self.user4.save()

        self.course1 = MyCourse(name="System Programming", number=337)
        self.course1.save()

        self.section1 = MySection(course=self.course1, number=837)
        self.section1.save()

        self.section2 = MySection(course=self.course1, number=200)
        self.section2.save()

        self.section3 = MySection(course=self.course1, number=900)
        self.section3.save()

        self.section4 = MySection(course=self.course1, number=300)
        self.section4.save()

    #user2 = instructor
    #user3 = ta
    def test_valid_ta_and_valid_lab_section(self):
        self.assertTrue(ValidTeacherForSection(self.user3, self.section1))
        self.assertTrue(ValidTeacherForSection(self.user3, self.section3))

    def test_valid_instructor_to_lecture_section(self):
        self.assertTrue(ValidTeacherForSection(self.user2, self.section2))
        self.assertTrue(ValidTeacherForSection(self.user2, self.section4))

    def test_valid_ta_and_invalid_section(self):
        self.assertTrue(ValidTeacherForSection(self.user3, self.section2))
        self.assertTrue(ValidTeacherForSection(self.user3, self.section4))

    def test_valid_instructor_and_invalid_section(self):
        self.assertTrue(ValidTeacherForSection(self.user2, self.section1))
        self.assertTrue(ValidTeacherForSection(self.user2, self.section3))

    def test_invalid_role_and_valid_section(self):
        self.assertTrue(ValidTeacherForSection(self.user1, self.section3))

    def test_no_role_and_valid_section(self):
        self.assertTrue(ValidTeacherForSection(self.user4, self.section3))

    def test_not_MyUser(self):
        with self.assertRaises(TypeError):
            ValidTeacherForSection(self.section1, self.section1)
    def test_not_MySection(self):
        with self.assertRaises(TypeError):
            ValidTeacherForSection(self.user3, self.user3)

    def test_not_enough_args(self):
        with self.assertRaises(TypeError):
            ValidTeacherForSection(self.user3)

    def test_too_many_args(self):
        with self.assertRaises(TypeError):
            ValidTeacherForSection(self.user3, self.user3, self.user3)


class TestValidateDeleteAccount(TestCase):
    def test_session_email_deleted_email_same(self):
        self.assertEqual(ValidateDeleteAccount("test@uwm.edu", "test@uwm.edu"),
                         "Cannot delete the account that is logged into this session.")

    def test_session_email_deleted_email_different(self):
        self.assertEqual(ValidateDeleteAccount("test@uwm.edu", "test1@uwm.edu"), "Valid")

    def test_validate_delete_account_first_arg_bad(self):
        with self.assertRaises(TypeError, msg= "ValidateDeleteAccount() function must take the emails as strings"):
            ValidateDeleteAccount(123, "test@uwm.edu")

    def test_validate_delete_account_second_arg_bad(self):
        with self.assertRaises(TypeError, msg= "ValidateDeleteAccount() function must take the emails as strings"):
            ValidateDeleteAccount("test@uwm.edu", 123)

    def test_validate_delete_account_too_many_args(self):
        with self.assertRaises(TypeError, msg= "ValidateDeleteAccount() function must take only two emails"):
            ValidateDeleteAccount("test@uwm.edu", "test1@uwm.edu", "test2@uwm.edu")

    def test_validate_delete_account_not_enough_args(self):
        with self.assertRaises(TypeError, msg= "ValidateDeleteAccount() function requires two arguments"):
            ValidateDeleteAccount("test@uwm.edu")