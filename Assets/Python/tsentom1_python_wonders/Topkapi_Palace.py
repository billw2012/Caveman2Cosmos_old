## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Topkapi Palace by Tsentom1.
##

## Dancing Hoskuld
##
## Converted to BUG/WoC standard

from CvPythonExtensions import *
import CvUtil
import PyHelpers
import BugUtil
import sys

gc = CyGlobalContext()
CyGameInstance = gc.getGame()
PyPlayer = PyHelpers.PyPlayer
#globals
gi_Topkapi   = -1                    ## Convert string to number to speed process
gi_Topkapi_ObsoleteTech  = -1  ## Do calculation once
gi_Topkapi_IsActive = False       ## sed to speed up stuff as a single value adjusted by onBuildingBuilt and onTechAcquired
gi_Topkapi_BuiltBy = -1            ## This building was built by player 
#~ gi_Topkapi_BuiltBIn = -1           ## In city


def init():
	global gi_Topkapi, gi_Topkapi_ObsoleteTech, gi_Topkapi_BuiltBy, gi_Topkapi_BuiltBIn
	gi_Topkapi = gc.getInfoTypeForString("BUILDING_TOPKAPI_PALACE")
	gi_Topkapi_ObsoleteTech = gc.getBuildingInfo(gi_Topkapi).getObsoleteTech()

def onLoadGame(argsList):
	global gi_Topkapi_BuiltBy, gi_Topkapi_BuiltBIn, gi_Topkapi_IsActive

	gi_Topkapi_IsActive = False
	for iPlayer in range(gc.getMAX_PLAYERS()):
		iRefCityList = PyPlayer(iPlayer).getCityList()
		for pyCity in iRefCityList:
			ppCity = pyCity.GetCy()
			if ppCity.getNumActiveBuilding(gi_Topkapi) > 0:
				gi_Topkapi_IsActive = True
				gi_Topkapi_BuiltBy = iPlayer
				#~ gi_Topkapi_BuiltBIn = iCity

def onBuildingBuilt(argsList):
	'Building Completed'
	pCity, iBuildingType = argsList

	global gi_Topkapi_BuiltBy, gi_Topkapi_BuiltBIn, gi_Topkapi_IsActive

	if (iBuildingType == gi_Topkapi):
		gi_Topkapi_IsActive = True
		gi_Topkapi_BuiltBy = pCity.getOwner()
		#~ gi_Topkapi_BuiltBIn = pCity



def onBeginPlayerTurn(argsList):
	'Called at the beginning of a players turn'
	iGameTurn, iPlayer = argsList

## Topkapi Palace Start ##
	pPlayer = gc.getPlayer(iPlayer)

	if gi_Topkapi_IsActive and iPlayer == gi_Topkapi_BuiltBy:
		iTeam = pPlayer.getTeam()
		
		for iPlayer in range(gc.getMAX_PLAYERS()):
			ppPlayer = gc.getPlayer(iPlayer)
			if ppPlayer.isAlive() and not ppPlayer.isNPC():
				if gc.getTeam(ppPlayer.getTeam()).isVassal(iTeam):

					iGold = ppPlayer.getEffectiveGold( )
					if ppPlayer.getEffectiveGold( ) >= 5000:
						ppPlayer.changeGold( 50 )
					if ppPlayer.getEffectiveGold( ) < 5000:
						if ppPlayer.getEffectiveGold( ) >= 100:
							ppPlayer.changeGold( iGold//50 )
						else:
							ppPlayer.changeGold( 2 )

					ppPlayer.changeCombatExperience( +1 )

## Topkapi Palace End ## 

def onUnitBuilt(argsList):
	'Unit Completed'
	city = argsList[0]
	unit = argsList[1]
	player = PyPlayer(city.getOwner())

## Topkapi Palace Start ##

	pCity = argsList[0]
	pUnit = argsList[1]
	pPlayer = gc.getPlayer(pUnit.getOwner())
	iUnitType = pUnit.getUnitType()

	if pPlayer == gi_Topkapi_BuiltBy or gi_Topkapi_IsActive == False:
		return
		
	ppPlayer = gc.getPlayer(gi_Topkapi_BuiltBy)
	iTeam = pPlayer.getTeam()
	pTeam = gc.getTeam(iTeam)
	
	if ( (ppPlayer.isAlive()==True) and (ppPlayer.isNPC()==False) ):
		if ( gc.getTeam(ppPlayer.getTeam()).isVassal(iTeam) == True ):

			l_vassalUB = []
			civ_type = gc.getPlayer(iPlayer).getCivilizationType()
			for iUnit in range(gc.getNumUnitClassInfos()):
				iUniqueUnit = gc.getCivilizationInfo(civ_type).getCivilizationUnits(iUnit);
				iDefaultUnit = gc.getUnitClassInfo(iUnit).getDefaultUnitIndex();
				if (iDefaultUnit > -1 and iUniqueUnit > -1 and iDefaultUnit != iUniqueUnit):
					if ( iUnitType == iDefaultUnit ):
						l_vassalUB.append(iUniqueUnit)
						
			if ( len(l_vassalUB) >= 1 ):
				iVassalUUChance = CyGame().getSorenRandNum( 4, "Vassal" )
				if iVassalUUChance == 0:
					chance = CyGame().getSorenRandNum(len(l_vassalUB), "Random for UB")
					iX = pUnit.getX()
					iY = pUnit.getY()
					pNewUnit = pPlayer.initUnit( l_vassalUB[chance], iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION )
					pNewUnit.convert(pUnit)


## Topkapi Palace End ##


def onTechAcquired(argsList):
	'Tech Acquired'
	iTechType, iTeam, iPlayer, bAnnounce = argsList
	
	if ( gi_Topkapi_ObsoleteTech > -1):
		if ( iPlayer == gi_Topkapi_BuiltBy and iTechType == gi_Topkapi_ObsoleteTech):
			gi_Topkapi_IsActive = False
	
