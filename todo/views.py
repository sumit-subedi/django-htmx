import datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import Task, Remainder
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.contrib import messages
from django.utils import timezone
from django.utils.decorators import method_decorator

from django.http import QueryDict, JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import TaskForm, RemainderForm

class IndexView(View):
    def get(self, request):
        if request.user.is_anonymous:
            user = authenticate(username = 'sumit', password = 'subedi')
            login(request, user)

        tasks = Task.objects.filter(user=request.user, date=datetime.date.today()).order_by('-id')
        context = {'tasks': tasks}
        return render(request, 'home.html', context)

class DailyTasksView(View):
    @method_decorator(login_required)
    def get(self, request):
        tasks = Task.objects.filter(user=request.user, date=datetime.date.today()).order_by('-id')
        return render(request, 'partials/tasklist.html', {'tasks': tasks})

    @method_decorator(login_required)
    @method_decorator(require_POST)
    def post(self, request, pk=None):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task Added Successfully!')
        else:
            messages.error(request, 'Failed to add task.')
        return redirect('daily_tasks', pk=pk)

    @method_decorator(login_required)
    @method_decorator(require_http_methods(['DELETE']))
    def delete(self, request, pk):
        task = get_object_or_404(Task, id=pk, user=request.user)
        task.delete()
        messages.warning(request, 'Successfully Deleted.')
        return JsonResponse({'status': 'ok'})

class HistoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'history.html')

    @method_decorator(login_required)
    @method_decorator(require_POST)
    def post(self, request):
        date = request.POST.get('month')
        if not date:
            messages.error(request, 'Invalid date format.')
            return redirect('history')
        
        from_date = f'{date}-01'
        year, month = date.split('-')
        to_date = f"{int(year) + 1}-01-01" if month == '12' else f"{year}-{int(month) + 1:02d}-01"

        dates = Task.objects.filter(user=request.user, date__gte=from_date, date__lt=to_date).annotate(
            month=TruncMonth('date')
        ).values('date').annotate(c=Count('id'))
        
        context = {'dates': dates}
        return render(request, 'partials/historydates.html', context)

class HistorySearchView(View):
    @method_decorator(login_required)
    def get(self, request, pk):
        tasks = Task.objects.filter(user=request.user, date=pk)
        context = {'date': pk, 'tasks': tasks}
        return render(request, 'partials/historydetail.html', context)

@method_decorator(login_required, name='dispatch')
class RemainderView(View):
    
    def get(self, request):
        remainders = Remainder.objects.filter(user=request.user, sent=False)
        form = RemainderForm(initial={'mail': request.user.email})
        return render(request, 'remainder.html', {'remainders': remainders, 'form': form})

    def post(self, request):
        form = RemainderForm(request.POST)
        print(form.data)
        if form.is_valid():
            remainder = form.save(commit=False)
            remainder.user = request.user
            remainder.save()
            messages.success(request, 'Reminder Added Successfully!')
        else:
            print(form.errors)
            messages.error(request, 'Failed to add reminder.')
        return redirect('remainder')

    def delete(self, request):
        body = QueryDict(request.body)
        id = body.get('id')
        remainder = get_object_or_404(Remainder, id=id, user=request.user)
        remainder.delete()
        messages.success(request, "Task successfully deleted.")
        
        remainders = Remainder.objects.filter(user = request.user, sent = False)
        form = RemainderForm(initial={'mail': request.user.email})
        return render(request, 'remainder.html', {'remainders': remainders, 'form': form})

def historyCompress(request, pk):
    dates = Task.objects.filter(user=request.user, date=pk).values('date').annotate(c=Count('id'))

    if dates:
        date = dates[0]
    else:
        date = None

    context = {
        'date': date
    }
    return render(request, 'partials/datelist.html', context)

def logoutuser(request):
    logout(request)
    return redirect('login')

def CustomLoginView(request):
    return render(request, 'login.html')
