from django.shortcuts import render, HttpResponse, redirect
from .models import ExtraTask, Quarter, Category, Task, AdditionData, ColumnData, ComboUpdate, BudgetBand, Goal, GoalTaskMap, Question, Process, SubProcess, ProgramType, ProgramTask, TaskData, SubProcessLevelUpdates, ProgramAdditionData, Faq, QualityFramework
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
from django.views.decorators.http import require_http_methods

from .utils import delete_process, delete_sub_process, delete_program_additional_data, delete_program_tasks, delete_program_types, delete_subprocess_level_data, delete_task_data


# view for Advertiser Goals


def home(request):
    goal_map = Goal.objects.all()
    quarter = None
    quarter_id = get_quarter()
    is_manager = True if request.user.groups.filter(name='CHAPERONE-MANAGER') else False
    sub_processs = SubProcess.objects.filter(is_disabled=False)
    context = RequestContext(request, {'request': request, 'user': request.user,
                                       'goal_map': goal_map, 'quarter': quarter_id,
                                       'is_manager': is_manager, 'sub_processs': sub_processs
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
    else:
        raise PermissionDenied

@login_required
def process_handler(request):
    context = {}
    success = False
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.POST:
            process_data = json.loads(request.POST.get("processData"))
            proId = process_data.get("proId", None)
            try:
                quarter = Quarter.objects.get(quarter=process_data.get("quarter"),quarter_year=process_data.get("quarter_year"))
            except Quarter.DoesNotExist:
                quarter = Quarter()
                quarter.quarter = process_data.get("quarter")
                quarter.quarter_year = process_data.get("quarter_year")
                quarter.save()
            try:
                process_objects = list()
                if not proId:
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
                else:
                    process = Process.objects.get(pk=proId)
                sub_process_url_name = process_data.get("sub_process_name").lower().replace(' ', '-')
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
    else:
        raise PermissionDenied


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
    else:
        raise PermissionDenied


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
        data["quarter"] = sub_process.quarter.quarter
        data["year"] = sub_process.quarter.quarter_year
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
    else:
        raise PermissionDenied


@login_required
def get_program_tasks(request, program_type_id):
    #if request.user.groups.filter(name='CHAPERONE-MANAGER'):
    if request.method == "GET":
        try:
            program_tasks = ProgramTask.objects.filter(program_type=program_type_id)
            tasks = [{task.name: task.id} for task in program_tasks]
        except ObjectDoesNotExist:
            program_tasks = []
        return HttpResponse(json.dumps({"data":tasks, "success":True, "msg":""}), content_type="application/json")    
    """
    else:
        raise PermissionDenied
    """

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
    else:
        raise PermissionDenied        



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
                        'msg':'Task data updated successfully'
             }
            if task_data_id:
                try:
                    task_data = TaskData.objects.get(id=task_data_id)
                except ObjectDoesNotExist:
                    context = {'success': False, 'msg' : 'Something went wrong, please try after some time'}
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
                context["msg"] = "Task data created successfully"
            return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        raise PermissionDenied        


@login_required
def show_process_data(request, process_id, sprocess_name):
    #if request.user.groups.filter(name='CHAPERONE-MANAGER'):
    if request.method == "GET":
        is_manager = True if request.user.groups.filter(name='CHAPERONE-MANAGER') else False
        sub_process = SubProcess.objects.get(process=process_id,url_name=sprocess_name)
            
        if sub_process:
            program_types = ProgramType.objects.filter(subprocess=sub_process).order_by('created_date')
            sub_processs = SubProcess.objects.filter(is_disabled=False)
        response = {'request': request, 'user': request.user,'sub_process':sub_process,
                    'program_types':program_types,'sub_processs':sub_processs,
                    'is_manager':is_manager
                    }
        faq = Faq.objects.all().count()
        if faq > 0:
            response['faq'] = True
        else:
            pass
        context = RequestContext(request, response)
        qf = QualityFramework.objects.all().count()
        if qf > 0:
            response['qf'] = True
        else:
            pass
        context = RequestContext(request, response)
        return render(request, "apollo_home.html", context_instance=context) 
    """
    else:
        raise PermissionDenied
    """


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
    elif request.method == "GET" and request.is_ajax():
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
    else:
        raise PermissionDenied


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
                        'msg':'Carousel data updated successfully'
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
                context["msg"] = "Carousel data created successfully"
            return HttpResponse(json.dumps(context), content_type="application/json") 
    else:
        raise PermissionDenied  


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
    else:
        raise PermissionDenied

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
                        'msg':'Task additional data updated successfully'
             }
            if additionaldata_id:
                try:
                    addl_data = ProgramAdditionData.objects.get(id=additionaldata_id)
                except ObjectDoesNotExist:
                    context = {'success': False, 'msg' : 'Something went wrong, please try after some time'}
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
                context["msg"] = "Task additional data created successfully"
            return HttpResponse(json.dumps(context), content_type="application/json") 
    else:
        raise PermissionDenied


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


@login_required
def get_subprocess_programdata(request, sub_process_id):
    program_types = ProgramType.objects.filter(subprocess=int(sub_process_id))
    programs = {}
    program_data = []
    for prog in program_types:
        tasks = []
        program_task = ProgramTask.objects.filter(program_type=prog)
        program_data_dict = {}
        program_data_dict['p_type_id'] = prog.id
        program_data_dict['p_type_name'] = prog.name
        program_task_dict = {}
        for task in program_task:
            program_task_dict[task.id] = task.name
        program_data_dict['program_tasks'] = program_task_dict
        tasks = [{task.id: task.name} for task in program_task]
        program_data.append(program_data_dict)
    return HttpResponse(json.dumps({"data":program_data, "success":True, "msg":""}), content_type="application/json") 


@login_required
def add_subprocess_programdata(request, sub_process_id):
    context = {}
    success = False
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.POST:
            process_data = json.loads(request.POST.get("processData"))
            try:
                process_objects = list()
                sub_process_id = process_data.get('sub_process_id')
                sub_process = SubProcess.objects.get(id=int(sub_process_id))
                programs = process_data.get("programs")
                prg_type_id = process_data.get("prg_type_id")
                for ptype,ptask in programs.iteritems():
                    try:
                        program_type_id = prg_type_id.get(ptype)
                        if program_type_id == u'':
                            program_type_id = None
                        program_type = ProgramType.objects.get(subprocess=sub_process,id=program_type_id)
                    except ObjectDoesNotExist:
                        program_type = ProgramType()
                    program_type.subprocess = sub_process
                    program_type.name = ptype
                    program_type.is_disabled = False
                    program_type.created_by = User.objects.get(email=request.user.email)
                    program_type.modified_by =  User.objects.get(email=request.user.email)
                    program_type.save()
                    process_objects.append(program_type)

                    program_tasks = ProgramTask.objects.filter(program_type=program_type).exclude(name__in=ptask)
                    if program_tasks:
                        program_tasks.delete()
                    for val in ptask:
                        try:
                            program_task = ProgramTask.objects.get(program_type=program_type,name=val)
                        except ObjectDoesNotExist:
                            program_task = ProgramTask()
                        program_task.program_type = program_type
                        program_task.name = val
                        program_type.is_disabled = False
                        program_task.created_by = User.objects.get(email=request.user.email)
                        program_task.modified_by =  User.objects.get(email=request.user.email)
                        program_task.save()
                        process_objects.append(program_task)
                del process_objects
                context = {'process_id':sub_process.process.id,'sub_process_url_name':sub_process.url_name,'success':True, 'msg':'Program type and tasks created successfully'}                        
            except Exception as e:
                for obj in process_objects:
                    obj.delete()
                context = {'success':False,'msg':'Something went wrong, please try after some time'}
            return HttpResponse(json.dumps(context), content_type="application/json")       
        else:
            return HttpResponse(json.dumps({"data":{}, "success":True, "msg":""}), content_type="application/json")       
    else:
        raise PermissionDenied

@login_required
def edit_subprocess(request, sub_process_id):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        context = {}
        if request.method == "POST":
            sub_process_name = request.POST.get("sub_process_name")
            try:
                quarter = Quarter.objects.get(quarter=request.POST.get("quarter"),quarter_year=request.POST.get("quarter_year"))
            except ObjectDoesNotExist:
                quarter = Quarter()
                quarter.quarter = request.POST.get("quarter")
                quarter.quarter_year = int(request.POST.get("quarter_year"))
                quarter.save()

            process = SubProcess.objects.get(id=sub_process_id).process
            sub_process_url_name = sub_process_name.lower().replace(' ','-')
            exists = True
            try:
                sub_process = SubProcess.objects.get(process=process,name=sub_process_name,quarter=quarter)
                if sub_process.id == int(sub_process_id):
                    exists = False
            except ObjectDoesNotExist:
                exists = False
            
            if exists:
                context = {'success':False,'msg':'Sub Process with this name , quarter and year already exists'}
            else:
                """
                update sub process
                """
                sub_process = SubProcess.objects.get(id=sub_process_id)
                sub_process.quarter = quarter
                sub_process.name = sub_process_name
                sub_process.url_name = sub_process_name.lower().replace(' ','-')
                sub_process.created_by = User.objects.get(email=request.user.email)
                sub_process.modified_by =  User.objects.get(email=request.user.email)
                sub_process.save()
                context = {
                        'process_id':process.id,
                        'sub_process_url_name':sub_process_url_name,
                        'success':True, 
                        'msg': sub_process_name + ' updated successfully.'
                    }                      
            return HttpResponse(json.dumps(context), content_type="application/json")


@require_http_methods(['POST'])
@login_required
@csrf_exempt
def clone_subprocess(request, process_id, sprocess_name):
    """
    Args:
        request: request object
        sprocess_name: subprocess URL
        process_id: Process ID

    Get sub process by ID, re create it with new PK.
    Take the new subprocess id and create program types and create columns an associate data to it.

    Returns: JSON response with parameters success/ message/ data

    """
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        sub_process = None
        try:
            process = Process.objects.get(id=process_id)
            sub_process = SubProcess.objects.get(url_name=sprocess_name, process=process)
        except ObjectDoesNotExist:
            resp = {"success": False, "msg": "There is no sub process with the given id"}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        subprocess_name = sub_process.name
        cloned_count = sub_process.cloned_count + 1
        sub_process.cloned_count = cloned_count
        sub_process.save()
        quarter = sub_process.quarter
        programs = ProgramType.objects.filter(subprocess=sub_process)
        updates = SubProcessLevelUpdates.objects.filter(subprocess=sub_process)

        # Creating new sub Process
        sub_process_url_name = sub_process.url_name + "-Copy"+ str(cloned_count)
        sub_process_name = subprocess_name + "-Copy" + str(cloned_count)
        sub_process = SubProcess()
        sub_process.process = process
        sub_process.quarter = quarter
        sub_process.name = sub_process_name
        sub_process.cloned_count = 0
        sub_process.is_disabled = True
        sub_process.url_name = sub_process_url_name
        sub_process.created_by = User.objects.get(email=request.user.email)
        sub_process.modified_by = User.objects.get(email=request.user.email)
        sub_process.save()

        # Creating programs
        for prog in programs:
            program_type = ProgramType()
            program_type.subprocess = sub_process
            program_type.name = prog.name
            program_type.is_disabled = False
            program_type.created_by = User.objects.get(email=request.user.email)
            program_type.modified_by = User.objects.get(email=request.user.email)
            program_type.save()

            # Creating program tasks
            ptask = ProgramTask.objects.filter(program_type=prog)
            for task in ptask:
                program_task = ProgramTask()
                program_task.program_type = program_type
                program_task.name = task.name
                program_task.is_disabled = False
                program_task.created_by = User.objects.get(email=request.user.email)
                program_task.modified_by = User.objects.get(email=request.user.email)
                program_task.save()

                # Creating Programming additional data, if exists.
                pad = ProgramAdditionData.objects.filter(program_task=task)
                for d in pad:
                    additional_data = ProgramAdditionData()
                    additional_data.program_task = program_task
                    additional_data.name = d.name
                    additional_data.data = d.data
                    additional_data.is_disabled = False
                    additional_data.created_by = User.objects.get(email=request.user.email)
                    additional_data.modified_by = User.objects.get(email=request.user.email)
                    additional_data.save()

                # Creating task data
                pvals = TaskData.objects.filter(program_task=task)
                for column in pvals:
                    task_data = TaskData()
                    task_data.program_task = program_task
                    task_data.column_name = column.column_name
                    task_data.column_number = column.column_number
                    task_data.data = column.data
                    task_data.is_disabled = False
                    task_data.created_by = User.objects.get(email=request.user.email)
                    task_data.modified_by = User.objects.get(email=request.user.email)
                    task_data.save()

        # Creating subprocess level updates
        for splu in updates:
            carousel_data = SubProcessLevelUpdates()
            carousel_data.subprocess = sub_process
            carousel_data.name = splu.name
            carousel_data.data = splu.data
            carousel_data.created_by = User.objects.get(email=request.user.email)
            carousel_data.modified_by = User.objects.get(email=request.user.email)
            carousel_data.save()

        resp = {"success": True, "msg": "Successfully cloned the sub process"}
        data = {
            "name": sub_process_name,
            "url_name": sub_process_url_name,
            "process_id": process_id,
            "sp_id": sub_process.id,
            "disabled": True,
            "quarter": {"quarter": quarter.quarter, "year": quarter.quarter_year}
        }
        resp['data'] = data
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        raise PermissionDenied


@login_required
def delete_carouseldata(request, carousel_data_id):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        context = {}
        if request.method == "POST":
            try:
                carousel_update = SubProcessLevelUpdates.objects.get(id=carousel_data_id)
                sub_process = SubProcess.objects.get(id=int(request.POST.get('sub_process_id')))
                process_id = sub_process.process.id
                sub_process_url_name = sub_process.url_name
                carousel_update.delete()

                context = {
                        'process_id':process_id,
                        'sub_process_url_name':sub_process_url_name,
                        'success':True, 
                        'msg': 'Carousel data deleted successfully.'
                    }
            except Exception as e:
                context = {'success':False,'msg':'Something went wrong, please try after some time'}                    
            return HttpResponse(json.dumps(context), content_type="application/json")            
    else:
        raise PermissionDenied  


@login_required
def delete_addldata(request, additional_data_id):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        context = {}
        if request.method == "POST":
            try:
                addl_data = ProgramAdditionData.objects.get(id=additional_data_id)
                program_task = ProgramTask.objects.get(id=int(request.POST.get('program_task_id')))
                process_id = program_task.program_type.subprocess.process.id
                sub_process_url_name = program_task.program_type.subprocess.url_name
                addl_data.delete()

                context = {
                        'process_id':process_id,
                        'sub_process_url_name':sub_process_url_name,
                        'success':True, 
                        'msg': 'Additional data deleted successfully.'
                    }
            except Exception as e:
                context = {'success':False,'msg':'Something went wrong, please try after some time'}                    
            return HttpResponse(json.dumps(context), content_type="application/json")            
    else:
        raise PermissionDenied 


@login_required
def delete_taskdata(request, task_data_id):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        context = {}
        if request.method == "POST":
            try:
                task_data = TaskData.objects.get(id=task_data_id)
                program_task = ProgramTask.objects.get(id=int(request.POST.get('program_task_id')))
                process_id = program_task.program_type.subprocess.process.id
                sub_process_url_name = program_task.program_type.subprocess.url_name
                task_data.delete()

                context = {
                        'process_id':process_id,
                        'sub_process_url_name':sub_process_url_name,
                        'success':True, 
                        'msg': 'Additional data deleted successfully.'
                    }
            except Exception as e:
                context = {'success':False,'msg':'Something went wrong, please try after some time'}                    
            return HttpResponse(json.dumps(context), content_type="application/json")            
    else:
        raise PermissionDenied        


@require_http_methods(['POST'])
@login_required
@csrf_exempt
def clone_subprocess(request, process_id, sprocess_name):
    """
    Args:
        request: request object
        sprocess_name: subprocess URL
        process_id: Process ID

    Get sub process by ID, re create it with new PK.
    Take the new subprocess id and create program types and create columns an associate data to it.

    Returns: JSON response with parameters success/ message/ data

    """
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        sub_process = None
        try:
            process = Process.objects.get(id=process_id)
            sub_process = SubProcess.objects.get(url_name=sprocess_name, process=process)
        except ObjectDoesNotExist:
            resp = {"success": False, "msg": "There is no sub process with the given id"}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        subprocess_name = sub_process.name
        cloned_count = sub_process.cloned_count + 1
        sub_process.cloned_count = cloned_count
        sub_process.save()
        quarter = sub_process.quarter
        programs = ProgramType.objects.filter(subprocess=sub_process)
        updates = SubProcessLevelUpdates.objects.filter(subprocess=sub_process)

        # Creating new sub Process
        sub_process_url_name = sub_process.url_name + "-Copy"+ str(cloned_count)
        sub_process_name = subprocess_name + "-Copy" + str(cloned_count)
        sub_process = SubProcess()
        sub_process.process = process
        sub_process.quarter = quarter
        sub_process.name = sub_process_name
        sub_process.cloned_count = 0
        sub_process.is_disabled = True
        sub_process.url_name = sub_process_url_name
        sub_process.created_by = User.objects.get(email=request.user.email)
        sub_process.modified_by = User.objects.get(email=request.user.email)
        sub_process.save()

        # Creating programs
        for prog in programs:
            program_type = ProgramType()
            program_type.subprocess = sub_process
            program_type.name = prog.name
            program_type.is_disabled = False
            program_type.created_by = User.objects.get(email=request.user.email)
            program_type.modified_by = User.objects.get(email=request.user.email)
            program_type.save()

            # Creating program tasks
            ptask = ProgramTask.objects.filter(program_type=prog)
            for task in ptask:
                program_task = ProgramTask()
                program_task.program_type = program_type
                program_task.name = task.name
                program_task.is_disabled = False
                program_task.created_by = User.objects.get(email=request.user.email)
                program_task.modified_by = User.objects.get(email=request.user.email)
                program_task.save()

                # Creating Programming additional data, if exists.
                pad = ProgramAdditionData.objects.filter(program_task=task)
                for d in pad:
                    additional_data = ProgramAdditionData()
                    additional_data.program_task = program_task
                    additional_data.name = d.name
                    additional_data.data = d.data
                    additional_data.is_disabled = False
                    additional_data.created_by = User.objects.get(email=request.user.email)
                    additional_data.modified_by = User.objects.get(email=request.user.email)
                    additional_data.save()

                # Creating task data
                pvals = TaskData.objects.filter(program_task=task)
                for column in pvals:
                    task_data = TaskData()
                    task_data.program_task = program_task
                    task_data.column_name = column.column_name
                    task_data.column_number = column.column_number
                    task_data.data = column.data
                    task_data.is_disabled = False
                    task_data.created_by = User.objects.get(email=request.user.email)
                    task_data.modified_by = User.objects.get(email=request.user.email)
                    task_data.save()

        # Creating subprocess level updates
        for splu in updates:
            carousel_data = SubProcessLevelUpdates()
            carousel_data.subprocess = sub_process
            carousel_data.name = splu.name
            carousel_data.data = splu.data
            carousel_data.created_by = User.objects.get(email=request.user.email)
            carousel_data.modified_by = User.objects.get(email=request.user.email)
            carousel_data.save()

        resp = {"success": True, "msg": "Successfully cloned the sub process"}
        data = {
            "name": sub_process_name,
            "url_name": sub_process_url_name,
            "process_id": process_id,
            "sp_id": sub_process.id,
            "disabled": True,
            "quarter": {"quarter": quarter.quarter, "year": quarter.quarter_year}
        }
        resp['data'] = data
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        raise PermissionDenied


@require_http_methods(['POST'])
@login_required
@csrf_exempt
def delete_process_handler(request, process_id):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        try:
            deleted = delete_process(process_id)
            if deleted:
                resp = {"success": True, "msg": "Successfully deleted process"}
            else:
                resp = {"success": False, "msg": "No Process found with the given ID"}
        except:
            resp = {"success": False, "msg": "Something went wrong. Please try after sometime"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        raise PermissionDenied


@require_http_methods(['POST'])
@login_required
@csrf_exempt
def delete_subprocess_handler(request, process_id, sub_process_id):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        try:
            deleted = delete_sub_process(sub_process_id)
            if deleted:
                resp = {"success": True, "msg": "Successfully deleted sub process"}
            else:
                resp = {"success": False, "msg": "No Sub-process found with the given ID"}
        except:
            resp = {"success": False, "msg": "Something went wrong. Please try after sometime"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        raise PermissionDenied


@require_http_methods(['POST'])
@login_required
def delete_programs_handler(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        program_ids = request.POST.get('program_ids', None)
        if not program_ids:
            resp = {"success": False, "msg": "Invalid Parameters."}
        else:
            try:
                program_type = ProgramType.objects.get(id=program_ids)
                process_id = program_type.subprocess.process.id
                sub_process_url_name = program_type.subprocess.url_name
                delete_program_types([program_ids])
                resp = {"success": True, "msg": "Successfully deleted",
                        'process_id':process_id,
                        'sub_process_url_name':sub_process_url_name}
            except:
                resp = {"success": False, "msg": "Something went wrong. Please try after sometime"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        raise PermissionDenied


@require_http_methods(['POST'])
@login_required
def delete_tasks_handler(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        task_ids = request.POST.get('task_ids', None)
        if not task_ids:
            resp = {"success": False, "msg": "Invalid Parameters."}
        else:
            try:
                delete_program_tasks(task_ids)
                resp = {"success": True, "msg": "Successfully deleted"}
            except:
                resp = {"success": False, "msg": "Something went wrong. Please try after sometime"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        raise PermissionDenied


@require_http_methods(['POST'])
@login_required
def delete_taskdata_handler(request, task_data_id):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        try:
            delete_task_data(task_data_id)
            resp = {"success": True, "msg": "Successfully deleted"}
        except:
            resp = {"success": False, "msg": "Something went wrong. Please try after sometime"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        raise PermissionDenied


@require_http_methods(['POST'])
@login_required
def delete_additionaldata_handler(request, additional_data_id):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        try:
            delete_program_additional_data(additional_data_id)
            resp = {"success": True, "msg": "Successfully deleted"}
        except:
            resp = {"success": False, "msg": "Something went wrong. Please try after sometime"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        raise PermissionDenied


@require_http_methods(['POST'])
@login_required
def delete_subprocess_level_data(request, data_id):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        try:
    #Add a comment to this line
            delete_subprocess_level_data(data_id)
            resp = {"success": True, "msg": "Successfully deleted"}
        except:
            resp = {"success": False, "msg": "Something went wrong. Please try after sometime"}
        return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        raise PermissionDenied



@login_required
def faq_handler(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        program_type = ProgramType.objects.all().filter(is_disabled=False)
        # program_task = ProgramTask.objects.all().filter(is_disabled=False)
        context = RequestContext(request, {'request': request, 'user': request.user,'program_type':program_type, 'program_task':"Others"})
        return render(request, "manage_admin/create_faq.html", context_instance=context) 
    else:
        raise PermissionDenied


@login_required
def faq_creater(request):
    context = {}
    success = False
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
    
        if request.POST:
            faq_data = json.loads(request.POST.get("faqData"))
            try:
                faq = Faq()
                try:
                    program_type = ProgramType.objects.get(pk=int(faq_data.get('program_type_id')))
                    faq.program_type = program_type
                except Exception as e:
                    pass
                try:
                    task = ProgramTask.objects.get(pk=int(faq_data.get('program_task')))
                    faq.program_task = task
                except Exception as e:
                    pass

                faq.question = faq_data.get('question')
                faq.answer = faq_data.get('answer')
                faq.created_by = User.objects.get(email=request.user.email)
                faq.modified_by =  User.objects.get(email=request.user.email)
                faq.save()

                resp = {'success':True, 'msg':'saved'}
                return HttpResponse(json.dumps(resp), content_type="application/json")
            except Exception as ex:
                resp = {'success':False, 'msg':'not saved, server'}
                return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            context = RequestContext(request, {'request': request, 'user': request.user, 'success':True})
            return render(request, "manage_admin/create_faq.html", context_instance = context)
    else:
        raise PermissionDenied


@login_required
def faq_all(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        faq = Faq.objects.all()
        context = RequestContext(request, {'request': request, 'user': request.user,'faq':faq,})
        return render(request, "manage_admin/list_faq.html", context_instance=context) 
    else:
        raise PermissionDenied


@login_required
def faq_edit(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.is_ajax:
            key = request.GET.get('faq_key')
            program_type = ProgramType.objects.all().filter(is_disabled=False)
            program_type_list = list()
            
            for each in program_type:
                temp = {}
                temp['program_type'] = each.name
                temp['program_type_key'] = each.id
                program_type_list.append(temp)

            resp = {}
            try:
                faq = Faq.objects.get(pk=key)

                if faq.program_type is not None:
                    resp['program_type'] = faq.program_type.name
                    resp['program_type_id'] = faq.program_type.id 
                else:
                    resp['program_type']  = "others"
                    resp['program_type_id'] = None

                if faq.program_task is not None:
                        resp['program_task'] = faq.program_task.name
                        resp['program_task_id'] = faq.program_task.id 
                else:
                    resp['program_task']  = "others"
                    resp['program_task_id'] = None

                resp['question'] = faq.question
                resp['answer'] = faq.answer
                resp['success'] = True
                resp['msg'] = 'succesfuly edited'
                resp['program_type_all'] = program_type_list
                return HttpResponse(json.dumps(resp), content_type="application/json")
            except Exception as e:
                resp = {'success':False, 'msg':'Not edited, exception','program_type_all':program_type_list }
                return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            resp = {'success':False, 'msg':'faild to edit'}
            return HttpResponse(json.dumps(resp), content_type="application/json")
    else:
        raise PermissionDenied


@login_required
def faq_update(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == 'POST':
            faq_data = json.loads(request.POST.get("faqData"))
            try:
                faq = Faq.objects.get(pk=int(faq_data.get('program_answer_edit_id')))

                try:
                    program_type = ProgramType.objects.get(pk=int(faq_data.get('program_type_id'))) 
                except Exception as e:
                    program_type = None
                    pass
                try:
                    task = ProgramTask.objects.get(pk=int(faq_data.get('program_task_id')))
                except Exception as e:
                    task = None
                    pass

                faq.program_type = program_type
                faq.program_task = task
                faq.question = faq_data.get('question')
                faq.answer = faq_data.get('answer')
                faq.modified_by =  User.objects.get(email=request.user.email)
                faq.save()

                resp = {'success':True, 'msg':''}
                return HttpResponse(json.dumps(resp), content_type="application/json")
            except:
                resp = {'success':False, 'msg':'failed eception'}
                return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            resp = {'success':False, 'msg':'failed'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def faq_delete(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == 'GET':
            faq_data = json.loads(request.POST.get("faqData"))
            try:
                faq = Faq.objects.get(pk=int(faq_data.get('program_answer_edit_id')))

                try:
                    program_type = ProgramType.objects.get(pk=int(faq_data.get('program_type_id'))) 
                except Exception as e:
                    program_type = None
                    pass
                try:
                    task = ProgramTask.objects.get(pk=int(faq_data.get('program_task_id')))
                except Exception as e:
                    task = None
                    pass

                faq.program_type = program_type
                faq.program_task = task
                faq.question = faq_data.get('question')
                faq.answer = faq_data.get('answer')
                faq.modified_by =  User.objects.get(email=request.user.email)
                faq.save()

                resp = {'success':True, 'msg':''}
                return HttpResponse(json.dumps(resp), content_type="application/json")
            except:
                resp = {'success':False, 'msg':'failed eception'}
                return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            resp = {'success':False, 'msg':'failed'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def faq_delete(request):
       if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == 'GET':
            try:
                faq = Faq.objects.get(pk=int(request.GET.get('faq_id')))
                faq.delete()
                resp = {'success':True, 'msg':'Successfully deleted'}
                return HttpResponse(json.dumps(resp), content_type="application/json")
            except Exception as e:
                resp = {'success':False, 'msg':'failed Eception '}
                return HttpResponse(json.dumps(resp), content_type="application/json")
        else:
            resp = {'success':False, 'msg':'failed'}
            return HttpResponse(json.dumps(resp), content_type="application/json")

        
@login_required
def faq_home_view(request):
    is_manager = True if request.user.groups.filter(name='CHAPERONE-MANAGER') else False
    sub_processs = SubProcess.objects.filter(is_disabled=False)
    faq = Faq.objects.filter(program_type__isnull=False)
    program_type_ids = list()
    program_type_ids = [each.program_type.id for each in faq]
    # for each in faq:
    #     program_type_ids.append(each.program_type.id) 
    program_types = ProgramType.objects.filter(is_disabled=False, pk__in=program_type_ids)
    
    if Faq.objects.filter(program_type__isnull=True).count() > 0:
        context = RequestContext(request, {'sub_processs':sub_processs, 'program_types':program_types, 'others':True, 'is_manager':is_manager})
    else:
        context = RequestContext(request, {'sub_processs':sub_processs, 'program_types':program_types,'is_manager':is_manager})

    qf = QualityFramework.objects.all().count()
    if qf > 0:
        context['qf'] = True
    else:
        pass

    return render(request, "faq_home.html", context_instance=context) 


@login_required
def get_faq(request):
    if request.GET.get('task_id') != 'other':
        try:
            faq = Faq.objects.filter(program_task=int(request.GET.get('task_id')))
            faq = [{'q':each.question,'a':each.answer} for each in faq]
            return HttpResponse(json.dumps({'success':True, 'msg':'successfuly data fetched','faq':faq }), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'success':False, 'msg':'exception','faq':'no data'}), content_type="application/json")
    else:
        try:
            faq = Faq.objects.filter(program_task=None, program_type=None)
            faq = [{'q':each.question,'a':each.answer} for each in faq]
            return HttpResponse(json.dumps({'success':True, 'msg':'successfuly data fetched','faq':faq }), content_type="application/json")
        except:
            return HttpResponse(json.dumps({'success':False, 'msg':'exception','faq':'no data'}), content_type="application/json")


@login_required
def qf_home(request):
    is_manager = True if request.user.groups.filter(name='CHAPERONE-MANAGER') else False
    sub_processs = SubProcess.objects.filter(is_disabled=False)
    qualityframeworks = QualityFramework.objects.all()
    
    if Faq.objects.filter(program_type__isnull=True).count() > 0:
        context = RequestContext(request, {'sub_processs':sub_processs, 'qualityframeworks':qualityframeworks, 'others':True, 'is_manager':is_manager})
    else:
        context = RequestContext(request, {'sub_processs':sub_processs, 'qualityframeworks':qualityframeworks,'is_manager':is_manager})

    return render(request, "qf_home.html", context_instance=context) 

@login_required
def qualityframework_handler(request):
    context = {}
    success = False
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.POST:
            qualityframework_data = json.loads(request.POST.get("qfData"))
           
            qf = QualityFramework()
                    
            qf.name = qualityframework_data.get("name")
            qf.data = qualityframework_data.get("data")
            qf.created_by = User.objects.get(email=request.user.email)
            qf.modified_by =  User.objects.get(email=request.user.email)

            qf.save()
            context = {'success':True, 'msg':'QualityFramework created successfully'}
            return HttpResponse(json.dumps(context), content_type="application/json")       
        else:
            context = RequestContext(request, {'request': request, 'user': request.user, 'success':True})
            return render(request, "manage_admin/create_qualityframework.html", context_instance = context) 
    else:
        raise PermissionDenied


@login_required
@csrf_exempt
def get_qualityframework_name(request):
    context = {}
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.POST:
            try:
                process = QualityFramework.objects.get(name=request.POST.get('name'))
                context['msg'] = "QualityFramework with the name already exists"
            except QualityFramework.DoesNotExist:
                context['msg'] = ''
            return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        raise PermissionDenied


@login_required
def get_qualityframework(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        qualityframeworks = QualityFramework.objects.all()
        context = RequestContext(request, {'request': request, 'user': request.user,'qualityframeworks':qualityframeworks})
        return render(request, "manage_admin/qualityframeworks.html", context_instance = context) 
    else:
        raise PermissionDenied


@login_required
def delete_qualityframework(request, qf_id):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        context = {}
        if request.method == "GET":
            try:
                qf_data = QualityFramework.objects.get(id=qf_id)
                qf_data.delete()

                context = {'success':True, 'msg': 'Quality Framework deleted successfully.'}
            except Exception as e:
                context = {'success':False,'msg':'Something went wrong, please try after some time'}                    
            return HttpResponse(json.dumps(context), content_type="application/json")            
    else:
        raise PermissionDenied


@login_required
def get_qf_data(request, qf_id):
    qf_data = QualityFramework.objects.get(id=qf_id)
    qfdata = {
        'name':qf_data.name,
        'data':qf_data.data,
        'id':qf_data.id,
    }
    return HttpResponse(json.dumps({"data":qfdata, "success":True, "msg":""}), content_type="application/json")    

@login_required
def qf_update(request):
    context = {}
    success = False
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.POST:
            qualityframework_data = json.loads(request.POST.get("qfData"))
            
            qf_id = request.POST.get('qf_id')
            qf = QualityFramework.objects.get(id=qf_id)

            qf.name = qualityframework_data.get("name")
            qf.data = qualityframework_data.get("data")
            qf.created_by = User.objects.get(email=request.user.email)
            qf.modified_by =  User.objects.get(email=request.user.email)

            qf.save()
            context = {'success':True, 'msg':'QualityFramework updated successfully'}
            return HttpResponse(json.dumps(context), content_type="application/json")       
        else:
            context = RequestContext(request, {'request': request, 'user': request.user, 'success':True})
            return render(request, "manage_admin/create_qualityframework.html", context_instance = context) 
    else:
        raise PermissionDenied