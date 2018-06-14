#_*_ coding:utf-8 _*_
#_author: "Administrator"
#date: 2018/2/6
from django import template
from django.core.exceptions import FieldDoesNotExist
from django.core.exceptions import FieldDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta

register = template.Library()

@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def render_filter_ele(filter_filed,admin_class,filter_condtions): #字典包含过滤信息
    select_ele='''<select class="form-control" name='{filter_filed}'><option value=''>-----</option>'''
    field_obj = admin_class.model._meta.get_field(filter_filed)
    if field_obj.choices: #字段是选择
        selected=''
        for choice_item in field_obj.choices: #列表(4, '51CTO')
            if filter_condtions.get(filter_filed) == str(choice_item[0]):
                selected = "selected"
            select_ele +='''<option value='%s' %s>%s</option>'''%(choice_item[0],selected,choice_item[1])
            selected = ''

    if type(field_obj).__name__ =='ForeignKey':
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_condtions.get(filter_filed) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
            selected = ''
    if type(field_obj).__name__  in ['DateTimeField','DateField']:
        date_els=[]
        today_ele = datetime.now().date()
        date_els.append(['今天',datetime.now().date()])
        date_els.append(['昨天',today_ele - timedelta(days=1)])
        date_els.append(["近7天", today_ele - timedelta(days=7)])
        date_els.append(["本月", today_ele.replace(day=1)])
        date_els.append(["近30天", today_ele - timedelta(days=30)])
        date_els.append(["近90天", today_ele - timedelta(days=90)])
        date_els.append(["近180天", today_ele - timedelta(days=180)])
        date_els.append(["本年", today_ele.replace(month=1, day=1)])
        date_els.append(["近一年", today_ele - timedelta(days=365)])

        selected=''
        for item in date_els:
            select_ele +='''<option value='%s' %s>%s</option>'''%(item[1],selected,item[0])

        filter_filed_name = "%s__gte" % filter_filed
    else:
        filter_filed_name=filter_filed

    select_ele += "</select>"
    select_ele = select_ele.format(filter_filed=filter_filed_name)

    return mark_safe(select_ele)

@register.simple_tag
def build_table_header_column(column,orderby_key,filte_condtions,admin_class):#filter coditions {'consult_course': '1', 'status': '0'}
    filters=''
    # print('test-------',column)
    for k,v in filte_condtions.items():
        filters += "&%s=%s"%(k,v)

    ele = '''<th><a href="?{filters}&o={orderby_key}">{column}</a>{sort_icon}</th>'''
    # ele = '''<th><a href="?{filters}&o={orderby_key}">{column}</a>{sort_icon}</th>'''
    if orderby_key:
        if orderby_key.startswith("-"):
            sort_icon ='''<span class="glyphicon glyphicon-chevron-up"></span>'''
        else:
            sort_icon= '''<span class="glyphicon glyphicon-chevron-down"></span>'''

        if orderby_key.strip("-") == column: #
            orderby_key=orderby_key
        else:
            orderby_key=column
            sort_icon=''

    else:#没有排序
        orderby_key=column
        sort_icon=''
    try:
        column_verbose_name = admin_class.model._meta.get_field(column).verbose_name.upper()
    except FieldDoesNotExist as e:
        column_verbose_name = getattr(admin_class,column).display_name.upper()
        ele = '''<th><a href="javascript:void(0);">{column}</a></th>'''.format(column=column_verbose_name)
        return mark_safe(ele)

    ele = ele.format(orderby_key=orderby_key, column=column_verbose_name, sort_icon=sort_icon, filters=filters)
    return mark_safe(ele)

@register.simple_tag
def build_table_row(request,obj,admin_class):
    row_ele = "<tr>"
    row_ele += "<td><input type='checkbox' tag='row-check' value='%s' > </td>" % obj.id
    for index,column in enumerate(admin_class.list_display):
        try:
            field_obj = obj._meta.get_field(column)
            if field_obj.choices:
                # print(obj)
                column_data = getattr(obj,"get_%s_display"%column)()
                # print(column_data)
            else:
                column_data = getattr(obj,column)
            if type(column_data).__name__ == 'datetime':
                column_data = column_data.strftime("%Y-%m-%d")
                row_ele += "<td style='background-color:#ddd'>%s</td>" % column_data
                continue

            if column in admin_class.list_editable:
                # print("走到这里",column)
                column_data = render_list_editable_column(admin_class, obj, field_obj)
                # print("特殊column",column_data)
            if index == 0:  # add a tag, 可以跳转到修改页
                column_data = "<a href='{request_path}{obj_id}/change/'>{data}</a>".format(request_path=request.path,obj_id=obj.id,
                                                                                            data=column_data)
        except FieldDoesNotExist as e:
            if hasattr(admin_class,column):
                column_func = getattr(admin_class,column)
                admin_class.instance = obj
                admin_class.request =request
                column_data =column_func()

        row_ele += "<td>%s</td>" % column_data

    return mark_safe(row_ele)


@register.simple_tag
def build_paginators(query_sets,filter_condtions,previous_orderby,search_text):
    '''返回整个分页元素'''
    page_btn=''
    filters =''
    for k,v in filter_condtions.items():
        filters +="&%s=%s"%(k,v)

    add_not_ele=False
    for page_num in query_sets.paginator.page_range:#page_num循环页   query_sets.number当前页
        if page_num <3 or page_num > query_sets.paginator.num_pages -2 \
            or abs(query_sets.number - page_num) <=2 :  #代表最前2页或最后2页 #abs判断前后2页
            ele_class =''
            if query_sets.number ==page_num:
                add_not_ele=False
                ele_class ="active"
            page_btn += '''<li class="%s"><a href="?page=%s%s&o=%s&_q=%s">%s</a></li>''' % (
                ele_class, page_num, filters, previous_orderby, search_text, page_num)
        else:#显示点点点
            if add_not_ele == False:
                page_btn += '<li><a>...</a></li>'
                add_not_ele=True
    return mark_safe(page_btn)



@register.simple_tag
def build_pag_next(query_sets,filter_condtions,previous_orderby,search_text):
    filters = ''
    for k, v in filter_condtions.items():
        filters += "&%s=%s" % (k, v)
    page_btn=''
    page_btn += '''%s&o=%s&_q=%s"''' % (filters,previous_orderby,search_text)



    return mark_safe(page_btn)


@register.simple_tag
def render_list_editable_column(admin_class, obj, field_obj):
    # print(admin_class,'admin_class---',obj,'obj-----',field_obj,'field_obj-----')
    if field_obj.get_internal_type() in("SmallIntegerField","CharField","ForeignKey","BingInterField","IntegerField"):
        column_data = field_obj._get_val_from_obj(obj)
        if not field_obj.choices and field_obj.get_internal_type() != "ForeignKey" :

            column = '''<input data-tag='editable' type='text' name='%s' value='%s' >''' %\
                     (field_obj.name,
                     field_obj._get_val_from_obj(obj) or '')
        else:
            column = '''<select data-tag='editable' class='form-control'  name='%s' >''' % field_obj.name
            # print("========",field_obj.get_choices())
            for option in field_obj.get_choices():
                if option[0] == column_data:
                    selected_attr = "selected"
                else:
                    selected_attr = ''
                column += '''<option value='%s' %s >%s</option>''' % (option[0], selected_attr, option[1])
            column += "</select>"
    elif field_obj.get_internal_type() == 'BooleanField':
        column_data = field_obj._get_val_from_obj(obj)
        if column_data == True:
            checked = 'checked'
        else:
            checked = ''
        column = '''<input data-tag='editable'   type='checkbox' name='%s' value="%s"  %s> ''' %(field_obj.name,
                                                                                               column_data,
                                                                                              checked)

    else:
        column = field_obj._get_val_from_obj(obj)

    return column



@register.simple_tag
def get_action_verbose_name(admin_class,action): #delete_selected_objs

    action_func = getattr(admin_class,action) #取得对象函数
    return  action_func.display_name if hasattr(action_func,'display_name') else action #如果没有对象就错了

@register.simple_tag
def get_m2m_obj_list(admin_class,field,form_obj):
    '''返回m2m所有数据'''
    field_obj = getattr(admin_class.model,field.name)
    all_obj_list = field_obj.rel.to.objects.all()

    if form_obj.instance.id:
        obj_instance_field = getattr(form_obj.instance,field.name)
        selected_obj_list = obj_instance_field.all()
    else:#代表这是在创建新的一条记录
        return all_obj_list

    standby_obj_list = []
    for obj in all_obj_list:
        if obj not in selected_obj_list:
            standby_obj_list.append(obj)

    return standby_obj_list


@register.simple_tag
def get_m2m_selected_obj_list(form_obj,field):
    '''返回已选择的m2m数据'''
    if form_obj.instance.id:
        field_obj = getattr(form_obj.instance,field.name)
        return field_obj.all()

def recursive_related_objs_lookup(objs):
    #model_name = objs[0]._meta.model_name
    print('objs:is ',objs)
    ul_ele = "<ul>"
    for obj in objs:  #处理每一个对象models.Customer.objects.get(id =1)
        li_ele = '''<li> %s: %s </li>'''%(obj._meta.verbose_name,obj.__str__().strip("<>"))
        ul_ele += li_ele

        #for local many to many
        # print("------- obj._meta.local_many_to_many", obj._meta.local_many_to_many)
        for m2m_field in obj._meta.local_many_to_many: #把所有跟这个对象直接关联的m2m字段取出来了
            print('-------',m2m_field)
            sub_ul_ele = "<ul>"
            m2m_field_obj = getattr(obj,m2m_field.name) #getattr(customer, 'tags')
            for o in m2m_field_obj.select_related():# customer.tags.select_related() 取出多对多关联的数据
                li_ele = '''<li> %s: %s </li>''' % (m2m_field.verbose_name, o.__str__().strip("<>"))
                sub_ul_ele +=li_ele

            sub_ul_ele += "</ul>"
            ul_ele += sub_ul_ele  #最终跟最外层的ul相拼接


        for related_obj in obj._meta.related_objects:
            if 'ManyToManyRel' in related_obj.__repr__():

                if hasattr(obj, related_obj.get_accessor_name()):  # hassattr(customer,'enrollment_set')
                    accessor_obj = getattr(obj, related_obj.get_accessor_name()) #customerfollowup_set

                    print("-------ManyToManyRel",accessor_obj,related_obj.get_accessor_name())
                    # 上面accessor_obj 相当于 customer.enrollment_set
                    if hasattr(accessor_obj, 'select_related'):  # slect_related() == all()
                        target_objs = accessor_obj.select_related()  # .filter(**filter_coditions)
                        # target_objs 相当于 customer.enrollment_set.all()

                        sub_ul_ele ="<ul style='color:red'>"
                        for o in target_objs:
                            li_ele = '''<li> %s: %s </li>''' % (o._meta.verbose_name, o.__str__().strip("<>"))
                            sub_ul_ele += li_ele
                        sub_ul_ele += "</ul>"
                        ul_ele += sub_ul_ele

            elif hasattr(obj,related_obj.get_accessor_name()): # hassattr(customer,'enrollment_set')
                accessor_obj = getattr(obj,related_obj.get_accessor_name())
                print("非常重要的一环：：",accessor_obj)
                if accessor_obj.model._meta.model_name == 'userprofile':
                    pass
                else:
                #上面accessor_obj 相当于 customer.enrollment_set
                    if hasattr(accessor_obj,'select_related'): # slect_related() == all()
                        target_objs = accessor_obj.select_related() #.filter(**filter_coditions)
                        # target_objs 相当于 customer.enrollment_set.all()
                    else:
                        print("one to one i guess:",accessor_obj)
                        target_objs = accessor_obj

                    if len(target_objs) >0:
                        #print("\033[31;1mdeeper layer lookup -------\033[0m")
                        #nodes = recursive_related_objs_lookup(target_objs,model_name)
                        nodes = recursive_related_objs_lookup(target_objs)
                        ul_ele += nodes
    ul_ele +="</ul>"
    return ul_ele


@register.simple_tag
def display_obj_related(objs):
    '''把对象及所有相关联的数据取出来'''
    #objs = [objs,] #fake    admin_class.model.objects.get(id=obj_id)
    print(objs, '------')
    if hasattr(objs,'name'):
        objs=[objs,]
        model_class = objs[0]._meta.model
        mode_name = objs[0]._meta.model_name
        # print('model_class,mode_name',model_class,mode_name)  表对象和表名
        return mark_safe(recursive_related_objs_lookup(objs))
    else:
        if objs:
            model_class = objs[0]._meta.model
            mode_name = objs[0]._meta.model_name
            return mark_safe(recursive_related_objs_lookup(objs))






