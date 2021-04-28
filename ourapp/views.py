
from django.shortcuts import render, redirect, get_object_or_404


from django.views import View
from .models import MyUser, MyCourse, MySection
from django.http import HttpResponse
from ourapp.helper_methods import login, get_user, create_course, create_section

# Create your views here.


class Accounts(View):
    def get(self, request):
        accounts = MyUser.objects.all()
        return render(request, "account.html", {"accounts": accounts})

    def create_account(self, request):
        # if create account button is clicked, we want to change pages to account creation page
        return redirect("/create/")


class CreateAccounts(View):
    def get(self, request):
        accounts = MyUser.objects.all()
        return render(request, "account.html", {"accounts": accounts})

    def post(self, request):
        email=request.POST['email']
        password=request.POST['password']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        address=request.POST['address']
        phone_number=request.POST['phone_number']
        role=request.POST['role']

        accounts = list(MyUser.objects.all())
        user_exists = True
        try:
            MyUser.objects.get(email=email)

        except:
            user_exists = False

        if user_exists:
            return render(request, "account.html", {"accounts": accounts, "message": "A user with this email has "
                                                                                "already been created.  Try again."})

        else:
            a = MyUser.objects.create(email=email, password=password, first_name=first_name, last_name=last_name,
            address=address, phone_number=phone_number, role=role)

            a.save()
            accounts.append(a)

            return render(request, "account.html", {"accounts": accounts, "message": "Account created successfully"})

class Course(View):
    def get(self, request):
        courses = MyCourse.objects.all()
        return render(request, "course.html", {"courses": courses})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        role = request.POST['role']

        accounts = list(MyUser.objects.all())
        user_exists = True
        try:
            MyUser.objects.get(email=email)

        except:
            user_exists = False

        if user_exists:
            return render(request, "account.html", {"accounts": accounts, "message": "A user with this email has "
                                                                                     "already been created.  Try again."})

        else:
            a = MyUser.objects.create(email=email, password=password, first_name=first_name, last_name=last_name,
                                      address=address, phone_number=phone_number, role=role)

            a.save()
            accounts.append(a)

            return render(request, "account.html", {"accounts": accounts, "message": "Account created successfully"})


class Login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            m = MyUser.objects.get(email__iexact=request.POST['uname'])
            badPassword = (m.password != request.POST['psw'])
        except:
            noSuchUser = True
        if noSuchUser:
            return render(request, "login.html",
                          {"message": "The username that you used does not exist. Please retry."})
        elif badPassword:
            return render(request, "login.html",
                          {"message": "The password that you entered is not correct.  Please retry."})
        else:
            request.session["name"] = m.email
            return redirect("/course/", request)


class SectionCreation(View):

    def get(self, request):
        sections = MySection.objects.all()
        courses = MyCourse.objects.all()
        return render(request, "section.html", {"courses":courses, "sections": sections})

    def post(self, request):

        # sections = MySection.objects.all()
        courses = MyCourse.objects.all()
        message = create_section(request.POST['course_selection'], request.POST['section_number'])
        if type(message) is MySection:  # There was good input
            # sections.append(message)
            return render(request, "course.html", {"courses": courses, "message": "Course successfully added"})
        else:
            return render(request, "course.html", {"courses": courses, "message": message})



    """
        accounts.append(a)

        return render(request, "account.html", {"accounts": accounts})
    """