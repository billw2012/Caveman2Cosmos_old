## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Adapted from platyping's Machu Picchu for C2C
##
## Machu Picchu
##
## Places Machu Picchu improvement on a Peak in city radius
## +1 food, +2 hammers, +1 commerce from all owned Peaks
## +1 commerce from all Peaks in city radius

from CvPythonExtensions import *

import CvUtil
import BugUtil
import sys

# globals
gc = CyGlobalContext()

###################################################


def onBuildingBuilt( argsList):
	'Building Completed'
	pCity, iBuildingType = argsList
	game = gc.getGame()
## Machu Picchu Start ##
	if iBuildingType == gc.getInfoTypeForString("BUILDING_MACHU_PICCHU"):
		iPlayer = pCity.getOwner()
		iX = pCity.getX()
		iY = pCity.getY()
		PeakPlot = []
		iCountPeaksNearCity = -1
		for x in range(iX - 3, iX + 4):
			for y in range(iY - 3, iY + 4):
				pPlot = CyMap().plot(x, y)
				if pCity.canWork(pPlot) == 1 and pPlot.isPeak():
					CyGame().setPlotExtraYield(x, y, YieldTypes.YIELD_COMMERCE, 1)
					PeakPlot.append(pPlot)
					iCountPeaksNearCity = iCountPeaksNearCity + 1
		for i in range(CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getOwner() == iPlayer and pPlot.isPeak():
				CyGame().setPlotExtraYield(pPlot.getX(), pPlot.getY(), YieldTypes.YIELD_FOOD, 1)
				CyGame().setPlotExtraYield(pPlot.getX(), pPlot.getY(), YieldTypes.YIELD_PRODUCTION, 2)
				CyGame().setPlotExtraYield(pPlot.getX(), pPlot.getY(), YieldTypes.YIELD_COMMERCE, 1)
		if iCountPeaksNearCity > -1:
			pPeakPlot = PeakPlot[CyGame().getSorenRandNum(iCountPeaksNearCity, "Random Peak")]
			pPeakPlot.setImprovementType(gc.getInfoTypeForString("IMPROVEMENT_MACHU_PICCHU"))
		else:
			BugUtil.error("Machu Picchu has been built in a city (%s) without a peak in it.",  pCity.getName())
