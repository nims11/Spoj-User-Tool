from django.db import models
from django.http import HttpResponse
import re
import urllib2
import logging
import pickle
import base64
from google.appengine.api import urlfetch
regex = re.compile(r'<td><a href="/ranks/([A-Z0-9_]+)" title="Value [0-9]+\.?[0-9]* points. See the best solutions.">([0-9]+)</a></td>')
last_regex = re.compile(r'<a href="/problems/classical/sort=0,start=([0-9]+)" class="pager_link">&gt;</a>')
# Create your models here.
class ProblemClassical(models.Model):
	_data = models.TextField(db_column='data')
	def set_data(self, data):
		self._data = base64.encodestring(data)
	def get_data(self):
		return base64.decodestring(self._data)

	data = property(get_data, set_data)


def parsePage(html, tar_dict):
	res = regex.finditer(html)
	for match in res:
		tar_dict[match.group(1)] = match.group(2)
		logging.info(match.group(1) + ' ' + match.group(2))

def iterPages():
	res = {}
	prefix = 'http://www.spoj.com/problems/classical/sort=0,start='
	html = urlfetch.fetch(prefix+'0', deadline=30).content
	parsePage(html, res)
	end = 0
	match = last_regex.search(html)
	if match:
		end = int(match.group(1))
	step = 50
	curr = step
	
	logging.info('Going through problem pages, curr = %d, step = %d, end = %d' % (curr, step, end))
	for i in xrange(curr, end+1, step):
		html = urlfetch.fetch(prefix+str(i), deadline=30).content
		parsePage(html, res)
	
	ProblemClassical.objects.all().delete()
	ProblemClassical(data=pickle.dumps(res)).save()

def gen(request, x):
	iterPages()
	return HttpResponse('done')