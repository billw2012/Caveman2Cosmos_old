## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
##
## Field of the Cloth of Gold
##
## When the Field is built the player gets +3 relations with all other players already met.

## Dancing Hoskuld
##
## Converted to BUG/WoC standard
##

## Adapted from Ishtar.py by Vokarya


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


## Field Start ##

	if iBuildingType == gc.getInfoTypeForString( 'BUILDING_FIELD_GOLD' ):

		pPlayer = gc.getPlayer(pCity.getOwner())
		iTeam = pPlayer.getTeam()
		pTeam = gc.getTeam(iTeam)

		for iPlayer in range(gc.getMAX_PC_PLAYERS()):			
			loopPlayer = gc.getPlayer(iPlayer)
			if loopPlayer.isAlive():
				loopTeam = gc.getTeam(loopPlayer.getTeam())
				if iTeam != loopPlayer.getTeam() and loopTeam.isHasMet(iTeam):
					loopPlayer.AI_changeAttitudeExtra(iTeam, 3)

## Field End ##

