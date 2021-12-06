from django.contrib import admin

from .models import (Task, Remainder)

admin.site.register(Task)
admin.site.register(Remainder)