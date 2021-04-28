from .models import MyUser, MyCourse, MySection
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from django.http import request


def get_user(email):
    pass

def is_ta(request):
    pass

def is_instructor(request):
    pass

def is_supervisor(request):
    pass

def get_password(request):
    pass

def get_email():
    pass

def login(email, password):
    pass

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
