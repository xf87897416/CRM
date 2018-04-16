#_*_ coding:utf-8 _*_
#_author: "Administrator"
#date: 2018/2/7
import time
'''
三大难点，
1，动态创建model  使用type类动态生成  
_model_from_class = type("DynamicModelForm",(ModelForm,),attrs)


2，关联数据显示出来
每一个对象models.Customer.objects.get(id =1)
c._meta.local_many_to_many




3，actions来了
action_func(admin_class,request,selected_objs)
执行函数
注意执行顺序
$(form_ele).append(selected_ids_ele);！！



4 自定制验证规则










'''

print("ok")






