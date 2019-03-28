# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
# Orion's Immigration Mod
from CvPythonExtensions import *
import CvUtil
import CvTechChooser
import traceback
import os
import sys
import PyHelpers
import pickle
import CvGameUtils
import CvEventInterface

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
PyCity = PyHelpers.PyCity
PyGame = PyHelpers.PyGame

# ###################################
#	Begin Immigration Functions		#
# ###################################

def doImmigrantPlacementAI(pUnit, pCity):
# Orion's Immigration Mod
	iOwner = pUnit.getOwner()
	pPlayer = gc.getPlayer(iOwner)
	MyPopulation = pCity.getPopulation()
	
	if MyPopulation > 0 and MyPopulation < 7:
		if pUnit.getX() != pCity.getX() or pUnit.getY() != pCity.getY():
			pUnit.getGroup().pushMission(MissionTypes.MISSION_MOVE_TO, pCity.getX(), pCity.getY(), 0, False, True, MissionAITypes.NO_MISSIONAI, pUnit.plot(), pUnit)
			#CyInterface().addImmediateMessage("Push Immigrant", "")
			
		else:
			#CyInterface().addImmediateMessage("Do Join City", "")
			doJoinCity(pUnit)
# Orion's Immigration Mod			
				
				
def doJoinCity(pUnit):
	# Orion's Immigration Mod
	iOwner = pUnit.getOwner()
	pPlayer = gc.getPlayer(iOwner)
	iPlotX = pUnit.getX()
	iPlotY = pUnit.getY()
	pPlot = CyMap( ).plot( pUnit.getX( ), pUnit.getY( ) )
	pCity = pPlot.getPlotCity()
	NewCityPopulation = pCity.getPopulation() + 1
	
	pCity.setPopulation(NewCityPopulation)	
	if pPlayer.isHuman():
		CyInterface().addMessage(CyGame().getActivePlayer(),False,25,CyTranslator().getText("TXT_KEY_MESSAGE_IMMIGRATION",(pCity.getName(),)),"AS2D_WELOVEKING",InterfaceMessageTypes.MESSAGE_TYPE_INFO,pUnit.getButton(),ColorTypes(8),pCity.getX(),pCity.getY(),True,True)
	
	# Unit expended
	pUnit.kill(0, -1)	
	# Orion's Immigration Mod	
				
def getLeastPopulatedCity(iPlayer):
	# Orion's Immigration Mod
	PopulationValue = 25
	pPlayer = gc.getPlayer(iPlayer)
	iRefCityList = PyPlayer(iPlayer).getCityList()
	intCity = -1
	
	for pyCity in iRefCityList:
		pCity = pyCity.GetCy()
		iCity = pCity.getID()
		pCityPopulation = pCity.getPopulation()
		
		if PopulationValue > pCityPopulation:
			PopulationValue = pCityPopulation
			intCity = iCity
	
	return intCity
	# Orion's Immigration Mod


#~ def cityCanTrainImmigrant(pCity):
	#~ # Orion's Immigration Mod
	#~ iOwner = pCity.getOwner()
	#~ pPlayer = gc.getPlayer(iOwner)
	#~ ImmigrantTech = gc.getInfoTypeForString("TECH_CONSTRUCTION")
	
	#~ # Does the Player have the required Tech
	#~ if gc.getTeam(pPlayer.getTeam()).isHasTech(ImmigrantTech):
		#~ # Does the city have a Population of at least 10
		#~ if pCity.getPopulation() > 9:
			#~ #CyInterface().addImmediateMessage("Can Train Immigrant", "")
			#~ return True
			
	#~ return False
	#~ # Orion's Immigration Mod

#~ def showJoinCityButton(pUnit):
	#~ # Orion's Immigration Mod
	#~ iOwner = pUnit.getOwner()
	#~ pUnitOwner = gc.getPlayer(iOwner)
	#~ iUnitType = pUnit.getUnitType()
	#~ ImmigrantType = gc.getInfoTypeForString("UNIT_IMMIGRANT")
	#~ zShowButton = False
	
	#~ if iUnitType == ImmigrantType:
		#~ pCity = gc.getMap().plot(pUnit.getX(), pUnit.getY()).getPlotCity()
		#~ iCityOwner = pCity.getOwner()
		#~ pCityPlayer = gc.getPlayer(iCityOwner)
		#~ pCityPopulation = pCity.getPopulation()
		
		#~ if pCityPopulation > 0 and pCityPopulation < 7:
			#~ if (iCityOwner == iOwner) or (gc.getTeam(pCityPlayer.getTeam()).isVassal(gc.getPlayer(iOwner).getTeam())):
				#~ zShowButton = True

	#~ return zShowButton
	#~ # Orion's Immigration Mod


#~ def getImmigrantProductionChance(pPlayer):
	#~ # Orion's Immigration Mod
	#~ # Accelerates Immigrant Production for Expansive traits
	#~ iTrait = gc.getInfoTypeForString("TRAIT_EXPANSIVE")
	
	#~ if (pPlayer.hasTrait(iTrait)):
		#~ # Expansive Players get a 33% chance for Producing an Immigrant
		#~ return 33
	#~ else:
		#~ # Non Spiritual Players get a 25% chance for Producing an Immigrant
		#~ return 25
		#~ # Orion's Immigration Mod	
			
#~ def doRandumChance(Number):
	#~ # Orion's Immigration Mod
	#~ # Produces a number between 0 and 100
	#~ chance = CyGame().getSorenRandNum(100,"")
		
	#~ if chance <= Number:
		#~ return True
	#~ else:
		#~ return False
		#~ # Orion's Immigration Mod	

# End Orion's Immigration Mod Functions	

