## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
##
## Silk Road
##
## Silk Road connects by Road (if no better Route already exists) all sources of Silk to the building city, then connects the building city to the capital, and then from the capital to the biggest city you don't own on the same continent.

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
	
## Silk Road Start ##

	if iBuildingType == gc.getInfoTypeForString( 'BUILDING_SILK_ROAD' ):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		pHomePlot = pCity.plot()
		pCapitalCity = pPlayer.getCapitalCity()
		pTargetCity = pCapitalCity
		iSilk = gc.getInfoTypeForString("BONUS_SILK")
		iUnit = gc.getInfoTypeForString("UNIT_SPY")
		iTrail = gc.getInfoTypeForString("ROUTE_TRAIL")
		iPath = gc.getInfoTypeForString("ROUTE_PATH")
		iTargetPop = 0
		iTargetPath = 0
		

		for i in range(CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getArea() == pHomePlot.getArea():
				if pPlot.getOwner() == iPlayer and pPlot.getBonusType(-1) == iSilk and CyMap().generatePathForHypotheticalUnit(pCity.plot(), pPlot, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1:
					for k in range(CyMap().getLastPathStepNum()):
						pRoutePlot = CyMap().getLastPathPlotByIndex(k)
						if pRoutePlot.getRouteType() == -1 or pRoutePlot.getRouteType() == iTrail or pRoutePlot.getRouteType() == iPath:
							pRoutePlot.setRouteType(gc.getInfoTypeForString("ROUTE_ROAD"))
				if pPlot.isCity() == 1 and pPlot.getOwner() != iPlayer and CyMap().generatePathForHypotheticalUnit(pCapitalCity.plot(), pPlot, iPlayer, iUnit, PathingFlags.MOVE_IGNORE_DANGER+PathingFlags.MOVE_THROUGH_ENEMY, 1000) == 1:
					pPotentialCity = pPlot.getPlotCity()
					iPotentialPop = pPotentialCity.getPopulation()
					iPathCheck = CyMap().getLastPathStepNum()
					if (iPotentialPop > iTargetPop) or ((iPotentialPop == iTargetPop) and (iPathCheck > iTargetPath)):
						pTargetCity = pPotentialCity
						if iPotentialPop > iTargetPop:
							iTargetPop = iPotentialPop
							iTargetPath = 0
						else:
							iTargetPath = iPathCheck					
							
		if CyMap().generatePathForHypotheticalUnit(pCapitalCity.plot(), pCity.plot(), iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1:
			for k in range(CyMap().getLastPathStepNum()):
				pRoutePlot = CyMap().getLastPathPlotByIndex(k)
				if pRoutePlot.getRouteType() == -1 or pRoutePlot.getRouteType() == iTrail or pRoutePlot.getRouteType() == iPath:
					pRoutePlot.setRouteType(gc.getInfoTypeForString("ROUTE_ROAD"))

		if CyMap().generatePathForHypotheticalUnit(pCapitalCity.plot(), pTargetCity.plot(), iPlayer, iUnit, PathingFlags.MOVE_IGNORE_DANGER+PathingFlags.MOVE_THROUGH_ENEMY, 1000) == 1:
			for k in range(CyMap().getLastPathStepNum()):
				pRoutePlot = CyMap().getLastPathPlotByIndex(k)
				if pRoutePlot.getRouteType() == -1 or pRoutePlot.getRouteType() == iTrail or pRoutePlot.getRouteType() == iPath:
					pRoutePlot.setRouteType(gc.getInfoTypeForString("ROUTE_ROAD"))