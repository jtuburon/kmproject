from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from helpers import *

from lessonsadmin.models import *

# Create your views here.

def index(request):
	context= {}
	return render(request, 'lessonsadmin/index.html', context)

def show_info(request):
	context = {}
	return render(request, 'lessonsadmin/info_main.html', context)

def lessons_main(request):
	context = {}
	return render(request, 'lessonsadmin/lessons_main.html', context)

@csrf_exempt
def lessons_filter(request):
	filter_type= int(request.POST.get('filter_type', '0'))
	filter_text= request.POST.get('filter_text', '')
	page= int(request.POST.get('page', '1'))

	lessons_list= []
	lessons_list= get_lessons_list_with_filter(filter_type, filter_text, page)
	context = {"lessons_list": lessons_list}
	return render(request, 'lessonsadmin/lessons_list.html', context)

def lessons_new(request):
	context = {"lesson": None}
	return render(request, 'lessonsadmin/lessons_form.html', context)

@csrf_exempt
def lessons_create(request):
	project= request.POST.get('project', '')
	leader= request.POST.get('leader', '')
	author= request.POST.get('author', '')
	role= request.POST.get('role', '')
	title= request.POST.get('title', '')
	problem= request.POST.get('problem', '')
	context= request.POST.get('context', '')
	solution= request.POST.get('solution', '')

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