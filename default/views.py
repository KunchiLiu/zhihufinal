from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import Context
from  django.contrib.auth.forms import UserCreationForm,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from default.models import UserProfile
from django.contrib import messages
from default.models import Question
from default.models import Answer
def log(request):
     if request.method == 'GET':
          return render(request, "log.html")
     elif request.method == 'POST':
          username = request.POST['logname']
          password = request.POST['logpass']
          user = authenticate(username=username, password=password)
          if user is not None:
               login(request,user)
               request.session['username']=username
               return HttpResponseRedirect("/questionlist/")
          else:
               messages.error(request, '用户名不存在或者密码错误')
               return render(request, "log.html")

def register(request):
     if request.method == 'GET':
          return render(request, "register.html")
     elif request.method == "POST":
          form = UserCreationForm(request.POST)
          username = request.POST['signname']
          password1 = request.POST['signpass1']
          password2 = request.POST['signpass2']
          if password1 != password2:
               messages.error(request, '两次密码输入不一致')
               return render(request, "register.html")
          elif User.objects.filter(username__exact=username):
               messages.error(request, '该用户名已存在')
               return render(request, "register.html")
          user = User.objects.create_user(username,"null",password1)
          profile = UserProfile(user=user,name=user.username,prompt=0)
          profile.save()
          request.session['username'] = user.username#用session记住用户的用户名
          login(request, user)#登录用户
          return HttpResponseRedirect("/questionlist/")

def questionlist(request):
     if request.method == 'GET':
        theuserprofile = UserProfile.objects.get(user_id=request.user.id)
        questionlist = Question.objects.filter(author=request.user)
        myfollowquestions=theuserprofile.question.all()
        questions = Question.objects.all()
        questions =sorted(questions, key=lambda Question: Question.answernum, reverse=True)
        answers=Answer.objects.all()
        answers.query.group_by=['question_id']
        hotquestions = []
        hotquestions.append(questions[0])
        hotquestions.append(questions[1])
        hotquestions.append(questions[2])
        user=request.user
        return render(request, "questionlist.html", {'myfollowquestions':myfollowquestions,'questionlist': questionlist,'userprofile': theuserprofile,'questions': questions,'hotquestions':hotquestions,'answers':answers,'user':user})
     elif request.method=='POST':
        new_question=request.POST['myask']
        new_question_type=request.POST['category']
        newask=Question(type=new_question_type,content=new_question,author=request.user)
        newask.save()
        return HttpResponseRedirect("/questionlist/")

def logoutview(request):
    logout(request)
    return HttpResponseRedirect("/")

def question(request):
     if request.method == 'GET':
         questionid = request.GET['sendid']
         question= Question.objects.get(id=questionid)
         answers = question.question_answer.all()
         user=request.user
         return render(request, 'question.html', {'question':question,'answers':answers,'user':user})
     elif request.method=='POST':
        thequestion_id=request.POST['id']
        thequestion=Question.objects.get(id=thequestion_id)
        theuser=UserProfile.objects.get(user_id=thequestion.author_id)
        new_answer_content=request.POST['myanswer']
        new_answer=Answer(content=new_answer_content,author=request.user,question=thequestion)
        new_answer.save()
        new_answernum = thequestion.answernum + 1
        thequestion.answernum = new_answernum
        thequestion.save()
        theuser.prompt=True
        theuser.save()
        return HttpResponseRedirect("/questionlist/")

def attention(request):
    if request.method == 'POST':
        questionid = request.POST['questionid']
        aquestion=Question.objects.get(id=questionid)
        theuserprofile = UserProfile.objects.get(user_id=request.user.id)
        theuserprofile.question.add(aquestion)
        theuserprofile.save()
        questionlist = Question.objects.filter(author=request.user)
        myfollowquestions = theuserprofile.question.all()
        questions = Question.objects.all()
        questions = sorted(questions, key=lambda Question: Question.answernum, reverse=True)
        answers = Answer.objects.all()
        answers.query.group_by = ['question_id']
        hotquestions = []
        hotquestions.append(questions[0])
        hotquestions.append(questions[1])
        hotquestions.append(questions[2])
        user = request.user
        return render(request, "questionlist.html",
                      {'myfollowquestions': myfollowquestions, 'questionlist': questionlist,
                       'userprofile': theuserprofile, 'questions': questions, 'hotquestions': hotquestions,
                       'answers': answers, 'user': user})

def data(request):
    if request.method == 'POST':
        theuserprofile = UserProfile.objects.get(user=request.user)
        theuserprofile.prompt=False#我把判断的工作改在前端完成，此处prompt一定是true
        theuserprofile.save()
        theuserprofile = UserProfile.objects.get(user_id=request.user.id)
        questionlist = Question.objects.filter(author=request.user)
        myfollowquestions = theuserprofile.question.all()
        questions = Question.objects.all()
        questions = sorted(questions, key=lambda Question: Question.answernum, reverse=True)
        answers = Answer.objects.all()
        answers.query.group_by = ['question_id']
        hotquestions = []
        hotquestions.append(questions[0])
        hotquestions.append(questions[1])
        hotquestions.append(questions[2])
        user = request.user
        return render(request, "questionlist.html",
                      {'myfollowquestions': myfollowquestions, 'questionlist': questionlist,
                       'userprofile': theuserprofile, 'questions': questions, 'hotquestions': hotquestions,
                       'answers': answers, 'user': user})
def follow(request):
    if request.method == 'POST':
        questionid=request.POST['followquestionid']
        question = Question.objects.get(id=questionid)
        answers = question.question_answer.all()
        return render(request, 'question.html', {'question': question, 'answers': answers})