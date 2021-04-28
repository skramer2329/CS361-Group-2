from .models import MyUser, MyCourse, MySection
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.http import request


def get_user(email):
    try:
        u = MyUser.objects.get(email=email)
        return u
    except:
        return None


def login(email, password):
    noSuchUser = False
    badPassword = False
    try:
        m = MyUser.objects.get(email__iexact=email)
        badPassword = (m.password != password)
    except:
        noSuchUser = True

    if noSuchUser:
        return "The username that you used does not exist. Please retry."
    elif badPassword:
        return "The password that you entered is not correct.  Please retry."
    else:
        return "Valid"


def validate_course_number(number):
    return len(str(number)) == 3


def create_course(name, number):
    valid = validate_course_number(number)

    if not valid:
        return "The course number is not 3 digits long.  Try again."

    course_exists = True
    try:
        MyCourse.objects.get(number=number)

    except:
        course_exists = False

    if course_exists:
        return "A course with this number has already been created.  Try again."

    else:
        a = MyCourse.objects.create(name=name, number=number)
        a.save()
        return a


def validate_section_number(number):
    pass


def create_section(course, number):
    valid = validate_course_number(number)
    if not valid:
        return "The section number is not 3 digits long.  Try again."
    section_exists = True

    try:
        MySection.objects.get(number=number)
    except:
        section_exists = False

    if section_exists:
        return "A section with this number within this course has already been created.  Try again."

    else:
        a = MySection.objects.create(number=number, course=course)

        a.save()

        return a


def CreateAccountsFunction(email, phone_number):
    message = "Valid"
    if valid_email_format(email) == "Email does not contain @.":
        message = "Email format must contain '@' symbol."

    elif valid_email_format(email) == "Email should not contain a space.":
        message = "Email should not contain a space."

    elif valid_phone_number(phone_number) == False:
        message = "Phone number must be all digits.  Do not type hyphens."

    return message


def valid_email_format(email):
    if "@" not in email:
        return "Email does not contain @."
    elif ' ' in email:
        return "Email should not contain a space."
    else:
        return "Valid"


def valid_phone_number(phone_number):
    return phone_number.isdigit()
