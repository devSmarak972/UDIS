from django.shortcuts import render, redirect
from .models import *
import datetime
# Create your views here.
# import Http Response from django
from django.shortcuts import render

# create a function


def dashboard(request):
    # create a dictionary to pass
    # data to the template
    feedone = []
    students = []
    students = Student.objects.all()
    print(totalFees(Fees.objects.filter(sem=4)))
    for student in students:
        if student.feespaid == totalFees(Fees.objects.filter(sem=student.sem))['amount__sum']:
            feedone.append("Yes")
        else:
            feedone.append('No')
    context = {
        "students": students,
        "fees": feedone,
    }
    # return response with template and context
    return render(request, "dashboard.html", context)


def research(request):
    # create a dictionary to pass
    # data to the template
    context = {
        "data": "some data",
        "list": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    # return response with template and context
    return render(request, "ProjectsPublications/research.html", context)


def Subregistration(request):
    student = Student.objects.filter(rollno="21CS30061")
    regcourses = student[0].regcourses.all()
    appcourses = student[0].appcourses.all()
    rejcourses = student[0].rejcourses.all()
    courses = Course.objects.all()
    print(regcourses)
    slots = []
    departments = []
    for course in courses:
        slots += course.getSlots()
        departments += [course.department]

    slots = set(slots)
    slots = list(slots)
    departments = set(departments)
    departments = list(departments)
    context = {
        "user": "Secretary",
        "regcourses": regcourses,
        "courses": courses,
        "slots": slots,
        "departments": departments,
        "rejcourses": rejcourses,
        "appcourses": appcourses,
    }
    # return response with template and context
    return render(request, "subject-reg.html", context)


def applySubject(request, subno,rollno):
    value = request.POST.get('message')
    # print(value,subno,request.POST)
    # data=json.loads(request.body)

    dic=dict(request.POST.lists())
    print(dic.get('message')[0])
    course=Course.objects.filter(subno=subno)[-1]
    student=Course.objects.filter(rollno=rollno)[-1]
    sa = subjectApplication(course=course,message=dic.get('message')[0],student=student)
    sa.save()
    student.appcourses.add(course)
    student.save()
    
    return redirect('/subreg')


def calendar(request):
    # create a dictionary to pass
    # data to the template
    context = {
        "user": "Secretary",
        "list": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    # return response with template and context
    return render(request, "calendar.html", context)


def profile(request, rollno):
    # create a dictionary to pass
    # data to the template
    courses = [{"subno": "CS21204", "name": "Formal Language Automata Theory", "url": "/coursepage", "type": "DEPTH CORE", "LTP": "3-1-0", "credits": "4.0", "faculty": "Animesh Mukherjee , Soumyajit Dey", "status": "Registered"}, {"subno": "CS21204", "name": "Formal Language Automata Theory", "url": "/coursepage", "type": "DEPTH CORE", "LTP": "3-1-0", "credits": "4.0", "faculty": "Animesh Mukherjee , Soumyajit Dey", "status": "Registered"}, {"subno": "CS21204", "name": "Formal Language Automata Theory", "url": "/coursepage", "type": "DEPTH CORE", "LTP": "3-1-0", "credits": "4.0", "faculty": "Animesh Mukherjee , Soumyajit Dey", "status": "Registered"},
               {"subno": "CS21204", "name": "Formal Language Automata Theory", "url": "/coursepage", "type": "DEPTH CORE", "LTP": "3-1-0", "credits": "4.0", "faculty": "Animesh Mukherjee , Soumyajit Dey", "status": "Registered"}, {"subno": "CS21204", "name": "Formal Language Automata Theory", "url": "/coursepage", "type": "DEPTH CORE", "LTP": "3-1-0", "credits": "4.0", "faculty": "Animesh Mukherjee , Soumyajit Dey", "status": "Registered"}, {"subno": "CS21204", "name": "Formal Language Automata Theory", "url": "/coursepage", "type": "DEPTH CORE", "LTP": "3-1-0", "credits": "4.0", "faculty": "Animesh Mukherjee , Soumyajit Dey", "status": "Registered"}]
    sgpa = [9.76, 9.84, 9.44, 9.28]
    today = datetime.date.today()

    print(today.year, rollno)
    student = Student.objects.get(rollno=rollno)
    courses = student.courses.all()

    print(student)
    context = {
        "user": "Student",
        "backlogs": 0,
        "courses": courses,
        "course": student.course,
        "cgpa": student.getcgpa()[-1],
        "name": student.name,
        "rollno": student.rollno,
        "gender": student.gender,
        "department": student.department,
        "course": student.course,
        "nationality": student.nationality,
        "hall": student.hall,
        "aadhar": student.aadhar,
        "status": student.status,
        "EAA": student.EAA,
        "adm_year": student.adm_year,
        "adm_nature": student.adm_nature,
        "primary_email": student.primary_email,
        "inst_email": student.inst_email,
        "teams_pass": student.teams_pass,
        "mobile": student.mobile,
        "guardian_email": student.guardian_email,
        "address": student.address,
        "location": student.location,
        "pin": student.pin_code,
        "state": student.state,
        "cleared_sem_crd": student.cleared_sem_crd,
        "sem_crd": student.sem_crd,
        "cleared_tot_crd": student.cleared_sem_crd,
        "tot_crd": student.tot_crd,
        "sgpa": student.getsgpa()[-1]
    }
    # return response with template and context
    return render(request, "student-profile.html", context)


def curriculum(request):
    # create a dictionary to pass
    # data to the template

    courses = Course.objects.all()
    # courses=[{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"}]
    context = {
        "user": "Secretary",
        "courses": courses,
    }
    # return response with template and context
    return render(request, "curriculum.html", context)


def cashregister(request):
    # create a dictionary to pass
    # data to the template
    total = 200000
    transactions = [{"type": "paid", "person": "Arun Biswas", "organisation": "Premium Woodworks Ltd", "contact": "arun143@gmail.com", "amount": "₹50000", "date": "March 30, 2023"}, {"type": "received", "person": "Viswanath Thakur", "organisation": "Alice Corporation",
                                                                                                                                                                                       "contact": "vsthakur@gmail.com", "amount": "₹100000", "date": "March 31, 2023"}, {"type": "received", "person": "Viswanath Thakur", "organisation": "Premium Woodworks Ltd", "contact": "arun143@gmail.com", "amount": "₹50000", "date": "March 30, 2023"},]
    context = {
        "user": "Secretary",
        "transactions": transactions,
        "expenditure": "₹"+str(sum(float(i["amount"][1:]) for i in transactions if i["type"] == "paid")),
        "received": "₹"+str(sum(float(i["amount"][1:]) for i in transactions if i["type"] == "received")),
        "balance": "₹"+str(total),

    }
    # return response with template and context
    return render(request, "cash-register.html", context)


def Fee(request):
    # create a dictionary to pass
    # data to the template
    total = 200000
    semfeepaid = 50000
    instfeepaid = 50000
    HMCfeepaid = 50000
    totsemfee = 100000
    totinstfee = 100000
    totHMCfee = 100000
    pending = 20000
    hmcfee = Fees.objects.all().filter(type="hmcfee")
    instfee = Fees.objects.filter(type="instfee")
    semfee = Fees.objects.all().filter(type="semfee")
    print(hmcfee, instfee, semfee)
    context = {
        "user": "secretary",
        "semfeepaid": semfeepaid,
        "instfeepaid": instfeepaid,
        "HMCfeepaid": HMCfeepaid,
        "totfeepaid": total,
        "totsemfee": totsemfee,
        "totinstfee": totinstfee,
        "totHMCfee": totHMCfee,
        "hmcfee": hmcfee,
        "instfee": instfee,
        "semfee": semfee,
        "pending": pending,

    }
    # return response with template and context
    return render(request, "fee.html", context)


def register(request):
    return render(request, "register_student.html")
