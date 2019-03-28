## Code for Caveman2Cosmos
##
## Gives a player a free gatherer when they discover the correct tech.
##
## When a city is conquered there is a chance that the conquerer's state religion will spread to the city.
##
## When a wooden ship is lost at sea there is the chance that a wreck improvement will be placed there.
##

from CvPythonExtensions import *
import CvScreensInterface

# globals
GC = CyGlobalContext()

giTechGather = -1

## Religion Conquest
gi_ReligionCivic = -1
gi_Intolerant = -1
gi_Secular = -1
gi_Athiest = -1

## Ancient religion Spread
#~ gi_Druid = -1
#~ gi_Shaman = -1
#~ gi_Ngai = -1


def init():
	print "Caveman2Cosmos.init"

	#~ iHandicap = CyGame().getHandicapType()
	#~ handicapInfo = GC.getHandicapInfo(iHandicap)
	#~ iGameSpeed = CyGame().getGameSpeedType()

	## Define the globals for the free unit in the first city built
	global giTechGather
	giTechGather = GC.getInfoTypeForString("TECH_GATHERING")

	## Define the globals for Improvement Upgrade

	gi_MessageColour = GC.getInfoTypeForString("COLOR_YELLOW")

	## Religion Conquest
	global gi_ReligionCivic, gi_Intolerant, gi_Secular, gi_Athiest
	gi_ReligionCivic = GC.getInfoTypeForString('CIVICOPTION_RELIGION')
	# CIVIC_FOLKLORE, CIVIC_PROPHETS, CIVIC_DIVINE_RULE, CIVIC_STATE_CHURCH, CIVIC_FREE_CHURCH, CIVIC_INTOLERANT, CIVIC_SECULAR, CIVIC_ATHEIST 
	gi_Intolerant = GC.getInfoTypeForString('CIVIC_INTOLERANT')
	gi_Secular = GC.getInfoTypeForString('CIVIC_SECULAR')
	gi_Athiest = GC.getInfoTypeForString('CIVIC_ATHEIST')

	## Ancient Religion Spread ##
	#~ global gi_Druid, gi_Shaman, gi_Ngai
	#~ gi_Druid = GC.getInfoTypeForString("RELIGION_DRUID")
	#~ gi_Shaman = GC.getInfoTypeForString("RELIGION_NGAI")
	#~ gi_Ngai = GC.getInfoTypeForString("RELIGION_SHAMAN")


def onTechAcquired(argsList):
	iTech, iTeam, iPlayer, bAnnounce = argsList
	print "Caveman2Cosmos.onTechAcquired"

	# Note that iPlayer may be NULL (-1) and not a refer to a player object
	if iPlayer == -1 or GC.getPlayer(iPlayer).isNPC(): return

	CyPlayer = GC.getPlayer(iPlayer)
	if not CyPlayer.isAlive(): return

	# Provide a free gather unit when Gathering is acquired
	if iTech == giTechGather and bAnnounce:
		pCity = CyPlayer.getCapitalCity()
		if pCity != None and not pCity.isNone():
			if GC.getCivilizationInfo(CyPlayer.getCivilizationType()).getType() == "CIVILIZATION_NEANDERTHAL":
				iWorker = GC.getInfoTypeForString("UNIT_NEANDERTHAL_GATHERER")
			else:
				iWorker = GC.getInfoTypeForString("UNIT_GATHERER")
			if iWorker > -1:
				CyPlayer.initUnit(iWorker, pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)


def onCityBuilt(argsList):
	CyCity, CyUnit, = argsList

	if not CyCity:
		return # not a real city

	# Give extra population to new cities
	# The "Great Bath of M..." wonder is dealt with in another python file.
	# It should be transferred here imo.
	if CyUnit:
		iPop = 0
		iPlayer = CyCity.getOwner() 
		CyPlayer = GC.getPlayer(iPlayer)
		iUnit = CyUnit.getUnitType()
		# The help text for these settler units should reflect the extra population they provide.
		mapSettlerPop = {
			GC.getInfoTypeForString("UNIT_COLONIST")	: 1,
			GC.getInfoTypeForString("UNIT_PIONEER")		: 2,
			GC.getInfoTypeForString("UNIT_AIRSETTLER")	: 4
		}
		if iUnit in mapSettlerPop:
			iPop += mapSettlerPop[iUnit]
		if iPop:
			CyCity.changePopulation(iPop)
			if CyGame().isOption(GameOptionTypes.GAMEOPTION_1_CITY_TILE_FOUNDING):
				CyCity.changeFood(CyCity.growthThreshold()/4)
			else:
				CyCity.changeFood(CyCity.growthThreshold()/8)

		# Give a free defender to the first city when it is built
		if iUnit == GC.getInfoTypeForString("UNIT_BAND"):
			i_Defender = GC.getInfoTypeForString("UNIT_TRIBAL_GUARDIAN")
			if i_Defender > -1:
				CyPlayer.initUnit(i_Defender, CyCity.getX(), CyCity.getY(), UnitAITypes.UNITAI_PROPERTY_CONTROL, DirectionTypes.DIRECTION_SOUTH)


def onCityAcquiredAndKept(argsList):
	iOwner,pCity = argsList

## Religion Conquest

	pPlayer = GC.getPlayer(iOwner)
	iPlayerCivic = pPlayer.getCivics(gi_ReligionCivic)
	iPlayerStateReligion = pPlayer.getStateReligion()

	if iPlayerStateReligion == -1 or iPlayerCivic == gi_Secular or iPlayerCivic == gi_Athiest:
		return # No state Religion or Religion Civic is secular or athiest

	if iPlayerCivic == gi_Intolerant:
		pCity.setHasReligion(iPlayerStateReligion,True,True,False)
		return

	if CyGame().getSorenRandNum(99, "ReligionConquest") < 50:
		pCity.setHasReligion(iPlayerStateReligion,True,True,False)


def onUnitLost(argsList): return
''' Replace ships wthat sink with the sunken ship improvement sometimes.
#	unit = argsList[0]

	if unit.getUnitCombatType() == GC.getInfoTypeForString('UNITCOMBAT_WOODEN_SHIPS'):
		print "C2C onUnitLost - A wooden ship has been lost at sea."
'''

def onCombatResult(argsList):
	pWinner,pLoser = argsList
###respawn part 1 start###

	iRespawn2 = GC.getInfoTypeForString('PROMOTION_LIVE2')
	iRespawn1 = GC.getInfoTypeForString('PROMOTION_LIVE1')
	pPlayer = GC.getPlayer(pLoser.getOwner())
	pPID = pPlayer.getID()
	promotion = []
	promotion.append(iRespawn2)
	promotion.append(iRespawn1)

	if ((iRespawn1 != -1 and pLoser.isHasPromotion(iRespawn1))or(iRespawn2 != -1 and pLoser.isHasPromotion(iRespawn2))):
		iUnit = pLoser.getUnitType()
		pCity= pPlayer.getCapitalCity()
		iX =pCity.getX()
		iY = pCity.getY()
		if pLoser.getDomainType ()==GC.getInfoTypeForString('DOMAIN_SEA'):
			for iCity in range(pPlayer.getNumCities () ):
				ppCity = pPlayer.getCity(iCity)
				if ppCity.isNone():continue
				if ppCity.getOwner()<>pPID:continue
				pPlot = CyMap().plot(ppCity.getX(),ppCity.getY())
				if pPlot.isCoastalLand ():
					iX = ppCity.getX()
					iY = ppCity.getY()
					break

		newUnit = pPlayer.initUnit(iUnit, iX,iY, UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
		pLoser.setDamage(0, False)
		newUnit.convert(pLoser)

		newUnit.finishMoves()
		counter=0
		CyInterface().addMessage(pPID, False, 15, CyTranslator().getText("TXT_KEY_REBORN",()), '', 0, 'Art/Interface/Buttons/Phoenix1.dds', ColorTypes(44), iX, iY, True, True)
		for i in range(2):
			counter=counter+1
			newUnit.setHasPromotion(promotion[i], False)
		for i in range(2):
			if pLoser.isHasPromotion(promotion[i]):
				if i==1:
					break
				newUnit.setHasPromotion(promotion[i+1], True)
		pLoser.setDamage(100, False)
###respawn part 1 end###

def onUnitPromoted(argsList):
	pUnit, iPromotion = argsList
###Respawn Part 2 AI start###
	pWinner = pUnit
	pPlayer = GC.getPlayer(pWinner.getOwner())
	if not pPlayer.isHuman():
		iRespawnPromo1 = GC.getInfoTypeForString('PROMOTION_LIVE1')
		if (iPromotion<>iRespawnPromo1):
			if not pWinner.isHasPromotion(iRespawnPromo1):
				if pWinner.canAcquirePromotion(iRespawnPromo1):
					pWinner.setHasPromotion(iPromotion,False)
					if pWinner.canAcquirePromotion(iRespawnPromo1):
						pWinner.setHasPromotion(iRespawnPromo1,True)
					else:
						pWinner.setHasPromotion(iPromotion,True)
					return

	pWinner = pUnit
	pPlayer = GC.getPlayer(pWinner.getOwner())
	if not pPlayer.isHuman():
		iRespawnPromo2 = GC.getInfoTypeForString('PROMOTION_LIVE2')
		if (iPromotion<>iRespawnPromo2):
			if not pWinner.isHasPromotion(iRespawnPromo2):
				if pWinner.canAcquirePromotion(iRespawnPromo2):
					pWinner.setHasPromotion(iPromotion,False)
					if pWinner.canAcquirePromotion(iRespawnPromo2):
						pWinner.setHasPromotion(iRespawnPromo2,True)
					else:
						pWinner.setHasPromotion(iPromotion,True)
					return
###Respawn Part 2 AI End###

def onKbdEvent(argsList):
	'keypress handler - return 1 if the event was consumed'

	eventType,key,mx,my,px,py = argsList
	# game = GC.getGame()

	if ( eventType == 6): #EventKeyDown ):
		theKey=int(key)
		# < Remove to test Test new screens >
		return
		# < Test new screens >
		if (theKey == int(InputTypes.KB_F10)):
			# CvScreensInterface.showC2CMainOptionsScreen()
			CvScreensInterface.showC2CNationAdvisorScreen()
			return 1
		# < Test new screens >
