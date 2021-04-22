from django.shortcuts import render, redirect
from django.views import View
from .models import User, Instructor, Supervisor, Ta, Course, Section
# Create your views here.


class Accounts(View):
    def get(self, request):
        accounts = User.objects.all()
        return render(request, "account.html", {"accounts": accounts})

    def create_account(self, request):
        # if create account button is clicked, we want to change pages to account creation page
        return redirect("/create/")


class CreateAccounts(View):
    def creation(self, request):
        # We will have to change this because we cannot instantiate User objects (User is abstract)
        email=request.POST['email']
        password=request.POST['password']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        address=request.POST['address']
        phone_number=request.POST['phone_number']
        role=request.POST['role']

        user_exists = False

        accounts = User.objects.all()

        for i in accounts:
            if i.email == email:
                return render(request, "account.html", {"accounts": accounts, "message": "email already exists"})

        if role == 'Instructor':
            a = Instructor.objects.create(email=email, password=password, first_name=first_name, last_name=last_name,
                                          address=address, phone_number=phone_number)

        elif role == 'Supervisor':
            a = Supervisor.objects.create(email=email, password=password, first_name=first_name, last_name=last_name,
                                          address=address, phone_number=phone_number)

        else: #Ta
            a = Ta.objects.create(email=email, password=password, first_name=first_name, last_name=last_name,
                                          address=address, phone_number=phone_number)

        a.save()

        accounts.append(a)

        return render(request, "account.html", {"accounts": accounts})