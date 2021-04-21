from django.shortcuts import render
from django.views import View
from .models import User
# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        noSuchUser = False
        badPassword = False
        try:
            m = User.objects.get(email=request.POST['uname'])
            badPassword = (m.password != request.POST['psw'])
        except:
            noSuchUser = True
        if noSuchUser:
            return render(request, "login.html", {"message": "The username that you used does not exist. Please retry."})
        elif badPassword:
            return render(request, "login.html", {"message": "The password that you entered is not correct.  Please retry."})
        else:
            request.session["name"] = m.email
            return redirect("/course/")

