from lessonsadmin.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from SPARQLWrapper import SPARQLWrapper, JSON

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