from django.shortcuts import render,redirect
from .models import Question_Bank,Answer
from home.models import Course,Question
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def similarity(X,Y):
    # tokenization
    X_list = word_tokenize(X)
    Y_list = word_tokenize(Y)

    # sw contains the list of stopwords
    sw = stopwords.words('english')
    l1 = [];
    l2 = []

    # remove stop words from string
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}

    # form a set containing keywords of both strings
    rvector = X_set.union(Y_set)
    for w in rvector:
        if w in X_set:
            l1.append(1)  # create a vector
        else:
            l1.append(0)
        if w in Y_set:
            l2.append(1)
        else:
            l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(rvector)):
        c += l1[i] * l2[i]
    cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
    if cosine*100>60.00:
        return True
    else:
        return False


def submission(request):
    course_id = request.POST.get('course_id')
    if course_id is not None:
        try:
            question_obj = Question.objects.filter(course_id=course_id)
        except Question.DoesNotExist:
            return redirect("index")
        questionbank_obj, questionbanknew_obj = Question_Bank.objects.new_or_get(request)

        for ques in question_obj:
            questionbank_obj.questions.add(ques)
        data = request.POST

        for item in question_obj:
            ques_obj = Question.objects.filter(statement=item.statement)[0]
            answer = data[item.statement]
            if ques_obj.self_check:
                if similarity(ques_obj.predefined_answer,answer):
                    remark = ques_obj.predefined_remark
                else:
                    remark = "Not upto the mark"
                obj = Answer.objects.create(username=request.user, question_statement=item.statement, answer=answer,remark=remark, course_id=data['course_id'])

            else:
                obj = Answer.objects.create(username=request.user,question_statement=item.statement,answer=answer,remark=None,course_id=data['course_id'])

            # added = True
    return redirect('courses')

def student_details(request):
    if request.method=='POST':
        username = request.POST.get('student_username')
        student_answers = Answer.objects.filter(username=username)
        content = {
            'student_answers':student_answers,
            'student_username':username,
        }
    return render(request,'student_detail.html',content)


def feedback(request):
    if request.method=='POST':
        data = request.POST;
        username = request.POST.get('student_username')
        student_answers = Answer.objects.filter(username=username)
        for question in student_answers:
            question.remark = data[question.question_statement]
            question.save()
    return redirect('profile')