from datetime import *

class Purchase:
	#Purchas has type, location, year, month, and day

	def __init__(self, t, store, year, month, day):
		self.type = self.categoryToIndex(t)
		self.store = store
		self.date = date(year, month, day)

	def getType(self):
		t = self.type
		return t

	def getStore(self):
		store = self.store
		return store

	def getDate(self):
		date = self.date
		return date

	def categoryToIndex(self, category):
		category = category.lower().strip()

		if category == 'general':
			return 0
		elif category == 'dining' or category == 'fast food restaurants':
			return 1
		elif category == 'entertainment':
			return 2
		elif category == 'travel':
			return 3
		elif category == 'gas':
			return 4
		elif category == 'groceries':
			return 5
		elif category == 'department stores' or category == 'retail':
			return 6
		elif category == 'online shopping':
			return 7
		elif category == 'wholesale clubs':
			return 8
		elif category == 'office supply':
			return 9
		elif category == 'pharmacies':
			return 10
		else:
			return 0
