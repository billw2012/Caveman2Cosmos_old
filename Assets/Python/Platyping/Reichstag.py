## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Platyping's Reichstag
## Converted by Vokarya

from CvPythonExtensions import *

GC = CyGlobalContext()

###################################################

def onVassalState(argsList):
	iTeamMaster, iTeamVassal, bVassal = argsList
	if bVassal:
		for iPlayerX in range(GC.getMAX_PC_PLAYERS()):
			CyPlayerX = GC.getPlayer(iPlayerX)
			if CyPlayerX.getTeam() == iTeamMaster and CyPlayerX.countNumBuildings(GC.getInfoTypeForString("BUILDING_REICHSTAG")):
				CyPlayerX.changeGoldenAgeTurns(CyPlayerX.getGoldenAgeLength())