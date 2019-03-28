# Sid Meier's Civilization 4
# Copyright Firaxis Games 2007
# OIMEvents
# Orion's Immigration Mod
# Modular python project to eliminate or reduce merging tasks

from CvPythonExtensions import *
import CvUtil
import CvScreensInterface
import CvDebugTools
import CvWBPopups
import PyHelpers
import Popup as PyPopup
import CvCameraControls
import CvTopCivs
import sys
import CvWorldBuilderScreen
import CvAdvisorUtils
import CvTechChooser
import Immigration

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
PyCity = PyHelpers.PyCity
PyGame = PyHelpers.PyGame


class ImmigrationEvents:
	def __init__(self, eventMgr):
# ###############################################################################
#		Important!!!!															#
#		Each function added from CvEventManager.py must be initialized here 	#
# ###############################################################################
		self.__LOG_MOVEMENT = 0
		self.__LOG_UNITBUILD = 0
		self.eventMgr = eventMgr
				
		eventMgr.addEventHandler("unitBuilt", self.onUnitBuilt)
		
	def onUnitBuilt(self, argsList):
		'Unit Completed'
		city = argsList[0]
		unit = argsList[1]
		player = PyPlayer(city.getOwner())
# Immigration Mod
		iOwner = city.getOwner()
		pPlayer = gc.getPlayer(iOwner)
		UnitType = unit.getUnitType()
		iImmigrant = gc.getInfoTypeForString("UNIT_IMMIGRANT")
		intCity = Immigration.getLeastPopulatedCity(iOwner)
				
		if UnitType == iImmigrant:
			#CyInterface().addImmediateMessage("B", "")
			if pPlayer.isAlive() and not pPlayer.isNPC():
				ReducedCityPopulation = city.getPopulation() - 2
				city.setPopulation(ReducedCityPopulation)				
				if intCity != -1:
					MigrationCity = pPlayer.getCity(intCity)
					Immigration.doImmigrantPlacementAI(unit, MigrationCity)					
# End Immigration Mod

		CvAdvisorUtils.unitBuiltFeats(city, unit)
		
		if (not self.__LOG_UNITBUILD):
			return
		CvUtil.pyPrint('%s was finished by Player %d Civilization %s' 
			%(PyInfo.UnitInfo(unit.getUnitType()).getDescription(), player.getID(), player.getCivilizationName()))				
					
			
		

