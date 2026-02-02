from django.contrib import admin

from . models import Thought
from . models import Profile


admin.site.register(Thought)
admin.site.register(Profile)