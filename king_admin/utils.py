#_*_ coding:utf-8 _*_
#_author: "Administrator"
#date: 2018/2/6

from django.db.models import Q

def table_filter(request,admin_class):
    '''进行条件过滤并返回过滤后的数据'''
    filter_conditions={}
    keywords=['page','o','_q']
    for k,v in request.GET.items():
        print('k,v',k,v)
        if k in keywords:#保留的分页关键字 and 排序关键字
            continue
        if v:
            filter_conditions[k]=v
    print("filter coditions", filter_conditions)
    return admin_class.model.objects.filter(**filter_conditions).\
        order_by("-%s"%admin_class.ordering if admin_class.ordering else "-id"),filter_conditions


def table_search(request,admin_class,object_list):
    search_key = request.GET.get('_q',"")
    q_obj =Q()
    q_obj.connector ="OR"
    for column in admin_class.search_fields:
        q_obj.children.append(("%s__contains"%column,search_key))
    # print(q_obj)
    #(OR: ('qq__contains', '222'), ('name__contains', '222'), ('consultant__name__contains', '222'))
    res = object_list.filter(q_obj)
    return res



def table_sort(request,admin_class,objs):
    orderby_key = request.GET.get("o")

    if orderby_key:
        res = objs.order_by(orderby_key)
        if orderby_key.startswith("-"):
            orderby_key=orderby_key.strip("-")
        else:
            orderby_key = "-%s"%orderby_key
    else:
        res=objs
    return res,orderby_key























