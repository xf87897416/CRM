from django.shortcuts import render,redirect,HttpResponse

from django.contrib.auth import login,authenticate,logout
from crm import models
# Create your views here.


def acc_login(request):

    errors = {}
    # if request.is_ajax():
    #     print("this is GET")
    #     # _email1 = request.COOKIES.get("name")
    #     # _password1= request.COOKIES.get("password")
    #     _email1=request.GET.get("email1")
    #     _password1=request.GET.get("password1")
    #     obj=models.UserProfile.objects.filter(email=_email1)
    #     # print(_email1,'email')
    #     # print(_password1,'_password1')
    #     # print(obj.count(),'obj.count()')
    #     # print(obj[0].auto_login,"obj0")
    #     if obj.count() and obj[0].auto_login == True:
    #         user = authenticate(username=_email1, password=_password1)
    #         if user:
    #             print(user,'user')
    #             login(request, user)
    #             next_url = request.GET.get("next", "/king_admin")
    #             print("zoudaozheyibule ")
    #             return redirect(next_url)



    if request.method == "POST":
        _email = request.POST.get("email")
        _password = request.POST.get("password")
        _check=request.POST.get("remember-me")


        # print(request.POST)
        # print(_email,_password,'email password')
        user = authenticate(username = _email, password = _password)
        if user:
            login(request,user)
            if _check:
                request.session.set_expiry(72000)
            else:
                request.session.set_expiry(3600)
            obj = models.UserProfile.objects.get(email=_email)
            obj.auto_login =True
            obj.save()
            next_url = request.GET.get("next","/")

            return redirect(next_url)
        else:
            errors['error'] = "Wrong username or password!"


    return render(request,"login.html",{"errors":errors})

def acc_logout(request):

    logout(request)

    return redirect("/account/login/")


def begin(request):
    if request.method == "GET":
        return render(request,'begin.html')


def test(request):
    return render(request,'test.html')







