from datetime import *
import ast

class CreditCard:
	#Credit Card class contains type, number, reward, reward type 
	#store rewards, stores, date rewards, dates,
	#money conversion, limit, and description.

	def __init__(self, t, number, reward, rewardType, sReward, stores,
			dRewards, byear, bmonth, bdate, eyear, emonth, edate,
			moneyConversion, limit, description):
		self.type = t
		self.number = number
		self.reward = ast.literal_eval(reward)
		self.rewardType= rewardType
		self.sReward = ast.literal_eval(sReward)
		self.stores = ast.literal_eval(stores)
		self.dRewards = ast.literal_eval(dRewards)

		if byear != 0:
			begin = date(byear, bmonth, bdate)
			end = date(eyear, emonth, edate)
			self.dates = [begin, end]
		else:
			self.dates = []

		self.moneyConversion = ast.literal_eval(moneyConversion)
		self.description = description
		self.limit = limit
		self.pastSpending = 0

	def increaseSpending(amount):
		self.pastSpending += amount

	def getReward(self):
		r = self.reward
		return r

	def getRewardType(self):
		rt = self.rewardType
		return rt

	def getMoneyConversion(self):
		mc = self.moneyConversion
		return mc

	def getStores(self):
		s = self.stores
		return s

	def getSReward(self):
		sr = self.sReward
		return sr

	def getName(self):
		name = self.type
		return name

	def getDates(self):
		dates = self.dates
		return dates

	def getDRewards(self):
		dRewards = self.dRewards
		return dRewards