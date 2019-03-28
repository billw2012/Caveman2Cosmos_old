## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
##
## The Ishtar Gate by Tsentom1.
##
## When the Ishtar gate is built the player gets contact with all other players.

## Dancing Hoskuld
##
## Converted to BUG/WoC standard
##
## Modified to only contact civilizations on same continent by Vokarya.

from CvPythonExtensions import *

import CvUtil
import sys

# globals
gc = CyGlobalContext()

###################################################


def onBuildingBuilt( argsList):
	'Building Completed'
	pCity, iBuildingType = argsList
	#~ game = gc.getGame()
	cityArea = pCity.area()

## Ishtar Start ##

	if iBuildingType == gc.getInfoTypeForString( 'BUILDING_ISHTAR' ):
		pPlayer = gc.getPlayer(pCity.getOwner())
		iTeam = pPlayer.getTeam()
				
		for iTeamX in xrange(gc.getMAX_PC_TEAMS()):
			if not iTeam == iTeamX:
				pTeamX = gc.getTeam(iTeamX)
				if (pTeamX.countNumCitiesByArea(cityArea) > 0):
					pTeamX.meet(iTeam, True)

## Ishtar End ##
