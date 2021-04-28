
from django.shortcuts import render, redirect, get_object_or_404


from django.views import View
from .models import MyUser, MyCourse, MySection
from django.http import HttpResponse

from ourapp.helper_methods import login, get_user, create_course, create_section

from ourapp.helper_methods import CreateAccountsFunction


# Create your views here.


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

        valid = CreateAccountsFunction(email, phone_number)
        if valid != "Valid":
            return render(request, "account.html", {"accounts": accounts, "message": "A user with this email has "
                                                                                     "already been created.  Try again."})
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
        name = request.POST['name']
        number = request.POST['number']
        courses = list(MyCourse.objects.all())
        message = create_course(request.POST['name'], number)
        if type(message) is MyCourse:  # There was good input
            courses.append(message)
            return render(request, "course.html", {"courses": courses, "message": "Course successfully added"})
        else:
            return render(request, "course.html", {"courses": courses, "message": message})


class Login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        x = request.POST['uname']
        message = login(x, request.POST['psw'])
        if message == "Valid":
            u = get_user(x)
            request.session['name'] = u.email
            return redirect("/course/", request)
        else:
            return render(request, "login.html", {"message": message})


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
