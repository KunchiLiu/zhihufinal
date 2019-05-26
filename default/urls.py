from django.conf.urls import url

from . import views

urlpatterns =[
   url(r'^$',views.log),
   url(r'^register$',views.register),
   url(r'^log$',views.log),
   url(r'^questionlist/$',views.questionlist),
   url(r'^logout$',views.logoutview),
   url(r'^question/$', views.question),
   url(r'^attention/$', views.attention),
   url(r'^data/$',views.data),
   url(r'^follow/$',views.follow),
]