from django.urls import path
#now import the views.py file into this code
from . import views
from django.contrib.auth import views as auth
urlpatterns=[
  path('',views.dashboard),
  path('dashboard',views.dashboard),
  path('research',views.research),
  path('calendar',views.calendar),
  path('student-profile/<str:rollno>',views.profile),
  path('curriculum',views.curriculum),
  path('cashregister',views.cashregister),
  path('feepayment',views.Fee),
  path('subreg',views.Subregistration),
  path('applysub/<str:subno>',views.applySubject),
  # path('signup',views.register),
   ##### user related path##########################
  # path('login/', views.Login, name ='login'),
  # path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
  # path('register/', views.register, name ='register'),
]