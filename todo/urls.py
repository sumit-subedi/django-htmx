from django.urls import path
from .views import *
from django.urls.conf import include


urlpatterns = [
    path('accounts/login', CustomLoginView , name='login'),
    path('accounts/', include('allauth.urls')),

    path('', IndexView.as_view(), name='home-page'),
    path('history', HistoryView.as_view(), name='history'),
    path('logout', logoutuser, name="logout"),

    path('htmx/tasklist/<pk>/', DailyTasksView.as_view(), name='tasklist'),
    path('htmx/historydetail/<pk>', HistorySearchView.as_view(), name='historydetail'),
    path('htmx/historycompress/<pk>', historyCompress, name='historycompress'),
    path('htmx/remainder', RemainderView.as_view(), name='remainder'),
]