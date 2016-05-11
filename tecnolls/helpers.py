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

def get_lessons_list_with_tags(query_tags, page):
	lessons = []
	lessons_list =[]
	if len(query_tags)==0:
		t_lessons_list = Lesson._get_collection().aggregate([
			{"$unwind": {"path": "$rates", "preserveNullAndEmptyArrays": True}},
			{"$group": {
				"_id":  "$_id", 
				"number": {"$first": "$number"},
				"pub_date": {"$first": "$pub_date"},
				"author": {"$first": "$author"},
				"title": {"$first": "$title"},
				"problem": {"$first": "$problem"},
				"tags": {"$first": "$tags"},
				"hitsCount": {"$first": "$hitsCount"},
				"problem": {"$first": "$problem"},
				"rating": { "$avg": "$rates.rate" }
			}},
			{"$sort": {"rating":-1}}
		])["result"];
	else:		
		t_lessons_list = Lesson._get_collection().aggregate([
			{"$project": {"hits": { "$setIntersection":[ "$tags.label", ["ORM"] ]}, "_id": 1, "number": 1, "pub_date": 1 , "author": 1 , "title": 1 , "problem": 1, "tags": 1, "rates": 1}},
			{"$project": {"hits": 1, "hitsCount": { "$size": "$hits"}, "tagsCount": { "$size": "$tags"}, "_id": 1, "number": 1, "pub_date": 1 , "author": 1 , "title": 1 , "problem": 1, "tags": 1, "rates": 1}},
			{"$match": {"hitsCount": {"$gt": 0 }} },
			{"$unwind": {"path": "$rates", "preserveNullAndEmptyArrays": True}},
			{"$group": {
				"_id":  "$_id", 
				"number": {"$first": "$number"},
				"pub_date": {"$first": "$pub_date"},
				"author": {"$first": "$author"},
				"title": {"$first": "$title"},
				"problem": {"$first": "$problem"},
				"tags": {"$first": "$tags"},
				"hits": {"$first": "$hits"},
				"hitsCount": {"$first": "$hitsCount"},
				"problem": {"$first": "$problem"},
				"rating": { "$avg": "$rates.rate" }
			}},
			{"$sort": {"hitsCount":-1, "tagsCount":1, "rating": -1}}
		])["result"];

	for l in t_lessons_list:
		author = User.objects().get(id= l['author'])			
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
		lesson.rate_avg= l['rating']
		lessons_list.append(lesson)
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
		lesson.rate_avg= l.rate_avg

		lessons_list.append(lesson)
	lessons_list = sorted(lessons_list, key= lambda l: l.rate_avg, reverse=True)	
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