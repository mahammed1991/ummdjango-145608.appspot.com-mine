from django.shortcuts import render, HttpResponse
from .models import ExtraTask, Quarter, Category, Task, AdditionData, ColumnData, ComboUpdate, BudgetBand, Goal, GoalTaskMap, Question
import json
from django.core import serializers


# view for Advertiser Goals

def home(request):
    goal_map = GoalTaskMap.objects.all()
    return render(request, "index.html", {'goal_map': goal_map})


def tasks(request):
    task_name = request.GET['data']
    goal = Goal.objects.filter(goal_name=task_name)
    goal_map = None
    extra_tasks = None
    questions = None
    result = {}
    goal_map_json = []
    addition_task_list = []
    questions_list = []
    if goal:
        goal_map = GoalTaskMap.objects.filter(parent_goal_id=goal[0])
        extra_tasks = ExtraTask.objects.filter(parent_goal_id=goal[0])
        questions = Question.objects.filter(parent_goal_id=goal[0])

    if goal_map:
        task_names = goal_map[0].parent_task_id.values()
    else:
        task_names = None
    if task_names is not None:
        for item in task_names:
            goal_map_json.append(item['task_name'])
            result['goals'] = goal_map_json
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

def home1(request):
    template = "home.html"
    quarters = Quarter.objects.filter(is_active=True)
    for q in quarters:
        a = q.id
    categorys = Category.objects.filter(parent_quarter_id=a, is_disable=False)
    tasks = Task.objects.filter(parent_category_id=categorys[0], is_disable=False)
    lefttab = ColumnData.objects.filter(parent_task_id=tasks[0], is_disable=False)
    righttab = AdditionData.objects.filter(parent_task_id=tasks[0], is_disable=False)
    return render(request, template, {'tasks': tasks, 'lefttab': lefttab, 'righttab': righttab, 'categorys': categorys, 'quarters':quarters})


def task_list(request, cat_id):
    tasks = Task.objects.filter(parent_category_id_id=cat_id, is_disable=False)
    data = serializers.serialize('json', tasks)
    response = HttpResponse(data, content_type='application/json')
    return response


def combo_data(request):
    quarters = Quarter.objects.filter(is_active=True)
    for q in quarters:
        a = q.id
    combodata = ComboUpdate.objects.filter(parent_quarter_id_id=a)
    data = serializers.serialize('json', combodata)
    response = HttpResponse(data, content_type='application/json')
    return response


def left_column_list(request, task_id):
    column_listing_left = ColumnData.objects.filter(parent_task_id_id=task_id, is_disable=False)
    data = serializers.serialize('json', column_listing_left)
    response = HttpResponse(data, content_type='application/json')
    return response


def right_column_list(request, task_id):
    column_listing_right = AdditionData.objects.filter(parent_task_id_id=task_id, is_disable=False)
    data = serializers.serialize('json', column_listing_right)
    response = HttpResponse(data, content_type='application/json')
    return response


def elevator_pitch_data(request, task_id):
    elevator_pitch_data = AdditionData.objects.filter(parent_task_id_id=task_id, is_disable=False)
    data = serializers.serialize('json', elevator_pitch_data)
    response = HttpResponse(data, content_type='application/json')
    return response








def budget_band(request):
    quarters = Quarter.objects.filter(is_active=True)
    for q in quarters:
        a = q.id
    budgetbanddetail = BudgetBand.objects.filter(parent_quarter_id_id=a)
    data = serializers.serialize('json', budgetbanddetail)
    response = HttpResponse(data, content_type='application/json')
    return response
