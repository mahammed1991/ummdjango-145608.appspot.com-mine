from django.shortcuts import render, HttpResponse, redirect
from .models import ExtraTask, Quarter, Category, Task, AdditionData, ColumnData, ComboUpdate, BudgetBand, Goal, GoalTaskMap, Question, Process, SubProcess, ProgramType, ProgramTask, TaskData
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
        context = RequestContext(request, {'request': request, 'user': request.user,'goal_map': goal_map, 'quarter':quarter_id, 'is_manager':is_manager})
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
def apollo_home(request):
    quarter = None
    template = "apollo-home.html"
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
def manage_admin(request):
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        context = RequestContext(request, {'request': request, 'user': request.user})
    return render(request, "manage_admin/umm_admin.html", context_instance = context) 


@login_required
def create_process(request):
    context = {}
    success = False
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == 'POST':
            form = ProcessForm(request.POST)
            if form.is_valid():
                process = form.save(commit=False)
                print request.POST,form.cleaned_data
                if request.FILES:
                    img_file = request.FILES['image_ref']
                    process.image_ref = img_file

                if 'is_disabled' in form.cleaned_data:
                    print form.cleaned_data['is_disabled'],'is_disabled'
                    process.is_disabled = form.cleaned_data['is_disabled']
                process.url_name = form.cleaned_data['name'].lower().replace(' ','-')
                process.created_by = User.objects.get(email=request.user.email)
                process.modified_by =  User.objects.get(email=request.user.email)
                process.save()
                form = ProcessForm()
                success = True
                messages.success(request, 'Process created successfully')
            print form.data,'form.data'
            #import pdb
            #pdb.set_trace()
            context = RequestContext(request, {'request': request, 'user': request.user, 'form':form, 'success':success})
        else:
            form = ProcessForm()
            context = RequestContext(request, {'request': request, 'user': request.user,'form':form,'success':success})
    print context,'context'
    return render(request, "manage_admin/create_process.html", context_instance = context)  


@login_required
def view_process(request):
    print request,request.user.groups.filter(name='CHAPERONE-MANAGER')
    context = {}
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == 'GET':
            processes = Process.objects.all()
            print processes,'processes'
            context = RequestContext(request, {'request': request, 'user': request.user,'processes':processes, 'update':False})
    return render(request, "manage_admin/view_process.html", context_instance = context)   


@login_required
def update_process(request,pk):
    print request,request.user.groups.filter(name='CHAPERONE-MANAGER')
    context = {}
    success = False
    update = True
    process = Process.objects.get(id=pk)
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == 'POST':
            print request.POST,'post'
            process = Process.objects.get(id=pk)
            form = ProcessForm(request.POST, instance=process)
            if form.is_valid():
                #process = form.save(commit=False)
                print request.POST,form.cleaned_data
                if request.FILES:
                    img_file = request.FILES['image_ref']
                    process.image_ref = img_file

                if 'is_disabled' in form.cleaned_data:
                    print form.cleaned_data['is_disabled'],'is_disabled'
                    process.is_disabled = form.cleaned_data['is_disabled']
                process.name = form.cleaned_data['name']
                process.url_name = form.cleaned_data['name'].lower().replace(' ','-')
                process.created_by = User.objects.get(email=request.user.email)
                process.modified_by =  User.objects.get(email=request.user.email)
                process.save()
                success = True
                messages.success(request, 'Process updated successfully')
                context = RequestContext(request, {'request': request, 'user': request.user,'form':form, 'update':False})
                return redirect('view_process')
            else:
                context = RequestContext(request, {'request': request, 'user': request.user,'form':form, 'update':True})
        else:
            print process,'process'
            form = ProcessForm(instance=process)
            context = RequestContext(request, {'request': request, 'user': request.user,'form':form, 'update':update})
    
    return render(request, "manage_admin/view_process.html", context_instance = context) 


@login_required
def create_program_type(request):
    context = {}
    success = False
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        processes = [(int(process.id), process.name) for process in  Process.objects.all()]
        quarters = [(int(q.id), str(q.quarter) + '-' + str(q.quarter_year)) for q in  Quarter.objects.all()]
        if request.method == 'POST':
            form = ProgramTypeForm(request.POST)
            print form.data,'form.data',form.is_valid(),form.errors
            if form.is_valid():
                program_type = form.save(commit=False)
                print request.POST,form.cleaned_data
                if 'process' in form.cleaned_data:
                    print form.cleaned_data['process'],'process'
                    import pdb
                    pdb.set_trace()
                    #process = Process.objects.get(id=int(form.cleaned_data['process']))
                    program_type.process = form.cleaned_data['process']
                if 'quarter' in form.cleaned_data:
                    print form.cleaned_data['quarter'],'quarter'
                    #quarter = Quarter.objects.get(id=int(form.cleaned_data['quarter']))
                    program_type.quarter = form.cleaned_data['quarter']
                if 'is_disabled' in form.cleaned_data:
                    print form.cleaned_data['is_disabled'],'is_disabled'
                    program_type.is_disabled = form.cleaned_data['is_disabled']
                program_type.name = form.cleaned_data['name']
                program_type.created_by = User.objects.get(email=request.user.email)
                program_type.modified_by =  User.objects.get(email=request.user.email)
                program_type.save()
                form = ProgramTypeForm()
                success = True
                messages.success(request, 'Process Type created successfully')
            print form.data,'form.data'
            #context = RequestContext(request, {'request': request, 'user': request.user, 'form':form, 'success':success})
        else:
            form = ProgramTypeForm()
            #processes = [(int(process.id), process.name) for process in  Process.objects.all()]
            #quarters = [(int(q.id), str(q.quarter) + '-' + str(q.quarter_year)) for q in  Quarter.objects.all()]
            print quarters
        print form.data
        #import pdb
        #pdb.set_trace()
        context = RequestContext(request, {'request': request, 'user': request.user,'form':form,'success':success, 'processes':processes,'quarters':quarters})
    return render(request, "manage_admin/program_type.html", context_instance = context)


def view_program_type(request):
    print request,request.user.groups.filter(name='CHAPERONE-MANAGER')
    context = {}
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == 'GET':
            process_types = ProgramType.objects.all()
            print process_types,'process_types'
            context = RequestContext(request, {'request': request, 'user': request.user,'process_types':process_types, 'update':False})
    return render(request, "manage_admin/view_process_types.html", context_instance = context)   


@login_required
def update_program_type(request,pk):
    print request,request.user.groups.filter(name='CHAPERONE-MANAGER')
    context = {}
    success = False
    update = True
    program_type = ProgramType.objects.get(id=pk)
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        processes = [(int(process.id), process.name) for process in  Process.objects.all()]
        quarters = [(int(q.id), str(q.quarter) + '-' + str(q.quarter_year)) for q in  Quarter.objects.all()]
        if request.method == 'POST':
            print request.POST,'post'
            process_type = ProgramType.objects.get(id=pk)
            form = ProgramTypeForm(request.POST, instance=program_type)
            if form.is_valid():
                #process = form.save(commit=False)
                print request.POST,form.cleaned_data
                if 'is_disabled' in form.cleaned_data:
                    print form.cleaned_data['is_disabled'],'is_disabled'
                    process_type.is_disabled = form.cleaned_data['is_disabled']
                process_type.process = form.cleaned_data['process']
                process_type.quarter = form.cleaned_data['quarter']
                process_type.name = form.cleaned_data['name']
                process_type.created_by = User.objects.get(email=request.user.email)
                process_type.modified_by =  User.objects.get(email=request.user.email)
                process_type.save()
                success = True
                messages.success(request, 'Process Type updated successfully')
                context = RequestContext(request, {'request': request, 'user': request.user,'form':form, 'update':False, 'processes':processes,'quarters':quarters})
                return redirect('view_program_type')
            else:
                context = RequestContext(request, {'request': request, 'user': request.user,'form':form, 'update':True, 'processes':processes,'quarters':quarters})
        else:
            form = ProgramTypeForm(instance=program_type)
            context = RequestContext(request, {'request': request, 'user': request.user,'form':form, 'update':update, 'processes':processes,'quarters':quarters})
    
    return render(request, "manage_admin/view_process_types.html", context_instance = context) 


@login_required
def create_task_data(request):
    context = {}
    success = False
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        program_tasks = [(int(process.id), process.name) for process in  ProgramType.objects.all()]
        if request.method == 'POST':
            form = TaskDataForm(request.POST)
            if form.is_valid():
                process = form.save(commit=False)
                print request.POST,form.cleaned_data
                if 'is_disabled' in form.cleaned_data:
                    print form.cleaned_data['is_disabled'],'is_disabled'
                    process.is_disabled = form.cleaned_data['is_disabled']
                process.url_name = form.cleaned_data['name'].lower().replace(' ','-')
                process.created_by = User.objects.get(email=request.user.email)
                process.modified_by =  User.objects.get(email=request.user.email)
                process.save()
                form = TaskDataForm()
                success = True
                messages.success(request, 'Process created successfully')
            print form.data,'form.data'
            context = RequestContext(request, {'request': request, 'user': request.user, 'form':form, 'success':success})
        else:
            form = TaskDataForm()
            context = RequestContext(request, {'request': request, 'user': request.user,'form':form,'success':success})
    return render(request, "manage_admin/task_data.html", context_instance = context) 


@login_required
def create_program_task(request):
    context = {}
    success = False
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        program_types = [(int(process.id), process.name) for process in  ProgramType.objects.all()]
        if request.method == 'POST':
            form = ProgramTaskForm(request.POST)
            print form.is_valid()
            if form.is_valid():
                program_task = form.save(commit=False)
                print request.POST,form.cleaned_data
                if 'is_disabled' in form.cleaned_data:
                    print form.cleaned_data['is_disabled'],'is_disabled'
                    program_task.is_disabled = form.cleaned_data['is_disabled']
                program_task.program_type = form.cleaned_data['program_type']
                program_task.name = form.cleaned_data['name']
                program_task.created_by = User.objects.get(email=request.user.email)
                program_task.modified_by =  User.objects.get(email=request.user.email)
                program_task.save()
                form = ProgramTaskForm()
                success = True
                messages.success(request, 'Program Task created successfully')
            print form.data,'form.data'
            context = RequestContext(request, {'request': request, 'user': request.user, 'form':form, 'success':success, 'program_types':program_types})
        else:
            form = ProgramTaskForm()
            context = RequestContext(request, {'request': request, 'user': request.user,'form':form,'success':success, 'program_types':program_types})
    return render(request, "manage_admin/program_task.html", context_instance = context)  


def view_program_task(request):
    print request,request.user.groups.filter(name='CHAPERONE-MANAGER')
    context = {}
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == 'GET':
            program_tasks = ProgramTask.objects.all()
            print program_tasks,'program_tasks'
            context = RequestContext(request, {'request': request, 'user': request.user,'program_tasks':program_tasks, 'update':False})
    return render(request, "manage_admin/view_program_tasks.html", context_instance = context)   


@login_required
def update_program_task(request,pk):
    print request,request.user.groups.filter(name='CHAPERONE-MANAGER')
    context = {}
    success = False
    update = True
    program_task = ProgramTask.objects.get(id=pk)
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        program_types = [(int(process.id), process.name) for process in  ProgramType.objects.all()]
        if request.method == 'POST':
            print request.POST,'post'
            form = ProgramTaskForm(request.POST, instance=program_task)
            if form.is_valid():
                print request.POST,form.cleaned_data
                if 'is_disabled' in form.cleaned_data:
                    print form.cleaned_data['is_disabled'],'is_disabled'
                    program_task.is_disabled = form.cleaned_data['is_disabled']
                program_task.program_type = form.cleaned_data['program_type']
                program_task.name = form.cleaned_data['name']
                program_task.created_by = User.objects.get(email=request.user.email)
                program_task.modified_by =  User.objects.get(email=request.user.email)
                program_task.save()
                success = True
                messages.success(request, 'Program Task updated successfully')
                context = RequestContext(request, {'request': request, 'user': request.user,'form':form, 'update':False, 'program_types':program_types})
                return redirect('view_program_task')
            else:
                context = RequestContext(request, {'request': request, 'user': request.user,'form':form, 'update':True, 'program_types':program_types})
        else:
            form = ProgramTaskForm(instance=program_task)
            context = RequestContext(request, {'request': request, 'user': request.user,'form':form, 'update':update, 'program_types':program_types})
    
    return render(request, "manage_admin/view_program_tasks.html", context_instance = context)

@login_required
def create(request):
    context = {}
    success = False
    #import pdb
    #pdb.set_trace()
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.POST:
            form = ProcessForm(request.POST)
            print request.POST
            try:
                quarter = Quarter.objects.get(quarter=request.POST.get('quarter'),quarter_year=request.POST.get('quarter_year'))
            except Quarter.DoesNotExist:
                quarter = Quarter()
                quarter.quarter = request.POST.get('quarter')
                quarter.quarter_year = request.POST.get('quarter_year')
                quarter.save()
            
            """
            sub_process_form = SubProcessForm({'name':request.POST.get('sub-process-name'), 'quarter':quarter})
            print sub_process_form.data,'sub form data',form.is_valid() and sub_process_form.is_valid()
            """
            program_type_name = [l for l in request.POST.keys() if l.startswith("program_type_")]
            program_task_name = [l for l in request.POST.keys() if l.startswith("program_task_")]

            """
            program_type_name = request.POST.getlist('program-type-name')
            program_task_name = request.POST.getlist('program-task-name')
            
            program_type_forms = ProgramTypeForm()
            program_task_forms = ProgramTaskForm()
            print program_type_name,'program_type_name'
            if program_type_name:
                program_type_forms = [ProgramTypeForm({'name':name}) for indx,name in enumerate(program_type_name)]
            #else:
            #    program_type_forms = ProgramTypeForm()
            program_task_name_multiple = []
            if program_task_name:
                for p in program_task_name:
                    if ',' in p:
                        program_task_name_multiple += p.strip().split(',') 
                    else:
                        program_task_name_multiple.append(p)
                program_task_forms = [ProgramTaskForm({'name':name}) for indx,name in enumerate(program_task_name_multiple)]
            #else:
            #    program_task_forms = ProgramTaskForm()

            #import pdb
            #pdb.set_trace()
            print program_type_forms,'program_type_forms'
            print program_task_forms,'program_task_forms'
            program_type_is_valid = all([ty.is_valid() for ty in program_type_forms])
            program_task_is_valid = all([ta.is_valid() for ta in program_task_forms])
            
            print form.is_valid(),'form'
            print sub_process_form.is_valid(),'sub process'
            print program_type_is_valid,'program_type_is_valid'
            print program_task_is_valid,'program_task_is_valid'
            """
            program_type_forms = ProgramTypeForm()
            program_task_forms = ProgramTaskForm()
            program_type_errors = []
            program_task_errors = []
            program_task_is_valid = True
            program_type_is_valid = True
            if form.is_valid():# and sub_process_form.is_valid() and program_type_is_valid and program_task_is_valid:
                print form,'form'
                process_e = Process.objects.filter(name=form.cleaned_data['name'])
                print process_e,'process_e'
                process = form.save(commit=False)
                print request.POST,form.cleaned_data
                if request.FILES:
                    img_file = request.FILES['image_ref']
                    process.image_ref = img_file

                if 'is_disabled' in form.cleaned_data:
                    print form.cleaned_data['is_disabled'],'is_disabled'
                    process.is_disabled = form.cleaned_data['is_disabled']
                process.url_name = form.cleaned_data['name'].lower().replace(' ','-')
                process.created_by = User.objects.get(email=request.user.email)
                process.modified_by =  User.objects.get(email=request.user.email)
                process.save()
                print process.id,'process.id'

                process_id = Process.objects.get(id=process.id)
                sub_process_form = SubProcessForm({'name':request.POST.get('sub_process_name'), 'quarter':quarter.id, 'process':process.id})
                print sub_process_form.data,'sub form data',form.is_valid() and sub_process_form.is_valid()
                if sub_process_form.is_valid():
                    sub_process = sub_process_form.save(commit=False)
                    #sub_process.process = process_id
                    #sub_process.quarter = quarter
                    #sub_process.name = sub_process_form.cleaned_data['name']
                    sub_process.url_name = sub_process_form.cleaned_data['name'].lower().replace(' ','-')
                    sub_process.created_by = User.objects.get(email=request.user.email)
                    sub_process.modified_by =  User.objects.get(email=request.user.email)
                    sub_process.save()

                    print sub_process.id,'sub_process_id'

                    sub_process_id = SubProcess.objects.get(id=sub_process.id)
                    program_type_forms = ProgramTypeForm()
                    program_task_forms = ProgramTaskForm()
                    print program_type_name,'program_type_name'
                    if program_type_name:
                        program_type_forms = [ProgramTypeForm({'name':name, 'subprocess':sub_process.id}) for indx,name in enumerate(program_type_name)]
                    #else:
                    #    program_type_forms = ProgramTypeForm()
                    program_type_is_valid = all([ty.is_valid() for ty in program_type_forms])
                    program_type_errors = [{str(ty.data['name']):ty.errors} for ty in program_type_forms if not ty.is_valid()]
                    if program_type_is_valid:

                        for ptype,index in enumerate(program_type_forms):
                            print ptype,index,'ptype,index'
                            program_type = ptype.save(commit=False)
                            #program_type.subprocess = SubProcess.objects.get(id=sub_process.id)
                            #program_type.name = ptype.cleaned_data['name']
                            program_type.created_by = User.objects.get(email=request.user.email)
                            program_type.modified_by =  User.objects.get(email=request.user.email)
                            program_type.save()

                            print program_type.id,'program_type'

                            program_task_name_multiple = []
                            if program_task_name:
                                for p in program_task_name[index]:
                                    if ',' in p:
                                        program_task_name_multiple += p.strip().split(',') 
                                    else:
                                        program_task_name_multiple.append(p)
                                program_type_id = ProcessType.objects.get(id=program_type_id)
                                print program_task_name_multiple,'program_task_name_multiple'
                                program_task_forms = [ProgramTaskForm({'name':name, 'program_type':program_type.id}) for indx,name in enumerate(program_task_name_multiple)]
                                program_task_is_valid = all([ta.is_valid() for ta in program_task_forms])
                                program_task_errors = [{str(ta.data['name']):ta.errors} for ta in program_task_forms if not ta.is_valid()]
                                if program_task_is_valid:
                                    program_task = ProgramTask()
                                    #program_task.program_type = program_type_id
                                    for task in ptask.strip().split(','):
                                        program_task.name = task
                                        program_task.created_by = User.objects.get(email=request.user.email)
                                        program_task.modified_by =  User.objects.get(email=request.user.email)
                                        program_task.save()
                                        print program_task.id,'program_task'
                                    #else:
                                    #    program_task.name = ptask
                                    #program_task.created_by = User.objects.get(email=request.user.email)
                                    #program_task.modified_by =  User.objects.get(email=request.user.email)
                                    #program_task.save()

                                        print program_task.id,'program_task'
                #form = ProcessForm()
                #sub_process = SubProcessForm()
                #success = True
                #messages.success(request, 'Process created successfully')
                #print form.data,'form.data'
                #import pdb
                #pdb.set_trace()
                #context = RequestContext(request, {'request': request, 'user': request.user, 'form':form, 'success':success, 'sub_process_form':sub_process_form})
            #else:
            #import pdb
            #pdb.set_trace()
            #import pdb
            #pdb.set_trace()
            #form_name['field_name'].value()
            #[error.keys()[0] for error in program_type_errors]
            print program_type_errors,'program_type_errors'
            print program_task_errors,'program_task_errors'
                #import pdb
                #pdb.set_trace()                
            context =  {'form':form.errors, 'success':success, 'sub_process_form':sub_process_form.errors, 'error':True, 'program_type_errors':program_type_errors,'program_task_errors':program_task_errors}
            #context.update(form.cleaned_data)
            #context.update(sub_process_form.cleaned_data)
            import pdb
            pdb.set_trace()
            #res = serializers.serialize('json',context)
            return HttpResponse(json.dumps(context), content_type="application/json")
        else:
            form = ProcessForm()
            sub_process_form = SubProcessForm()
            print form.errors,sub_process_form.errors
            context = RequestContext(request, {'request': request, 'user': request.user,'form':form,'success':success, 'sub_process_form':sub_process_form})
    #import pdb
    #pdb.set_trace()
    print context,'context'
    """
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        form = ProcessForm(request.POST)
        context = RequestContext(request, {'request': request, 'user': request.user, 'form':form})
    """
    return render(request, "manage_admin/create_page.html", context_instance = context) 


@login_required
@csrf_exempt
def get_process(request):
    context = {}
    print request.POST.get('name'),'request.POST.get'
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.POST:
            try:
                process = Process.objects.get(name=request.POST.get('name'))
                context['process_error'] = "Process with the name already exists"
            except Process.DoesNotExist:
                context['process_error'] = ''
    return HttpResponse(json.dumps(context), content_type="application/json")