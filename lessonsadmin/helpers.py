from lessonsadmin.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

PAGE_SIZE=5

def get_lessons_list_with_filter(filter_type, filter_p, page):
	lessons = []
	lessons_list = Lesson.objects.all()
	paginator = Paginator(lessons_list, PAGE_SIZE) # Show 25 contacts per page
	try:
		lessons = paginator.page(page)
	except PageNotAnInteger:
		lessons = paginator.page(1)
	except EmptyPage:
		lessons = paginator.page(paginator.num_pages)

	return lessons