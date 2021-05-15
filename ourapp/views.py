
from django.shortcuts import render, redirect, get_object_or_404


from django.views import View
from .models import MyUser, MyCourse, MySection
from django.http import HttpResponse

from ourapp.helper_methods import login, get_user, create_course, create_section, validate_session, ValidTeacherForSection, ValidateDeleteAccount

from ourapp.helper_methods import CreateAccountsFunction


# Create your views here.


class CreateAccounts(View):

    def get(self, request):
        ValidSession = validate_session(request)
        if not ValidSession:
            return redirect("/")

        request.session['submitted'] = False
        accounts = MyUser.objects.all()

        return render(request, "account.html", {"accounts": accounts})

    def post(self, request):

        if request.method == 'POST' and 'create_butt' in request.POST:
            accounts = MyUser.objects.all()
            user = request.POST['user']
            user = MyUser(user)
            email = request.POST['email']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            phone_number = request.POST['phone_number']
            role = request.POST['role']

            user.email = email
            user.password = password
            user.first_name = first_name
            user.last_name = last_name
            user.address = address
            user.phone_number = phone_number
            user.role = role

            user.save()
            return render(request, "account.html", {"accounts": accounts})

class Course(View):
    def get(self, request):

        ValidSession = validate_session(request)
        if not ValidSession:
            return redirect("/")

        courses = MyCourse.objects.all()
        sections = MySection.objects.all()
        request.session['submitted'] = False
        accounts = MyUser.objects.filter(role__in=['instructor', 'ta'])
        return render(request, "course.html", {"courses": courses, "accounts": accounts, "sections": sections})

    def post(self, request):
        accounts = MyUser.objects.filter(role__in=['instructor', 'ta'])
        courses = MyCourse.objects.all()
        sections = MySection.objects.all()
        request.session['submitted'] = True
        if request.method == 'POST' and 'course_button' in request.POST:
            number = request.POST['number']
            courses = list(MyCourse.objects.all())
            message = create_course(request.POST['name'], number)
            if type(message) is MyCourse:  # There was good input
                courses.append(message)
                request.session['error'] = False
                return render(request, "course.html", {"courses": courses, "message": "Course successfully added",
                                                       "accounts": accounts, "sections": sections})
            else:
                request.session['error'] = True
                return render(request, "course.html", {"courses": courses, "message": message,
                                                       "accounts": accounts, "sections": sections})

        if request.method == 'POST' and 'section_button' in request.POST:
            message = create_section(request.POST['course_selection'], request.POST['section_number'])
            if type(message) is MySection:  # There was good input
                # sections.append(message)
                request.session['error'] = False
                return render(request, "course.html", {"courses": courses, "message": "Section successfully added",
                                                       "accounts": accounts, "sections": sections})
            else:
                request.session['error'] = True
                return render(request, "course.html", {"courses": courses, "message": message, "accounts": accounts,
                                                    "sections": sections})

        if request.method == 'POST' and 'ass_butt' in request.POST:
            courses = MyCourse.objects.all()
            accounts = MyUser.objects.filter(role__in=['instructor', 'ta'])
            sections = MySection.objects.all()
            course_selection = request.POST['course_selection']
            course_selection = MyCourse(course_selection)
            person_selection = request.POST['person_selection']
            person_selection = MyUser(person_selection)

            course_selection.people.add(person_selection)
            accounts = MyUser.objects.filter(role__in=['instructor', 'ta'])
            return render(request, "course.html",
                          {"message": "Course assignments updated", "courses": courses, "accounts": accounts, "sections": sections})

        if request.method == 'POST' and 'ass_section_butt' in request.POST:
            accounts = MyUser.objects.filter(role__in=['instructor', 'ta'])
            courses = MyCourse.objects.all()
            sections = MySection.objects.all()
            person_selection = request.POST['person_selection']
            person_selection = MyUser.objects.get(id=person_selection)
            #person_selection = MyUser(person_selection)
            section_selection = request.POST['section_selection']
            section_selection = MySection.objects.get(id=section_selection)
            #section_selection = MySection(section_selection)

            message = ValidTeacherForSection(person_selection, section_selection)
            request.session['error'] = message[0]
            return render(request, "course.html", {"message": message[1], "courses": courses, "accounts": accounts, "sections": sections})

        if request.method == 'POST' and 'delSButt' in request.POST:
            accounts = MyUser.objects.all()
            courses = MyCourse.objects.all()
            sections = MySection.objects.all()
            section_to_remove = request.POST['section_to_remove']
            section_to_remove = MySection(section_to_remove)
            section_to_remove.delete()

            return render(request, "course.html", {"message": "section successfully deleted", "courses": courses, "accounts": accounts,
                                                   "sections": sections})

        if request.method == 'POST' and 'delCButt' in request.POST:
            accounts = MyUser.objects.filter(role__in=['instructor', 'ta'])
            sections = MySection.objects.all()
            course_to_remove = request.POST['course_to_remove']
            course_to_remove = MyCourse(course_to_remove)
            for i in sections:
                if i.course == course_to_remove:
                    i.delete()
            sections = MySection.objects.all()
            course_to_remove.delete()
            courses = MyCourse.objects.all()

            return render(request, "course.html", {"message": "Course successfully deleted", "courses": courses, "accounts": accounts,
                                                   "sections": sections})



class Login(View):
    def get(self, request):
        request.session.flush()
        return render(request, "login.html", {})

    def post(self, request):
        x = request.POST['uname']
        message = login(x, request.POST['psw'])
        if message == "Valid":
            u = get_user(x)
            request.session['name'] = u.email
            request.session.set_expiry(0)
            if u.is_supervisor():
                request.session['supervisor'] = True
            else:
                request.session['supervisor'] = False
            return redirect("/course/", request)
        else:
            return render(request, "login.html", {"message": message})


class SectionCreation(View):

    def get(self, request):
        ValidSession = validate_session(request)
        if not ValidSession:
            return redirect("/")
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

class Contacts(View):

    def get(self, request):
        request.session['submitted'] = False
        accounts = MyUser.objects.all()
        return render(request, "contacts.html", {"accounts": accounts})

    def post(self, request):
        request.session['submitted'] = True
        if request.method == 'POST' and 'edit_butt' in request.POST:

            accounts = MyUser.objects.all()

            user = request.POST['user']
            user = MyUser(user)
            email = request.POST['email']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            phone_number = request.POST['phone_number']
            role = request.POST['role']

            user.email = email
            user.password = password
            user.first_name = first_name
            user.last_name = last_name
            user.address = address
            user.phone_number = phone_number
            user.role = role

            valid = CreateAccountsFunction(email, phone_number)
            if valid != "Valid":
                request.session['error'] = True
                return render(request, "contacts.html", {"accounts": accounts, "message": valid})

            user.save()

            return render(request,  "contacts.html", {"accounts": accounts, "message": "Account edited successfully"})

        if request.method == 'POST' and 'create_butt' in request.POST:

            email = request.POST['email']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            address = request.POST['address']
            phone_number = request.POST['phone_number']
            role = request.POST['role']

            accounts = MyUser.objects.filter(role__in=['instructor', 'ta'])
            accounts = list(accounts)
            valid = CreateAccountsFunction(email, phone_number)
            if valid != "Valid":
                request.session['error'] = True
                return render(request, "contacts.html", {"accounts": accounts, "message": valid})
            user_exists = True
            try:
                MyUser.objects.get(email=email)

            except:
                user_exists = False

            if user_exists:
                request.session['error'] = True
                return render(request, "contacts.html", {"accounts": accounts, "message": "A user with this email has "
                                                                                         "already been created.  Try again."})

            else:
                a = MyUser.objects.create(email=email, password=password, first_name=first_name, last_name=last_name,
                                          address=address, phone_number=phone_number, role=role)

                a.save()
                accounts.append(a)
                request.session['error'] = False
                return render(request, "contacts.html",
                              {"accounts": accounts, "message": "Account created successfully"})

        if request.method == 'POST' and 'delContactButt' in request.POST:
            user = request.POST['Contact_to_remove']
            user = MyUser.objects.get(id= user)
            valid = ValidateDeleteAccount(request.session['name'], user.email)
            if valid == "Valid":
                user.delete()
                valid = "Contact was successfully deleted."
            else:
                request.session['error'] = True
            accounts = MyUser.objects.all()
            return render(request, "contacts.html", {"accounts": accounts, "message": valid})

