import datetime
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import (Task, Remainder)
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.contrib import messages
from django.utils import timezone
from django.http import QueryDict

from allauth.account.views import LoginView
# Create your views here.
def index(request):
    if request.user.is_anonymous:
        user = authenticate(username = 'sumit', password = 'subedi')
        login(request, user)
    else:
        user = request.user
    tasks = Task.objects.filter(user = user, date = datetime.date.today()).order_by('-id')

    context = {
        'tasks' : tasks
    }
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
        
        messages.success(request, 'Task Added Successfully!')
    
    if request.method == 'DELETE':      
        Task.objects.get(id = pk).delete()
        messages.warning(request, "Successfully Deleted.")

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
    return render (request, 'partials/datelist.html', context)

def CustomLoginView(request):
    return render(request, 'login.html')

def RemainderView(request):
    
    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']
        mail = request.POST['email']
        re_date = request.POST['re_date']
        re_time = request.POST['re_time']
        text = request.POST['text']
        
        dateobj = timezone.make_aware(datetime.datetime.strptime(date+time, '%Y-%m-%d%H:%M:%S'))
        
        diff = timezone.now() - dateobj
        
        re_dateobj = timezone.make_aware(datetime.datetime.strptime(re_date+re_time, '%Y-%m-%d%H:%M'))

        obj = Remainder(user = request.user, added = dateobj, time = re_dateobj+diff, text = text, mail = mail)
        obj.save()
    
    if request.method == 'DELETE':
        # print(str(request.body), request.body)
        id = QueryDict(request.body).get('id')
        Remainder.objects.get(id = id).delete()

        
    remainders = Remainder.objects.filter(user = request.user, sent = False)
    return render(request, 'remainder.html', {'remainders':remainders})


def logoutuser(request):
    logout(request)
    return redirect('login')