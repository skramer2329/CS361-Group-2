from django.test import TestCase, Client
from ourapp.models import MyCourse, MySection, MyUser
from django.urls import reverse


# Create your tests here.

class TestLoginSuccess(TestCase):

    def setUp(self):
        self.client = Client()
        self.supervisor = MyUser(first_name="supervisor", last_name="super", email="testsupervisor@uwm.edu",
                                 password="supervisor",
                                 address="123 straight st", phone_number="1234567890", role="supervisor")
        self.supervisor.save()

        # self.emptyUserEmail = MyUser(first_name="supervisor", last_name="super", email="", password="supervisor",
        #                                        address="123 straight st", phone_number="1234567890", role="supervisor")
        # self.emptyUserEmail.save()
        self.instructor = MyUser(first_name="instructor", last_name="instruct", email="instructor@uwm.edu",
                                 password="instructor",
                                 address="123 corner st", phone_number="7777777", role="instructor")
        self.ta = MyUser.objects.create(first_name="ta", last_name="assist", email="ta@uwm.edu",
                                        password="ta", address="123 round st", phone_number="1234567890", role="ta")

    def test_correct_user_password_logs_in_successfully(self):

        response = self.client.post("/", {"uname": "testsupervisor@uwm.edu", "psw": "supervisor"}, follow=True)
        self.assertTemplateUsed(response, "course.html")
        #expected, actual
        #should contain course in context
        #successful redirect to correct template
        #could check session - is there a username in the session
        #reading from session - can just check the session


    def test_no_such_user_exists(self):
        response = self.client.post("/", {"uname": "", "psw": ""}, follow=True)
        self.assertEqual("The username that you used does not exist. Please retry.", response.context["message"])

    def test_user_exists_but_invalid_password(self):
        response = self.client.post("/", {"uname": self.supervisor.email, "psw": "WrongPassword"}, follow=True)
        self.assertEqual("The password that you entered is not correct.  Please retry.", response.context["message"])

    def test_user_exists_but_valid_password_for_wrong_user_doesnt_log_in(self):
        response = self.client.post("/", {"uname": self.supervisor.email, "psw": self.instructor.password}, follow=True)
        self.assertEqual("The password that you entered is not correct.  Please retry.", response.context["message"])


class TestAccountCreation(TestCase):
    def setUp(self):
        self.client = Client()
        self.super = MyUser(first_name="supervisor", last_name="super", email="test1@uwm.edu", password="pass1",
                            address="123 straight st", phone_number="1234567890", role="supervisor")
        self.super.save()
        self.instructor = MyUser(first_name="instructor", last_name="super", email="test2@uwm.edu",
                                 password='pass2', address="123 straight st", phone_number="1234567890",
                                 role='instructor')
        self.instructor.save()

        self.ta = MyUser(first_name="ta", last_name="super", email="test3@uwm.edu",
                         password='pass3', address="123 straight st", phone_number="1234567890",
                         role='ta')
        self.ta.save()

    def test_create_new_supervisor(self):
        response = self.client.post("/account/",
                                    {"first_name": "bill", "last_name": "johnson", "email": "newsupervisor@uwm.edu",
                                     "password": "pass3",
                                     "phone_number": "1234567890", "address": "123 Main St, Milwaukee, WI, 53211",
                                     "role": "supervisor"}, follow=True)
        self.assertIn(MyUser.objects.get(email='newsupervisor@uwm.edu'), response.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual("Account created successfully", response.context["message"])

        # testing a password that was already used
        r = self.client.post("/account/", {"email": "test4@uwm.edu", "password": "pass2", "first_name": "bill","last_name": "johnson", "phone_number": "1234567890",
                                           "address": "123 Main St, Milwaukee, WI, 53211",
                                           "role": "supervisor"}, follow=True)
        self.assertIn(MyUser.objects.get(email="test4@uwm.edu"), r.context['accounts'],
                      "new account not showing up in rendered response")
        self.assertEqual("Account created successfully", r.context["message"])

    def test_create_new_instructor(self):

        r = self.client.post("/accounts/", {"email": "newinstructor@uwm.edu", "password": "pass5", "first_name": "bill",
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

        # self.session1 = self.client.session
        # self.session1['email'] = self.supervisor.email
        # self.session1.save()

    def test_createNewCourse(self):

        r = self.client.post("/course/", {"name": "Math", "number": 100, "course_button": ''}, follow=True)
        self.assertEqual("Course successfully added", r.context['message'])

    def test_courseTaken(self):
        # course name is already used but not number
        r = self.client.post("/course/", {"name": self.course.name, "number": 103, "course_button": ''}, follow=True)
        print(r.context['message'])
        self.assertEqual(r.context['message'], "Course successfully added")

        # course number is already used but not name

        r = self.client.post("/course/", {"name": "CompSci", "number": 102, "course_button": ''}, follow=True)
        print(r.context['message'])
        self.assertEqual(r.context['message'], "Course successfully added")

        # course name and number are already used.

        r = self.client.post("/course/", {"name": self.course.name,
                                                "number": self.course.number, "course_button": ''}, follow=True)
        self.assertEqual(r.context['message'], "A course with this name and number has already been created.  Try again.")


class TestSectionCreation(TestCase):
    client = None
    courseList = None

    def setUp(self):
        self.client = Client()
        self.mathCourse = MyCourse(name="Math", number=100)
        self.mathCourse.save()
        self.mathSection = MySection(course=self.mathCourse, number=1)


        self.mathSection.save()

        """self.courseList = {"Math": 1, "Chemistry": 2, "Art": 3}
        for i in self.courseList.keys():
            temp = MyCourse(name=i, number=self.courseList[i])
            temp.save()
            for j in self.courseList[i]:
                MySection(course=temp, number=j)"""

    # number is not three digits
    def test_add_section_already_exists(self):
        c = self.client.session
        c["number"] = 1
        c.save

        resp = self.client.post("/course/", {"course_selection": MyCourse.objects.get(name=self.mathCourse.name, number=self.mathCourse.number).id,
                                                    "section_number":self.mathSection.number, "section_button": ''}, follow=True)
        print(resp.context)
        self.assertEqual("The section number is not 3 digits long.  Try again.", resp.context["message"])

    def test_add_section(self):

        resp = self.client.post("/course/", {"course_selection": MyCourse.objects.get(name=self.mathCourse.name, number=self.mathCourse.number).id, "section_number": 400, "section_button": ''}, follow=True)
        print(resp.context)
        self.assertEqual("Section successfully added", resp.context["message"])

class TestAssignToCourse(TestCase):

    def setUp(self):
        self.client = Client()
        self.mathCourse = MyCourse(name="Math", number=100)
        self.mathCourse.save()

        self.instructor = MyUser(first_name="instructor", last_name="super", email="test2@uwm.edu",
                                 password='pass2', address="123 straight st", phone_number="1234567890",
                                 role='instructor')

        self.instructor2 = MyUser(first_name="instructor2", last_name="super2", email="test3@uwm.edu",
                                 password='pass2', address="123 straight st", phone_number="1234567890",
                                 role='instructor')

        self.ta = MyUser.objects.create(first_name="ta", last_name="assist", email="ta@uwm.edu",
                                        password="ta", address="123 round st", phone_number="1234567890", role="ta")

        self.ta2 = MyUser.objects.create(first_name="ta2", last_name="assist", email="ta2@uwm.edu",
                                        password="ta", address="123 round st", phone_number="1234567890", role="ta")

        self.instructor.save()
        self.ta.save()
        self.instructor2.save()
        self.ta2.save()

    def test_assign_instructor_to_course(self):
        resp = self.client.post("/course/", {
            "course_selection": MyCourse.objects.get(name=self.mathCourse.name, number=self.mathCourse.number).id,
            "person_selection": MyUser.objects.get(email=self.instructor.email).id, "ass_butt": ''}, follow=True)

        self.assertEqual("Course assignments updated", resp.context["message"])

    def test_assign_ta_to_course(self):
        resp = self.client.post("/course/", {
            "course_selection": MyCourse.objects.get(name=self.mathCourse.name, number=self.mathCourse.number).id,
            "person_selection": MyUser.objects.get(email=self.ta.email).id, "ass_butt": ''}, follow=True)

        self.assertEqual("Course assignments updated", resp.context["message"])

    def test_assign_multiple_assignments(self):
        resp = self.client.post("/course/", {
            "course_selection": MyCourse.objects.get(name=self.mathCourse.name, number=self.mathCourse.number).id,
            "person_selection": MyUser.objects.get(email=self.instructor.email).id, "ass_butt": ''}, follow=True)
        self.assertEqual("Course assignments updated", resp.context["message"])

        resp = self.client.post("/course/", {
            "course_selection": MyCourse.objects.get(name=self.mathCourse.name, number=self.mathCourse.number).id,
            "person_selection": MyUser.objects.get(email=self.instructor2.email).id, "ass_butt": ''}, follow=True)
        self.assertEqual("Course assignments updated", resp.context["message"])

        resp = self.client.post("/course/", {
            "course_selection": MyCourse.objects.get(name=self.mathCourse.name, number=self.mathCourse.number).id,
            "person_selection": MyUser.objects.get(email=self.ta.email).id, "ass_butt": ''}, follow=True)
        self.assertEqual("Course assignments updated", resp.context["message"])

        resp = self.client.post("/course/", {
            "course_selection": MyCourse.objects.get(name=self.mathCourse.name, number=self.mathCourse.number).id,
            "person_selection": MyUser.objects.get(email=self.ta2.email).id, "ass_butt": ''}, follow=True)
        self.assertEqual("Course assignments updated", resp.context["message"])

class TestAssignToSection(TestCase):

    def setUp(self):
        self.client = Client()
        self.mathCourse = MyCourse(name="Math", number=100)
        self.mathCourse.save()
        self.labSection = MySection(course=self.mathCourse, number=800, teacher=None)
        self.lectureSection = MySection(course=self.mathCourse, number=301, teacher=None)
        self.labSection.save()
        self.lectureSection.save()




        self.supervisor = MyUser(first_name="supervisor", last_name="super", email="test1@uwm.edu", password="pass1",
                            address="123 straight st", phone_number="1234567890", role="supervisor")

        self.instructor = MyUser(first_name="instructor", last_name="super", email="test2@uwm.edu",
                                 password='pass2', address="123 straight st", phone_number="1234567890",
                                 role='instructor')

        self.instructor2 = MyUser(first_name="instructor2", last_name="super2", email="test3@uwm.edu",
                                 password='pass2', address="123 straight st", phone_number="1234567890",
                                 role='instructor')

        self.ta = MyUser.objects.create(first_name="ta", last_name="assist", email="ta@uwm.edu",
                                        password="ta", address="123 round st", phone_number="1234567890", role="ta")

        self.ta2 = MyUser.objects.create(first_name="ta2", last_name="assist", email="ta2@uwm.edu",
                                        password="ta", address="123 round st", phone_number="1234567890", role="ta")

        self.instructor.save()
        self.ta.save()
        self.instructor2.save()
        self.ta2.save()
        self.supervisor.save()

        self.labSection2 = MySection(course=self.mathCourse, number=801, teacher=self.ta2)
        self.lectureSection2 = MySection(course=self.mathCourse, number=302, teacher=self.instructor2)
        self.labSection2.save()
        self.lectureSection2.save()

    def test_assign_ta_to_lecture_fails(self):
        resp = self.client.post("/course/", {
            "section_selection": MySection.objects.get(number=self.lectureSection.number, course=self.mathCourse).id,
            "person_selection": MyUser.objects.get(email=self.ta.email).id, "ass_section_butt": ''}, follow=True)
        self.assertEqual("Only Instructors can be assigned to lecture sections.", resp.context["message"])

    def test_assign_ta_to_empty_lab(self):
        resp = self.client.post("/course/", {
            "section_selection": MySection.objects.get(number=self.labSection.number, course=self.mathCourse).id,
            "person_selection": MyUser.objects.get(email=self.ta.email).id, "ass_section_butt": ''}, follow=True)
        self.assertEqual("Added Teacher to section.", resp.context["message"])

    def test_assign_ta_to_ta_lab(self):

        resp = self.client.post("/course/", {
            "section_selection": MySection.objects.get(number=self.labSection2.number, course=self.mathCourse).id,
            "person_selection": MyUser.objects.get(email=self.ta.email).id, "ass_section_butt": ''}, follow=True)
        self.assertEqual("Teacher: ta2 assist was removed.\nTeacher: ta assist was added.", resp.context["message"])

    def test_assign_instructor_to_empty_lecture(self):
        resp = self.client.post("/course/", {
            "section_selection": MySection.objects.get(number=self.lectureSection.number, course=self.mathCourse).id,
            "person_selection": MyUser.objects.get(email=self.instructor.email).id, "ass_section_butt": ''}, follow=True)
        self.assertEqual("Added Teacher to section.", resp.context["message"])

    def test_assign_instructor_to_instructor_lecture(self):
        resp = self.client.post("/course/", {
            "section_selection": MySection.objects.get(number=self.lectureSection2.number, course=self.mathCourse).id,
            "person_selection": MyUser.objects.get(email=self.instructor.email).id, "ass_section_butt": ''}, follow=True)
        self.assertEqual("Teacher: instructor2 super2 was removed.\nTeacher: instructor super was added.", resp.context["message"])

    def test_assign_instructor_to_lab_fails(self):
        resp = self.client.post("/course/", {
            "section_selection": MySection.objects.get(number=self.labSection.number, course=self.mathCourse).id,
            "person_selection": MyUser.objects.get(email=self.instructor.email).id, "ass_section_butt": ''}, follow=True)
        self.assertEqual("Only TAs can be assigned to lab sections.", resp.context["message"])

    def test_assign_supervisor_to_section_fails(self):
        resp = self.client.post("/course/", {
            "section_selection": MySection.objects.get(number=self.labSection.number, course=self.mathCourse).id,
            "person_selection": MyUser.objects.get(email=self.supervisor.email).id, "ass_section_butt": ''},
                                follow=True)
        self.assertEqual("Only TAs can be assigned to lab sections.", resp.context["message"])

        resp = self.client.post("/course/", {
            "section_selection": MySection.objects.get(number=self.lectureSection.number, course=self.mathCourse).id,
            "person_selection": MyUser.objects.get(email=self.supervisor.email).id, "ass_section_butt": ''}, follow=True)
        self.assertEqual("Only Instructors can be assigned to lecture sections.", resp.context["message"])


class TestDeleteCourse(TestCase):

    def setUp(self):
        self.courses = MyCourse.objects.all()
        self.client = Client()
        self.mathCourse = MyCourse(name="Math", number=100)
        self.mathCourse.save()
        self.labSection = MySection(course=self.mathCourse, number=800, teacher=None)
        self.lectureSection = MySection(course=self.mathCourse, number=301, teacher=None)
        self.labSection.save()
        self.lectureSection.save()

        self.newCourse = MyCourse(name="CS", number=150)
        self.newCourse.save()

    def test_delete_course_no_sections(self):
        resp = self.client.post("/course/", {"course_to_remove": self.newCourse.id, "delCButt": ''}, follow=True)
        self.assertNotIn(self.newCourse, resp.context['courses'])
        self.assertEqual("Course successfully deleted", resp.context['message'])

    def test_delete_course_with_section(self):
        resp = self.client.post("/course/", {"course_to_remove": self.mathCourse.id, "delCButt": ''}, follow=True)

        self.assertNotIn(self.mathCourse, resp.context['courses'])
        self.assertEqual("Course successfully deleted", resp.context['message'])

class TestDeleteSection(TestCase):
    def setUp(self):
        self.courses = MyCourse.objects.all()
        self.client = Client()
        self.mathCourse = MyCourse(name="Math", number=100)
        self.mathCourse.save()
        self.labSection = MySection(course=self.mathCourse, number=800, teacher=None)
        self.lectureSection = MySection(course=self.mathCourse, number=201, teacher=None)
        self.labSection.save()
        self.lectureSection.save()

        self.newCourse = MyCourse(name="CS", number=150)
        self.newCourse.save()

    def test_delete_section_lab(self):
        resp = self.client.post("/course/", {"section_to_remove": self.labSection.id, "delSButt": ''}, follow=True)
        self.assertNotIn(self.labSection, resp.context['sections'])
        self.assertEqual("Section successfully deleted", resp.context['message'])

    def test_delete_section_lecture(self):
        resp = self.client.post("/course/", {"section_to_remove": self.lectureSection.id, "delSButt": ''}, follow=True)
        self.assertNotIn(self.lectureSection, resp.context['sections'])
        self.assertEqual("Section successfully deleted", resp.context['message'])


class TestEditAccounts(TestCase):

    def setUp(self):
        self.client = Client()
        self.super = MyUser(first_name="supervisor", last_name="super", email="test1@uwm.edu", password="pass1",
                            address="123 straight st", phone_number="1234567890", role="supervisor")
        self.super.save()
        self.instructor = MyUser(first_name="instructor", last_name="super", email="test2@uwm.edu",
                                 password='pass2', address="123 straight st", phone_number="1234567890",
                                 role='instructor')
        self.instructor.save()

        self.ta = MyUser(first_name="ta", last_name="super", email="test3@uwm.edu",
                         password='pass3', address="123 straight st", phone_number="1234567890",
                         role='ta')
        self.ta.save()

    def test_edit_account_first_name(self):
        print(self.ta.id)
        resp = self.client.post("/contacts/", {"first_name": "ta2", "last_name": "super", "email": "test3@uwm.edu",
                                           "password": "pass3", "address": "123 straight st",
                                           "phone_number": "1234567890",
                                           "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

    def test_edit_account_last_name(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super2", "email": "test3@uwm.edu",
                                           "password": "pass3", "address": "123 straight st",
                                           "phone_number": "1234567890",
                                           "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

    def test_edit_account_valid_email(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super", "email": "test32@uwm.edu",
                                               "password": "pass3", "address": "123 straight st",
                                               "phone_number": "1234567890",
                                               "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

    def test_edit_account_invalid_email(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super", "email": "test3uwm.edu",
                                               "password": "pass3", "address": "123 straight st",
                                               "phone_number": "1234567890",
                                               "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Email format must contain '@' symbol.", resp.context["message"])

    def test_edit_account_password(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super", "email": "test3@uwm.edu",
                                               "password": "pass4", "address": "123 straight st",
                                               "phone_number": "1234567890",
                                               "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

    def test_edit_address(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super", "email": "test3@uwm.edu",
                                               "password": "pass3", "address": "1234 straight st",
                                               "phone_number": "1234567890",
                                               "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

    def test_edit_phone_number(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super", "email": "test3@uwm.edu",
                                               "password": "pass3", "address": "123 straight st",
                                               "phone_number": "1234567899",
                                               "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

    def test_edit_role(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super", "email": "test3@uwm.edu",
                                               "password": "pass3", "address": "123 straight st",
                                               "phone_number": "1234567890",
                                               "role": "supervisor", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

class TestDeleteAccounts(TestCase):

    def setUp(self):
        self.client = Client()

        self.super = MyUser(first_name="supervisor", last_name="super", email="test1@uwm.edu", password="pass1",
                            address="123 straight st", phone_number="1234567890", role="supervisor")
        self.super.save()
        self.instructor = MyUser(first_name="instructor", last_name="super", email="test2@uwm.edu",
                                 password='pass2', address="123 straight st", phone_number="1234567890",
                                 role='instructor')
        self.instructor.save()

        self.ta = MyUser(first_name="ta", last_name="super", email="test3@uwm.edu",
                         password='pass3', address="123 straight st", phone_number="1234567890",
                         role='ta')
        self.ta.save()

    def test_delete_account(self):
        print(self.ta.id)
        response = self.client.post("/", {"uname": "test1@uwm.edu", "psw": "pass1"}, follow=True)

        resp = self.client.post("/contacts/", {"Contact_to_remove": '3', "delContactButt": ''}, follow=True)
        self.assertEqual("Contact was successfully deleted.", resp.context["message"])

    def test_cannot_delete_own_account(self):
        print(self.ta.id)
        response = self.client.post("/", {"uname": "test1@uwm.edu", "psw": "pass1"}, follow=True)

        resp = self.client.post("/contacts/", {"Contact_to_remove": '1', "delContactButt": ''}, follow=True)
        self.assertEqual("Cannot delete the account that is logged into this session.", resp.context["message"])

class TestEditAccounts(TestCase):

    def setUp(self):
        self.client = Client()
        self.super = MyUser(first_name="supervisor", last_name="super", email="test1@uwm.edu", password="pass1",
                            address="123 straight st", phone_number="1234567890", role="supervisor")
        self.super.save()
        self.instructor = MyUser(first_name="instructor", last_name="super", email="test2@uwm.edu",
                                 password='pass2', address="123 straight st", phone_number="1234567890",
                                 role='instructor')
        self.instructor.save()

        self.ta = MyUser(first_name="ta", last_name="super", email="test3@uwm.edu",
                         password='pass3', address="123 straight st", phone_number="1234567890",
                         role='ta')
        self.ta.save()

    def test_edit_account_first_name(self):
        print(self.ta.id)
        resp = self.client.post("/contacts/", {"first_name": "ta2", "last_name": "super", "email": "test3@uwm.edu",
                                           "password": "pass3", "address": "123 straight st",
                                           "phone_number": "1234567890",
                                           "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

    def test_edit_account_last_name(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super2", "email": "test3@uwm.edu",
                                           "password": "pass3", "address": "123 straight st",
                                           "phone_number": "1234567890",
                                           "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

    def test_edit_account_valid_email(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super", "email": "test32@uwm.edu",
                                               "password": "pass3", "address": "123 straight st",
                                               "phone_number": "1234567890",
                                               "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

    def test_edit_account_invalid_email(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super", "email": "test3uwm.edu",
                                               "password": "pass3", "address": "123 straight st",
                                               "phone_number": "1234567890",
                                               "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Email format must contain '@' symbol.", resp.context["message"])

    def test_edit_account_password(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super", "email": "test3@uwm.edu",
                                               "password": "pass4", "address": "123 straight st",
                                               "phone_number": "1234567890",
                                               "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

    def test_edit_address(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super", "email": "test3@uwm.edu",
                                               "password": "pass3", "address": "1234 straight st",
                                               "phone_number": "1234567890",
                                               "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

    def test_edit_phone_number(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super", "email": "test3@uwm.edu",
                                               "password": "pass3", "address": "123 straight st",
                                               "phone_number": "1234567899",
                                               "role": "ta", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

    def test_edit_role(self):
        resp = self.client.post("/contacts/", {"first_name": "ta", "last_name": "super", "email": "test3@uwm.edu",
                                               "password": "pass3", "address": "123 straight st",
                                               "phone_number": "1234567890",
                                               "role": "supervisor", "user": '3', "edit_butt": ''}, follow=True)
        self.assertEqual("Account edited successfully", resp.context["message"])

class TestDeleteAccounts(TestCase):

    def setUp(self):
        self.client = Client()

        self.super = MyUser(first_name="supervisor", last_name="super", email="test1@uwm.edu", password="pass1",
                            address="123 straight st", phone_number="1234567890", role="supervisor")
        self.super.save()
        self.instructor = MyUser(first_name="instructor", last_name="super", email="test2@uwm.edu",
                                 password='pass2', address="123 straight st", phone_number="1234567890",
                                 role='instructor')
        self.instructor.save()

        self.ta = MyUser(first_name="ta", last_name="super", email="test3@uwm.edu",
                         password='pass3', address="123 straight st", phone_number="1234567890",
                         role='ta')
        self.ta.save()

    def test_delete_account(self):
        print(self.ta.id)
        response = self.client.post("/", {"uname": "test1@uwm.edu", "psw": "pass1"}, follow=True)

        resp = self.client.post("/contacts/", {"Contact_to_remove": '3', "delContactButt": ''}, follow=True)
        self.assertEqual("Contact was successfully deleted.", resp.context["message"])

    def test_cannot_delete_own_account(self):
        print(self.ta.id)
        response = self.client.post("/", {"uname": "test1@uwm.edu", "psw": "pass1"}, follow=True)

        resp = self.client.post("/contacts/", {"Contact_to_remove": '1', "delContactButt": ''}, follow=True)
        self.assertEqual("Cannot delete the account that is logged into this session.", resp.context["message"])
