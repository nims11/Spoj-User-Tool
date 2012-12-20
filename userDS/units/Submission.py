class Submission:
	def __init__(self):
		self.main = {}
		self.total = 0
	def update(self, sub_status):
		self.total += 1
		if self.main.has_key(sub_status):
			self.main[sub_status] += 1
		else:
			self.main[sub_status] = 1

	def __str__(self):
		return str(self.main) + 'Total :' + str(self.total)