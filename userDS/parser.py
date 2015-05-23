import re
from lxml import html as xpathDoc
from userDS.spojUser import spojUser
from datetime import datetime

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

class SpojParserError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def parse_user(contentTree):
	"""
	Parses name of the user_info_html
	"""
        ret = contentTree.xpath('./table[1]/tr[1]/td[2]//text()')[0]
        if len(ret) == 0:
            raise SpojParserError('Cannot Parse username')
        return ret

def parse_rank(contentTree):
	"""
	Parses the world rank of the user
	"""
        ret = contentTree.xpath('./p[1]//a/text()')[0][1:]
        if len(ret) == 0:
            raise SpojParserError('Cannot Parse rank')
        return ret

def parse_points(contentTree):
	"""
	Parses the total points of the user
	"""
        ret = contentTree.xpath('./p[1]/text()')[0].strip()[1:-8]
        if len(ret) == 0:
            raise SpojParserError('Cannot Parse points')
        return ret

def parse_problems(contentTree):
	"""
	Parses the solved Classical Problems
	"""
        pcodes = contentTree.xpath('.//b[contains(text(), "solved classical problems")]/following::table[1]/tr/td/a/text()')
	ret = set(pcodes)
	return ret

def user_page_parse(html, user_name):
	"""
	Handles Parsing of the user page
	"""
        doc = xpathDoc.fromstring(html)
        mainContent = doc.xpath('//td[@class="content0"]//td[@class="content"]')[0]

	name = parse_user(mainContent)
	World_Rank = parse_rank(mainContent)
	Points = parse_points(mainContent)
	Problems = parse_problems(mainContent)
	ret = spojUser(name, user_name, World_Rank, Points, Problems)
	return ret

def signed_list_parse(html, userds):
	ret = {}
	html = html.split('\n')
	regex = re.compile(r'\| +\d+ +\| +(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}) \| +([A-Z0-9_]+) \| +([A-Z0-9?.]+) \|.*?\|.*?\| *([^ \t\r\n\v\f]*) *\|')
	subs = []
	for line in html:
		result = regex.match(line)
		if result != None:
			date_of_sub = datetime(int(result.group(1)), int(result.group(2)), int(result.group(3)),int(result.group(4)), int(result.group(5)), int(result.group(6)))
			problem_id = result.group(7)
			sub_result = result.group(8)
			lng_sub = result.group(9)
			if is_number(sub_result):
				sub_result = 'AC'
			subs.append((date_of_sub, problem_id, sub_result, lng_sub))
	subs.reverse()
	for sub in subs:
		userds.merge_submission(*sub)
