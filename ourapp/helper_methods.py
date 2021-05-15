from .models import MyUser, MyCourse, MySection
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.http import request

# TODO write tests
def validate_session(request):
    try:
        key = request.session['name']
    except:
        return False

    return True
# has tests already
def get_user(email):
    try:
        u = MyUser.objects.get(email__iexact=email)
        return u
    except:
        return None

# has tests already
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

# has tests already
def validate_course_number(number):
    x = str(number)
    if len(str(number)) == 3 and str(number).isdigit():
        return True
    else:
        return False

# has tests already
def create_course(name, number):
    valid = validate_course_number(number)

    if not valid:
        return "The course number is not 3 digits long.  Try again."

    course_exists = True
    try:
        MyCourse.objects.get(number=number, name=name)

    except:
        course_exists = False

    if course_exists:
        return "A course with this name and number has already been created.  Try again."

    else:
        a = MyCourse.objects.create(name=name, number=number)
        a.save()
        return a

# has tests already
def validate_section_number(number):
    x = str(number)
    if len(str(number)) == 3 and str(number).isdigit():
        return True
    else:
        return False

# has tests already
def create_section(course, number):
    course = MyCourse(course)
    valid = validate_course_number(number)
    if not valid:
        return "The section number is not 3 digits long.  Try again."
    section_exists = True

    try:
        MySection.objects.get(course=course, number=number)
    except:
        section_exists = False

    if section_exists:
        return "A section with this number within this course has already been created.  Try again."

    else:
        a = MySection.objects.create(number=number, course=course)

        a.save()

        return a

# has tests
def CreateAccountsFunction(email, phone_number):
    message = "Valid"
    if valid_email_format(email) == "Email does not contain @.":
        message = "Email format must contain '@' symbol."

    elif valid_email_format(email) == "Email should not contain a space.":
        message = "Email should not contain a space."

    elif valid_phone_number(phone_number) == False:
        message = "Phone number must be all digits.  Do not type hyphens."

    return message

# has tests
def valid_email_format(email):
    if "@" not in email:
        return "Email does not contain @."
    elif ' ' in email:
        return "Email should not contain a space."
    else:
        return "Valid"

# has tests
def valid_phone_number(phone_number):
    return phone_number.isdigit()

# has tests
def ValidTeacherForSection(person_selection, section_selection):
    if type(person_selection) is not MyUser:
        raise TypeError
    elif type(section_selection) is not MySection:
        raise TypeError
    person = person_selection.role
    sectionnumber = str(section_selection.number)
    message = ""
    if (sectionnumber.startswith('8') or sectionnumber.startswith('9')) and not person == "ta":
        message = "Only TAs can be assigned to lab sections."
        return [True, message]
    elif (not (sectionnumber.startswith('8') or sectionnumber.startswith('9'))) and not person == "instructor":
        message = "Only Instructors can be assigned to lecture sections."
        return [True, message]
    else:
        if(section_selection.teacher == None):
            message = "Added Teacher to section."
        else:
            CurrentInstructor = section_selection.teacher.__str__()
            message = "Teacher: " + CurrentInstructor + " was removed.\nTeacher: " + person_selection.__str__() + " was added."
        section_selection.teacher = person_selection
        section_selection.save()
        return [False, message]

def ValidateDeleteAccount(sessionemail, useremail):
    if(sessionemail != useremail):
        return "Valid"
    else:
        return "Cannot delete the account that is logged into this session."