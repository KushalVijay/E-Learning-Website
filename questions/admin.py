from django.contrib import admin

# Register your models here.
from .models import Question_Bank,Answer

admin.site.register(Question_Bank)

admin.site.register(Answer)