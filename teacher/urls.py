
from django.conf.urls import url
from teacher import views

urlpatterns = [
    url(r'^$', views.teacher_manger,name="teacher_manger"),
    # url(r'^class_stu/(\d+)/$', views.class_stu, name="class_stu"),
    url(r'^my_classes/(\d+)/stu_list/$', views.view_class_stu_list, name="view_class_stu_list"),

]
