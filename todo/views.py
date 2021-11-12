import datetime
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import (Task)
from django.db.models.functions import TruncMonth
from django.db.models import Count



# Create your views here.
def index(request):
    print('hjh')
    if request.user.is_anonymous:
        user = authenticate(username = 'sumit', password = 'subedi')
        login(request, user)
    else:
        user = request.user
    tasks = Task.objects.filter(user = user, date = datetime.date.today()).order_by('-id')

    context = {
        'tasks' : tasks
    }
    print(context)
    return render(request, 'home.html', context)

def dailyTasks(request, pk):
    
    if request.user.is_anonymous:
        user = authenticate(username = 'sumit', password = 'subedi')
    else:
        user = request.user
    
    if request.method == 'POST':
       
        date = request.POST['date']
        time = request.POST['time']
        task = request.POST['task']
        taskObj = Task(user = user, date = date, time = time, task = task)
        taskObj.save()
    
    if request.method == 'DELETE':      
        Task.objects.get(id = pk).delete()

    tasks = Task.objects.filter(user = user, date = datetime.date.today()).order_by('-id')

    return render(request, 'partials/tasklist.html', {'tasks':tasks})

def history(request):
    if request.method == 'POST':
        date = request.POST['month']
        
        fromdate = date+'-1'
        year, month = date.split('-')
        todate = year + "-" + str(int(month)+1) +"-1" 
        
        dates = Task.objects.filter(user = request.user, date__gt = fromdate, date__lt = todate).annotate(month=TruncMonth('date')).values('date').annotate(c=Count('id'))
        context = {
            'dates':dates
        }
        print(dates)
        return render(request, 'partials/historydates.html', context)

    return render(request, 'history.html')

def historySearch(request, pk):
    
    tasks = Task.objects.filter(user = request.user, date = pk)

    context = {
        'date': pk,
        'tasks' : tasks
    }

    return render (request, 'partials/historydetail.html', context)

def historyCompress(request, pk):
    date = Task.objects.filter(user = request.user,date = pk).annotate(month=TruncMonth('date')).values('date').annotate(c=Count('id'))
    context = {
        'date':date[0]
        }
    print(date[0])
    return render (request, 'partials/datelist.html', context)