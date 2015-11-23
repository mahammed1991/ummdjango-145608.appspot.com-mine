from django.shortcuts import render, HttpResponse
from .models import ExtraTask, Quarter, Category, Task, AdditionData, ColumnData, ComboUpdate, BudgetBand, Goal, GoalTaskMap, Question
import json


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
