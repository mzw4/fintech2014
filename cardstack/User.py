from CreditCard import *
from Purchase import *
from datetime import *

class User:
	#User has first name, last name, credit cards, and preferences

	def __init__(self, firstName, lastName, creditCards, preferences):
		self.firstName = firstName
		self.lastName = lastName
		self.creditCards = creditCards
		self.preferences = preferences

	def addCard(self, card):
		self.creditCards.append(card)

	def maximum(self, utilities):
		x = sorted(utilities, key=lambda tup: tup[1])
		(c,u,m) = x[len(x)-1]
		return (c,u,m)

	def optimalCard(self, purchase):
		utilities = []
		for c in self.creditCards:
			if len(c.getDates()) != 0 and purchase.getDate() >= c.getDates()[0] and purchase.getDate() <= c.getDates()[1]:
				r = c.getDRewards()[purchase.getType()]
			else:
				r = c.getReward()[purchase.getType()]

			mc = c.getMoneyConversion()

			for m in range(len(mc)):
				u = mc[m]*self.preferences[m]*r
				utilities.append((c,u,m))

			if purchase.getStore() in c.getStores():
				r = c.getSReward()[c.getStores().index(purchase.getStore())]
				for m in range(len(mc)):
					u = mc[m]*self.preferences[m]*r
					utilities.append((c,u,m))

		(c,u,m) = self.maximum(utilities)
		return (c,m)

	def getUtilityType(self, m):
		if m == 0:
			return ""
		elif m == 1:
			return " towards Hotel and Car Rentals"
		elif m == 2:
			return " towards Airline Mileage"
		elif m == 3:
			return " towards Dining"
		elif m == 4:
			return " toward Gifts"

