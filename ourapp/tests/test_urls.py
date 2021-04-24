from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ourapp import views
from ourapp.views import Login, Course, Accounts, Section


class TestUrls(SimpleTestCase):

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, Login)

    def test_course_url_is_resolved(self):
        url = reverse('course')
        self.assertEquals(resolve(url).func.view_class, Course)

    def test_account_url_is_resolved(self):
        url = reverse('account')
        self.assertEquals(resolve(url).func.view_class, Accounts)

    def test_section_url_is_resolved(self):
        url = reverse('section')
        self.assertEquals(resolve(url).func.view_class, Section)