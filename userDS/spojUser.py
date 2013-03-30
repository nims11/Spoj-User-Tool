from units.Lang import Lang
from units.ProbPool import ProbPool
from units.Submission import Submission
from datetime import datetime, timedelta
class spojUser:
	"""
	Everything needed about the spoj user
	"""
	def __init__(self, name, user_name, rank, points, classical):
		self.name = name
		self.user_name = user_name
		self.rank = rank
		self.points = points
		self.classical = classical
		
		self.lang = Lang()
		self.probPool = ProbPool()
		self.submission = Submission()
		self.classical_table = {}

	def merge_submission(self, date_of_sub, problem_id, sub_result, lng_sub):
		self.lang.update(lng_sub)
		self.submission.update(sub_result)
		self.probPool.update(problem_id, sub_result, date_of_sub)

	def classical_total(self):
		return len(self.classical)

	def get_classical_table(self):
		ret = {}
		for id in self.classical:
			ret[id] = '-1 days ago'
			if self.probPool.main.has_key(id) and self.probPool.main[id].AC:
				days = (datetime.now()+timedelta(hours=1)-self.probPool.main[id].first_AC)
				ret[id] = '%d days ago' % days.days
		self.classical_table = ret
