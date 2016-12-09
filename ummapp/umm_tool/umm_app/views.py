from django.shortcuts import render, HttpResponse, redirect
from .models import ExtraTask, Quarter, Category, Task, AdditionData, ColumnData, ComboUpdate, BudgetBand, Goal, GoalTaskMap, Question, Process
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.conf import settings
import json
import datetime
from datetime import date
from .forms import ProcessForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms.models import model_to_dict
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
        return render(request, "apollo-index.html", context_instance=context)

    
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
    return render(request, "manage_admin/admin-home.html", context_instance = context) 


@login_required
def create_process(request):
    context = {}
    success = False
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == 'POST':
            print request.POST,'post'
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
                success = True
                messages.success(request, 'Process created successfully')
            print form.data
            context = RequestContext(request, {'request': request, 'user': request.user, 'form':form, 'success':success})
        else:
            form = ProcessForm()
            context = RequestContext(request, {'request': request, 'user': request.user,'form':form,'success':success})
    return render(request, "manage_admin/create-process.html", context_instance = context)  


@login_required
def view_process(request):
    print request,request.user.groups.filter(name='CHAPERONE-MANAGER')
    context = {}
    if request.user.groups.filter(name='CHAPERONE-MANAGER'):
        if request.method == 'GET':
            processes = Process.objects.all()
            print processes,'processes'
            context = RequestContext(request, {'request': request, 'user': request.user,'processes':processes, 'update':False})
    return render(request, "manage_admin/view-process.html", context_instance = context)   


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
            #import pdb
            #pdb.set_trace()
            context = RequestContext(request, {'request': request, 'user': request.user,'form':form, 'update':update})
    
    return render(request, "manage_admin/view-process.html", context_instance = context) 

