from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

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
	filter_type= int(request.POST.get('filter_type', '1'))
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


def tags_main(request):
	context = {}
	return render(request, 'lessonsadmin/tags_main.html', context)

@csrf_exempt
def tags_filter(request):
	filter_type= request.POST.get('filter_type', 'label')
	filter_text= request.POST.get('filter_text', '')
	page= int(request.POST.get('page', '1'))

	tags_list= []
	tags_list= get_tags_list_from_fuseki_with_filter(filter_type, filter_text, page)
	
	context = {"tags_list": tags_list}
	return render(request, 'lessonsadmin/tags_list.html', context)

def tags_list(request):
	tags_list= get_tags_list_from_fuseki()
	return JsonResponse(tags_list, safe=False)
	

def tags_new(request):
	context = {"tag": None}
	return render(request, 'lessonsadmin/tags_form.html', context)

@csrf_exempt
def tags_create(request):
	label= request.POST.get('label', '')
	uri= request.POST.get('uri', '')

	tag = DomainTag();
	tag.label=label
	tag.uri=uri
	try:
		tag.save()	
		return JsonResponse({'status': 1, "msg": "Tag created succesfully"})
	except ValidationError, e:
		return JsonResponse({'status': 0, "msg": "URI is not in valid format"})

@csrf_exempt
def lessons_add_tag(request):
	lesson_id= request.POST.get('lesson_id', 0)
	uri= request.POST.get('tag[uri]')
	label= request.POST.get('tag[label]')
	l= Lesson.objects.get(number=lesson_id)
	if l != None:
		print l.tags
		ed = DomainTag(label= label, uri= uri)
		l.tags.append(ed)
		l.save()
	return JsonResponse({'status': 1, "msg": "Tag added succesfully"})

@csrf_exempt
def lessons_remove_tag(request):
	lesson_id= request.POST.get('lesson_id', 0)
	uri= request.POST.get('tag[uri]')
	print uri
	l= Lesson.objects.get(number=lesson_id)
	if l != None:
		print l.tags
		map={}
		for t in l.tags:
			map[t.uri]=t
		del map[uri]
		print "VALUES"
		print map.values()
		l.tags= map.values()
		l.save()
	return JsonResponse({'status': 1, "msg": "Tag added succesfully"})