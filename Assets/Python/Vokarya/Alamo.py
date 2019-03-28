## The Alamo
## When a unit you control is killed, adds its base strength as Culture in all cities.

## Adapted from tsentom1's Carhenge by Vokarya

from CvPythonExtensions import *
# globals
GC = CyGlobalContext()
bc_Alamo = GC.getInfoTypeForString("BUILDING_ALAMO")

def onUnitKilled(argsList):
	CyUnit, iAttacker = argsList # iAttacker is a PlayerType
	iPlayerL = CyUnit.getOwner()
	CyPlayerL = GC.getPlayer(iPlayerL)
	if CyPlayerL:
		if CyPlayerL.countNumBuildings(bc_Alamo):
			iValue = CyUnit.baseCombatStr()
			CyCity, i = CyPlayerL.firstCity(False)
			while CyCity:
				CyCity.changeCulture(iPlayerL, iValue, False)
				CyCity, i = CyPlayerL.nextCity(i, False)

