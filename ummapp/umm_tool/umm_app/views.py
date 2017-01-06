from django.shortcuts import render, HttpResponse, redirect
from .models import ExtraTask, Quarter, Category, Task, AdditionData, ColumnData, ComboUpdate, BudgetBand, Goal, GoalTaskMap, Question, Process, SubProcess, ProgramType, ProgramTask, TaskData, SubProcessLevelUpdates, ProgramAdditionData
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.conf import settings
import json
import datetime
from datetime import date
from .forms import ProcessForm, SubProcessForm, ProgramTypeForm, ProgramTaskForm, TaskDataForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
# view for Advertiser Goals


def home(request):
    subdomain = request.META.get('HTTP_HOST').split(".")[0]
    if subdomain == "ummtools":
        goal_map = Goal.objects.all()
        quarter = None
        quarter_id = get_quarter()
        context = RequestContext(request, {'request': request, 'user': request.user,'goal_map': goal_map, 'quarter':quarter_id})
        return render(request, "index.html", context_instance=context)
    elif subdomain == "apollotools":
        goal_map = Goal.objects.all()
        quarter = None
        quarter_id = get_quarter()
        is_manager = True if request.user.groups.filter(name='CHAPERONE-MANAGER') else False
        sub_processs = SubProcess.objects.filter(is_disabled=False)
        context = RequestContext(request, 
                    {'request': request, 'user': request.user,
                    'goal_map': goal_map, 'quarter':quarter_id, 
                    'is_manager':is_manager,
                    'sub_processs':sub_processs
                })
        return render(request, "apollo_index.html", context_instance=context)

    
@login_required
def tasks(request):
    goal_id_list = json.loads(request.GET.get('task_id_list'))
    goal = Goal.objects.filter(id__in=goal_id_list)

    goal_map = None
    extra_tasks = None
    questions = None
    result = {}
    goal_map_json = []
    addition_task_list = []
    questions_list = []
    task_names = []

    if goal:
        goal_map = GoalTaskMap.objects.filter(parent_goal_id__in=goal_id_list).distinct()
        extra_tasks = ExtraTask.objects.filter(parent_goal_id__in=goal_id_list).distinct()
        questions = Question.objects.filter(parent_goal_id__in=goal_id_list).distinct()
    
    if goal_map:
        for item in goal_map:
            task_items = item.parent_task_id.values()
            for item in task_items:
                task_names.append(item)
        if task_names is not None:
            for item in task_names:
                temp = {}
                temp['name'] = item['task_name']
                temp['id'] = item['id']
                temp['parent_id'] = item['parent_category_id_id']
                goal_map_json.append(temp)
        result['goals'] = goal_map_json
        result['goals'] = [dict(t) for t in set([tuple(d.items()) for d in result['goals']])]
    else:
        task_names = None
    if extra_tasks is not None:
        for item in extra_tasks:
            addition_task_list.append(item.extra_task_name)
        result['extra_tasks'] = addition_task_list
    if questions is not None:
        for item in questions:
            questions_list.append(item.question)
        result['questions'] = questions_list
    return HttpResponse(json.dumps(result), content_type="application/json")


# view for UMM Offerings
def get_quarter():
    quarter_id = None
    month = int(datetime.datetime.now().strftime("%m"))
    current_quarter = 4
    current_year = 2015
    quarters = Quarter.objects.all()
    if len(quarters):
        for q in quarters:
            if q.quarter_year == current_year:
                if int(q.quarter) == current_quarter:
                    quarter_id = q.id
    return [quarter_id,current_quarter,current_year]


@login_required
def home1(request):
    quarter = None
    template = "home.html"
    categorys = list()
    tasks = list()
    lefttab = list()
    righttab = list()
    quarter_id = get_quarter()
    if quarter_id[0]:
        quarter = Quarter.objects.get(pk=quarter_id[0])
        categorys = Category.objects.filter(parent_quarter_id=quarter_id[0], is_disable=False)
        if len(categorys):
            tasks = Task.objects.filter(parent_category_id=categorys[0], is_disable=False)
            if len(tasks):
                lefttab = ColumnData.objects.filter(parent_task_id=tasks[0], is_disable=False)
                righttab = AdditionData.objects.filter(parent_task_id=tasks[0], is_disable=False)
    return render(request, template, {'tasks': tasks, 'lefttab': lefttab, 'righttab': righttab, 'categorys': categorys, 'quarter': quarter_id})


@login_required
def task_list(request, cat_id):
    tasks = Task.objects.filter(parent_category_id_id=cat_id, is_disable=False)
    data = serializers.serialize('json', tasks)
    response = HttpResponse(data, content_type='application/json')
    return response


@login_required
def combo_data(request):
    quarter_id = get_quarter()
    data = dict()
    combodata = ComboUpdate.objects.filter(parent_quarter_id_id=quarter_id[0])
    data = serializers.serialize('json', combodata)
    response = HttpResponse(data, content_type='application/json')
    return response


@login_required
def left_column_list(request, task_id):
    column_listing_left = ColumnData.objects.filter(parent_task_id_id=task_id, is_disable=False)
    data = serializers.serialize('json', column_listing_left)
    response = HttpResponse(data, content_type='application/json')
    return response


@login_required
def right_column_list(request, task_id):
    column_listing_right = AdditionData.objects.filter(parent_task_id_id=task_id, is_disable=False)
    data = serializers.serialize('json', column_listing_right)
    response = HttpResponse(data, content_type='application/json')
    return response


@login_required
def elevator_pitch_data(request, task_id):
    elevator_pitch_data = AdditionData.objects.filter(parent_task_id_id=task_id, is_disable=False)
    data = serializers.serialize('json', elevator_pitch_data)
    response = HttpResponse(data, content_type='application/json')
    return response


@login_required
def budget_band(request):
    quarter_id = get_quarter()
    data = dict()
    budgetbanddetail = BudgetBand.objects.filter(parent_quarter_id_id=quarter_id[0])
    data = serializers.serialize('json', budgetbanddetail)
    response = HttpResponse(data, content_type='application/json')
    return response


def auth_error(request):
    error = "Please sign out from current Google account and use your Regalix Email Id to login"
    context = RequestContext(request, {'request': request, 'user': request.user, 'error': error})
    return render(request, 'index.html', context_instance=context)


def check_email(request, strategy, details, *args, **kwargs):
    email = details.get('email')
    domain = details.get('email').split('@')[1]
    if domain not in settings.SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS:
        if email not in settings.SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS:
            return redirect('/auth/error')



# All Appolo code
@login_required
def manage_admin(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        processes = Process.objects.all()
        context = RequestContext(request, {'request': request, 'user': request.user,'processes':processes})
    return render(request, "manage_admin/umm_admin.html", context_instance = context) 


@login_required
def process_handler(request):
    context = {}
    success = False
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.POST:
            process_data = json.loads(request.POST.get("processData"))
            try:
                quarter = Quarter.objects.get(quarter=process_data.get("quarter"),quarter_year=process_data.get("quarter_year"))
            except Quarter.DoesNotExist:
                quarter = Quarter()
                quarter.quarter = process_data.get("quarter")
                quarter.quarter_year = process_data.get("quarter_year")
                quarter.save()
            try:
                process_objects = list()
                process = Process()
                if request.FILES:
                    img_file = request.FILES['file']
                    process.image_ref = img_file
                process.name = process_data.get("name")
                process.url_name = process_data.get("name").lower().replace(' ','-')
                process.created_by = User.objects.get(email=request.user.email)
                process.modified_by =  User.objects.get(email=request.user.email)
                process.save()
                process_objects.append(process)

                sub_process_url_name = process_data.get("sub_process_name").lower().replace(' ','-')
                sub_process = SubProcess()
                sub_process.process = process
                sub_process.quarter = quarter
                sub_process.is_disabled = True
                sub_process.name = process_data.get("sub_process_name")
                sub_process.url_name = sub_process_url_name
                sub_process.created_by = User.objects.get(email=request.user.email)
                sub_process.modified_by =  User.objects.get(email=request.user.email)
                sub_process.save()
                process_objects.append(sub_process)

                programs = process_data.get("programs")
                for ptype,ptask in programs.iteritems():
                    program_type = ProgramType()
                    program_type.subprocess = sub_process
                    program_type.name = ptype
                    program_type.is_disabled = False
                    program_type.created_by = User.objects.get(email=request.user.email)
                    program_type.modified_by =  User.objects.get(email=request.user.email)
                    program_type.save()
                    process_objects.append(program_type)

                    for val in ptask:
                        program_task = ProgramTask()
                        program_task.program_type = program_type
                        program_task.name = val
                        program_type.is_disabled = False
                        program_task.created_by = User.objects.get(email=request.user.email)
                        program_task.modified_by =  User.objects.get(email=request.user.email)
                        program_task.save()
                        process_objects.append(program_task)
                del process_objects
                context = {'process_id':process.id,'sub_process_url_name':sub_process_url_name,'success':True, 'msg':'Process created successfully'}
            except Exception as e:
                for obj in process_objects:
                    obj.delete()
                context = {'success':False,'msg':'Something went wrong, please try after some time'}
            return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            context = RequestContext(request, {'request': request, 'user': request.user, 'success':True})
    return render(request, "manage_admin/create_process1.html", context_instance = context) 


@login_required
@csrf_exempt
def get_process(request):
    context = {}
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.POST:
            try:
                process = Process.objects.get(name=request.POST.get('name'))
                context['msg'] = "Process with the name already exists"
            except Process.DoesNotExist:
                context['msg'] = ''
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
@csrf_exempt
def create_task_data(request, process_id=None, sprocess_name=None):
    data = {}
    context = {}
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        process = Process.objects.get(id=process_id)
        sub_process = SubProcess.objects.get(url_name=sprocess_name, process=process)
        data["process_name"] = process.name
        data["process_id"] = process.id
        data["sub_process_name"] = sub_process.name
        data["sub_process_id"] =  sub_process.id
        programs = {}
        program_task = None
        program_types = ProgramType.objects.filter(subprocess=sub_process)
        for prog in program_types:
            tasks = []
            program_task = ProgramTask.objects.filter(program_type=prog)
            for task in program_task:
                tasks.append({"task_name":task.name, "task_id":task.id})
            programs[prog.name] = {"id":prog.id, "tasks":tasks}
        data["programs"] = programs
        task_data_list = []
        context = RequestContext(request, {
                        'request': request, 'user': request.user, 
                        'success':True,
                        'data':data
                        })
    return render(request, "manage_admin/additional_data.html", context_instance = context) 



@login_required
def get_program_tasks(request, program_type_id):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == "GET":
            try:
                program_tasks = ProgramTask.objects.filter(program_type=program_type_id)
                tasks = [{task.name: task.id} for task in program_tasks]
            except ObjectDoesNotExist:
                program_tasks = []
    return HttpResponse(json.dumps({"data":tasks, "success":True, "msg":""}), content_type="application/json")    

@login_required
def get_task_data(request, task_id):
    task_data = TaskData.objects.filter(program_task=int(task_id)).order_by("column_number")
    columns = []
    for td in task_data:
        tdata = {
            'column_name':td.column_name,
            'column_number':td.column_number,
            'data':td.data,
            'data_id':td.id
        }
        columns.append(tdata)
    return HttpResponse(json.dumps({"data":columns, "success":True, "msg":""}), content_type="application/json")    


@login_required
@csrf_exempt
def get_column_name(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == "POST":
            task_id = request.POST.get("task_id")  
            column_name = request.POST.get("column_name")
            data_id = request.POST.get("task_data_id", None)
            context = {}
            task_data = TaskData.objects.filter(program_task=task_id, column_name=column_name)
            if data_id:
                columns = [clmn.column_name for clmn in task_data if clmn.id != int(data_id)]
                if columns.count(column_name) > 0:
                    context["success"] = False
                    context["msg"] = "Column Name already exists, please try other."
                else:
                    context["success"] = True
                    context["msg"] = ""
            else:
                if len(task_data) == 0:
                    context["success"] = True
                    context["msg"] = ""
                else:
                    context["success"] = False
                    context["msg"] = "Column Name already exists, please try other."
    return HttpResponse(json.dumps(context), content_type="application/json")        



@login_required
@csrf_exempt
def add_task_data(request):
    """
        Add or update the task data
    """
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == "POST":
            program_task_id = int(request.POST.get('program_task_id'))
            task_data_id = request.POST.get('task_data_id')
            column_number = int(request.POST.get('column_number'))
            column_data = request.POST.get('column_data')
            column_name = request.POST.get('column_name')
            context = {
                        'task_data_id':task_data_id,
                        'task_id':program_task_id,
                        'column_name':column_name, 
                        'column_data':column_data, 
                        'success':True, 
                        'msg':'Updated successfully'
             }
            if task_data_id:
                try:
                    task_data = TaskData.objects.get(id=task_data_id)
                except ObjectDoesNotExist:
                    context = {'msg' : 'Something went wrong, please try after some time'}
                task_data.column_name = column_name
                task_data.column_number = column_number
                task_data.data = column_data
                task_data.modified_by =  User.objects.get(email=request.user.email)
                task_data.save()
            else:
                task = ProgramTask.objects.get(id=program_task_id)
                task_data = TaskData()
                task_data.program_task = task
                task_data.column_name = column_name
                task_data.column_number = column_number
                task_data.data = column_data
                task_data.is_disabled = False
                task_data.created_by = User.objects.get(email=request.user.email)
                task_data.modified_by =  User.objects.get(email=request.user.email)
                task_data.save()
                context["task_data_id"] = task_data.pk
                context["msg"] = "Column created successfully"
    return HttpResponse(json.dumps(context), content_type="application/json")        


@login_required
def show_process_data(request, sprocess_name):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == "GET":
            sub_process = SubProcess.objects.get(url_name=sprocess_name)
            if sub_process:
                program_types = ProgramType.objects.filter(subprocess=sub_process)
                sub_processs = SubProcess.objects.filter(is_disabled=False)
            context = RequestContext(request, 
                        {'request': request, 'user': request.user,'sub_process':sub_process,
                        'program_types':program_types,'sub_processs':sub_processs})
            return render(request, "apollo_home.html", context_instance=context) 
    else:
        raise PermissionDenied


@login_required
def subprocess_handler(request, reference_id=None):
    """
        If get request returns all the sub processes of a given reference_id (here it is process id).
        If post request, reference_id will act as sub process id and allows us to update the particulat record.
    """
    if request.method == "GET" and not request.is_ajax():
        context = {}
        sub_process = SubProcess.objects.filter(process=reference_id).order_by('-created_date')
        if sub_process:
            context["subprocess_name"] = sub_process[0].process.name
        return render(request, "manage_admin/subprocess_list.html", context_instance=RequestContext(request,context)) 
    if request.method == "GET" and request.is_ajax():
        enableProcess = request.GET.get("enable", None)
        if enableProcess:
            stat = False if enableProcess == "true" else True
            sub_process = SubProcess.objects.get(id=reference_id)
            sub_process.is_disabled = stat
            sub_process.save()
            toggleStat = " Disabled " if stat else " Enabled "
            return HttpResponse(json.dumps({"success":True, "msg": "Successfully" + toggleStat + sub_process.name}), content_type="application/json")
        else:
            sub_processes = []
            sub_process = SubProcess.objects.filter(process=reference_id).order_by('-created_date')
            for sub in sub_process:
                resp = {
                "process_name": sub.process.name,
                "process_id":sub.process.id,
                "sp_id": sub.id,
                "name": sub.name,
                "quarter": {
                    "quarter": sub.quarter.quarter,
                    "year": sub.quarter.quarter_year
                    },
                "url_name": sub.url_name,
                "is_disabled": sub.is_disabled
                }
            sub_processes.append(resp)
            return HttpResponse(json.dumps(sub_processes), content_type="application/json")
    elif request.method == "POST":
        if request.user.groups.filter(name='CHAPERONE-MANAGER'):
            print request.post
        else:
            raise PermissionDenied
        

@login_required
def subprocess_data_handler(request, subprocess_id=None):
    """
        Returns/Updates the data of subprocess based on the subprocess id provided
    """
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass


@login_required
@csrf_exempt
def get_carousel_column_name(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == "POST":
            subprocess_id = request.POST.get("subprocess_id")  
            column_name = request.POST.get("column_name")
            carousel_data_id = request.POST.get("carousel_data_id", None)
            context = {}
            carousel_data = SubProcessLevelUpdates.objects.filter(subprocess=subprocess_id, name=column_name)
            if carousel_data_id:
                columns = [clmn.name for clmn in carousel_data if clmn.id != int(carousel_data_id)]
                if columns.count(column_name) > 0:
                    context["success"] = False
                    context["msg"] = "Column Name already exists, please try other."
                else:
                    context["success"] = True
                    context["msg"] = ""
            else:
                if len(carousel_data) == 0:
                    context["success"] = True
                    context["msg"] = ""
                else:
                    context["success"] = False
                    context["msg"] = "Column Name already exists, please try other."
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
@csrf_exempt
def add_carousel_data(request):
    """
        Add or update the carousel data
    """
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == "POST":
            sub_process_id = int(request.POST.get('sub_process_id'))
            carousel_data_id = request.POST.get('carousel_data_id')
            column_data = request.POST.get('column_data')
            column_name = request.POST.get('column_name')
            context = {
                        'sub_process_id':sub_process_id,
                        'carousel_data_id':carousel_data_id,
                        'column_name':column_name, 
                        'column_data':column_data, 
                        'success':True, 
                        'msg':'Updated successfully'
             }
            if carousel_data_id:
                try:
                    carousel_data = SubProcessLevelUpdates.objects.get(id=carousel_data_id)
                except ObjectDoesNotExist:
                    context = {'msg' : 'Something went wrong, please try after some time'}
                carousel_data.name = column_name
                carousel_data.data = column_data
                carousel_data.modified_by =  User.objects.get(email=request.user.email)
                carousel_data.save()
            else:
                subprocess = SubProcess.objects.get(id=sub_process_id)
                carousel_data = SubProcessLevelUpdates()
                carousel_data.subprocess = subprocess
                carousel_data.name = column_name
                carousel_data.data = column_data
                carousel_data.created_by = User.objects.get(email=request.user.email)
                carousel_data.modified_by =  User.objects.get(email=request.user.email)
                carousel_data.save()
                context["carousel_data_id"] = carousel_data.pk
                context["msg"] = "Column created successfully"
    return HttpResponse(json.dumps(context), content_type="application/json")   


@login_required
def get_carousel_data(request, sub_process_id):
    carousel_data = SubProcessLevelUpdates.objects.filter(subprocess=int(sub_process_id))
    columns = []
    for td in carousel_data:
        tdata = {
            'column_name':td.name,
            'data':td.data,
            'data_id':td.id
        }
        columns.append(tdata)

    return HttpResponse(json.dumps({"data":columns, "success":True, "msg":""}), content_type="application/json")


@login_required
@csrf_exempt
def get_addldata_column_name(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == "POST":
            task_id = request.POST.get("task_id")  
            column_name = request.POST.get("column_name")
            data_id = request.POST.get("addl_data_id", None)
            context = {}
            addl_data = ProgramAdditionData.objects.filter(program_task=task_id, name=column_name)
            print data_id,'data_id'
            if data_id:
                columns = [clmn.name for clmn in addl_data if clmn.id != int(data_id)]
                if columns.count(column_name) > 0:
                    context["success"] = False
                    context["msg"] = "Column Name already exists, please try other."
                else:
                    context["success"] = True
                    context["msg"] = ""
            else:
                if len(addl_data) == 0:
                    context["success"] = True
                    context["msg"] = ""
                else:
                    context["success"] = False
                    context["msg"] = "Column Name already exists, please try other."
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
@csrf_exempt
def add_addldata(request):
    """
        Add or update the addititonal task data
    """
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == "POST":
            program_task_id = int(request.POST.get('program_task_id'))
            additionaldata_id = request.POST.get('additionaldata_id')
            column_data = request.POST.get('column_data')
            column_name = request.POST.get('column_name')
            context = {
                        'additionaldata_id':additionaldata_id,
                        'task_id':program_task_id,
                        'column_name':column_name,
                        'column_data':column_data, 
                        'success':True, 
                        'msg':'Updated successfully'
             }
            if additionaldata_id:
                try:
                    addl_data = ProgramAdditionData.objects.get(id=additionaldata_id)
                except ObjectDoesNotExist:
                    context = {'msg' : 'Something went wrong, please try after some time'}
                addl_data.name = column_name
                addl_data.data = column_data
                addl_data.modified_by =  User.objects.get(email=request.user.email)
                addl_data.save()
            else:
                task = ProgramTask.objects.get(id=program_task_id)
                addl_data = ProgramAdditionData()
                addl_data.program_task = task
                addl_data.name = column_name
                addl_data.data = column_data
                addl_data.is_disabled = False
                addl_data.created_by = User.objects.get(email=request.user.email)
                addl_data.modified_by =  User.objects.get(email=request.user.email)
                addl_data.save()
                context["addl_data_id"] = addl_data.pk
                context["msg"] = "Column created successfully"
    return HttpResponse(json.dumps(context), content_type="application/json") 


@login_required
def get_addldata(request, task_id):
    addl_data = ProgramAdditionData.objects.filter(program_task=int(task_id))
    columns = []
    for td in addl_data:
        tdata = {
            'column_name':td.name,
            'data':td.data,
            'data_id':td.id
        }
        columns.append(tdata)
    return HttpResponse(json.dumps({"data":columns, "success":True, "msg":""}), content_type="application/json")