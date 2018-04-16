from django.shortcuts import render,redirect
from king_admin.utils import table_filter,table_search,table_sort
# Create your views here.
from king_admin import king_admin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from king_admin.forms import create_model_form
from django.contrib.auth.decorators import login_required
from crm.permissions import permission

@login_required
def index(request):
    return render(request,'king_admin/table_index.html',{'table_list':king_admin.enabled_admins})

# @permission.check_permission
@login_required
def display_table_objs(request,app_name,table_name):
    admin_class=king_admin.enabled_admins[app_name][table_name]

    if request.method =="POST":#action 来了
        selected_ids = request.POST.get("selected_ids")
        action = request.POST.get("action")
        if selected_ids:
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids.split(','))
            print(selected_objs,'selected_objs----------')
        else:
            raise KeyError("No object selected")
        if hasattr(admin_class,action):
            action_func = getattr(admin_class,action)
            request._admin_action = action
            print('1先执行',selected_ids)
            return action_func(admin_class,request,selected_objs) #执行函数 并返回结果




    object_list,filter_condtions = table_filter(request,admin_class) #过滤后的结果

    object_list = table_search(request,admin_class,object_list)

    object_list,orderby_key=table_sort(request,admin_class,object_list)

    paginator = Paginator(object_list,admin_class.list_per_page)
    page =request.GET.get('page')

    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)


    # print('search:',request.GET.get('_q', '')) #22
    # print('query_sets',query_sets)
    return render(request,'king_admin/table_objs.html',{'admin_class':admin_class,
                                                        "filter_condtions": filter_condtions,
                                                        "search_text": request.GET.get('_q', ''),
                                                        "orderby_key": orderby_key,
                                                        "query_sets":query_sets,
                                                        "previous_orderby": request.GET.get("o", ''),
                                                        'app_name':app_name
                                                        })


# @permission.check_permission
@login_required
def table_obj_change(request,app_name,table_name,obj_id):
    print('进入了函数')
    admin_class= king_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)
    # print(model_form_class)

    obj=admin_class.model.objects.get(id=obj_id)
    if request.method == "POST":
        form_obj = model_form_class(request.POST,instance=obj)#更新操作
        if form_obj.is_valid():
            form_obj.save()
    else:
        form_obj = model_form_class(instance=obj)
    # print(form_obj,'is --------')
    return render(request,'king_admin/table_obj_change.html',{'form_obj':form_obj,
                                                              'admin_class':admin_class,
                                                              'app_name':app_name,
                                                              'table_name':table_name})

@login_required
def table_obj_delete(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    obj = admin_class.model.objects.get(id=obj_id)
    if  admin_class.readonly_table:
        errors = {"readonly_table": "table is readonly ,obj [%s] cannot be deleted" % obj}
    else:
        errors = {}

    if request.method =="POST":
        if not admin_class.readonly_table:
            obj.delete()
        # print('走到这里了',"king_admin/%s/%s"%(app_name,table_name))
            return redirect("/king_admin/%s/%s"%(app_name,table_name))

    return render(request,"king_admin/table_obj_delete.html",{'obj':obj,
                                                              "admin_class": admin_class,
                                                              "app_name": app_name,
                                                              "table_name": table_name,
                                                              'errors':errors
                                                              })


@login_required
def table_obj_add(request,app_name,table_name):

    admin_class = king_admin.enabled_admins[app_name][table_name]
    admin_class.is_add_form = True
    model_form_class = create_model_form(request,admin_class)

    if request.method == "POST":
        form_obj = model_form_class(request.POST)  #
        if form_obj.is_valid():
            form_obj.save()

            return  redirect(request.path.replace("/add/","/"))
    else:
        form_obj = model_form_class()

    # print('form_obj:',form_obj,'admin_class',admin_class)
    return render(request, "king_admin/table_obj_add.html", {"form_obj": form_obj,
                                                             "admin_class": admin_class,
                                                             'app_name':app_name,
                                                             'table_name':table_name,
                                                             })

@login_required
def password_reset(request,app_name,table_name,obj_id):

    admin_class = king_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)

    obj = admin_class.model.objects.get(id=obj_id)
    errors = {}
    if request.method == "POST":
        _password1 = request.POST.get("password1")
        _password2 = request.POST.get("password2")

        if _password1 == _password2:
            if len(_password2) >5:
                obj.set_password(_password1)
                obj.save()
                return redirect(request.path.rstrip("password/"))

            else:
                errors["password_too_short"] = "must not less than 6 letters"
        else:
            errors['invalid_password'] = "passwords are not the same"
    return render(request,'king_admin/password_reset.html', {"obj":obj,'errors':errors})



@login_required
def app_tables(request,app_name):
    enabled_admins = {app_name:king_admin.enabled_admins[app_name]}
    print(enabled_admins,'-----------')
    print(app_name,'app_name')
    return render(request, 'king_admin/app_index.html',{'enabled_admins':enabled_admins,'current_app':app_name})





