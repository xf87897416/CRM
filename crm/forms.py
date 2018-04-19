#_*_ coding:utf-8 _*_
#_author: "Administrator"
#date: 2018/2/11


from django.forms import ModelForm
from crm import models

class EnrollmentForm(ModelForm):

    def __new__(cls, *args, **kwargs):
        # super(CustomerForm, self).__new__(*args, **kwargs)
        #print("base fields",cls.base_fields)
        for field_name,field_obj in cls.base_fields.items():
            #print(field_name,dir(field_obj))
            field_obj.widget.attrs['class'] = 'form-control'

        return ModelForm.__new__(cls)
    class Meta:
        model =  models.Enrollment
        fields = ["enrolled_class","consultant"]


class CustomerForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class': 'form-control'})
            if field_name in CustomerForm.Meta.readonly_fields:
                field.widget.attrs.update({'disabled': 'disabled'})

                #print("required:",field.required)


    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'

            if field_name in cls.Meta.readonly_fields:
                field_obj.widget.attrs['disabled'] = 'disabled'
        return ModelForm.__new__(cls)

    def clean_qq(self):
        if self.instance.qq != self.cleaned_data['qq']:
            self.add_error("qq","傻逼你还尝试黑我")
        return self.cleaned_data['qq']

    class Meta:
        model = models.Customer
        exclude = ()
        readonly_fields = [ 'qq','consultant']
        # readonly_fields = [ ]















