from django.test import TestCase, Client
from ourapp.models import MyCourse, Section, MyUser

class TestLoginFunction(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                            last_name='johnson', address='123 main st.', phone_number='123', role='ta')
        self.user1.save()

        self.user2 = MyUser.objects.create(email='user2@uwm.edu', password='password2', first_name='joe',
                        last_name='johnson', address='123 main st.', phone_number='123',role='ta')

    def test_valid_email(self):
        self.assertTrue(canLogin('user1@uwm.edu', 'password1'), "canLogin function "
                                        "should allow login to occur when data is stored")

        self.assertFalse(canLogin('user1@uwm.edu', 'password2'), "canLogin function "
                            "should return false with wrong password, even if email is correct")

    def test_invalid_email(self):
        self.assertFalse(canLogin('user3@uwm.edu', 'password3'), "canLogin function "
                                "did not reject the case with an unused email and unused password")

        self.assertFalse(canLogin('user3@uwm.edu', 'password2'), "canLogin function did "
                        "not reject the case with an unused email and password for another user")

