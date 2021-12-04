from django.urls import path
from .views import *
from django.urls.conf import include


urlpatterns = [
    path('accounts/login', CustomLoginView , name='login'),
    path('accounts/', include('allauth.urls')),

    path('', index, name='home-page'),
    path('history', history, name='history'),
    path('logout', logoutuser, name="logout"),

    path('htmx/tasklist/<pk>/', dailyTasks, name='tasklist'),
    path('htmx/historydetail/<pk>', historySearch, name='historydetail'),
    path('htmx/historycompress/<pk>', historyCompress, name='historycompress'),
]