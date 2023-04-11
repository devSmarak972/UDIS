from django.urls import path
# now import the views.py file into this code
from . import views
from django.contrib.auth import views as auth
urlpatterns = [
    path('', views.dashboard),
    path('dashboard', views.dashboard),
    path('research', views.research),
    path('inventory', views.inventory),
    path('calendar', views.calendar),
    path('student-profile/<str:rollno>', views.profile),
    path('curriculum', views.curriculum),
    path('cashregister', views.cashregister),
    path('feepayment', views.Fee),
    path('subreg', views.Subregistration),
    path('applysub/<str:subno>', views.applySubject),
    path('signup/<str:utype>', views.signUp),
    path('addpub', views.addPublication),
    path('payfee', views.payfees),
    path('confirmpay/<int:transid>', views.confirmpay),
    path('denypay/<int:transid>', views.denypay),
    # path('payfee', views.payfees),
    # path('signin',views.signIn),
    path('signin', views.signIn),
    path('logout', views.logout_view),
    path('registerstudent/<str:rollno>/<str:subno>', views.registerStudent),
    path('rejectstudent/<str:rollno>/<str:subno>', views.rejectStudent),
    path('addEvent/<str:date>/<str:text>', views.addEvent),
    path('getEvents', views.getEvents),
    path('gradecard/<str:rollno>/<str:name>', views.gradeCard),
    path('addOrder/<int:id>', views.addOrder),
    path('deleteOrder/<int:id>', views.deleteOrder),

    ##### user related path##########################
    # path('login/', views.Login, name ='login'),
    # path('logout/', auth.LogoutView.as_view(template_name ='user/index.html'), name ='logout'),
    # path('register/', views.register, name ='register'),
]
