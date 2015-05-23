from django.db import models
from django.http import HttpResponse
import re
import urllib2
import logging
import pickle
import base64
from lxml import html as xpathDoc
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

def getNextUrl(contentTree):
    try:
        urls = contentTree.xpath('//table[@class="navigation"]//a[text()="Next"]/@href')
    except:
        return False
    if len(urls) == 0:
        return False
    return 'http://www.spoj.com'+urls[0]

def iterPages():
	res = {}
	url = 'http://www.spoj.com/SPOJ/problems/classical/'
        while url != False:
            logging.info('URL: '+url)
            html = urlfetch.fetch(url, deadline=30).content
            doc = xpathDoc.fromstring(html)
            for row in doc.xpath('//tr[@class="problemrow"]'):
                pcode = row.xpath('./td[3]/a/text()')[0].strip()
                users = row.xpath('./td[4]/a/text()')[0].strip()
                res[pcode] = users
                logging.info(pcode+': '+users)
            url = getNextUrl(doc)
        ProblemClassical.objects.all().delete()
        ProblemClassical(data=pickle.dumps(res)).save()

def gen(request, x):
	iterPages()
	return HttpResponse('done')
