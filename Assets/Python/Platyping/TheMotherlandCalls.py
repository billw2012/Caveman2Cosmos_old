## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Platyping's The Motherland Calls
## Converted by Vokarya

from CvPythonExtensions import *

# globals
GC = CyGlobalContext()

###################################################

def onChangeWar(argsList):
	bIsWar, iAttacker, iDefender = argsList # iAttacker & iDefender are Teams not Players.
	# The Motherland Calls
	if bIsWar:
		iBuilding = GC.getInfoTypeForString("BUILDING_THE_MOTHERLAND_CALLS")
		for iPlayerX in xrange(GC.getMAX_PC_PLAYERS()):
			CyPlayerX = GC.getPlayer(iPlayerX)
			if CyPlayerX.getTeam() != iDefender:
				continue
			if CyPlayerX.countNumBuildings(iBuilding):
				CyCity, i = CyPlayerX.firstCity(False)
				while CyCity:
					CyCity.changeHappinessTimer(10)
					CyUnit = CyPlayerX.initUnit(CyCity.getConscriptUnit(), CyCity.getX(), CyCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
					CyCity.addProductionExperience(CyUnit, True)
					CyCity, i = CyPlayerX.nextCity(i, False)
				break