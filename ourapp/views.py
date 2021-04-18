from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, request, HttpResponse
from django.views import generic
from .models import Account, Course


# NOTE: arguments for views may change
# still need to work on this view - Sabrina
def HomeView():
    return HttpResponse("This is the home view")


def LoginView():
    return HttpResponse("This is the login view")


def CourseView():
    return HttpResponse("This is the course view")


def AccountView():
    return HttpResponse("This is the account view")
