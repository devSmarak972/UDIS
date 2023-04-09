from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import json


# class usermodel(AbstractUser):
#     created_At = models.DateTimeField(null=True, blank=True, auto_now=True)
#     primary_email = models.EmailField()
#     name = models.CharField(max_length=200)
#     department = models.TextField(default="Computer Science and Engineering")

#     def get_derived_type(self):
#         if self.derived_type == 'Secretary':
#             return "secretary"
#         elif self.derived_type == 'Student':
#             return "student"

# class Meta:
# 	abstract = True


class usermodel(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    created_At = models.DateTimeField(null=True, blank=True, auto_now=True)
    name = models.CharField(max_length=200, null=False)
    department = models.TextField(default="Computer Science and Engineering")
    firstname = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    derived_type = models.CharField(
        max_length=200, default="Student", blank=True, null=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_derived_type(self):
        if self.derived_type == 'Secretary':
            return "secretary"
        elif self.derived_type == 'Student':
            return "student"


class Course(models.Model):
    subno = models.CharField(max_length=200)
    name = models.TextField()
    department = models.CharField(
        max_length=255, default="Computer Science and Engineering", blank=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=200, default="Depth Core", blank=True)
    mode = models.CharField(
        max_length=200, default="Theory", blank=True)  # rtheory or lab
    LTP = models.CharField(max_length=200, default="4-1-0", blank=True)
    credits = models.IntegerField(default=3, blank=True)
    sem = models.IntegerField()
    session = models.IntegerField()  # starting year
    capacity = models.IntegerField(default=100, blank=True)  # starting year
    enrolled = models.IntegerField(default=0, blank=True)  # starting year
    available = models.CharField(
        max_length=255, default="Available", blank=True)  # starting year
    prerequisites = models.ManyToManyField(
        "self", related_name="prerequisites", blank=True, null=True)
    slot = models.CharField(max_length=255, default='', blank=True, null=True)
    room = models.CharField(max_length=255, default='', blank=True, null=True)

    def __str__(self):
        return self.name

    def register(self):
        print("registering")
        if self.enrolled == self.capacity:
            print("Course full")
            return False
        else:
            self.enrolled += 1
            if self.enrolled >= 0.8*self.capacity:
                self.available = "Filling Fast"
            elif self.enrolled == self.capacity:
                self.available = "Filled"
            else:
                self.available = "Available"
            self.save()

            return True

    def getSlots(self):
        print(self.slot)
        return self.slot.split(",")

    def getRooms(self):
        return self.room.split(",")


class Publication(models.Model):
    name = models.TextField()
    abstract = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=200, default="Journal")
    place = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class Experience(models.Model):
    organisation = models.CharField(max_length=200)
    startDate = models.DateField()
    endDate = models.DateField()
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.organisation+" "+self.type


class Professor(usermodel):
    # name=models.CharField(max_length=200)
    # department=models.CharField(max_length=200)
    mobile = models.CharField(max_length=200, blank=True, null=True)
    courses = models.ManyToManyField(Course, blank=True, null=True)
    education = models.ManyToManyField(
        Experience, related_name="education", blank=True, null=True)
    workex = models.ManyToManyField(
        Experience, related_name="workexperience", blank=True, null=True)
    publications = models.ManyToManyField(Publication, blank=True, null=True)
    # projects = models.ManyToManyField(Project, blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.TextField()
    desc = models.TextField()
    url = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    prof = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    count = models.IntegerField()
    expenditure = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Order(models.Model):
    item = models.CharField(max_length=200)
    qty = models.IntegerField()
    price = models.FloatField()
    status = models.CharField(max_length=200)  # confirmed,recieved

    def __str__(self):
        return self.item


class Person(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    amount = models.CharField(max_length=200)
    date = models.DateField()

    def __str__(self):
        return str(self.id)+"_"+str(self.amount)


class Secretary(usermodel):
    mobile = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Student(usermodel):
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pin_code = models.IntegerField(null=True, blank=True)
    backlogs = models.IntegerField(default=0)
    regcourses = models.ManyToManyField(
        Course, blank=True, null=True, related_name="regcourses")
    appcourses = models.ManyToManyField(
        Course, blank=True, null=True, related_name="appcourses")
    rejcourses = models.ManyToManyField(
        Course, blank=True, null=True, related_name="rejcourses")
    cgpa = models.CharField(max_length=200, default="9.9")
    rollno = models.CharField(max_length=200, null=True, blank=True)
    gender = models.TextField(default="N/A")
    # department=models.CharField(max_length=200)
    course = models.CharField(max_length=200, blank=True, default="B.Tech 4Y")
    hall = models.CharField(max_length=200, default="N/A")
    aadhar = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, default="On-Roll")
    EAA = models.CharField(max_length=200, null=True, blank=True)
    adm_year = models.DateField(auto_now=True)
    nationality = models.CharField(max_length=200, default="Indian")
    adm_nature = models.CharField(max_length=200, default="JEE")
    inst_email = models.EmailField(null=True, blank=True)
    teams_pass = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, default="N/A")
    guardian_email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    cleared_sem_crd = models.FloatField(default=0)
    sem_crd = models.FloatField(default=0)
    cleared_tot_crd = models.FloatField(default=0)
    tot_crd = models.FloatField(default=0)
    sgpa = models.CharField(max_length=200, default="""{"sgpa":["-"]}""")
    sem = models.IntegerField(default=1)
    feespaid = models.FloatField(default=0)
    totalpaid = models.FloatField(default=0)
    regdone = models.CharField(max_length=10, default="Yes")

    def updatePaid(self, amt):
        self.totalpaid += amt
        self.feespaid+=amt
        self.save()
    # def updatePaid(self, amt):
    #     self.totalpaid += amt

    def __str__(self):
        return self.name

    def getsgpa(self):
        print(self.sgpa)
        return self.cgpa.split(",")[-1]
        # return [9]

    def addsgpa(self, sg):

        self.sgpa=self.sgpa+","+str(sg)
        self.save()
    

    def getcgpa(self):
        print(self.cgpa)
        # return [9]
        return self.cgpa.split(",")[-1]

    def addcgpa(self, cg):
        self.cgpa=self.cgpa+","+str(cg)
        self.save()

    def enrollCourse(self, course):
        if course.register():
            self.courses.add(course)
            self.save()
            return True
        else:
            return False
     

    class Meta:
        unique_together = ('rollno', 'adm_year',)


class FeeTransaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, default="Pending")
    sem = models.IntegerField()
    year = models.IntegerField()

    def __str__(self):
        return str(self.id)+"_"+str(self.amount)


class subjectApplication(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    message = models.TextField(default="", blank=True, null=True)
    student = models.ForeignKey(
        Student, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message+'_'+str(self.id)


class Fees(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=200)  # semster,institue,hmc
    amount = models.FloatField()
    sem = models.IntegerField()

    def __str__(self):
        return self.name+'_'+str(self.amount)


def totalFees(objs):
    return objs.aggregate(models.Sum('amount'))


class Notification(models.Model):
    title = models.TextField()
    content = models.TextField()
    date = models.DateField(auto_now=True)
    sender = models.OneToOneField(
        usermodel, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ManyToManyField(usermodel, related_name="receiver")

    def __str__(self):
        return self.title
