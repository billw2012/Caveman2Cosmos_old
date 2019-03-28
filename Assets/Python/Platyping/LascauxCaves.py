# Lascaux Caves

from CvPythonExtensions import *
GC = CyGlobalContext()

def onGreatPersonBorn(argsList):
	CyUnit, iPlayer, CyCity = argsList
	if CyUnit.isNone() or CyCity.isNone(): return

	if GC.getPlayer(iPlayer).countNumBuildings(GC.getInfoTypeForString("BUILDING_LASCAUX")):
		if CyCity.getAddedFreeSpecialistCount(GC.getInfoTypeForString("SPECIALIST_GREAT_ARTIST")) > 0:
			CyCity.changeCulture(iPlayer, min(2000, CyCity.getCultureThreshold() /10), True)
		else:
			CyCity.changeCulture(iPlayer, min(1000, CyCity.getCultureThreshold() /20), True)