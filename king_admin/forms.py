#_*_ coding:utf-8 _*_
#_author: "Administrator"
#date: 2018/2/7

from django.forms import forms,ModelForm
from crm import models
from django.forms import ValidationError
from django.utils.translation import ugettext as _

class CustomerModelForm(ModelForm):
    class Meta:
        models = models.Customer
        fields = '__all__'

def create_model_form(request,admin_class,fields='__all__',form_create=False,**kwargs):
    '''动态生成MODEL FORM'''
    def __new__(cls,*args,**kwargs):
        # print('base fields',cls.base_fields)
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'

            if not hasattr(admin_class,'is_add_form'): #代表这是添加form,不需要disabled
                if field_name in admin_class.readonly_fields:
                    field_obj.widget.attrs['disabled']='disabled'

            if hasattr(admin_class,"clean_%s" % field_name):
                field_clean_func = getattr(admin_class,"clean_%s" %field_name)
                setattr(cls,"clean_%s"%field_name, field_clean_func)

            if cls.Meta.form_create is False:
                if field_name in admin_class.readonly_fields:
                    field_obj.widget.attrs['disabled'] = 'disabled'


        return ModelForm.__new__(cls)

    def default_clean(self):
        print("cleaned_data:", self.cleaned_data)
        error_list=[]
        if self.instance.id:# 这是个修改的表单
            for field in admin_class.readonly_fields: # ["qq", "consultant", "tags"]

                field_val = getattr(self.instance,field)  #val in db

                # if hasattr(field_val,"select_related"): #m2m
                #     m2m_objs = getattr(field_val,"select_related")().select_related()
                #     m2m_vals = [i[0] for i in m2m_objs.values_list('id')]
                #     set_m2m_vals = set(m2m_vals)
                #     set_m2m_vals_from_frontend = set([i.id for i in self.cleaned_data.get(field)])
                #     if set_m2m_vals != set_m2m_vals_from_frontend:
                #         # error_list.append(ValidationError(
                #         #     _('Field %(field)s is readonly'),
                #         #     code='invalid',
                #         #     params={'field': field},
                #         # ))
                #         self.add_error(field,"readonly field")
                #     continue
                field_val_from_frontend = self.cleaned_data.get(field)
                # print("filed differ compare:", field_val_from_frontend, field_val)
                if field_val != field_val_from_frontend:
                    if self.Meta.partial_update:
                        if field not in self.cleaned_data:
                            print("过滤其他字段")
                            continue  #

                    error_list.append(ValidationError(
                                _('Field %(field)s is readonly,data should be %(val)s'),
                                code='invalid',
                                params={'field': field,'val':field_val},
                                   ))
        if admin_class.readonly_table:
            raise ValidationError(
                _('Table is  readonly,cannot be modified or added'),
                code='invalid'
            )
        self.ValidationError = ValidationError
        response = admin_class.default_form_validation(self)
        if response:
            error_list.append(response)
        if error_list:
            raise  ValidationError(error_list)

    class Meta:
        model = admin_class.model
        exclude = admin_class.modelform_exclude_fields
    attrs = {'Meta':Meta}
    _model_from_class = type("DynamicModelForm",(ModelForm,),attrs)
    setattr(_model_from_class,'__new__',__new__)
    setattr(_model_from_class,'clean',default_clean)
    setattr(Meta, 'form_create', form_create)
    setattr(Meta, 'fields', fields)
    setattr(Meta, 'partial_update', kwargs.get("partial_update"))
    if request: #for form validator
        setattr(_model_from_class,'_request',request)
        print("不知道这句话有什么用")
    return _model_from_class









