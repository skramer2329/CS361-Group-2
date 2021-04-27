from django.test import TestCase, Client
from ourapp.models import MyCourse, MySection, MyUser
#models to test are: MyUser, MyCourse, and Section

class TestMyUserModel(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                last_name='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                                           address='123 main st.', phone_number='123', role='ta')
        self.user1.save()

        self.user2 = MyUser.objects.create(email='user2@uwm.edu', password='password2',
                                           first_name='joeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
                last_name='johnson', address='123 main st.', phone_number='123', role='supervisor')
        self.user2.save()

        self.user3 = MyUser.objects.create(email='user3@uwm.edu', password='password3',
                                           first_name='joeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',
                                           last_name='johnsonnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn'
                                                     '', address='123 main st.', phone_number='123',role='instructor')
        self.user3.save()

        self.user4 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='a',
                                           last_name='a', address='123 main st.', phone_number='123', role='ta')
        self.user4.save()

        self.user5 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='',
                                           last_name='johnson', address='123 main st.', phone_number='123', role='ta')
        self.user5.save()

        self.user6 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                                           last_name='', address='123 main st.', phone_number='123', role='ta')
        self.user6.save()

        self.user7 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='',
                                           last_name='', address='123 main st.', phone_number='123', role='ta')
        self.user7.save()


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

        self.assertEqual(self.user1.__str__(), self.user1.first_name+ " " + self.user1.last_name)

    def test_str_short_short(self):

        self.assertEqual(self.user4.__str__(), self.user4.first_name+ " " + self.user4.last_name)

    def test_str_long_short(self):

        self.assertEqual(self.user2.__str__(), self.user2.first_name + " " + self.user2.last_name)

    def test_str_long_long(self):

        self.assertEqual(self.user3.__str__(), self.user3.first_name + " " + self.user3.last_name)

    def test_str_fname_blank(self):

        self.assertEqual(self.user5.__str__(), self.user5.first_name + " " + self.user5.last_name)

    def test_str_lname_blank(self):

        self.assertEqual(self.user6.__str__(), self.user6.first_name + " " + self.user6.last_name)

    def test_str_fname_lname_blank(self):

        self.assertEqual(self.user7.__str__(), self.user7.first_name + " " + self.user7.last_name)


class TestCourseModel(TestCase):

    def setUp(self):
        self.course1 = MyCourse(name="Introduction to Software Engineering", number=361)
        self.course1.save()

        self.course2 = MyCourse(name="Course", number=111)
        self.course2.save()

        self.user1 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                                           last_name='johnson',address='123 main st.', phone_number='123', role='ta')
        self.user1.save()

        self.course3 = MyCourse(name="Third Course", number=222)
        self.course3.save()
        self.course3.people.add(self.user1)
        self.course3.save()

    def test_course_str_long(self):
        self.assertEqual(self.course1.__str__(), "Introduction to Software Engineering")

    def test_course_str_short(self):
        self.assertEqual(self.course2.__str__(), "Course")

    def test_course_str_with_user(self):
        self.assertEqual(self.course3.__str__(), "Third Course")


class TestSectionModel(TestCase):
    def setUp(self):
        self.course1 = MyCourse(name="Introduction to Software Engineering", number=361)
        self.course1.save()

        self.user1 = MyUser.objects.create(email='user1@uwm.edu', password='password1', first_name='joe',
                                           last_name='johnson', address='123 main st.', phone_number='123', role='ta')
        self.user1.save()

        self.section901 = MySection(number=901, course=self.course1, teacher=self.user1)
        self.section901.save()

        self.section902 = MySection(number=902, course=self.course1)
        self.section902.save()

    def test_section_str_with_teacher(self):
        self.assertEqual(self.section901.__str__(), "361-901")

    def test_section_str_without_teacher(self):
        self.assertEqual(self.section902.__str__(), "361-902")
