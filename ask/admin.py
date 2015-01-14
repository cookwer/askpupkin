from django.contrib import admin
from ask.models import *

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)