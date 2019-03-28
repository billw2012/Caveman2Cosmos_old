#
# This Python script does absolutly nothing apart from changing a value in the dll that is used for absolutly nothing.
#
# Water Animals Mod
# CvWaterAnimalsModEventManager
#
from CvPythonExtensions import *

def loadConfigurationData():
	import CvConfigParser

	config = CvConfigParser.CvConfigParser("Water Animals Mod Config.ini")

	if config:
		iSpawnChance = config.getint("Water Animals Mod", "Water Animal Spawn Chance", 25)
		if iSpawnChance > -1:
			CyGame().setWaterAnimalSpawnChance(iSpawnChance)
	else:
		CyGame().setWaterAnimalSpawnChance(0)


class CvWaterAnimalsModEventManager:

	def __init__(self, eventManager):

		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("windowActivation", self.onWindowActivation)

		loadConfigurationData()

	def onWindowActivation(self, argsList):
		'Called when the game window activates or deactivates'
		bActive = argsList[0]

		if bActive:
			loadConfigurationData()


	def onGameStart(self, argsList):
		loadConfigurationData()
