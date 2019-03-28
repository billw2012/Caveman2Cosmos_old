## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
##
## Appian Way
##
## When the Appian Way is built it creates a Paved Road network to all cities.

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
	
## Appian Way Start ##

	if iBuildingType == gc.getInfoTypeForString( 'BUILDING_APPIAN_WAY' ):

		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		player = PyPlayer(iPlayer)
		iMinPath = 10000000
		iUnit = gc.getInfoTypeForString("UNIT_WORKER")
		lCityIndex = []
		lCityNet = {}

		CyInterface().addImmediateMessage(CyTranslator().getText("TXT_APPIAN_BUILT",()), None)

		cityList = player.getCityList()
		for city in cityList:
			lCityIndex.append(city.getID())
			lCityNet[city.getID()]= 0

		lCityNet[pCity.getID()] = 1
		pCity1 = pCity
		
		for i in range(pPlayer.getNumCities()):
			pTCity = pPlayer.getCity(lCityIndex[i])
			if lCityNet[pTCity.getID()] == 0 and pTCity.area().getID() == pCity.area().getID():
				if (CyMap().generatePathForHypotheticalUnit(pCity1.plot(), pTCity.plot(), iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
					pCity2 = None
					for j in range(pPlayer.getNumCities()):
						pTCity2 = pPlayer.getCity(lCityIndex[j])
						if lCityNet[pTCity2.getID()] == 1 and pTCity2.area().getID() == pCity.area().getID():
							if (CyMap().generatePathForHypotheticalUnit(pTCity.plot(), pTCity2.plot(), iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
								if CyMap().getLastPathStepNum() < iMinPath:
									iMinPath = CyMap().getLastPathStepNum()
									pCity2 = pTCity2
					if ( (not (pCity2 == None)) and CyMap().generatePathForHypotheticalUnit(pTCity.plot(), pCity2.plot(), iPlayer, iUnit, PathingFlags.MOVE_SAFE_TERRITORY, 1000) == 1):
						for k in range(CyMap().getLastPathStepNum()):
							pPavePlot = CyMap().getLastPathPlotByIndex(k)
							pPavePlot.setRouteType(gc.getInfoTypeForString("ROUTE_PAVED"))
						pCity1 = pCity2
						lCityNet[pCity1.getID()] = 1
						iMinPath = 10000000