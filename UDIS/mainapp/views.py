from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect
from .models import *
import datetime

# Create your views here.
# import Http Response from django
from django.shortcuts import render

from .forms import *

# create a function


@login_required(login_url="/signin")
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
    # print(request.user.__subclasses__)
    user = request.user
    print(user.name, user.derived_type)
    context = {
        "students": students,
        "fees": feedone,
        "user": {"user": request.user, "utype": request.user.derived_type}

    }

    # return response with template and context
    return render(request, "dashboard.html", context)


# @login_required(login_url="/signin")
def research(request):
    # create a dictionary to pass
    # data to the template

    profs = Project.objects.all()
    publ = Publication.objects.all()
    projects = Project.objects.all()

    context = {
        "profs": profs,
        "publications": publ,
        "projects": projects,

        # "list": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    if request.user.is_authenticated:
        context["user"] = {"user": request.user,
                           "utype": request.user.derived_type}

    # return response with template and context
    return render(request, "research.html", context)


@login_required(login_url="/signin")
def Subregistration(request):
    slots = []
    departments = []
    regcourses = []
    appcourses = []
    rejcourses = []
    print(request.user.derived_type)
    if request.user.derived_type == "Student":
        student = Student.objects.filter(email=request.user.email)
        regcourses = student[0].regcourses.all()
        appcourses = student[0].appcourses.all()
        rejcourses = student[0].rejcourses.all()
        courses = Course.objects.all()
        for course in courses:
            slots += course.getSlots()
            departments += [course.department]
        slots = set(slots)
        slots = list(slots)
        departments = set(departments)
        departments = list(departments)
        print(regcourses, appcourses, rejcourses)
        context = {
            "user": request.user.derived_type,
            "regcourses": regcourses,
            "courses": courses,
            "slots": slots,
            "departments": departments,
            "rejcourses": rejcourses,
            "appcourses": appcourses,
        }

    elif request.user.derived_type == "Professor":
        prof = Professor.objects.filter(email=request.user.email)[0]
        profcourses = prof.courses.all()
        applications = subjectApplication.objects.all().filter(course__in=profcourses)
        print(applications)
        context = {
            "user": request.user.derived_type,
            "profcourses": profcourses,
            "applications": applications

        }
    else:
        courses = Course.objects.all()

        for course in courses:
            slots += course.getSlots()
            departments += [course.department]
        context = {
            "user": request.user.derived_type,
            "courses": courses,
        }
    context["user"] = {"user": request.user,
                       "utype": request.user.derived_type}

    # return response with template and context
    if request.user.derived_type == "Student":
        return render(request, "subject-reg.html", context)
    elif request.user.derived_type == "Professor":
        return render(request, "subject-reg-prof.html", context)
    else:
        return render(request, "subject-reg-sec.html", context)


def applySubject(request, subno):
    # value = request.POST.get('message')
    # print(value,subno,request.POST)
    # data=json.loads(request.body)

    dic = dict(request.POST.lists())
    print(dic.get('message')[0])
    course = Course.objects.filter(subno=subno)[0]
    # student = Course.objects.filter(rollno=requerollno)[-1]
    student = Student.objects.get(email=request.user.email)
    sa = subjectApplication(course=course, message=dic.get(
        'message')[0], student=student)
    sa.save()
    if not student.appcourses.contains(course):
        student.appcourses.add(course)
        student.save()

    return redirect("/subreg")


def registerStudent(request, rollno, subno):

    # value = request.POST.get('message')
    # print(value,subno,request.POST)
    # data=json.loads(request.body)
    student = Student.objects.filter(rollno=rollno)[0]
    course = Course.objects.filter(subno=subno)[0]
    print(student, course)
    if course.register():
        student.appcourses.remove(course)
        student.regcourses.add(course)
        student.save()
    else:
        print("failed")
    appl = subjectApplication.objects.filter(
        course=course, student=student)
    appl.delete()

    return redirect("/subreg")


def rejectStudent(request, rollno, subno):

    # value = request.POST.get('message')
    # print(value,subno,request.POST)
    # data=json.loads(request.body)
    student = Student.objects.filter(rollno=rollno)[0]
    course = Course.objects.filter(subno=subno)[0]
    print(student, course)
    student.appcourses.remove(course)
    student.rejcourses.add(course)
    appl = subjectApplication.objects.filter(
        course=course, student=student)
    appl.delete()

    return redirect("/subreg")


@login_required(login_url="/signin")
def calendar(request):
    # create a dictionary to pass
    # data to the template
    context = {
        "user": "Secretary",
        "list": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    context["user"] = {"user": request.user,
                       "utype": request.user.derived_type}

    # return response with template and context
    return render(request, "calendar.html", context)


@login_required(login_url="/signin")
def profile(request, rollno):
    # create a dictionary to pass
    # data to the template
    courses = [{"subno": "CS21204", "name": "Formal Language Automata Theory", "url": "/coursepage", "type": "DEPTH CORE", "LTP": "3-1-0", "credits": "4.0", "faculty": "Animesh Mukherjee , Soumyajit Dey", "status": "Registered"}, {"subno": "CS21204", "name": "Formal Language Automata Theory", "url": "/coursepage", "type": "DEPTH CORE", "LTP": "3-1-0", "credits": "4.0", "faculty": "Animesh Mukherjee , Soumyajit Dey", "status": "Registered"}, {"subno": "CS21204", "name": "Formal Language Automata Theory", "url": "/coursepage", "type": "DEPTH CORE", "LTP": "3-1-0", "credits": "4.0", "faculty": "Animesh Mukherjee , Soumyajit Dey", "status": "Registered"},
               {"subno": "CS21204", "name": "Formal Language Automata Theory", "url": "/coursepage", "type": "DEPTH CORE", "LTP": "3-1-0", "credits": "4.0", "faculty": "Animesh Mukherjee , Soumyajit Dey", "status": "Registered"}, {"subno": "CS21204", "name": "Formal Language Automata Theory", "url": "/coursepage", "type": "DEPTH CORE", "LTP": "3-1-0", "credits": "4.0", "faculty": "Animesh Mukherjee , Soumyajit Dey", "status": "Registered"}, {"subno": "CS21204", "name": "Formal Language Automata Theory", "url": "/coursepage", "type": "DEPTH CORE", "LTP": "3-1-0", "credits": "4.0", "faculty": "Animesh Mukherjee , Soumyajit Dey", "status": "Registered"}]
    sgpa = [9.76, 9.84, 9.44, 9.28]
    today = datetime.date.today()

    print(today.year, rollno)
    student = Student.objects.get(rollno=rollno)
    courses = student.regcourses.all()

    print(student)
    context = {
        "user": "Student",
        "backlogs": 0,
        "courses": courses,
        "course": student.course,
        "cgpa": student.getcgpa(),
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
        "primary_email": student.email,
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
        "sgpa": student.getsgpa()
    }
    context["user"] = {"user": request.user,
                       "utype": request.user.derived_type}

    # return response with template and context
    return render(request, "student-profile.html", context)


@login_required(login_url="/signin")
def curriculum(request):
    # create a dictionary to pass
    # data to the template

    courses = Course.objects.all()
    # courses=[{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"}]
    context = {
        "user": "Secretary",
        "courses": courses,
    }
    context["user"] = {"user": request.user,
                       "utype": request.user.derived_type}

    # return response with template and context
    return render(request, "curriculum.html", context)


@login_required(login_url="/signin")
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
    context["user"] = {"user": request.user,
                       "utype": request.user.derived_type}

    # return response with template and context
    return render(request, "cash-register.html", context)


@login_required(login_url="/signin")
def Fee(request):
    # create a dictionary to pass
    # data to the template
    hmcfee = Fees.objects.filter(type="hmcfee")
    instfee = Fees.objects.filter(type="instfee")
    semfee = Fees.objects.filter(type="semfee")
    context = {
        "hmcfee": hmcfee,
        "semfee": semfee,
        "instfee": instfee,
    }
    if request.user.derived_type == "Student":
        student = Student.objects.filter(email=request.user.email)[0]
        total = student.totalpaid
        feespaid = student.feespaid
        totalfee = Fees.objects.filter(sem=student.sem)
        totalfee = sum([fee.amount for fee in totalfee])
        print(totalfee)
        pending = totalfee-feespaid
        feetrans = FeeTransaction.objects.filter(student=student)
        print(feetrans)
        context = {
            "totfeepaid": total,
            "hmcfee": hmcfee,
            "instfee": instfee,
            "semfee": semfee,
            "pending": pending,
            "feetrans": feetrans

        }
    if request.user.derived_type == "Secretary":
        secretary = Secretary.objects.filter(email=request.user.email)[0]
        today = datetime.date.today()
        year = today.year
        deptotal = FeeTransaction.objects.filter(year=int(year))
        depamt = sum([float(fee.amount) for fee in deptotal])
        students = Student.objects.filter(department=secretary.department)
        count = 0
        for student in students:
            feespaid = student.feespaid
            totalfee = Fees.objects.filter(sem=student.sem)
            totalfee = sum([fee.amount for fee in totalfee])
            pending = totalfee-feespaid
            print(pending)
            if pending <= 0:
                count += 1

        context = {
            # "totfeepaid": total,
            "hmcfee": hmcfee,
            "instfee": instfee,
            "semfee": semfee,
            "pending": pending,
            # "feetrans": feetrans,
            "stupaid": count,
            "totalstu": len(students),
            "deptotal": depamt,
            "feetrans": deptotal,
            "year": year


        }

    # total = 200000
    semfeepaid = 50000
    instfeepaid = 50000
    HMCfeepaid = 50000
    totsemfee = 100000
    totinstfee = 100000
    totHMCfee = 100000
    # pending = 20000

    print(hmcfee, instfee, semfee)

    context["user"] = {"user": request.user,
                       "utype": request.user.derived_type}

    # return response with template and context
    return render(request, "fee.html", context)


def payfees(request):
    dic = dict(request.POST.lists())
    print(dic.get('amount')[0])
    student = Student.objects.filter(email=request.user.email)[0]
    # student.updatePaid(float(dic.get('amount')[0]))
    # student = Course.objects.filter(rollno=requerollno)[-1]
    today = datetime.date.today()
    year = today.year
    sa = FeeTransaction(student=student, amount=dic.get(
        'amount')[0], sem=student.sem, year=year)
    sa.save()

    return redirect("/feepayment")
def confirmpay(request,transid):
    # dic = dict(request.POST.lists())
    # print(dic.get('amount')[0])
    sa = FeeTransaction.objects.filter(id=transid)[0]
    sa.status="Success"
    
    student =sa.student
    student.updatePaid(float(sa.amount))
    sa.save()
    student.save()
    # student.updatePaid(float(dic.get('amount')[0]))
    # student = Course.objects.filter(rollno=requerollno)[-1]
    # today = datetime.date.today()
    # year = today.year
    # sa.save()

    return redirect("/feepayment")
def denypay(request,transid):
    sa = FeeTransaction.objects.filter(id=transid)[0]
    sa.status = "Failed"
    
    student =sa.student
    student.updatePaid(float(sa.amount))
    sa.save()
    student.save()

    return redirect("/feepayment")


def signUp(request, utype):
    if request.user.is_authenticated:
        return redirect('/')
    if utype.lower() == "student":
        utype = "Student"
    elif utype.lower() == "secretary":
        utype = "Secretary"
    elif utype.lower() == "professor":
        utype = "Professor"
    else:
        return redirect("/signup/student")

    if request.method == 'POST':
        dic = dict(request.POST.lists())
        if utype == "Student":
            email = dic.get('email')[0]
            password1 = dic.get('password1')[0]
            firstname = dic.get('firstname')[0]
            lastname = dic.get('lastname')[0]
            rollno = dic.get('rollno')[0]
            mobile = dic.get('mobile')[0]
            gender = dic.get('gender')[0]
            address = dic.get('address')[0]
            state = dic.get('state')[0]
            location = dic.get('location')[0]
            aadhar = dic.get('aadhar')[0]
            pin_code = dic.get('pin')[0]
            instemail = dic.get('instemail')[0]
            a = Student.objects.create_user(email=email, password=password1, firstname=firstname, lastname=lastname, name=firstname+" "+lastname,
                                            rollno=rollno, mobile=mobile, gender=gender, address=address, state=state, location=location, aadhar=aadhar, pin_code=pin_code, inst_email=instemail)

            a.derived_type = "Student"
            a.save()
        elif utype == "Secretary":
            email = dic.get('email')[0]
            password1 = dic.get('password1')[0]
            firstname = dic.get('firstname')[0]
            lastname = dic.get('lastname')[0]
            # rollno = dic.get('rollno')[0]
            mobile = dic.get('mobile')[0]

            a = Secretary.objects.create_user(email=email, password=password1, firstname=firstname, lastname=lastname, name=firstname+" "+lastname,
                                              mobile=mobile, is_superuser=True, is_staff=True)

            a.derived_type = "Secretary"
            a.save()
        if utype == "Professor":
            email = dic.get('email')[0]
            password1 = dic.get('password1')[0]
            firstname = dic.get('firstname')[0]
            lastname = dic.get('lastname')[0]
            # rollno = dic.get('rollno')[0]
            mobile = dic.get('mobile')[0]
            a = Professor.objects.create_user(email=email, password=password1, firstname=firstname, lastname=lastname, name=firstname+" "+lastname,
                                              mobile=mobile, is_superuser=True, is_staff=True)

            a.derived_type = "Professor"
            a.save()

            print(password1, email)
            user = authenticate(email=email, password=password1)
            print(user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
    if utype == "Professor":
        return render(request, "signup_prof.html", {"utype": utype})
    elif utype == "Secretary":
        return render(request, "signup_prof.html", {"utype": utype})
    else:
        return render(request, "signup.html", {"utype": utype})

    # return render(request, "signup.html")


def signIn(request):
    if request.user.is_authenticated:
        return redirect('/')
    # if utype.lower() == "student":
    #     utype = "Student"
    # elif utype.lower() == "secretary":
    #     utype = "Secretary"
    # elif utype.lower() == "professor":
    #     utype = "Professor"
    # else:
    #     return redirect("/signin/student")

    if request.method == 'POST':
        dic = dict(request.POST.lists())
        email = dic.get('email')[0]
        password1 = dic.get('password1')[0]
        print(password1, email)
        user = authenticate(email=email, password=password1)
        print(user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('/')
    return render(request, "signin.html")

    # form=CustomUserCreationForm()
    # context={
    # 	"user":user,
    # 	"form":form
    # }


def addPublication(request):

    # if utype.lower() == "student":
    #     utype = "Student"
    # elif utype.lower() == "secretary":
    #     utype = "Secretary"
    # elif utype.lower() == "professor":
    #     utype = "Professor"
    # else:
    #     return redirect("/signin/student")

    if request.method == 'POST':
        dic = dict(request.POST.lists())
        name = dic.get('name')[0]
        place = dic.get('name')[0]
        date = dic.get('name')[0]
        abstract = dic.get('name')[0]
        professor = Professor.object.filter(
            name__in=dic.get('professor')[0].split(","))
        pub = Publication.objects.create(
            name=name, place=place, date=date, abstract=abstract, professor=professor)
        pub.save()
    return redirect("/research")

    # form=CustomUserCreationForm()
    # context={
    # 	"user":user,
    # 	"form":form
    # }


def logout_view(request):
    logout(request)
    return redirect('/')

# class SignInView(LoginView):

#     template_name = 'path/to/my_template.html'

#     def form_valid(self, form):
#         # Form is valid, do whatever you need.
#         login(self.request, form.get_user())
#         response = HttpResponseRedirect(self.get_success_url())
#         return response
