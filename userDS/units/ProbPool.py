from datetime import date
class ProbElt:
	def __init__(self, ID):
		self.id = ID
		self.AC = False
		self.first_sub = None
		self.first_AC = None
		self.sub_till_AC = 0

	def update(self, status, date_sub):
		if not self.AC:
			if self.sub_till_AC == 0:
				self.first_sub = date_sub
			if status == 'AC':
				self.AC = True
				self.first_AC = date_sub
			else:
				self.sub_till_AC += 1

	def __str__(self):
		return 'AC: %s, first_sub: %s, first_AC: %s, sub_till_AC: %d' % (self.AC, self.first_sub, self.first_AC, self.sub_till_AC)

	def __cmp__(self, other):
		return self.first_AC.__cmp__(other.first_AC)

class ProbPool:
	def __init__(self):
		self.main = {}
		self.total = 0
		self.total_solved = 0
		self.avg_attempt = 0
		self.first_attempt = 0
		self.most_attempt = 0
		self.most_attempt_ques = ''

		# time based
		self.most_day = 0
		self.most_day_val = ''
		self.most_month = 0
		self.most_month_val = ''
		self.avg_day = 0
		self.latest = ''

	def update(self, ID, status, date_sub):
		if self.main.has_key(ID):
			self.main[ID].update(status, date_sub)
		else:
			self.total += 1
			self.main[ID] = ProbElt(ID)
			self.main[ID].update(status, date_sub)

	def __str__(self):
		ret = str(self.total) + ' ++++ '
		keys = self.main.keys()
		for key in keys:
			ret += key + ': ' + str(self.main[key]) + ' *** '
		return ret
	
	def calc_stats(self):
		items = self.main.items()
		for key, val in items:
			if val.AC:
				self.total_solved += 1
				self.avg_attempt += val.sub_till_AC + 1
				if val.sub_till_AC == 0:
					self.first_attempt += 1
				if val.sub_till_AC>self.most_attempt:
					self.most_attempt = val.sub_till_AC
					self.most_attempt_ques = key
		if self.total_solved == 0:
			self.avg_attempt = 'NA'
		else:
			self.avg_attempt /= float(self.total_solved)
			self.avg_attempt = '%.2f' % self.avg_attempt

		# Time based
		tmp = [x for a, x in items if x.first_AC != None]
		tmp.sort(key=lambda r: r.first_AC)
		if len(tmp) >0:
			self.latest = tmp[len(tmp)-1].id
		else:
			self.latest = ''

		#Most prob in a day
		pre, curr = None, 0
		for val in tmp:
			if pre == None:
				curr += 1
				pre = val.first_AC
			else:
				if (pre.day, pre.month, pre.year) == (val.first_AC.day, val.first_AC.month, val.first_AC.year):
					curr += 1
				else:
					if curr>self.most_day:
						self.most_day = curr
						self.most_day_val = date(pre.year, pre.month, pre.day)
					curr = 0
					pre = None

		#Most prob in a month
		pre = None
		curr = 0
		for val in tmp:
			if pre == None:
				curr += 1
				pre = val.first_AC
			else:
				if (pre.month, pre.year) == (val.first_AC.month, val.first_AC.year):
					curr += 1
				else:
					if curr>self.most_month:
						self.most_month = curr
						self.most_month_val = date(pre.year, pre.month, pre.day).strftime('%b, %Y')
					curr = 0
					pre = None

		#Avg Prob per day
		if len(tmp)>0:
			foo = (tmp[len(tmp)-1].first_AC - tmp[0].first_AC).days
		else:
			foo = 1
			
		if foo==0:
			foo = 1;
		self.avg_day = '%.2f' % (float(self.total_solved)/foo)
