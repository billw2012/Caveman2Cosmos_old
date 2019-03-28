## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Platyping's Helsinki Cathedral
## Converted by Vokarya

from CvPythonExtensions import *

# globals
GC = CyGlobalContext()

###################################################

def onCityAcquired(argsList):
	iOwnerOld, iOwnerNew, CyCity, bConquest, bTrade = argsList

	# Helsinki Cathedral
	if GC.getPlayer(iOwnerNew).countNumBuildings(GC.getInfoTypeForString("BUILDING_HELSINKI")):
		iX = CyCity.getX()
		iY = CyCity.getY()
		for x in range(iX - 1, iX + 2):
			for y in range(iY - 1, iY + 2):
				pPlot = CyMap().plot(x,y)
				foreignCulture = pPlot.getCulture(iOwnerOld) / 10
				pPlot.changeCulture(iOwnerOld, - foreignCulture, True)
				pPlot.changeCulture(iOwnerNew, foreignCulture, True)