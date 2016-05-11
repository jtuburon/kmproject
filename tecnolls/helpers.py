from tecnolls.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from mongoengine.django.auth import User


PAGE_SIZE=5

def get_users_list_with_filter(filter_type, filter_text, page):
	filter_p={}
	pattern= re.compile(filter_text, re.IGNORECASE)
	filter_p= {filter_type: pattern}

	users = []
	users_list = User.objects(__raw__=filter_p).order_by('username')
	paginator = Paginator(users_list, PAGE_SIZE) # Show 25 contacts per page
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	return users

def calculate_avg_rate(l):
	avg_result = Lesson._get_collection().aggregate([
					{"$match": {"number": l['number'] }},
					{ "$project": {
					    "_id": "$$ROOT",
					    "rates": 1
					}},
					{ "$unwind": "$rates" },                                                                                                                                                                          
					{ "$group": {
					    "_id": "$_id",
					    "rating": { "$avg": "$rates.rate" },
					}},
				])['result']
	return avg_result[0]['rating'] if len(avg_result) >0 else None

def get_lessons_list_with_tags(query_tags, page):
	lessons = []
	lessons_list =[]
	if len(query_tags)==0:
		t_lessons_list = Lesson.objects().all().order_by('-number')
	else:		
		t_lessons_list = Lesson._get_collection().aggregate([
			{"$project": {"hits": { "$setIntersection":[ "$tags.label", query_tags ]}, "_id": 1, "number": 1, "pub_date": 1 , "author": 1 , "title": 1 , "problem": 1, "tags": 1}},
			{"$project": {"hits": 1, "hitsCount": { "$size": "$hits"}, "tagsCount": { "$size": "$tags"}, "_id": 1, "number": 1, "pub_date": 1 , "author": 1 , "title": 1 , "problem": 1, "tags": 1}},
			{"$match": {"hitsCount": {"$gt": 0 }} },
			{"$sort": {"hitsCount":-1, "tagsCount":1}}
		])["result"]
	for l in t_lessons_list:
		author = l['author'] if len(query_tags)==0 else User.objects().get(id= l['author'])			
		lesson = LessonResult()
		lesson.number= l['number']
		lesson.author= author
		lesson.pub_date= l['pub_date']
		lesson.title= l['title']
		lesson.problem= l['problem']
		lesson.tags= l['tags']
		if len(query_tags)!=0:
			lesson.hits= l['hits']
			lesson.hits_count= l['hitsCount']
		lesson.rate_avg= calculate_avg_rate(l)
		lessons_list.append(lesson)
	if len(query_tags)!=0:
		lessons_list = sorted(lessons_list, key= lambda l: (l.hits_count, l.rate_avg), reverse= True)
	
	paginator = Paginator(lessons_list, PAGE_SIZE) # Show 25 contacts per page
	try:
		lessons = paginator.page(page)
	except PageNotAnInteger:
		lessons = paginator.page(1)
	except EmptyPage:
		lessons = paginator.page(paginator.num_pages)
	return lessons

def get_lessons_list_with_filter(filter_type, filter_text, page):

	filter_p={}
	filters_list=[]
	pattern= re.compile(filter_text, re.IGNORECASE)
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
	lessons = []
	lessons_list = []
	t_lessons_list= Lesson.objects(__raw__=filter_p).order_by('-number')
	for l in t_lessons_list:
		author = l['author']
		lesson = LessonResult()
		lesson.number= l['number']
		lesson.author= author
		lesson.pub_date= l['pub_date']
		lesson.title= l['title']
		lesson.problem= l['problem']
		lesson.tags= l['tags']
		lesson.rate_avg= calculate_avg_rate(l)
		lessons_list.append(lesson)
	paginator = Paginator(lessons_list, PAGE_SIZE) # Show 25 contacts per page
	try:
		lessons = paginator.page(page)
	except PageNotAnInteger:
		lessons = paginator.page(1)
	except EmptyPage:
		lessons = paginator.page(paginator.num_pages)
	return lessons


def get_tags_list_from_fuseki_with_filter(filter_type, filter_text, page):
	PAGE_SIZE=15
	tags = []
	sparql = SPARQLWrapper("http://127.0.0.1:3030/j2eedataset/sparql")
	query="""
		PREFIX owl: <http://www.w3.org/2002/07/owl#>
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		SELECT DISTINCT ?uri ?label
			{?uri rdf:type owl:NamedIndividual .
		  	 ?uri rdfs:label ?label
		  	 FILTER regex(str(?label), '%s', 'i')
			}
		ORDER BY ASC(lcase(?label))
	""" % filter_text
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)

	results = sparql.query().convert()

	tags_list = [DomainTag(label=result["label"]["value"] , uri=result["uri"]["value"] )for result in results["results"]["bindings"]]
	#tags_list= sorted(tags_list, key= lambda t: t.label.lower())
	
	paginator = Paginator(tags_list, PAGE_SIZE) # Show 25 contacts per page
	try:
		tags = paginator.page(page)
	except PageNotAnInteger:
		tags = paginator.page(1)
	except EmptyPage:
		tags = paginator.page(paginator.num_pages)
	return tags

def get_tags_list_from_fuseki():
	PAGE_SIZE=15
	tags = []
	sparql = SPARQLWrapper("http://127.0.0.1:3030/j2eedataset/sparql")
	query="""
		PREFIX owl: <http://www.w3.org/2002/07/owl#>
		PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		SELECT DISTINCT ?uri ?label
			{?uri rdf:type owl:NamedIndividual .
		  	 ?uri rdfs:label ?label
			}
		ORDER BY ASC(lcase(?label))
	"""
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	tags_list = [{"label": result["label"]["value"] , "uri":result["uri"]["value"]} for result in results["results"]["bindings"]]
	return tags_list