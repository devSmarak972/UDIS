
from ..models import *
import datetime
from django import template
register = template.Library()


@register.filter
def at_index(array, index):
	return array[index]


@register.filter
def getCgpa(student):
	return student.getcgpa()


@register.filter
def arr_contains(array, item):
	if item in array:
		return True
	else:
		return False


@register.filter
def to_str(project):
	str = ""
	array = project.professor_set.all()
	for item in array:
		str += item.name+","
	return str[:-2]


@register.filter
def prereq(course):
	str = ""
	print(course.name)
	array = course.prerequisites.all()
	print(array)
	for item in array:
		str += item.subno+","
	return str[:-1]


@register.filter
def multiply(a, b):
	return a*b


@register.filter
def getStudents(attendance):
	return attendance.student.all()


@register.filter
def prevDate(date):
	now = datetime.datetime.strptime(date, '%B %d, %Y')
	now -= datetime.timedelta(days=1)
	return datetime.datetime.strftime(now, "%d-%m-%Y")


@register.filter
def nextDate(date):
	now = datetime.datetime.strptime(date, '%B %d, %Y')
	now += datetime.timedelta(days=1)
	return datetime.datetime.strftime(now, "%d-%m-%Y")


@register.filter
def getdate(course):
	# now = datetime.datetime.strptime(date, '%B %d, %Y')
	# now+=datetime.timedelta(days=1)
	return datetime.datetime.strftime(datetime.datetime.now(), "%d-%m-%Y")


@register.filter
def grade(student,course):
	# now = datetime.datetime.strptime(date, '%B %d, %Y')
	# now+=datetime.timedelta(days=1)
	grade = Grades.objects.filter(student=student.id, course=course)
	print(grade)
	if len(grade)>0:
		print("grades",grade[0].grade)
		return grade[0].grade
	else :
		return "-"



@register.filter
def getProfs(course):
	str = ""
	profs = course.professor_set.all()
	for prof in profs:
		str += prof.name+", "
	return str[:-2]
