## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
##
## Maginot Line
##
## The Maginot Line builds Bunkers every other square along your frontiers on completion.

from CvPythonExtensions import *
import CvUtil
import sys

# globals
gc = CyGlobalContext()

###################################################


def onBuildingBuilt( argsList):
	'Building Completed'
	pCity, iBuildingType = argsList
	game = gc.getGame()
	
## Maginot Line Start ##

	if iBuildingType == gc.getInfoTypeForString( 'BUILDING_MAGINOTLINE' ):
		iBunker = gc.getInfoTypeForString("IMPROVEMENT_BUNKER")
		iPlayer = pCity.getOwner()
		pHomePlot = pCity.plot()
		
		for i in range(CyMap().numPlots()):
			pPlot = CyMap().plotByIndex(i)
			if pPlot.getOwner() == iPlayer and pPlot.getArea() == pHomePlot.getArea():
				iXCenter = pPlot.getX()
				iYCenter = pPlot.getY()
				iNorth = iYCenter + 1
				if iNorth > (CyMap().getGridHeight() - 1):
					iNorth = (CyMap().getGridHeight() - 1)
				iEast = iXCenter + 1
				if iEast > (CyMap().getGridWidth() - 1):
					iEast = (CyMap().getGridWidth() - 1)
				iSouth = iYCenter - 1
				if iSouth < 0:
					iSouth = 0
				iWest = iXCenter - 1
				if iWest < 0:
					iWest = 0
				pNorthwest = CyMap().plot(iWest, iNorth)
				pNorth = CyMap().plot(iXCenter, iNorth)
				pNortheast = CyMap().plot(iEast, iNorth)
				pWest = CyMap().plot(iWest, iYCenter)
				pEast = CyMap().plot(iEast, iYCenter)
				pSouthwest = CyMap().plot(iWest, iSouth)
				pSouth = CyMap().plot(iXCenter, iSouth)
				pSoutheast = CyMap().plot(iEast, iSouth)
				if (pNorthwest.getArea() == pHomePlot.getArea() and (pNorthwest.isOwned() == False or pNorthwest.getOwner() != iPlayer)) or (pNorth.getArea() == pHomePlot.getArea() and (pNorth.isOwned() == False or pNorth.getOwner() != iPlayer)) or (pNortheast.getArea() == pHomePlot.getArea() and (pNortheast.isOwned() == False or pNortheast.getOwner() != iPlayer)) or (pWest.getArea() == pHomePlot.getArea() and (pWest.isOwned() == False or pWest.getOwner() != iPlayer)) or (pEast.getArea() == pHomePlot.getArea() and (pEast.isOwned() == False or pEast.getOwner() != iPlayer)) or (pSouthwest.getArea() == pHomePlot.getArea() and (pNorthwest.isOwned() == False or pSouthwest.getOwner() != iPlayer)) or (pSouth.getArea() == pHomePlot.getArea() and (pSouth.isOwned() == False or pSouth.getOwner() != iPlayer)) or (pSoutheast.getArea() == pHomePlot.getArea() and (pSoutheast.isOwned() == False or pSoutheast.getOwner() != iPlayer)):
					if ((pNorthwest.getOwner() == iPlayer and pNorthwest.getImprovementType() == iBunker) or (pNorth.getOwner() == iPlayer and pNorth.getImprovementType() == iBunker) or (pNortheast.getOwner() == iPlayer and pNortheast.getImprovementType() == iBunker) or (pWest.getOwner() == iPlayer and pWest.getImprovementType() == iBunker) or (pEast.getOwner() == iPlayer and pEast.getImprovementType() == iBunker) or (pSouthwest.getOwner() == iPlayer and pSouthwest.getImprovementType() == iBunker) or (pSouth.getOwner() == iPlayer and pSouth.getImprovementType() == iBunker) or (pSoutheast.getOwner() == iPlayer and pSoutheast.getImprovementType() == iBunker) or (pPlot.getImprovementType() == iBunker)) == False:
						pPlot.setImprovementType(iBunker)