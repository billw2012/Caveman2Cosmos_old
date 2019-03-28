## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
##
## Marco Polo's Embassy
##
## When Marco Polo's Embassy is built the player gets contact with all other players.

## Dancing Hoskuld
##
## Converted to BUG/WoC standard
## Converted from Ishtar Gate by Vokarya

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

## Marco Start ##

	if iBuildingType == gc.getInfoTypeForString( 'BUILDING_MARCO_POLO' ):
		pPlayer = gc.getPlayer(pCity.getOwner())
		iTeam = pPlayer.getTeam()
				
		for iTeamX in xrange(gc.getMAX_PC_TEAMS()):
			pTeamX = gc.getTeam(iTeamX)
			if (pTeamX.countNumCitiesByArea(pCity.area()) > 0):
				pTeamX.meet(iTeam, True)

## Marco End ##
