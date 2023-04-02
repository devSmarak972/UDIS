from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import json

class usermodel(models.Model):
	created_At = models.DateTimeField(null=True)
	primary_email=models.EmailField()
	name=models.CharField(max_length=200)
	department=models.TextField()
	def get_derived_type(self):
		if self.derived_type ==  'Secretary':
			return "secretary"
		elif self.derived_type == 'Student':
			return "student"
	# class Meta:
	# 	abstract = True
  
  
class Course(models.Model):
	subno=models.CharField(max_length=200)
	name=models.TextField()
	url=models.CharField(max_length=200)
	type=models.CharField(max_length=200)
	mode=models.CharField(max_length=200)#rtheory or lab
	LTP=models.CharField(max_length=200)
	credits=models.IntegerField()
	sem=models.IntegerField()
	session=models.IntegerField()#starting year
	prerequisites=models.ManyToManyField("self",related_name="prerequisites")
	def __str__(self):
		return self.name
 
	
class Publication(models.Model):           
	name=models.TextField()
	abstract=models.TextField()
	url=models.CharField(max_length=200)
	type=models.CharField(max_length=200)
	place=models.TextField()
	date=models.DateField()
	def __str__(self):
		return self.name
 
	
class Experience(models.Model):
	organisation=models.CharField(max_length=200)
	startDate=models.DateField()
	endDate=models.DateField()
	type=models.CharField(max_length=200)
	def __str__(self):
		return self.organisation+" "+self.type
	
	
class Professor(usermodel):
	# name=models.CharField(max_length=200)
	# department=models.CharField(max_length=200)
	mobile=models.CharField(max_length=200)
	courses=models.ManyToManyField(Course)
	education=models.ManyToManyField(Experience,related_name="education")
	workex=models.ManyToManyField(Experience,related_name="workexperience")
	publications=models.ManyToManyField(Publication)
	def __str__(self):
		return self.name
	
class Item(models.Model):
	name=models.CharField(max_length=200)
	count=models.IntegerField()
	expenditure=models.CharField(max_length=200)
	def __str__(self):
		return self.name
class Order(models.Model):
	item=models.CharField(max_length=200)
	qty=models.IntegerField()
	price=models.FloatField()
	status=models.CharField(max_length=200)#confirmed,recieved
	def __str__(self):
		return self.item
class Person(models.Model):
	name=models.CharField(max_length=200)
	email=models.EmailField()
	def __str__(self):
		return self.name
	
class Transaction(models.Model):
	id=models.BigAutoField(primary_key=True)
	person=models.ForeignKey(Person, on_delete=models.CASCADE)
	amount=models.CharField(max_length=200)
	
	def __str__(self):
		return self.id+"_"+self.amount

class Secretary(usermodel):
	mobile=models.CharField(max_length=200)
	def __str__(self):
		return self.name
	
	
class Student(usermodel):
	state = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	pin_code = models.IntegerField()
	backlogs=models.IntegerField()
	courses=models.ManyToManyField(Course)
	cgpa=models.CharField(max_length=200)
	rollno=models.CharField(max_length=200)
	gender=models.TextField()
	# department=models.CharField(max_length=200)
	course=models.CharField(max_length=200)
	hall=models.CharField(max_length=200)
	aadhar=models.CharField(max_length=200)
	status=models.CharField(max_length=200)
	EAA=models.CharField(max_length=200)
	adm_year=models.DateField()
	nationality=models.CharField(max_length=200)
	adm_nature=models.CharField(max_length=200)
	inst_email=models.EmailField()
	teams_pass=models.CharField(max_length=200)
	mobile=models.CharField(max_length=200)
	guardian_email=models.EmailField()
	address=models.TextField()
	location=models.CharField(max_length=200)
	pin=models.CharField(max_length=200)
	state=models.CharField(max_length=200)
	cleared_sem_crd=models.FloatField()
	sem_crd=models.FloatField()
	cleared_tot_crd=models.FloatField()
	tot_crd=models.FloatField
	sgpa=models.CharField(max_length=200)
	def __str__(self):
		return self.name
	def getsgpa(self):
		return json.load(self.sgpa)["sgpa"]
	def addsgpa(self,sg):
		return json.dumps("{ 'sgpa': "+str(self.getsgpa()+[sg])+"}")
	def getcgpa(self):
		return json.load(self.sgpa)["cgpa"]
	def addcgpa(self,sg):
		return json.dumps("{ 'cgpa': "+str(self.getcgpa()+[sg])+"}")
	 
class Notification(models.Model):
	title=models.TextField()
	content=models.TextField()
	date=models.DateField(auto_now=True)
	sender=models.OneToOneField(usermodel,related_name="sender",on_delete=models.CASCADE)
	receiver=models.ManyToManyField(usermodel,related_name="receiver")
	def __str__(self):
		return self.title
	
	

