## 
## tsentom1's python wonders - Temple of the Great Jaguar
## 
## Modularised, converted to BUG (and WoC optionally) by Dancing Hoskuld
## 


from CvPythonExtensions import *
import CvUtil
import PyHelpers
import sys
import SdToolKit as SDTK

gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer

# globals
gi_GreatJaguarTemple = None
gi_GreatJaguarTempleObosleteTech = None

gb_GreatJaguarTempleBuilt = False
gi_GreatJaguarTempleBuiltBy = None

###################################################
def init():
	global gi_GreatJaguarTemple, gi_GreatJaguarTempleObosleteTech, gb_GreatJaguarTempleBuilt, gi_GreatJaguarTempleBuiltBy
	
	gi_GreatJaguarTemple = gc.getInfoTypeForString( 'BUILDING_GREAT_JAGUAR_TEMPLE')
	gi_GreatJaguarTempleObosleteTech = gc.getBuildingInfo(gi_GreatJaguarTemple).getObsoleteTech()
	gb_GreatJaguarTempleBuilt = False
	gi_GreatJaguarTempleBuiltBy = None


def onLoadGame(argsList):
	global gi_GreatJaguarTemple, gi_GreatJaguarTempleObosleteTech, gb_GreatJaguarTempleBuilt, gi_GreatJaguarTempleBuiltBy
	
	for iPlayer in range(gc.getMAX_PLAYERS()):  ## for each player
		pPlayer = gc.getPlayer(iPlayer)
		if (pPlayer.isAlive()) and ( gc.getTeam(pPlayer.getTeam()).isHasTech(gi_GreatJaguarTempleObosleteTech) == False or gi_GreatJaguarTempleObosleteTech == -1 ):
			
			iRefCityList = PyPlayer(iPlayer).getCityList()

			for pyCity in iRefCityList:
				pCity = pyCity.GetCy()
				if (pCity.getNumRealBuilding(gi_GreatJaguarTemple) > 0):  ## If the city has the Great Bath in it
					gb_GreatJaguarTempleBuilt = True
					gi_GreatJaguarTempleBuiltBy = iPlayer
					return




def onCombatResult(argsList):
	'Combat Result'
	pWinner,pLoser = argsList

## Jaguar Temple Start ##
	global gi_GreatJaguarTempleObosleteTech, gb_GreatJaguarTempleBuilt, gi_GreatJaguarTempleBuiltBy

	player = pWinner.getOwner()

	if ((gb_GreatJaguarTempleBuilt == True) and (player == gi_GreatJaguarTempleBuiltBy)):
		if ( not SDTK.sdObjectExists('JaguarTemple', pWinner) ) :
			iHealTurn = -1
		else :
			iHealTurn = SDTK.sdObjectGetVal( 'JaguarTemple', pWinner, 'HealTurn' )
		if( iHealTurn == None or gc.getGame().getGameTurn() > iHealTurn ) :
			iHealChance = CyGame().getSorenRandNum( 4, "Temple_of_the_Great_Jaguar" )
			if iHealChance == 0:
				pWinner.setDamage(0, False)
				if ( not SDTK.sdObjectExists('JaguarTemple', pWinner) ) :
					SDTK.sdObjectInit('JaguarTemple', pWinner, {})
				SDTK.sdObjectSetVal( 'JaguarTemple', pWinner, 'HealTurn', gc.getGame().getGameTurn() )

## Jaguar Temple End ##

def onBuildingBuilt(argsList):
	'Building Completed'
	pCity, iBuildingType = argsList

## Jaguar Temple Start ##
	global gi_GreatJaguarTemple,  gb_GreatJaguarTempleBuilt, gi_GreatJaguarTempleBuiltBy

	if iBuildingType == gi_GreatJaguarTemple:

		gb_GreatJaguarTempleBuilt = True
		gi_GreatJaguarTempleBuiltBy = pCity.plot().getOwner()
		
## Jaguar Temple End ##

def onTechAcquired(argsList):
	'Tech Acquired'
	iTechType, iTeam, iPlayer, bAnnounce = argsList
	
## Great Bath Start ##
	global gi_GreatJaguarTempleObosleteTech, gb_GreatJaguarTempleBuilt, gi_GreatJaguarTempleBuiltBy
	
	if ( gi_GreatJaguarTempleObosleteTech > -1):
		if ( iPlayer == gi_GreatJaguarTempleBuiltBy and iTechType == gi_GreatJaguarTempleObosleteTech):
			gb_GreatJaguarTempleBuilt = False

		
## Great Bath End ##
