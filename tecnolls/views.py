from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from django.contrib.auth import login
from mongoengine.queryset import DoesNotExist
from django.contrib import messages

from helpers import *

from tecnolls.models import *
from mongoengine.django.auth import User

# Create your views here.

def index(request):
	context= {"admin": request.session["admin"]} if "admin" in request.session else {}
	return render(request, 'tecnolls/index.html', context)

@csrf_exempt
def login(request):
    try:
    	username= request.POST.get('username', '')
    	password= request.POST.get('password', '')
    	user = User.objects.get(username= username)
        if user.check_password(password):
			user.backend = 'mongoengine.django.auth.MongoEngineBackend'
			request.session["user"] = user.username
			request.session["admin"] = user.is_superuser
			return JsonResponse({'status': 1, "msg": "Login OK"})
        else:
            return JsonResponse({'status': 0, "msg": "Invalid password"})
    except DoesNotExist:
        return JsonResponse({'status': 0, "msg": "Invalid password"})

@csrf_exempt
def signup(request):
	firstname= request.POST.get('firstname', '')
	lastname= request.POST.get('lastname', '')
	username= request.POST.get('username', '')
	password= request.POST.get('password', '')
	email= request.POST.get('email', '')    	
	user = User(first_name = firstname, last_name= lastname, username= username, password= password,  email= email)
	user.set_password(password)
	user.save()
	user.backend = 'mongoengine.django.auth.MongoEngineBackend'
	request.session["user"] = user.username
	request.session["admin"] = user.is_superuser
	return JsonResponse({'status': 1, "msg": "SignUp OK"})

@csrf_exempt
def logout(request):
	del request.session["user"]
	del request.session["admin"]
	return JsonResponse({'status': 1, "msg": "Logout OK"})

def users_main(request):
	context = {}
	return render(request, 'tecnolls/users_main.html', context)


@csrf_exempt
def users_filter(request):
	filter_type= request.POST.get('filter_type', '')
	filter_text= request.POST.get('filter_text', '')
	page= int(request.POST.get('page', '1'))
	users_list= get_users_list_with_filter(filter_type, filter_text, page)
	context = {"users_list": users_list}
	return render(request, 'tecnolls/users_list.html', context)

def show_info(request):
	context = {}
	return render(request, 'tecnolls/info_main.html', context)

def lessons_index(request):
	context = {}
	return render(request, 'tecnolls/lessons_index.html', context)


def lessons_main(request):
	context = {}
	return render(request, 'tecnolls/lessons_main.html', context)

@csrf_exempt
def lessons_filter(request):
	filter_type= int(request.POST.get('filter_type', '1'))
	filter_text= request.POST.get('filter_text', '')
	page= int(request.POST.get('page', '1'))

	lessons_list= []
	lessons_list= get_lessons_list_with_filter(filter_type, filter_text, page)
	context = {"lessons_list": lessons_list}
	return render(request, 'tecnolls/lessons_list.html', context)

@csrf_exempt
def lessons_search(request):
	query_tags = request.POST.getlist('query_tags[]')
	page= int(request.POST.get('page', '1'))
	lessons_list= []
	lessons_list= get_lessons_list_with_tags(query_tags, page)
	context = {"lessons_list": lessons_list}
	return render(request, 'tecnolls/lessons_result.html', context)

def lessons_new(request):
	context = {"lesson": None, "readOnly": False}
	return render(request, 'tecnolls/lessons_form.html', context)


@csrf_exempt
def lessons_create(request):
	if "user" in request.session:	
		project= request.POST.get('project', '')
		leader= request.POST.get('leader', '')
		role= request.POST.get('role', '')
		title= request.POST.get('title', '')
		problem= request.POST.get('problem', '')
		context= request.POST.get('context', '')
		solution= request.POST.get('solution', '')

		author= User.objects.get(username= request.session["user"])
		
		lesson = Lesson();
		lesson.project=project
		lesson.leader=leader
		lesson.author=author
		lesson.role=role
		lesson.title=title
		lesson.problem=problem
		lesson.context=context
		lesson.solution=solution

		lesson.save()
		return JsonResponse({'status': 1, "msg": "Lesson created succesfully"})
	else:
		return JsonResponse({'status': 0, "msg": "Lesson was not created. Session is closed"})
@csrf_exempt
def lessons_edit(request):
	lesson_id= request.POST.get('lesson_id', 0)
	lesson = Lesson.objects.get(number=lesson_id) if lesson_id>0 else None
	context = {"lesson": lesson, "readOnly": False}
	return render(request, 'tecnolls/lessons_form.html', context)


@csrf_exempt
def lessons_update(request):
	project= request.POST.get('project', '')
	leader= request.POST.get('leader', '')
	role= request.POST.get('role', '')
	title= request.POST.get('title', '')
	problem= request.POST.get('problem', '')
	context= request.POST.get('context', '')
	solution= request.POST.get('solution', '')

	lesson_id= request.POST.get('lesson_id', 0)
	lesson = Lesson.objects.get(number=lesson_id) if lesson_id>0 else None
	if lesson != None:
		lesson.project=project
		lesson.leader=leader
		lesson.role=role
		lesson.title=title
		lesson.problem=problem
		lesson.context=context
		lesson.solution=solution

		lesson.save()
		return JsonResponse({'status': 1, "msg": "Lesson updated succesfully"})
	else:
		return JsonResponse({'status': 0, "msg": "Lesson doesn't exist"})

@csrf_exempt
def lessons_show(request):
	lesson_id= request.POST.get('lesson_id', 0)
	lesson = Lesson.objects.get(number=lesson_id) if lesson_id>0 else None
	context = {"lesson": lesson, "readOnly": True}
	return render(request, 'tecnolls/lessons_form.html', context)


@csrf_exempt
def lessons_rate(request):
	lesson_id= request.POST.get('lesson_id', 0)
	lesson_rate= request.POST.get('lesson_rate', 0)
	lesson = Lesson.objects.get(number=lesson_id) if lesson_id>0 else None
	if lesson_id != None:
		user= User.objects.get(username= request.session["user"])
		rate = LessonRate(rate= lesson_rate, user=user)
		lesson.rates.append(rate)
		lesson.save()
		return JsonResponse({'status': 1, "msg": "Lesson was rated succesfully"})
	else:
		return JsonResponse({'status': 1, "msg": "Lesson was not rated"})

def tags_main(request):
	context = {}
	return render(request, 'tecnolls/tags_main.html', context)

@csrf_exempt
def tags_filter(request):
	filter_type= request.POST.get('filter_type', 'label')
	filter_text= request.POST.get('filter_text', '')
	page= int(request.POST.get('page', '1'))

	tags_list= []
	tags_list= get_tags_list_from_fuseki_with_filter(filter_type, filter_text, page)
	
	context = {"tags_list": tags_list}
	return render(request, 'tecnolls/tags_list.html', context)

def tags_list(request):
	tags_list= get_tags_list_from_fuseki()
	return JsonResponse(tags_list, safe=False)

@csrf_exempt
def lessons_add_tag(request):
	lesson_id= request.POST.get('lesson_id', 0)
	uri= request.POST.get('tag[uri]')
	label= request.POST.get('tag[label]')
	l= Lesson.objects.get(number=lesson_id)
	if l != None and uri!= None and label!=None:
		ed = DomainTag(label= label, uri= uri)
		l.tags.append(ed)
		l.save()
	return JsonResponse({'status': 1, "msg": "Tag added succesfully"})

@csrf_exempt
def lessons_remove_tag(request):
	lesson_id= request.POST.get('lesson_id', 0)
	uri= request.POST.get('tag[uri]')
	l= Lesson.objects.get(number=lesson_id)
	if l != None:
		map={}
		for t in l.tags:
			map[t.uri]=t
		del map[uri]
		l.tags= map.values()
		l.save()
	return JsonResponse({'status': 1, "msg": "Tag removed succesfully"})

