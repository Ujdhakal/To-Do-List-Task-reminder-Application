"""Business logic of the application."""
from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from tasks.models import Task
# Create your views here.

def project_homepage(request):
    """The Default homepage of application."""
    all_task = Task.objects.all().order_by('-date')
    page = request.GET.get('page', 1)

    paginator = Paginator(all_task, 10)
    try:
        tasklist = paginator.page(page)
    except PageNotAnInteger:
        tasklist = paginator.page(1)
    except EmptyPage:
        tasklist = paginator.page(paginator.num_pages)

    return render(request, 'apphome.html', { 'tasklist': tasklist })

def edit_task(request, task_id):
    """Return Specific task id details."""
    task = Task.objects.get(id=task_id)
    if request.method == "POST":
        new_title = request.POST.get('title')
        new_date = request.POST.get('date')
        task.title, task.date = new_title, new_date
        task.save()
        task = Task.objects.get(id=task_id)
    tdate = f"{task.date.year}-{task.date.month}-{task.date.day}"
    print(tdate)
    return render(request, 'edit_task.html', {'task':task, 'day':tdate})

@api_view(['POST'])
def create_task(request):
    """This function saves the task."""
    if request.method == "POST":
        title = request.POST.get('title').strip()
        date = request.POST.get('date')
        Task.objects.create(title=title, date=date)
    return redirect('/')

def today_task(request):
    """This functions shows the tasks for the day."""
    task_list = Task.objects.filter(date=date.today())
    return render(request, 'todaytask.html',{'tasklist':task_list})

def update_task(request, task_id):
    """This function removes the existing task."""
    task = Task.objects.get(id=task_id)
    task.done = False if task.done else True
    task.save()
    return redirect('/')
