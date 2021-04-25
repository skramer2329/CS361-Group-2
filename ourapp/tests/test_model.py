from django.test import TestCase, Client
from ourapp.models import MyCourse, Section, MyUser
#models to test are: MyUser, MyCourse, and Section

class TestMyUserModel(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                last_name='', address='123 main st.', phone_number='123', role='ta')
        self.user1.save()

        self.user2 = MyUser.objects.create(email='user2@uwm.edu', password='password2', first_name='joe',
                last_name='johnson', address='123 main st.', phone_number='123', role='supervisor')
        self.user2.save()

        self.user3 = MyUser.objects.create(email='user3@uwm.edu', password='password3', first_name='joe',
                                           last_name='johnson', address='123 main st.', phone_number='123',
                                           role='instructor')
        self.user3.save()

        self.user4 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='a',
                last_name='a', address='123 main st.', phone_number='123', role='ta')
        self.user4.save()

    def test_is_ta(self):
        self.assertTrue(self.user1.is_ta())
        self.assertFalse(self.user2.is_ta())
        self.assertFalse(self.user3.is_ta())

    def test_is_instructor(self):
        self.assertFalse(self.user1.is_instructor())
        self.assertFalse(self.user2.is_instructor())
        self.assertTrue(self.user3.is_instructor())

    def test_is_supervisor(self):
        self.assertFalse(self.user1.is_supervisor())
        self.assertTrue(self.user2.is_supervisor())
        self.assertFalse(self.user3.is_supervisor())

    def test_str_short_long(self):
        self.assertEqual("")

    def test_str_short_short(self):
        self.assertEqual(self.user4.__str__(), self.user4.first_name+ " " + self.user4.last_name)

    def test_str_long_short(self):
        pass

    def test_str_long_long(self):
        pass