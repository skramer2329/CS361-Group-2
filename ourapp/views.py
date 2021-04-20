from django.shortcuts import render, redirect
from django.views import View
from .models import User, Instructor
# Create your views here.


class Accounts(View):
    def get(self, request):
        accounts = list(User.objects)
        return render(request, "account.html", {"accounts": accounts})

    def create_account(self, request):
        # if create account button is clicked, we want to change pages to account creation page
        return redirect("/create/")


class CreateAccounts(View):
    def creation(self, request):
        # We will have to change this because we cannot instantiate User objects (User is abstract)
        a = User(email=request.POST['email'], password=request.POST['password'], first_name=request.POST['first_name'],
                 last_name=request.POST['last_name'], address=request.POST['address'],
                 phone_number=request.POST['phone_number'])
        a.save()
        accounts = list(User.objects)
        return render(request, "account.html", {"accounts": accounts})