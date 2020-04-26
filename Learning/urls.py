"""Learning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url,include
from django.contrib import admin
from home.views import index,course_detail,courses,learning,learning_detail,news
from accounts.views import  profile, Logout, Login_View
from questions.views import submission,student_details,feedback

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^logout/$', Logout, name='logout'),
    url(r'^login/$', Login_View.as_view(), name='login'),
    url(r'^learning/$', learning, name='learning'),
    url(r'^learning_details/$', learning_detail, name='learning_detail'),
    url(r'^courses/$', courses, name='courses'),
    url(r'^course_details/$', course_detail, name='course_detail'),
    url(r'^news/$', news, name='news'),
    url(r'^submission/$', submission, name='submission'),
    url(r'^feedback/$', feedback, name='feedback'),
    url(r'^student_details/$', student_details, name='student_details'),
]

if  settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
