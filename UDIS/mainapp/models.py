from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import json

class usermodel(models.Model):
	created_At = models.DateTimeField(null=True ,blank=True,auto_now=True)
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
	prerequisites=models.ManyToManyField("self",related_name="prerequisites",blank=True,null=True)
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
	courses=models.ManyToManyField(Course,blank=True,null=True)
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
	date=models.DateField()
	def __str__(self):
		return self.id+"_"+self.amount


class Secretary(usermodel):
	mobile=models.CharField(max_length=200)
	def __str__(self):
		return self.name
	
	
class Student(usermodel):
	state = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	pin_code = models.IntegerField(null=True ,blank=True)
	backlogs=models.IntegerField(default=0)
	courses=models.ManyToManyField(Course,blank=True,null=True)
	cgpa=models.CharField(max_length=200,default="""{"cgpa":["-"]}""")
	rollno=models.CharField(max_length=200,null=True ,blank=True)
	gender=models.TextField(default="N/A")
	# department=models.CharField(max_length=200)
	course=models.CharField(max_length=200,blank=True,default="B.Tech 4Y")
	hall=models.CharField(max_length=200,default="N/A")
	aadhar=models.CharField(max_length=200,null=True ,blank=True)
	status=models.CharField(max_length=200,default="On-Roll")
	EAA=models.CharField(max_length=200,null=True ,blank=True)
	adm_year=models.DateField(auto_now=True)
	nationality=models.CharField(max_length=200,default="Indian")
	adm_nature=models.CharField(max_length=200,default="JEE")
	inst_email=models.EmailField(null=True ,blank=True)
	teams_pass=models.CharField(max_length=200,null=True ,blank=True)
	mobile=models.CharField(max_length=200,default="N/A")
	guardian_email=models.EmailField(null=True ,blank=True)
	address=models.TextField(null=True ,blank=True)
	location=models.CharField(max_length=200,null=True ,blank=True)
	cleared_sem_crd=models.FloatField(default=0)
	sem_crd=models.FloatField(default=0)
	cleared_tot_crd=models.FloatField(default=0)
	tot_crd=models.FloatField(default=0)
	sgpa=models.CharField(max_length=200,default="""{"sgpa":["-"]}""")
	sem=models.IntegerField(default=1)
	feespaid=models.FloatField(default=0)
	totalpaid=models.FloatField(default=0)
	regdone=models.CharField(max_length=10,default="Yes")
	def updatePaid(self,amt):
		self.totalpaid+=amt
	def __str__(self):
		return self.name
	def getsgpa(self):
		print(self.sgpa)
		return json.loads(self.sgpa)["sgpa"]
		# return [9]
	def addsgpa(self,sg):
	   
		return json.dumps("{ \"sgpa\": "+str(self.getsgpa()+[sg])+"}")
	def getcgpa(self):
		print(self.cgpa)
		# return [9]
		return json.loads(self.cgpa)["cgpa"]
	def addcgpa(self,sg):
		return json.dumps("{ \"cgpa\": "+str(self.getcgpa()+[sg])+"}")
	class Meta:
	  unique_together = ('rollno', 'adm_year',)
   
class FeeTransaction(models.Model):
	id=models.BigAutoField(primary_key=True)
	student=models.OneToOneField(Student, on_delete=models.CASCADE)
	amount=models.CharField(max_length=200)
	datetime=models.DateTimeField()
	status=models.CharField(max_length=200,default="Pending")
	sem=models.IntegerField()
	year=models.IntegerField()
	
	def __str__(self):
		return self.id+"_"+self.amount

class Fees(models.Model):
	name=models.CharField(max_length=255)
	type=models.CharField(max_length=200)#semster,institue,hmc
	amount=models.FloatField()
	sem=models.IntegerField()
	
	def __str__(self):
		 return self.name+'_'+self.amount

def totalFees(objs):
	return objs.aggregate(models.Sum('amount'))

	 
class Notification(models.Model):
	title=models.TextField()
	content=models.TextField()
	date=models.DateField(auto_now=True)
	sender=models.OneToOneField(usermodel,related_name="sender",on_delete=models.CASCADE)
	receiver=models.ManyToManyField(usermodel,related_name="receiver")
	def __str__(self):
		return self.title
	
	

