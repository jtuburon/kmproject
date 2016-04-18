from lessonsadmin.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

PAGE_SIZE=5

def get_lessons_list_with_filter(filter_type, filter_text, page):
	filter_p={}
	filters_list=[]
	pattern= re.compile(filter_text, re.IGNORECASE)
	print filter_type
	print filter_text
	if filter_type==1:
		filter_field="title"
		filters_list.append({filter_field: pattern})
	elif filter_type==2:
		filter_field="problem"
		filters_list.append({filter_field: pattern})
		filter_field="context"
		filters_list.append({filter_field: pattern})
		filter_field="solution"
		filters_list.append({filter_field: pattern})
	elif filter_type==3:
		filter_field="number"
		try:
			filters_list.append({filter_field: int(filter_text)})	
		except:
			filters_list.append({filter_field: filter_text})	
	
	filter_p= {"$or": filters_list}
	print filter_p
	lessons = []
	lessons_list = Lesson.objects(__raw__=filter_p).order_by('-number')
	paginator = Paginator(lessons_list, PAGE_SIZE) # Show 25 contacts per page
	try:
		lessons = paginator.page(page)
	except PageNotAnInteger:
		lessons = paginator.page(1)
	except EmptyPage:
		lessons = paginator.page(paginator.num_pages)

	return lessons

def get_tags_list_with_filter(filter_type, filter_text, page):
	print filter_text
	pattern= re.compile(filter_text, re.IGNORECASE)
	filter_p={filter_type: pattern}
	print filter_p
	tags = []
	tags_list = DomainTag.objects(__raw__=filter_p).order_by('label')
	paginator = Paginator(tags_list, PAGE_SIZE) # Show 25 contacts per page
	try:
		tags = paginator.page(page)
	except PageNotAnInteger:
		tags = paginator.page(1)
	except EmptyPage:
		tags = paginator.page(paginator.num_pages)
	return sorted(tags, key= lambda t: t.label.lower())