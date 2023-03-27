from django.shortcuts import render

# Create your views here.
# import Http Response from django
from django.shortcuts import render

# create a function
def dashboard(request):
	# create a dictionary to pass
	# data to the template
	context ={
		"data":"some data",
		"list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	}
	# return response with template and context
	return render(request, "dashboard.html", context)
def research(request):
	# create a dictionary to pass
	# data to the template
	context ={
		"data":"some data",
		"list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	}
	# return response with template and context
	return render(request, "ProjectsPublications/research.html", context)
def calendar(request):
	# create a dictionary to pass
	# data to the template
	context ={
		"user":"Secretary",
		"list":[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	}
	# return response with template and context
	return render(request, "calendar.html", context)
def profile(request):
	# create a dictionary to pass
	# data to the template
	courses=[{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"},{"subno":"CS21204","name":"Formal Language Automata Theory","url":"/coursepage","type":"DEPTH CORE","LTP":"3-1-0","credits":"4.0","faculty":"Animesh Mukherjee , Soumyajit Dey","status":"Registered"}]    
	sgpa=[9.76,9.84,9.44,9.28]
	context ={
		"user":"Student",
		"backlogs":0,
		"courses":courses,
		"cgpa":9.29,
		"name":"Smarak Kanjilal",
		"rollno":"21CS30061",
		"gender":"Male",
		"department":"Department of Computer Science and Engineering",
		"course":"M.Tech Dual Degree 5Y",
		"nationality":"Indian",
		"hall":"Azad Hall",
		"aadhar":"531220019",
		"status":"On Roll",
		"EAA":"NSS - Unit 7",
		"adm_year": 2021,
		"adm_nature":"JEE",
		"primary_email":"smarakkanjilal@gmail.com",
		"inst_email":"smarakkanjilal@kgpian.iitkgp.ac.in",
		"teams_pass":"1jbs672h",
		"mobile":"9330223389",
		"guardian_email":"guardian@g.co",
		"address":"Harmony apartment, 28/1B, Nakuleswar Bhattacharya Lane ,Kolkata-70035",
		"location":"Kolkata",
		"pin":"700035",
		"state":"West Bengal",
		"cleared_sem_crd":24.0,
		"sem_crd":24.0,
		"cleared_tot_crd":73.0,
		"tot_crd":73.0,
		"sgpa":sgpa[-1]
	}
	# return response with template and context
	return render(request, "student-profile.html", context)
