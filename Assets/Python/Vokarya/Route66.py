## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
##
## Route 66
##
## When Route 66 is built it connects the building city to the biggest other city on the same continent.

## Dancing Hoskuld
##
## Converted to BUG/WoC standard
##

## Adapted from Ishtar.py and GIR's Via Appia by Vokarya


from CvPythonExtensions import *
from PyHelpers import PyPlayer
import CvUtil
import sys

# globals
gc = CyGlobalContext()

###################################################


def onBuildingBuilt( argsList):
	'Building Completed'
	pCity, iBuildingType = argsList
	game = gc.getGame()
	
## Route66 Start ##

	if iBuildingType == gc.getInfoTypeForString( 'BUILDING_ROUTE_66' ):

		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		player = PyPlayer(iPlayer)
		iMinPath = 0
		iPop = 0
		iTerminus = gc.getInfoTypeForString("BUILDING_ROUTE_66_TERMINUS")
		iUnit = gc.getInfoTypeForString("UNIT_WORKER")
			
		cityList = player.getCityList()
		for city in cityList:
			iChecker = city.getID()
			pChecker = pPlayer.getCity(iChecker)
			iAreaCheck = pPlayer.getCity(iChecker).area().getID()
			if iAreaCheck == pCity.area().getID() and iChecker != pCity.getID():
				if (CyMap().generatePathForHypotheticalUnit(pCity.plot(), pChecker.plot(), iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
					if (pChecker.getPopulation() > iPop) or (pChecker.getPopulation() == iPop and CyMap().getLastPathStepNum() > iMinPath):
						pFinalCity = pChecker
						iMinPath = CyMap().getLastPathStepNum()
						iPop = pChecker.getPopulation()
					
		if (CyMap().generatePathForHypotheticalUnit(pCity.plot(), pFinalCity.plot(), iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
			pFinalCity.setNumRealBuilding(iTerminus, 1)
			for k in range(CyMap().getLastPathStepNum()):
				pRoutePlot = CyMap().getLastPathPlotByIndex(k)
				pRoutePlot.setRouteType(gc.getInfoTypeForString("ROUTE_MODERN_ROAD"))