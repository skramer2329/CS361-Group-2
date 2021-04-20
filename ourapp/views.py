
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import User, Instructor
from django.http import HttpResponseRedirect, request, HttpResponse
from django.views import generic
from .models import Account, Course

# Create your views here.


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

  
  
class Accounts(View):
    def get(self, request):
        accounts = list(User.objects)
        return render(request, "account.html", {"accounts": accounts})

    def create_account(self, request):
        # if create account button is clicked, we want to change pages to account creation page
        return redirect("/create/")


class CreateAccounts(View):
    def creation(self, request):
        # We will have to change this because we cannot instantiate User objects (User is abstract) - Bennett
        a = User(email=request.POST['email'], password=request.POST['password'], first_name=request.POST['first_name'],
                 last_name=request.POST['last_name'], address=request.POST['address'],
                 phone_number=request.POST['phone_number'])
        a.save()
        accounts = list(User.objects)
        return render(request, "account.html", {"accounts": accounts})

