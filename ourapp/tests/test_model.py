from django.test import TestCase, Client
from ourapp.models import MyCourse, Section, MyUser
#models to test are: MyUser, MyCourse, and Section

class TestMyUserModel(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                last_name='johnson', address='123 main st.', phone_number='123', role='ta')
        self.user1.save()

        self.user2 = MyUser.objects.create(email='user2@uwm.edu', password='password2', first_name='joe',
                last_name='johnson', address='123 main st.', phone_number='123', role='supervisor')
        self.user2.save()

        self.user3 = MyUser.objects.create(email='user3@uwm.edu', password='password3', first_name='joe',
                                           last_name='johnson', address='123 main st.', phone_number='123',
                                           role='instructor')
        self.user3.save()

    def is_ta(self):
        self.assertTrue(is_ta("user1@uwm.edu"))
        self.assertFalse(is_ta("user2@uwm.edu"))
        self.assertFalse(is_ta("user3@uwm.edu"))