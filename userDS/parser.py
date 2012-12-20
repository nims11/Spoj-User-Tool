import re
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

def parse_user(user_info_html):
	"""
	Parses name of the user_info_html
	"""
	user_rx = re.compile(r'<H3> *(.*?)\'s user data *</H3>')
	result = user_rx.match(user_info_html)
	if result == None:
		raise SpojParserError('User Parsing Error with RegExp')
	else:
		return result.group(1)

def parse_rank(user_info_html):
	"""
	Parses the world rank of the user
	"""
	rank_rx = re.compile(r'.*?<b>Current world rank: <a href="/ranks/users/start=\d+">#(\d+)</a></b>.*?')
	world_leader_rx = re.compile(r'.*?<b>Current world rank: <a href="/ranks/users/start=0">world leader</a></b>.*?')
	result = rank_rx.match(user_info_html)
	if result == None:
		# If world leader
		result = world_leader_rx.match(user_info_html)
		if result == None:
			raise SpojParserError('World Rank Parsing Error with RegExp')
		else:
			return '1'
	else:
		return result.group(1)

def parse_points(user_info_html):
	"""
	Parses the total points of the user
	"""
	points_rx = re.compile(r'.*?<p align="center"><b>Current world rank: <a href="/ranks/users/start=\d+">.*?</a></b><br><br>\((\d+\.{0,1}\d*) points\)</p>.*?')
	result = points_rx.match(user_info_html)
	if result == None:
		raise SpojParserError('Points Parsing Error with RegExp')
	else:
		return result.group(1)

def parse_problems(html, user):
	"""
	Parses the solved Classical Problems
	"""
	ret = set([])
	problem_rx = re.compile(r'.*?<a href="/status/([A-Z0-9_]+)\,'+user+r'/">.*?')
	html2 = html.split('</td>')
	for line in html2:
		result = problem_rx.match(line)
		if result != None:
			ret.add(result.group(1))
	return ret

def user_page_parse(html, user_name):
	"""
	Handles Parsing of the user page
	"""
	html = html[html.find(r'<H3>'):]  # Trims the unneccessary starting of the page
	ret = {}				# dict holding the parsed keys and values
	if len(html) <4:
		raise SpojParserError('Assumed Starting Tag not found')
	end = html.find(
		'<b title="List of problems to which solutions were submitted but none of them got AC.">TODO list of classical problems:</b>'
		)
	if end==-1:
		raise SpojParserError('Assumed Ending Tag not found')
	html = html[:end]	# Trims the unneccessary ending of the page

	user_info_end = html.find('<table class="problems" width="90%">')	# Gets the end for user_info section
	if user_info_end == -1:
		raise SpojParserError('Assumed Ending Tag for user_info not found')
	user_info_html = html[:user_info_end]
	user_info_html = user_info_html.replace('\n', '')
	html = html[user_info_end:] 	# Now contains only the solved classical problems part

	name = parse_user(user_info_html)
	World_Rank = parse_rank(user_info_html)
	Points = parse_points(user_info_html)
	Problems = parse_problems(html, user_name)
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
