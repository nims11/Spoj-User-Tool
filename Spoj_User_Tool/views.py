from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render
from userDS.parser import user_page_parse, signed_list_parse
from userDS.spojUser import spojUser
import urllib2
from google.appengine.api import urlfetch
def home(request):
	return render(request, 'home.html')

def single_user(request, user_name):
	#html = urllib2.urlopen('http://www.spoj.pl/users/'+user_name).read()
	#html = urllib2.urlopen('http://localhost/nims11.htm').read()
	html = urlfetch.fetch('http://www.spoj.pl/users/'+user_name, deadline=30).content
	html = html.replace('\n','')
	#print 'Got the File!'
	ret = ''
	# user_info -> user, world rank, points, and classical problems solved
	user_info = user_page_parse(html, user_name)

	# parsing signed list
	#signed_html = urllib2.urlopen('http://www.spoj.pl/status/'+user_name+'/signedlist/').read()
	#signed_html = urllib2.urlopen('http://localhost/signedlist').read()
	#print 'Got the Other File!'
	signed_html = urlfetch.fetch('http://www.spoj.pl/status/'+user_name+'/signedlist/', deadline=30).content
	problem_info = signed_list_parse(signed_html, user_info)
	user_info.probPool.calc_stats()
	user_info.get_classical_table()
	return render(request, 'single.html',{'main': user_info})
