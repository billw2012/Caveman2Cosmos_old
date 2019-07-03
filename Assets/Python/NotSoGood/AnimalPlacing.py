## Sid Meier's Civilization 4
## Copyright Firaxis Games 2006
## 
## Animal Placing - placing of an animal resource on the map. 


from CvPythonExtensions import *
import CvUtil
import sys
import BugUtil
#~ import CvEventInterface
#~ import CvWorldBuilderScreen

# globals
gc = CyGlobalContext()
localText = CyTranslator()

gia_BonusList = None
gia_BonusImprovementList = None
gia_BonusBuildList = None
###################################################

def init():
	global gia_BonusList, gia_BonusImprovementList, gia_BonusBuildList
	bonusList = ["BONUS_DONKEY", "BONUS_HORSE", "BONUS_ELEPHANT", "BONUS_BISON", "BONUS_CAMEL", "BONUS_COW", "BONUS_DEER", "BONUS_FUR", "BONUS_KANGAROO", "BONUS_LLAMA", "BONUS_MAMMOTH", "BONUS_PIG", "BONUS_POULTRY", "BONUS_RABBIT", "BONUS_SEA_LIONS", "BONUS_SHEEP", "BONUS_WALRUS", "BONUS_GUINEA_PIG", "BONUS_PARROTS", "BONUS_BARLEY", "BONUS_CORN", "BONUS_FLAX", "BONUS_MELON", "BONUS_POTATO", "BONUS_POMEGRANATE", "BONUS_KAVA", "BONUS_GUAVA", "BONUS_PUMPKIN", "BONUS_RICE", "BONUS_SQUASH", "BONUS_WHEAT", "BONUS_ALMONDS", "BONUS_APPLE", "BONUS_BANANA", "BONUS_COCONUT", "BONUS_DATES", "BONUS_FIG", "BONUS_LEMON", "BONUS_MANGO", "BONUS_OLIVES", "BONUS_PAPAYA", "BONUS_PISTACHIO", "BONUS_WINE", "BONUS_HENNA", "BONUS_INDIGO", "BONUS_RUBBER", "BONUS_TIMBER", "BONUS_CANNABIS", "BONUS_COCA", "BONUS_COCOA", "BONUS_COFFEE", "BONUS_COTTON", "BONUS_INCENSE", "BONUS_MUSHROOMS", "BONUS_OPIUM", "BONUS_PAPYRUS", "BONUS_PEYOTE", "BONUS_PRICKLY_PEAR", "BONUS_RESIN", "BONUS_SILK", "BONUS_SPICES", "BONUS_SUGAR", "BONUS_TEA", "BONUS_TOBACCO", "BONUS_VANILLA"]
	
	gia_BonusList = {}
	gia_BonusImprovementList = {}
	gia_BonusBuildList = {}

	for i in range(bonusList.__len__()):
		iBonus = gc.getInfoTypeForString(bonusList[i])
		gia_BonusList[iBonus] = iBonus
	
		iImprovement = gc.getInfoTypeForString("IMPROVEMENT_" + bonusList[i])
		gia_BonusImprovementList[iImprovement] = iBonus
		
		iBuild = gc.getInfoTypeForString("BUILD_" + bonusList[i])
		gia_BonusBuildList[iBuild] = iBonus


# def onGameStart(argsList):
	# createList()

# def onLoadGame(argsList):
	# CvUtil.pyPrint("AnimalPlacing onLoad called")
	# createList()

# def createList():
	# global gia_BonusList, gia_BonusImprovementList, gia_BonusBuildList
	# bonusList = ["BONUS_DONKEY", "BONUS_HORSE", "BONUS_ELEPHANT", "BONUS_BISON", "BONUS_CAMEL", "BONUS_COW", "BONUS_DEER", "BONUS_FUR", "BONUS_KANGAROO", "BONUS_LLAMA", "BONUS_MAMMOTH", "BONUS_PIG", "BONUS_POULTRY", "BONUS_RABBIT", "BONUS_SEA_LIONS", "BONUS_SHEEP", "BONUS_WALRUS", "BONUS_BARLEY", "BONUS_CORN", "BONUS_FLAX", "BONUS_MELON", "BONUS_POTATO", "BONUS_PUMPKIN", "BONUS_RICE", "BONUS_SQUASH", "BONUS_WHEAT", "BONUS_ALMONDS", "BONUS_APPLE", "BONUS_BANANA", "BONUS_COCONUT", "BONUS_DATES", "BONUS_FIG", "BONUS_LEMON", "BONUS_MANGO", "BONUS_OLIVES", "BONUS_PAPAYA", "BONUS_PISTACHIO", "BONUS_WINE", "BONUS_HENNA", "BONUS_INDIGO", "BONUS_RUBBER", "BONUS_TIMBER", "BONUS_CANNABIS", "BONUS_COCA", "BONUS_COCOA", "BONUS_COFFEE", "BONUS_COTTON", "BONUS_INCENSE", "BONUS_MUSHROOMS", "BONUS_OPIUM", "BONUS_PAPYRUS", "BONUS_PEYOTE", "BONUS_PRICKLY_PEAR", "BONUS_RESIN", "BONUS_SILK", "BONUS_SPICES", "BONUS_SUGAR", "BONUS_TEA", "BONUS_TOBACCO", "BONUS_VANILLA"]
	
	# gia_BonusList = {}
	# gia_BonusImprovementList = {}
	# gia_BonusBuildList = {}

	# for i in range(bonusList.__len__()):
		# iBonus = gc.getInfoTypeForString(bonusList[i])
		# gia_BonusList[iBonus] = iBonus
	
		# iImprovement = gc.getInfoTypeForString("IMPROVEMENT_" + bonusList[i])
		# gia_BonusImprovementList[iImprovement] = iBonus
		
		# iBuild = gc.getInfoTypeForString("BUILD_" + bonusList[i])
		# gia_BonusBuildList[iBuild] = iBonus

	

def onImprovementBuilt(argsList):
	'Improvement Built'
	iImprovement, iX, iY = argsList
	# NotSoGood start
	pPlot = CyMap().plot(iX, iY)

	if iImprovement in gia_BonusImprovementList:
		pPlot.setImprovementType(-1)
		pPlot.setBonusType(gia_BonusImprovementList[iImprovement])

	#~ for i in range(bonusList.__len__()):
		#~ if iImprovement == gc.getInfoTypeForString("IMPROVEMENT_" + bonusList[i]):
			#~ pPlot.setImprovementType(-1)
			#~ pPlot.setBonusType(gc.getInfoTypeForString(bonusList[i]))
			#~ break
	# NotSoGood end

def canBuild(argsList):
	iX, iY, iBuild, iPlayer = argsList

	if iBuild in gia_BonusBuildList:
		plot = CyMap().plot(iX, iY)
		if plot.getPlotType() == 3: #  Water
			return 0
		if plot.isPlotGroupConnectedBonus(iPlayer, gia_BonusBuildList[iBuild]) and plot.getBonusType(-1) == -1:
			return 1
		return 0

	return -1	# Returning -1 means ignore; 0 means Build cannot be performed; 1 or greater means it can
