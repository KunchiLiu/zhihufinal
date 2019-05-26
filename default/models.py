from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    type = models.CharField(max_length=100)
    content =models.TextField(max_length=500)
    author = models.ForeignKey(User, null=True, blank=True,related_name='question_author',on_delete=models.SET_NULL)#一个用户可以问好多问题，一个问题只属于一个用户
    answernum = models.IntegerField(default= 0 )

class UserProfile(models.Model):
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name=models.TextField(max_length=10)
    telephone=models.CharField(max_length=20)
    prompt=models.BooleanField(default=False)
    question=models.ManyToManyField(Question)#用户关注的问题

class Answer(models.Model):
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(User, related_name='author_answer',on_delete=models.CASCADE)#cascade级联操作，用户不存在以后答案被删除
    question = models.ForeignKey(Question, related_name='question_answer',on_delete=models.CASCADE)


