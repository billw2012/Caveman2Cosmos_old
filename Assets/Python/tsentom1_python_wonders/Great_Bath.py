## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## The Great Bath of Mohenjo-daro by Tsentom1.
##
## When the Great Bath is built the plot it is on becomes a source of fresh water.  This does not obsolete.
## If you have the Great Bath then new cities will start with a population of 2.  This does obsolete.

## Dancing Hoskuld
##
## Converted to BUG/WoC standard

## I have reduced the CPU time for this mod by:-
##   1. reducing the number of calls to functions.
##   2. storing data in "globals" rather than recalculating them often (also part of 1. above).
##   3. storing important data between sessions rather than recalculating them on load tme.



from CvPythonExtensions import *
import CvUtil
import PyHelpers
import BugUtil
import sys

gc = CyGlobalContext()
CyGameInstance = gc.getGame()
PyPlayer = PyHelpers.PyPlayer

# globals
gi_GreatBath = -1
gi_RainWaterBasin = -1

gb_GreatBathBuilt = False
gi_GreatBathBuiltBy = None
gs_GreatBathBuiltIn = None

def init():
	BugUtil.debug("Great Bath INIT.")
	
	global gi_GreatBath, gi_RainWaterBasin, gb_GreatBathBuilt, gi_GreatBathBuiltBy, gi_GreatBathObsoleteTech, gs_GreatBathBuiltIn
	gi_GreatBath = gc.getInfoTypeForString( 'BUILDING_GREAT_BATH')
	gi_RainWaterBasin = gc.getInfoTypeForString( "FEATURE_RAINWATER_BASIN")

	gi_GreatBathObsoleteTech = gc.getBuildingInfo(gi_GreatBath).getObsoleteTech()
	#~ BugUtil.debug("gi_GreatBath=%d gi_RainWaterBasin=%d gi_GreatBathObsoleteTech=%d.",gi_GreatBath  , gi_RainWaterBasin , gi_GreatBathObsoleteTech)

	gb_GreatBathBuilt = False
	gi_GreatBathBuiltBy = None
	gs_GreatBathBuiltIn = None

def onGameStart(argsList):
	gb_GreatBathBuilt = False
	gi_GreatBathBuiltBy = None
	gs_GreatBathBuiltIn = None


def onLoadGame(argsList):
	global gi_GreatBath, gi_RainWaterBasin, gb_GreatBathBuilt, gi_GreatBathBuiltBy, gi_GreatBathObsoleteTech, gs_GreatBathBuiltIn
	
	for iPlayer in range(gc.getMAX_PLAYERS()):  ## for each player
		pPlayer = gc.getPlayer(iPlayer)
		if (pPlayer.isAlive()) and ( gc.getTeam(pPlayer.getTeam()).isHasTech(gi_GreatBathObsoleteTech) == False or gi_GreatBathObsoleteTech == -1 ):
			iRefCityList = PyPlayer(iPlayer).getCityList()

			for pyCity in iRefCityList:
				pCity = pyCity.GetCy()
			
				if (pCity.getNumRealBuilding(gi_GreatBath) > 0):  ## If the city has the Great Bath in it
					gb_GreatBathBuilt = True
					gi_GreatBathBuiltBy = iPlayer
					gs_GreatBathBuiltIn = str(pCity.getX()) + "-" + str(pCity.getY()) + "-" + str(pCity.getID())
					return



def onBuildingBuilt(argsList):
	'Building Completed'
	pCity, iBuildingType = argsList
	game = gc.getGame()

## Great Bath Start ##
	global gi_GreatBath, gi_RainWaterBasin, gb_GreatBathBuilt, gi_GreatBathBuiltBy, gs_GreatBathBuiltIn

	if (iBuildingType == gi_GreatBath):

		gb_GreatBathBuilt = True
		gi_GreatBathBuiltBy = pCity.getOwner()
		#~ BugUtil.debug("Great Bath built (onBuildingBuilt called). By player %d", gi_GreatBathBuiltBy)
		
		iX = pCity.getX()
		iY = pCity.getY()
		pPlot = CyMap().plot(iX +0, iY +0)

		gs_GreatBathBuiltIn = str(iX) + "-" + str(iY) + "-" + str(pCity.getID())

		pPlot.setFeatureType(gi_RainWaterBasin, 1)
		
## Great Bath End ##

	
def onCityBuilt(argsList):
	'City Built'
	city = argsList[0]

## Great Bath Start ##
	global gi_GreatBath, gi_RainWaterBasin, gb_GreatBathBuilt, gi_GreatBathBuiltBy, gi_GreatBathObsoleteTech
	
	if (gb_GreatBathBuilt == True):

		pPlayer = city.getOwner()
		if (pPlayer == gi_GreatBathBuiltBy):

			## test for obsolete tech now done onTechAquired meaning less calls here
			city.changePopulation(1)

## Great Bath End ##

def onCityLost( argsList):
	'City Lost'
	city = argsList[0]
	player = PyPlayer(city.getOwner())

## Great Bath Start #
	global gi_GreatBath, gi_RainWaterBasin, gb_GreatBathBuilt, gi_GreatBathBuiltBy, gi_GreatBathObsoleteTech

	iX = city.getX()
	iY = city.getY()
	pPlot = CyMap().plot(iX +0, iY +0)

	if ( pPlot.getFeatureType() == gi_RainWaterBasin):
		pPlot.setFeatureType(-1, 0)

## Great Bath End #


def onCityRaized(argsList):
	pCity = argsList[0]

## Great Bath Start ##
	global gi_RainWaterBasin, gs_GreatBathBuiltIn, gb_GreatBathBuilt
	
	if (gb_GreatBathBuilt == True):
		iX = pCity.getX()
		iY = pCity.getY()
		strCityID = str(iX) + "-" + str(iY) + "-" + str(pCity.getID())

		if (strCityID == gs_GreatBathBuiltIn):
			pPlot = CyMap().plot(iX +0, iY +0)

			pPlot.setFeatureType(gi_RainWaterBasin, 0)

			gb_GreatBathBuilt = False

			## Record the city that the Great Bath was built in to save info across game sessions.
			setGreatBathBuiltData( gs_GreatBathBuiltIn, -1)

## Great Bath End ##

def onTechAcquired(argsList):
	'Tech Acquired'
	iTechType, iTeam, iPlayer, bAnnounce = argsList
	
## Great Bath Start ##
	if ( gi_GreatBathObsoleteTech > -1):
		if ( iPlayer == gi_GreatBathBuiltBy and iTechType == gi_GreatBathObsoleteTech):
			gb_GreatBathBuilt = False
	
## Great Bath End ##
