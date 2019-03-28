## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
##
## Golden Spike
##
## When the Golden Spike is built it builds a Transcontinental Railroad.

## Dancing Hoskuld
##
## Converted to BUG/WoC standard
##

## Adapted from Ishtar.py and GIR's Via Appia by Vokarya


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
	
## Golden Spike Start ##

	if iBuildingType == gc.getInfoTypeForString( 'BUILDING_GOLDEN_SPIKE' ):

		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		iXStart = pCity.getX()
		iYStart = pCity.getY()
		iXMaxWest = iXStart
		iYMaxWest = iYStart
		iXMaxEast = iXStart
		iYMaxEast = iYStart
		pStart = CyMap().plot(iXStart, iYStart)
		pMaxWest = pStart
		pMaxEast = pStart
		iUnit = gc.getInfoTypeForString("UNIT_WORKER_ANDROID")
		
		CyInterface().addImmediateMessage(CyTranslator().getText("TXT_GOLDEN_SPIKE_BUILT",()), None)
		
		iPass = 0
		for i in range(CyMap().getGridWidth()):
			for j in range(CyMap().getGridHeight()):
				pWest = CyMap().plot(i, j)
				pNext = CyMap().plot(i+1, j)
				if i == (CyMap().getGridWidth() - 1):
					pNext = CyMap().plot(0, j)
				if (pWest.getArea() == pStart.getArea()) and (pNext.getArea() == pStart.getArea()) and (CyMap().generatePathForHypotheticalUnit(pStart, pWest, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1) and (CyMap().generatePathForHypotheticalUnit(pStart, pNext, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
					iPass = iPass + 1
					break
		if iPass == CyMap().getGridWidth():
			iYParam1 = 100000
			iYParam2 = 100000
			iYParam3 = 100000
			iOffset = int (CyMap().getGridWidth()/4)
			iXOff1 = iXStart - (3 * iOffset)
			if iXOff1 < 0:
				iXOff1 = iXStart + iOffset
			iXOff2 = iXStart - (2 * iOffset)
			if iXOff2 < 0:
				iXOff2 = iXStart + (2 * iOffset)
			iXOff3 = iXStart - iOffset
			if iXOff3 < 0:
				iXOff3 = iXStart + (3 * iOffset)
			for i in range(CyMap().getGridHeight()):
				pCheck1 = CyMap().plot(iXOff1, i)
				pCheck2 = CyMap().plot(iXOff2, i)
				pCheck3 = CyMap().plot(iXOff3, i)
				if (CyMap().generatePathForHypotheticalUnit(pStart, pCheck1, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
					if (pCheck1.getArea() == pStart.getArea()) and (abs(pCheck1.getY() - iYStart) <= abs(iYParam1 - iYStart)):
						iYParam1 = i
				if (CyMap().generatePathForHypotheticalUnit(pCheck1, pCheck2, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
					if (pCheck2.getArea() == pStart.getArea()) and (abs(pCheck2.getY() - iYStart) <= abs(iYParam2 - iYStart)):
						iYParam2 = i
				if (CyMap().generatePathForHypotheticalUnit(pCheck2, pCheck3, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
					if (pCheck3.getArea() == pStart.getArea()) and (abs(pCheck3.getY() - iYStart) <= abs(iYParam3 - iYStart)):
						iYParam3 = i
				pCheckPoint1 = CyMap().plot(iXOff1, iYParam1)
				pCheckPoint2 = CyMap().plot(iXOff2, iYParam2)
				pCheckPoint3 = CyMap().plot(iXOff3, iYParam3)
				if (CyMap().generatePathForHypotheticalUnit(pStart, pCheckPoint1, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
					for i in range(CyMap().getLastPathStepNum()):
						pRailPlot = CyMap().getLastPathPlotByIndex(i)
						pRailPlot.setRouteType(gc.getInfoTypeForString("ROUTE_RAILROAD"))
				if (CyMap().generatePathForHypotheticalUnit(pCheckPoint1, pCheckPoint2, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
					for i in range(CyMap().getLastPathStepNum()):
						pRailPlot = CyMap().getLastPathPlotByIndex(i)
						pRailPlot.setRouteType(gc.getInfoTypeForString("ROUTE_RAILROAD"))
				if (CyMap().generatePathForHypotheticalUnit(pCheckPoint2, pCheckPoint3, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
					for i in range(CyMap().getLastPathStepNum()):
						pRailPlot = CyMap().getLastPathPlotByIndex(i)
						pRailPlot.setRouteType(gc.getInfoTypeForString("ROUTE_RAILROAD"))
				if (CyMap().generatePathForHypotheticalUnit(pCheckPoint3, pStart, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
					for i in range(CyMap().getLastPathStepNum()):
						pRailPlot = CyMap().getLastPathPlotByIndex(i)
						pRailPlot.setRouteType(gc.getInfoTypeForString("ROUTE_RAILROAD"))

		if iPass < CyMap().getGridWidth():
			for i in range(CyMap().numPlots()):
				pPlot = CyMap().plotByIndex(i)
				if (pPlot.getArea() == pCity.getArea()):
					if (pPlot.getOwner() == iPlayer or pPlot.isOwned() == 0):
						if (CyMap().generatePathForHypotheticalUnit(pPlot, pStart, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
							pCheckPlot = CyMap().getLastPathPlotByIndex(1)
							if (pCheckPlot.getX() == pPlot.getX() + 1) or ((pCheckPlot.getX() == 0) and (pPlot.getX() == (CyMap().getGridWidth() - 1))) or (pPlot.getX() == (iXStart - 1)):
								if ((pPlot.getX() < iXMaxWest) and (pPlot.getX() < iXStart) and (iXMaxWest <= iXStart)) or (((pPlot.getX() - CyMap().getGridWidth()) < iXMaxWest) and (iXMaxWest <= iXStart) and (pPlot.getX() > iXStart)) or ((pPlot.getX() < iXMaxWest) and (pPlot.getX() > iXStart) and (iXMaxWest > iXStart)):
									if ((pPlot.getX() < iXMaxWest) or (pPlot.getX() > iXStart and iXMaxWest <= iXStart) or ((pPlot.getX() == iXMaxWest) and (abs(pPlot.getY() - pCity.getY()) <= abs(iYMaxWest - pCity.getY())))):
										iXMaxWest = pPlot.getX()
										iYMaxWest = pPlot.getY()
										pMaxWest = CyMap().plot(iXMaxWest, iYMaxWest)
							if (pCheckPlot.getX() == pPlot.getX() - 1) or ((pCheckPlot.getX() == (CyMap().getGridWidth() - 1)) and (pPlot.getX() == 0)) or (pPlot.getX() == (iXStart + 1)):
								if ((pPlot.getX() > iXMaxEast) and (pPlot.getX() > iXStart) and (iXMaxEast >= iXStart)) or (((pPlot.getX() + CyMap().getGridWidth()) > iXMaxEast) and (iXMaxEast >= iXStart) and (pPlot.getX() < iXStart)) or ((pPlot.getX() > iXMaxEast) and (pPlot.getX() < iXStart) and (iXMaxEast < iXStart)):
									if ((pPlot.getX() > iXMaxEast) or (pPlot.getX() < iXStart and iXMaxEast >= iXStart) or ((pPlot.getX() == iXMaxEast) and (abs(pPlot.getY() - pCity.getY()) <= abs(iYMaxEast - pCity.getY())))):
										iXMaxEast = pPlot.getX()
										iYMaxEast = pPlot.getY()
										pMaxEast = CyMap().plot(iXMaxEast, iYMaxEast)
			if (CyMap().generatePathForHypotheticalUnit(pStart, pMaxWest, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
				for i in range(CyMap().getLastPathStepNum()):
					pRailPlot = CyMap().getLastPathPlotByIndex(i)
					pRailPlot.setRouteType(gc.getInfoTypeForString("ROUTE_RAILROAD"))
			if (CyMap().generatePathForHypotheticalUnit(pStart, pMaxEast, iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
				for i in range(CyMap().getLastPathStepNum()):
					pRailPlot = CyMap().getLastPathPlotByIndex(i)
					pRailPlot.setRouteType(gc.getInfoTypeForString("ROUTE_RAILROAD"))