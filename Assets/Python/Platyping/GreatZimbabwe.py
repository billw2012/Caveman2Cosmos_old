## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Platyping's Great Zimbawee
## Converted by Vokarya

from CvPythonExtensions import *

GC = CyGlobalContext()
bGreatZim = GC.getInfoTypeForString("BUILDING_GREAT_ZIMBABWE")
iGWObsoleteTech = GC.getBuildingInfo(bGreatZim).getObsoleteTech()

###################################################

def onCityDoTurn(argsList):
	CyCity = argsList[0]
	iPlayer = argsList[1]

	if CyCity.isFoodProduction():
		CyPlayer = GC.getPlayer(iPlayer)
		if CyPlayer.countNumBuildings(bGreatZim):
			if not GC.getTeam(CyPlayer.getTeam()).isHasTech(iGWObsoleteTech):
				CyCity.changeFood(CyCity.getYieldRate(0) - CyCity.foodConsumption(False, 0))
				if CyCity.getFood() >= CyCity.growthThreshold():
					CyCity.changePopulation(1)
					CyCity.setFood(CyCity.getFoodKept())