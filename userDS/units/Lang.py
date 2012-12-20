class Lang:
	def __init__(self):
		self.main = {}
		self.total = 0
	def update(self, lang_name):
		self.total += 1
		if self.main.has_key(lang_name):
			self.main[lang_name] += 1
		else:
			self.main[lang_name] = 1

	def __str__(self):
		return str(self.main) + 'Total :' + str(self.total)