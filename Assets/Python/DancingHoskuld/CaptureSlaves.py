## By StrategyOnly converted to BUG by Dancing Hoskuld
## Completely rewritten when we went fom jus slaves to captives

## Modified by Dancing Hoskuld
##   Now Captives not Slaves
##     Chance of capturing a Military Captive when you attach a unit depends n your and their civics (to be done)
##     Capturing a military init now gives a Captive (Military)
##     Raizing a city will give Captive (Civilians) instead

from CvPythonExtensions import *
import BugUtil

gc = CyGlobalContext()

giDomainLand = -1
giUnitCaptiveMilitary = -1
giUnitCaptiveCivilian = -1

giUnitNeandethal = -1
giUnitCaptiveNeanderthal = -1

def init():
	global giDomainLand, giUnitCaptiveMilitary, giUnitCaptiveCivilian

	giDomainLand = gc.getInfoTypeForString('DOMAIN_LAND')
	giUnitCaptiveMilitary = gc.getInfoTypeForString('UNIT_CAPTIVE_MILITARY') 
	giUnitCaptiveCivilian = gc.getInfoTypeForString('UNIT_CAPTIVE_CIVILIAN') 
#	giUnitCaptiveSlave = gc.getInfoTypeForString('UNITCLASS_CAPTIVE_GATHERER') 

	#~ UNITCLASS_NEANDERTHAL
	global giUnitNeandethal, giUnitCaptiveNeanderthal

	giUnitNeandethal = gc.getInfoTypeForString('UNITCOMBAT_SPECIES_NEANDERTHAL') 
	giUnitCaptiveNeanderthal = gc.getInfoTypeForString('UNIT_CAPTIVE_NEANDERTHAL') 

def onCombatResult(argsList):
	CyUnitW, CyUnitL = argsList

	if CyUnitW.isMadeAttack() and not CyUnitL.isAnimal() and CyUnitL.getDomainType() == giDomainLand and CyUnitW.getDomainType() == giDomainLand:
		# Check that the losing unit is not an animal and the unit does not have a capture type defined in the XML
		iPlayerL = CyUnitL.getOwner()
		CyPlayerL = gc.getPlayer(iPlayerL)
		if CyUnitL.getCaptureUnitType(CyPlayerL.getCivilizationType()) == -1:

			iCaptureProbability = CyUnitW.captureProbabilityTotal()
			iCaptureResistance = CyUnitL.captureResistanceTotal()
			iChance =  iCaptureProbability - iCaptureResistance
			BugUtil.info("CaptureSlaves: Initial chance to capture a captive is %d (%d - %d)", iChance, iCaptureProbability, iCaptureResistance)

			if CyPlayerL.isNPC():
				iChance += 5
				BugUtil.info("CaptureSlaves: NPC defender +5% chance")

			if CyUnitL.plot().isCity():
				iChance += 5
				BugUtil.info("CaptureSlaves: City defender +5% chance")

			if iChance > 100:
				iChance = 100
			BugUtil.info("CaptureSlaves: Final chance to capture a captive is %d", iChance)

			iRandom = CyGame().getSorenRandNum(100, "Captive") # 0-99
			if iChance > iRandom:
				if CyUnitL.isHasUnitCombat(giUnitNeandethal):
					iUnit = giUnitCaptiveNeanderthal
					sMessage = CyTranslator().getText("TXT_KEY_MESSAGE_NEANDERTHAL_CAPTIVE",())
				else:
					iUnit = giUnitCaptiveMilitary
					sMessage = CyTranslator().getText("TXT_KEY_MESSAGE_MILITARY_CAPTIVE",())
				X = CyUnitW.getX()
				Y = CyUnitW.getY()
				iPlayerW = CyUnitW.getOwner()
				CyPlayerW = gc.getPlayer(iPlayerW)
				CyUnit = CyPlayerW.initUnit(iUnit, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
				if CyUnitW.isHiddenNationality():
					CyUnit.doHNCapture()
				if CyPlayerW.isHuman():
					CyInterface().addMessage(iPlayerW,False,15,sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)
				BugUtil.info('Player %d Civilization %s Unit %s has defeated and captured Player %d Civilization %s Unit %s.' 
					%(iPlayerW, CyPlayerW.getCivilizationDescription(0), CyUnitW.getName(), iPlayerL, CyPlayerL.getCivilizationDescription(0), CyUnitL.getName()))

def onCityRazed(argsList):
	CyCity, iPlayer = argsList

	if not CyCity: return
	CyPlayer = gc.getPlayer(iPlayer)
	bHuman = CyPlayer.isHuman()

	sCityName = CyCity.getName()
	X = CyCity.getX()
	Y = CyCity.getY()

	## Convert Great Specialists into captives or other
	iCount = CyCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_PRIEST'))
	if iCount > 0:
		iCountKilled = iCount
		iCountCaptured = 0
		if bHuman:
			sMessage = BugUtil.getText("TXT_KEY_MESSAGE_CITY_HAD_PRIESTS",(iCount,iCountCaptured))
			CyInterface().addMessage(iPlayer,False,15, sMessage ,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	iCount = CyCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_ARTIST'))
	if iCount > 0:
		iCountKilled = iCount
		iCountCaptured = 0
		if bHuman:
			sMessage = BugUtil.getText("TXT_KEY_MESSAGE_CITY_HAD_ARTISTS",(iCount,iCountCaptured))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	iCount = CyCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_SCIENTIST'))
	if iCount > 0:
		iCountKilled = iCount
		iCountCaptured = 0
		if bHuman:
			sMessage = BugUtil.getText("TXT_KEY_MESSAGE_CITY_HAD_SCIENTISTS",(iCount,iCountCaptured))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	iCount = CyCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_MERCHANT'))
	if iCount > 0:
		iCountKilled = iCount
		iCountCaptured = 0
		if bHuman:
			sMessage = BugUtil.getText("TXT_KEY_MESSAGE_CITY_HAD_MERCHANTS",(iCount,iCountCaptured))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	iCount = CyCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_ENGINEER'))
	if iCount > 0:
		iCountKilled = iCount
		iCountCaptured = 0
		if bHuman:
			sMessage = BugUtil.getText("TXT_KEY_MESSAGE_CITY_HAD_ENGINEERS",(iCount,iCountCaptured))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	iCount = CyCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_DOCTOR'))
	if iCount > 0:
		iCountKilled = iCount
		iCountCaptured = 0
		if bHuman:
			sMessage = BugUtil.getText("TXT_KEY_MESSAGE_CITY_HAD_DOCTORS",(iCount,iCountCaptured))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	iCount = CyCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_SPY'))
	if iCount > 0:
		iCountKilled = iCount
		Inhiding = 0
		iCountCaptured = 0
		if bHuman:
			sMessage = BugUtil.getText("TXT_KEY_MESSAGE_CITY_HAD_SPIES",(iCount,iCountCaptured))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	iCount = CyCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_GENERAL')) + CyCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_GREAT_WARLORD'))
	if iCount > 0:
		iCountKilled = iCount
		iCountRebelled = 0
		iCountCaptured = 0
		if bHuman:
			sMessage = BugUtil.getText("TXT_KEY_MESSAGE_CITY_HAD_GENERALS",(iCount,iCountKilled,iCountRebelled,iCountCaptured))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	## Slaves
	iSlaveSettled = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE")
	iSlaveFood = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_FOOD")
	iSlaveProd = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_PRODUCTION")
	iSlaveCom = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_COMMERCE")
	iSlaveHealth = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_HEALTH")
	iSlaveEntertain = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_ENTERTAINMENT")
	iSlaveTutor = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_TUTOR")
	iSlaveMilitary = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_MILITARY")

	iUnitCaptiveSlave = gc.getInfoTypeForString("UNIT_FREED_SLAVE")
	iUnitImmigrant = gc.getInfoTypeForString("UNIT_CAPTIVE_IMMIGRANT")
	iUnitEntertain = gc.getInfoTypeForString("UNIT_STORY_TELLER")
	iUnitMerCaravan = gc.getInfoTypeForString("UNIT_EARLY_MERCHANT_C2C")
	iUnitHealth = gc.getInfoTypeForString("UNIT_HEALER")

	iCountSettled = CyCity.getFreeSpecialistCount(iSlaveSettled)
	iCountFood = CyCity.getFreeSpecialistCount(iSlaveFood)
	iCountProd = CyCity.getFreeSpecialistCount(iSlaveProd)
	iCountCom = CyCity.getFreeSpecialistCount(iSlaveCom)
	iCountHealth = CyCity.getFreeSpecialistCount(iSlaveHealth)
	iCountEntertain = CyCity.getFreeSpecialistCount(iSlaveEntertain)
	iCountTutor = CyCity.getFreeSpecialistCount(iSlaveTutor)
	iCountMilitary = CyCity.getFreeSpecialistCount(iSlaveMilitary)

	## Process those that can become population or immagrants 
	##	where 3 slaves = 1 pop or immigrant
	##	and can only increase the city pop to 7
	iCount = iCountSettled + iCountFood + iCountCom + iCountTutor + iCountMilitary
	iCountNewPop = int(iCount / 3)
	iCount -= 3 * iCountNewPop

	if iCount > 0:
		for i in range (iCount):
			CyPlayer.initUnit(iUnitCaptiveSlave, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
		if bHuman:
			sMessage = BugUtil.getText("TXT_MESSAGE_FREED_SLAVES_AS_FREED_SLAVES",(sCityName, iCount))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	if iCountNewPop > 0:
		iCountImmigrants = iCountNewPop
		if iCountImmigrants > 0:
			for i in range (iCountImmigrants):
				CyPlayer.initUnit(iUnitImmigrant, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			if bHuman:
				sMessage = BugUtil.getText("TXT_MESSAGE_FREED_SLAVES_AS_IMMIGRANTS",(iCountImmigrants*3, sCityName, iCountImmigrants))
				CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	## Now remove those slaves
	if iCountSettled > 0: 
		CyCity.changeFreeSpecialistCount(iSlaveSettled,-iCountSettled)
	if iCountFood > 0: 
		CyCity.changeFreeSpecialistCount(iSlaveFood,-iCountFood)
	if iCountCom > 0: 
		CyCity.changeFreeSpecialistCount(iSlaveCom,-iCountCom)
	if iCountTutor > 0: 
		CyCity.changeFreeSpecialistCount(iSlaveTutor,-iCountTutor)
	if iCountMilitary > 0: 
		CyCity.changeFreeSpecialistCount(iSlaveMilitary,-iCountMilitary)

	## Now convert the other slaves
	if iCountProd > 0:
		for i in range (iCountProd):
			CyPlayer.initUnit(iUnitMerCaravan, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			CyCity.changeFreeSpecialistCount(iSlaveProd,-1)
		if bHuman:
			sMessage = BugUtil.getText("TXT_MESSAGE_FREED_SLAVES_AS_CARAVANS",(sCityName, iCountProd, "Early Merchants"))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	if iCountHealth > 0:
		for i in range (iCountProd):
			CyPlayer.initUnit(iUnitHealth, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			CyCity.changeFreeSpecialistCount(iSlaveHealth,-1)
		if bHuman:
			sMessage = BugUtil.getText("TXT_MESSAGE_FREED_SLAVES_AS_HEALERS",(sCityName, iCountHealth, "Healers"))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	if iCountEntertain > 0:
		for i in range (iCountEntertain):
			CyPlayer.initUnit(iUnitEntertain, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			CyCity.changeFreeSpecialistCount(iSlaveEntertain,-1)
		if bHuman:
			sMessage = BugUtil.getText("TXT_MESSAGE_FREED_SLAVES_AS_STORY_TELLERS",(sCityName, iCountEntertain, "Story Tellers"))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)
	'''
	iCount = CyCity.getSpecialistCount(gc.getInfoTypeForString('SPECIALIST_SETTLED_SLAVE'))
	if iCount > 0:
		for i in range (iCount):
			CyPlayer.initUnit(gc.getCivilizationInfo(CyPlayer.getCivilizationType()).getCivilizationUnits(giUnitCaptiveSlave), X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
		if bHuman:
			sMessage = BugUtil.getText("TXT_KEY_MESSAGE_CAPTURED_SLAVES_AS_GATHERERS",iCount)
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)
	'''

	## Convert population to captives
	iPop = CyCity.getPopulation()
	iCount = 0
	if iPop == 1:
		if CyGame().getSorenRandNum(100, "Captive") < 66:
			CyPlayer.initUnit(giUnitCaptiveCivilian, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			iCount = 1
	else:
		iCivilianCitizenUnits = (iPop + 1) / 2
		for loop in range(iCivilianCitizenUnits):
			CyPlayer.initUnit(giUnitCaptiveCivilian, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			iCount += 1

	if bHuman and iCount:
		sMessage = BugUtil.getText("TXT_KEY_MESSAGE_CIVILIAN_CAPTIVE",iCount)
		CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)


'''
def onCityAcquiredAndKept(self, argsList):
	'City Acquired and Kept'
	iPlayer, CyCity = argsList

	# If there are slaves in the city but the new owner does not run slavery remove the slave buildings and free the slaves
	CyPlayer = gc.getPlayer(iPlayer)
	if CyPlayer.countNumBuildings(gc.getInfoTypeForString("BUILDING_WV_SLAVERY")): return # Running slavery

	sCityName = CyCity.getName()
	X = CyCity.getX()
	Y = CyCity.getY()

	iSlaveSettled = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE")
	iSlaveFood = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_FOOD")
	iSlaveProd = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_PRODUCTION")
	iSlaveCom = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_COMMERCE")
	iSlaveHealth = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_HEALTH")
	iSlaveEntertain = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_ENTERTAINMENT")
	iSlaveTutor = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_TUTOR")
	iSlaveMilitary = gc.getInfoTypeForString("SPECIALIST_SETTLED_SLAVE_MILITARY")

	iUnitCaptiveSlave = gc.getInfoTypeForString("UNIT_FREED_SLAVE")
	iUnitImmigrant = gc.getInfoTypeForString("UNIT_CAPTIVE_IMMIGRANT")
	iUnitEntertain = gc.getInfoTypeForString("UNIT_STORY_TELLER")
	iUnitMerCaravan = gc.getInfoTypeForString("UNIT_EARLY_MERCHANT_C2C")
	iUnitHealth = gc.getInfoTypeForString("UNIT_HEALER")

	iCountSettled = CyCity.getFreeSpecialistCount(iSlaveSettled)
	iCountFood = CyCity.getFreeSpecialistCount(iSlaveFood)
	iCountProd = CyCity.getFreeSpecialistCount(iSlaveProd)
	iCountCom = CyCity.getFreeSpecialistCount(iSlaveCom)
	iCountHealth = CyCity.getFreeSpecialistCount(iSlaveHealth)
	iCountEntertain = CyCity.getFreeSpecialistCount(iSlaveEntertain)
	iCountTutor = CyCity.getFreeSpecialistCount(iSlaveTutor)
	iCountMilitary = CyCity.getFreeSpecialistCount(iSlaveMilitary)

	## Process those that can become population or immagrants 
	##	where 3 slaves = 1 pop or immigrant
	##	and can only increase the city pop to 7
	iCount = iCountSettled + iCountFood + iCountCom + iCountTutor + iCountMilitary
	iCountNewPop = int(iCount/3)
	iCount = iCount - 3*iCountNewPop

	if iCount > 0:
		for i in range (iCount):
			CyPlayer.initUnit(iUnitCaptiveSlave, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
		if bHuman:
			sMessage = BugUtil.getText("TXT_MESSAGE_FREED_SLAVES_AS_FREED_SLAVES",(sCityName, iCount))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	if iCountNewPop > 0:
		iCountImmigrants = iCountNewPop
		iCityPop = CyCity.getPopulation()
		if iCityPop < 7:
			## fill up the local pop and left overs become immigrants
			iMaxToAddPop = 7 - iCityPop
			if iMaxToAddPop > iCountImmigrants:
				CyCity.changePopulation(iCountImmigrants)
				if bHuman:
					sMessage = BugUtil.getText("TXT_MESSAGE_FREED_SLAVES_JOINED_CITY_POPULATION",(iCountImmigrants*3, sCityName, iCountImmigrants))
					CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)
				iCountImmigrants = 0
			else:
				CyCity.changePopulation(iMaxToAddPop)
				if bHuman:
					sMessage = BugUtil.getText("TXT_MESSAGE_FREED_SLAVES_JOINED_CITY_POPULATION",(iMaxToAddPop*3, sCityName, iMaxToAddPop))
					CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)
				iCountImmigrants = iCountImmigrants - iMaxToAddPop
		if iCountImmigrants > 0:
			for i in range (iCountImmigrants):
				CyPlayer.initUnit(iUnitImmigrant, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			if bHuman:
				sMessage = BugUtil.getText("TXT_MESSAGE_FREED_SLAVES_AS_IMMIGRANTS",(iCountImmigrants*3, sCityName, iCountImmigrants))
				CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	## Now remove those slaves
	if iCountSettled > 0: 
		CyCity.changeFreeSpecialistCount(iSlaveSettled,-iCountSettled)
	if iCountFood > 0: 
		CyCity.changeFreeSpecialistCount(iSlaveFood,-iCountFood)
	if iCountCom > 0: 
		CyCity.changeFreeSpecialistCount(iSlaveCom,-iCountCom)
	if iCountTutor > 0: 
		CyCity.changeFreeSpecialistCount(iSlaveTutor,-iCountTutor)
	if iCountMilitary > 0: 
		CyCity.changeFreeSpecialistCount(iSlaveMilitary,-iCountMilitary)

	## Now convert the other slaves
	if iCountProd > 0:
		for i in range (iCountProd):
			CyPlayer.initUnit(iUnitMerCaravan, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			CyCity.changeFreeSpecialistCount(iSlaveProd,-1)
		if bHuman:
			sMessage = BugUtil.getText("TXT_MESSAGE_FREED_SLAVES_AS_CARAVANS",(sCityName, iCountProd, "Early Merchants"))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	if iCountHealth > 0:
		for i in range (iCountProd):
			CyPlayer.initUnit(iUnitHealth, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			CyCity.changeFreeSpecialistCount(iSlaveHealth,-1)
		if bHuman:
			sMessage = BugUtil.getText("TXT_MESSAGE_FREED_SLAVES_AS_HEALERS",(sCityName, iCountHealth, "Healers"))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)

	if iCountEntertain > 0:
		for i in range (iCountEntertain):
			CyPlayer.initUnit(iUnitEntertain, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
			CyCity.changeFreeSpecialistCount(iSlaveEntertain,-1)
		if bHuman:
			sMessage = BugUtil.getText("TXT_MESSAGE_FREED_SLAVES_AS_STORY_TELLERS",(sCityName, iCountEntertain, "Story Tellers"))
			CyInterface().addMessage(iPlayer,False,15, sMessage,'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), X, Y, True,True)
'''