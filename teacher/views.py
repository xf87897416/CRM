from django.shortcuts import render

# Create your views here.


from django.shortcuts import render,HttpResponse,redirect
from crm import models
# Create your views here.
from MyperfectCRM import settings
import os,time,json
from crm.permissions import permission


def teacher_manger(request):
    # return redirect("/king_admin/crm/courserecord/")

    return render(request,'teacher/my_students.html')


def class_stu(request,enroll_obj_id):
    enroll_obj = models.Enrollment.objects.get(id=enroll_obj_id)
    return render(request, 'teacher/class_stu.html',{'enroll_obj':enroll_obj})


def view_class_stu_list(request,class_id):

    class_obj = models.ClassList.objects.get(id=class_id)
    return render(request,'teacher/class_stu_list.html',{'class_ojb':class_obj})









