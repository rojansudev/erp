from django.shortcuts import render,get_object_or_404, get_list_or_404
from .models import Enroll,Section,Student, Stream, Course
from django.db.models import Q
import time
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse


import collections

# Create your views here.

weekdays = ["mon", "tue", "wed", "thu", "fri", "sat"]

hourtime=collections.OrderedDict()

hourtime[1]='8:00 A.M'
hourtime[2]='9:00 A.M'
hourtime[3]='10:00 A.M'
hourtime[4]='11:00 A.M'
hourtime[5]='12:00 P.M'
hourtime[6]='1:00 P.M'
hourtime[7]='2:00 P.M'
hourtime[8]='3:00 P.M'
hourtime[9]='4:00 P.M'
hourtime[10]='5:00 P.M'
hourtime[11]='6:00 P.M'

#login users
def login(request):
	return render(request, 'studentsystem/login.html')

#authenticate users and add session
def authenticate(request):
	student = get_object_or_404(Student, pk=request.POST['student_id'])
	if(student.password == request.POST['student_password']):
		request.session['student_id'] = request.POST['student_id']
		request.session['student_name'] = student.student_name
		#request.session.modified = True
		return HttpResponseRedirect(reverse('studentsystem:menu'))
	else:
		return HttpResponse("The password doesnot match")

#menu of options
def menu(request):
	context = {
	'student_name' : request.session['student_name'],
	'student_id' : request.session['student_id']
	}
	return render(request, 'studentsystem/menu.html', context)

def viewcurrent(request):
	#getting stream id and student semester
	student = get_object_or_404(Student, pk=request.session['student_id'])

	#getting department offering above stream
	dept = get_object_or_404(Stream, pk=student.stream_id)

	#getting all the courses offered by the above dept
	courses = get_list_or_404(Course, dept_name=dept.dept_name, course_year=student.current_year, course_sem=student.current_sem)

	#getting list of course_id
	course_ids = []
	for course in courses:
		course_ids.append("-".join(course.course_id.split(' ')))

	course_objid = []
	itr = 0
	for course in courses:
		course_objid.append({})
		course_objid[itr][1] = course
		course_objid[itr][2] = course_ids[itr]
		itr += 1  


	return render(request, 'studentsystem/viewcurrent.html', {'courses': course_objid})

def CourseDetails(request, course_id):
    org_courseid = " ".join((course_id.split('-')))
    course = get_object_or_404(Course, pk=org_courseid)
    sections=get_list_or_404(Section,course_id=org_courseid)
    return render(request, 'studentsystem/CourseDetails.html', {'course':course,'temp':course_id,'sections':sections})

#get academic history
def history(request):

    #getting grades and courses completed
    courses = get_list_or_404(Enroll, course_status='Completed', student_id=request.session['student_id'])  
    #getting courses details of each course
    finalList = []
    total_credits = 0
    total_score = 0
    gradetoScore = {'A' : 10, 'A-' : 9, 'B' : 8, 'B-': 7, 'C' : 6, 'C-' : 5, 'E' : 2, 'NC' : 0}
    for course in courses:
        result = get_object_or_404(Course, pk=course.course_id)
        total_credits += result.course_credits
        total_score += gradetoScore[course.course_grade]*result.course_credits
        finalList.append({'course_id':result.course_id, 'course_name': result.course_name, 'credits': result.course_credits, 'grade' : course.course_grade})
    cgpa = "NA"
    if(total_credits > 0):
        cgpa = "{:.2f}".format(total_score/total_credits)
    return render(request, 'studentsystem/history.html', {'finalList': finalList, 'cgpa':cgpa})

#show all registered courses
def showregistered(request):
    #getting all the courses enrolled by student which are currently running
    courses = get_list_or_404(Enroll, course_status='Running', student_id=request.session['student_id'])    
    #getting names of the courses
    finalList = []
    for course in courses:
        result = get_object_or_404(Course, pk=course.course_id)
        finalList.append({'course_id':result.course_id, 'course_name':result.course_name, 'credits': result.course_credits})    
    return render(request, 'studentsystem/showregistered.html', {'finalList': finalList})


#create schedule
def viewSchedule(student_id):
    
    #creating calender object
    calendar = {}
    hours = {}
    for i in range(1,12):
        hours[hourtime[i]] = ' '
    for day in weekdays:
        calendar[day] = hours.copy()

    #getting all the courses enrolled by student which are currently running
    result=Enroll.objects.filter(Q(student=student_id) & Q(course_status='Running')).values('course_id')

    enrolled=[]
    for obj in result:
        enrolled.append(obj['course_id'])
            
    #getting all the sections of the courses enrolled
    sections=Section.objects.filter(course_id__in=enrolled).values()

    #placing sections in calendar
    for section in sections:
        entry = section['course_id'] + ', ' + section['section_type'] + ', ' + section['location']
        hour = section['section_hour']
        for day in weekdays:
            if section[day]:
                if section['section_type']=='Lab':
                    calendar[day][hourtime[hour]]=entry
                    calendar[day][hourtime[hour+1]]=entry
                else:
                    calendar[day][hourtime[hour]]=entry

    return calendar


#check clash
def checkClash(student_id,to_enroll_id):

    calendar = viewSchedule(student_id)
    
    #get sections of course to enroll
    sections=Section.objects.filter(course_id=to_enroll_id).values()

    #check clash
    for section in sections:
        entry = section['course_id'] + ', ' + section['section_type'] + ', ' + section['location']
        hour = section['section_hour']
        for day in weekdays:
            if section[day]:
                if section['section_type']=='Lab':
                    if calendar[day][hourtime[hour]]==' ' and calendar[day][hourtime[hour+1]]==' ':
                        calendar[day][hourtime[hour]]=entry
                        calendar[day][hourtime[hour+1]]=entry
                    else:
                        if calendar[day][hourtime[hour]]!=' ':
                            return [True,calendar[day][hourtime[hour]]]
                        return [True,calendar[day][hourtime[hour+1]]]    
                else:
                    if calendar[day][hourtime[hour]]==' ':
                        calendar[day][hourtime[hour]]=entry
                    else:
                        return [True,calendar[day][hourtime[hour]]]


    return [False,None]


#register to course
def registerForm(request):
    
    if request.method=='GET':
        return render(request,'studentsystem/course_register.html')

    else:
        student_id=request.session['student_id']
        to_enroll=request.POST['courseno']

        res=checkClash(student_id,to_enroll)
        if res[0]:
            return render(request,'studentsystem/enroll_result.html',{'res':'Clash with course '+res[1]})
        else:
            now=time.strftime('%Y-%m-%d')
            obj=Enroll(student_id=student_id,course_id=to_enroll,course_grade='NA',enroll_date=now,course_status='Running') 
            obj.save()
            return render(request,'studentsystem/enroll_result.html',{'res':"You are registered to "+ to_enroll})

#register to course from course details page
def registerDirect(request,course_id):
    org_courseid = " ".join((course_id.split('-')))
    course = get_object_or_404(Course, pk=org_courseid)
    sections=get_list_or_404(Section,course_id=org_courseid)
    student_id=request.session['student_id']
    to_enroll=org_courseid

    
    try:
        obj=Enroll.objects.get(course_id=to_enroll)
        if obj.course_status=='Running':
            msg="You are already registered to course"
        else:
            msg="Cannot register,You have taken it in previous semester"    
        return render(request, 'studentsystem/CourseDetails.html', {'course':course,'msg':msg,'temp':course_id,'sections':sections})
    except (KeyError, Enroll.DoesNotExist):
        res=checkClash(student_id,to_enroll)
    
        if res[0]:
            msg='Clash with course '+res[1]
        else:
            now=time.strftime('%Y-%m-%d')
            obj=Enroll(student_id=student_id,course_id=to_enroll,course_grade='NA',enroll_date=now,course_status='Running') 
            obj.save()
            msg="You are registered to "+ to_enroll
            

        return render(request, 'studentsystem/CourseDetails.html', {'course':course,'msg':msg,'temp':course_id,'sections':sections})
        

    
#view schedule
def schedule(request):
    student_id=request.session['student_id']
    calendar=viewSchedule(student_id)

    return render(request,'studentsystem/schedule.html',{'calendar':calendar,'hourtime':hourtime})
