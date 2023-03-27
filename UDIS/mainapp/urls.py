from django.urls import path
#now import the views.py file into this code
from . import views
urlpatterns=[
  path('',views.dashboard),
  path('dashboard',views.dashboard),
  path('professors',views.research),
  path('calendar',views.calendar),
  path('student-profile',views.profile),
]