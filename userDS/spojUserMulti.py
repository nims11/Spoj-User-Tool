class spojUserMulti:
	def __init__(self, user1, user2):
		self.name = (user1.name, user2.name)
		self.user_name = (user1.user_name, user2.user_name)
		self.rank = (user1.rank, user2.rank)
		self.points = (user1.points, user2.points)
		self.total_solved = (user1.probPool.total_solved, user2.probPool.total_solved)
		self.classical_total = (user1.classical_total, user2.classical_total)

		self.submission_total = (user1.submission.total, user2.submission.total)
		self.submission = {}
		for key, val in user1.submission.main.items():
			self.submission[key] = [val, 0, False]

		for key, val in user2.submission.main.items():
			if self.submission.has_key(key):
				self.submission[key][1] = val
			else:
				self.submission[key] = [0, val, False]
		if self.submission.has_key('AC'):
			self.submission['AC'][2] = True

		self.avg_attempt = (user1.probPool.avg_attempt, user2.probPool.avg_attempt)
		self.first_attempt = (user1.probPool.first_attempt, user2.probPool.first_attempt)
		self.most_attempt = (user1.probPool.most_attempt, user2.probPool.most_attempt)
		self.most_attempt_ques = (user1.probPool.most_attempt_ques, user2.probPool.most_attempt_ques)
		self.latest = (user1.probPool.latest, user2.probPool.latest)
		self.avg_day = (user1.probPool.avg_day, user2.probPool.avg_day)
		self.most_day = (user1.probPool.most_day, user2.probPool.most_day)
		self.most_day_val = (user1.probPool.most_day_val, user2.probPool.most_day_val)
		self.most_month = (user1.probPool.most_month, user2.probPool.most_month)
		self.most_month_val = (user1.probPool.most_month_val, user2.probPool.most_month_val)

		self.lang = {}
		for key, val in user1.lang.main.items():
			self.lang[key] = [val, 0]

		for key, val in user2.lang.main.items():
			if self.lang.has_key(key):
				self.lang[key][1] = val
			else:
				self.lang[key] = [0, val]

		self.table_solved_both = dict((key, value) for (key, value) in user1.classical_table.items() if user2.classical_table.has_key(key))
		self.table_solved_1 = dict((key, val) for (key, val) in user1.classical_table.items() if not self.table_solved_both.has_key(key))
		self.table_solved_2 = dict((key, val) for (key, val) in user2.classical_table.items() if not self.table_solved_both.has_key(key))