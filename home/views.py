from django.shortcuts import render,redirect
from .models import Course,Topic,Question
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.
def index(request):
    return render(request, "index.html")

def courses(request):
    courses = Course.objects.all()

    content = {
        'courses':courses,
    }
    return render(request,"courses.html",content)


def course_detail(request):
    if request.user.is_authenticated:
        course_id = request.POST.get("course_id")
        questions = Question.objects.filter(course_id=course_id)
        content = {
            'questions':questions,
            'course_id':course_id,
        }
        return render(request,"course_detail.html",content)
    else:
        return redirect('login')

def learning(request):
    topics = Topic.objects.all()
    content = {
        'topics': topics,
    }
    return render(request, "learning.html", content)

def learning_detail(request):
    topic_id = request.POST.get("topic_id")
    topic = Topic.objects.filter(id=topic_id)[0]
    content = {
        'name': topic.name,
        'description':topic.description,
    }
    return render(request, "learning_detail.html", content)

def news(request):
    return render(request,"news.html")

