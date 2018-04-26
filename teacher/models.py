from django.db import models

# Create your models here.
from crm.models import UserProfile,Customer

class teacherinfo(models.Model):
    name = models.CharField(max_length=32)
    age = models.SmallIntegerField()
    def __str__(self):
        return  "<%s %s>"%(self.name,self.age)

    class Meta:
        verbose_name_plural = '老师信息'
        verbose_name='老师信息'











