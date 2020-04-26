from django.contrib.auth import authenticate, login, get_user_model,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.db.models import Q
from .mixins import NextUrlMixin, RequestFormAttachMixin
from .forms import LoginForm
from .signals import user_logged_in
from questions.models import Question_Bank,Answer
from accounts.models import User

class Login_View(RequestFormAttachMixin, FormView):

    form_class = LoginForm
    template_name = 'login.html'
    success_url = 'profile.html'
    default_next = 'profile'


    def get(self, request, *args, **kwargs):
        context = {'next': request.GET['next'] if request.GET and 'next' in request.GET else ''}
        return render(request, "login.html", context)
    def form_valid(self, form):
        request = self.request

        next_post = request.POST.get('next')

        if next_post is None:
            next_post= self.default_next
        return redirect(next_post)


def profile(request):
    user = User.objects.filter(username=request.user)[0]
    if user.is_admin:
        students_list =  User.objects.filter(admin=False)
        content = {
            'students_list':students_list,
        }
        return render(request, 'profile.html',content)
    else:
        student_obj = Answer.objects.filter(username=request.user)
        content = {
            'student_answer':student_obj,
        }
        return render(request,'profile.html',content)
    return render(request,'profile.html')

def Logout(request):
    logout(request)
    messages.info(request,"Succefully Logged Out")
    return redirect("/")



