#_*_ coding:utf-8 _*_
#_author: "Administrator"
#date: 2018/2/16

from django import template
from django.core.exceptions import FieldDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
from django.db.models import Sum
from crm import models

register = template.Library()


@register.simple_tag()
def get_score(enroll_obj,customer_obj):
    study_records = enroll_obj.studyrecord_set.\
        filter(course_record__from_class_id = enroll_obj.enrolled_class.id)
    return study_records.aggregate(Sum("score"))



@register.simple_tag
def get_study_record_count(enroll_obj):
    study_records = []
    course_records = enroll_obj.enrolled_class.courserecord_set.select_related()
    for obj in course_records: #BJ linux 6 1
        # print("obj",obj.studyrecord_set.select_related())
        study_records.extend(obj.studyrecord_set.select_related().filter(student=enroll_obj))
    print('运行',study_records,'---')
    return study_records


@register.simple_tag
def get_study_record(course_record,enroll_obj):
    study_record_obj = course_record.studyrecord_set.select_related().filter(student=enroll_obj.customer)
    if study_record_obj:
        return study_record_obj[0]


@register.simple_tag
def get_course_grades(class_obj):
    '''返回整个班级的成绩'''
    # print("运行到这里")

    return dict(models.StudyRecord.objects.filter(course_record__from_class=class_obj).\
                values_list('student').annotate(Sum('score')) )


@register.simple_tag
def get_course_ranking(class_grade_dic):
    '''返回整个班级的排名数据'''
    ranking_dic = {}
    ranking_list = sorted(class_grade_dic.items(),key=lambda x:x[1])
    for item in ranking_list:
        ranking_dic[item[0]] = [item[1], ranking_list.index(item)+1]
    return ranking_dic


@register.simple_tag
def get_stu_grade_ranking(course_ranking_dic,enroll_obj):
    '''返回这个学员在本班的成绩排名'''

    score = course_ranking_dic.get(enroll_obj.customer.id)
    if score:
        return score[1]


@register.simple_tag
def fetch_stu_course_score(class_grade_dic, enroll_obj ):
    print(class_grade_dic,enroll_obj.customer.id,"class_grade_dic")
    return class_grade_dic.get(enroll_obj.customer.id)

@register.simple_tag
def get_greade(enroll_obj,class_ojb):
    study=models.StudyRecord.objects.get(student_id=enroll_obj.id).score

    # print(study)

    return study