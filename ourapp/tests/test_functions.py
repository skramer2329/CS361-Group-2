from django.test import TestCase, Client
from ourapp.models import MyCourse, MySection, MyUser
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from ourapp.helper_methods import login
from django.contrib.auth.models import User
from django.conf import settings
from importlib import import_module
from ourapp.helper_methods import login, get_user, CreateAccountsFunction, valid_email_format, valid_phone_number


class TestCanLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                            last_name='johnson', address='123 main st.', phone_number='123', role='ta')
        self.user1.save()

        self.user2 = MyUser.objects.create(email='user2@uwm.edu', password='password2', first_name='joe',
                        last_name='johnson', address='123 main st.', phone_number='123',role='ta')


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

    def test_get_user_from_supervisor(self):
        self.assertEqual(get_user('user2@uwm.edu'), self.user2)

    def test_get_user_from_instructor(self):
        self.assertEqual(get_user('user3@uwm.edu'), self.user3)

    def test_get_user_from_ta(self):
        self.assertEqual(get_user('user1@uwm.edu'), self.user1)

    def test_get_user_doesnt_exist(self):
        self.assertIsNone(get_user('user4@uwm.edu'))

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


    def test_valid_email_format_no_at_in_email_address_returns_no_at_message(self):
        self.assertEqual(valid_email_format(self.email1) == "Email does not contain @.", msg="Email not containing at symbol should fail validation.")

    def test_valid_email_format_space_in_email_address_returns_no_spaces_allowed_message(self):
        self.assertEqual(valid_email_format(self.email2) == "Email should not contain a space.", msg="Email cannot contain a space.")

    def test_valid_email_format_space_in_email_and_no_at_returns_no_at_message(self):
        self.assertEqual(valid_email_format(self.email3) == "Email does not contain @.", msg="Email containing both a space and not containing an @ symbol should warn about the @.")

    def test_valid_email_format_valid_email_returns_valid(self):
        self.assertEqual(valid_email_format(self.email4) == "Valid", msg="Valid email format returns valid message.")

    def test_valid_phone_number_invalid_phone_number_returns_false(self):
        self.assertFalse(valid_phone_number(self.phonenumber1), msg="phone number containing letters should not be valid phone number")

    def test_valid_phone_number_valid_phone_number_returns_true(self):
        self.assertTrue(valid_phone_number(self.phonenumber2), msg="valid phone number should pass test valid phone number.")

    def test_CreateAccountsFunction_at_missing_in_email_no_space_valid_phone_number_returns_email_no_at_message(self):
        self.assertEqual(CreateAccountsFunction(self.email1, self.phonenumber2) == "Email format must contain '@' symbol.", msg="should return no at message.")

    def test_CreateAccountsFunction_at_missing_in_email_space_valid_phone_number_returns_email_no_at_message(self):
        self.assertEqual(CreateAccountsFunction(self.email3, self.phonenumber2) == "Email format must contain '@' symbol.", msg="should return no at message.")

    def test_CreateAccountsFunction_at_missing_in_email_no_space_invalid_phone_number_returns_email_no_at_message(self):
        self.assertEqual(CreateAccountsFunction(self.email1, self.phonenumber1) == "Email format must contain '@' symbol.", msg="should return no at message.")

    def test_CreateAccountsFunction_at_missing_in_email_space_invalid_phone_number_returns_email_no_at_message(self):
        self.assertEqual(CreateAccountsFunction(self.email3, self.phonenumber1) == "Email format must contain '@' symbol.", msg="should return no at message.")

    def test_CreateAccountsFunction_at_space_valid_phone_number_returns_no_spaces_message(self):
        self.assertEqual(CreateAccountsFunction(self.email2, self.phonenumber2) == "Email should not contain a space.", msg="should return no should not contain space message.")

    def test_CreateAccountsFunction_at_space_invalid_valid_phone_number_returns_no_spaces_message(self):
        self.assertEqual(CreateAccountsFunction(self.email2, self.phonenumber1) == "Email should not contain a space.", msg="should return no should not contain space message.")

    def test_CreateAccountsFunction_at_no_space_invalid_phone_number_returns_invalid_phone_number_message(self):
        self.assertEqual(CreateAccountsFunction(self.email4, self.phonenumber1) == "Phone number must be all digits.  Do not type hyphens.", msg="should return phone number criteria.")

    def test_CreateAccountsFunction_at_missing_in_email_no_space_valid_phone_number_returns_email_no_at_message(self):
        self.assertEqual(CreateAccountsFunction(self.email4, self.phonenumber2) == "Valid", msg="should have been valid data.")