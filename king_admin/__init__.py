# from django.db.models.signals import pre_save, post_save
#
#
# def callback(sender, **kwargs):
#     print("测试信号")
#     print(sender, kwargs)
#
#
# post_save.connect(callback)
# # xxoo指上述导入的内容


import django.dispatch
pizza_done = django.dispatch.Signal(providing_args=["toppings", "size"])


def callback(sender, **kwargs):
    print("数据修改了")
    print(sender, kwargs)


pizza_done.connect(callback)

