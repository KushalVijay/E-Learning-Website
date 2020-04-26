from django.db import models
from accounts.models import User
from home.models import Question

class Answer(models.Model):
    username = models.CharField(max_length=200,blank=True,null=True)
    question_statement = models.CharField(max_length=200,blank=True,null=True)
    answer = models.CharField(max_length=200,null=True,blank=True)
    remark = models.CharField(max_length=200,null=True,blank=True)
    course_id = models.IntegerField(default=0)
    
    def __str__(self):
        return self.username + " Course : " +  str(self.course_id) + " Question : " +self.question_statement
    
class Question_BankManager(models.Manager):
    def new_or_get(self,request):
        print(request.session)
        questionbank_id = request.session.get("user_id", None)
        qs = self.get_queryset().filter(id=questionbank_id)
        if qs.exists():
            new_obj = False
            questionbank_obj = qs.first()
            if request.user.is_authenticated and questionbank_obj.user is None:
                questionbank_obj.user = request.user
                questionbank_obj.save()
        else:
            questionbank_obj = Question_Bank.objects.new(user=request.user)
            new_obj = True
            request.session['user_id'] = questionbank_obj.id
        return questionbank_obj,new_obj

    def new(self,user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Question_Bank(models.Model):
    user = models.ForeignKey(User,null=True,blank=True ,on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question,blank=True)

    objects = Question_BankManager()
    def __str__(self):
        return self.user.get_full_name()
