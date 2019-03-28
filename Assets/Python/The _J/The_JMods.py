## Interfaith Project by The_J
## Converted to BUG/WoC for C2C by Dancing Hoskuld
## 
from CvPythonExtensions import *
import BugUtil
import Popup as PyPopup

GC = CyGlobalContext()
GAME = CyGame()
TRNSLTR = CyTranslator()

# globals
###################################################
gb_BarbarianGenerals = -1

gaiEraToMilitiaUnit = None
giCivicForMilitia = -1
giImprovementForMilitia = -1

giSneakPromotion = -1
giMarauderPromot = -1
giIndEpionagePro = -1


def init():
	global gb_BarbarianGenerals
	gb_BarbarianGenerals = GAME.isOption(GameOptionTypes.GAMEOPTION_BARBARIAN_GENERALS) 

## Militia intialiasation.

	global giCivicForMilitia, giImprovementForMilitia, gaiEraToMilitiaUnit
	giCivicForMilitia = GC.getInfoTypeForString( "CIVIC_CONSCRIPTION1" )
	giImprovementForMilitia = GC.getInfoTypeForString('IMPROVEMENT_FARM')

	eraToMilitiaUnit = {
		'ERA_CLASSICAL' :  'UNIT_MILITIA_MEDIEVAL',
		'ERA_MEDIEVAL' :  'UNIT_MILITIA_MEDIEVAL',
		'ERA_RENAISSANCE' :  'UNIT_MILITIA_RENAISSANCE',
		'ERA_INDUSTRIAL' :  'UNIT_MILITIA_INDUSTRIAL',
		'ERA_MODERN' : 'UNIT_MILITIA_MODERN',
		'ERA_INFORMATION' : 'UNIT_MILITIA_MODERN'
		}

	gaiEraToMilitiaUnit = {}
	for sEra, sMilitiaUnit in eraToMilitiaUnit.iteritems():
		iEra = GC.getInfoTypeForString(sEra)
		iMilitiaUnit = GC.getInfoTypeForString(sMilitiaUnit)
		if (iEra >= 0 ) and (iMilitiaUnit >= 0):
			BugUtil.debug("In era %s (%d) militia unit is %s (%d).", sEra,  iEra, sMilitiaUnit, iMilitiaUnit)
			gaiEraToMilitiaUnit[iEra] = iMilitiaUnit
		else:
			BugUtil.debug("In era %s (%d) militia unit is %s (%d) - is invalid. (ignored)", sEra,  iEra, sMilitiaUnit, iMilitiaUnit)

## Sneak iniialisation

	global giSneakPromotion, giMarauderPromot, giIndEpionagePro
	giSneakPromotion = GC.getInfoTypeForString('PROMOTION_SNEAK')
	giMarauderPromot = GC.getInfoTypeForString('PROMOTION_MARAUDER')
	giIndEpionagePro = GC.getInfoTypeForString('PROMOTION_INDUSTRYESPIONAGE')


'''
def onProjectBuilt(argsList):
	CyCity, iProjectType = argsList

	# Interfaith
	if iProjectType == GC.getInfoTypeForString("PROJECT_INTERFAITH"):
		iNumReligions = GC.getNumReligionInfos()
		for iPlayerX in xrange(GC.getMAX_PC_PLAYERS()):
			CyPlayerX = GC.getPlayer(iPlayerX)
			if CyPlayerX.isAlive():
				CyCityX, i = CyPlayerX.firstCity(False)
				while CyCityX:
					for iReligions in xrange(iNumReligions):
						if GAME.isReligionFounded(iReligions) and not CyCityX.isHasReligion(iReligions):
							CyCityX.setHasReligion(iReligions, True, True, True)
					CyCity, i = CyPlayer.nextCity(i, False)
'''

def onReligionFounded(argsList):
	iReligion, iFounder = argsList
###real favorite religion start
	iMaxPlayer = GC.getMAX_PC_PLAYERS ()
	for i in xrange(iMaxPlayer):
		if i == iFounder:continue
		pPlayer = GC.getPlayer(i)
		if not pPlayer.isAlive():continue
		iLeader = pPlayer.getLeaderType ()
		pLeader = GC.getLeaderHeadInfo(iLeader)
		iFavoriteReligion = pLeader.getFavoriteReligion ()
		if iReligion == iFavoriteReligion:
			pCapital = pPlayer.getCapitalCity()
			pCapital.setHasReligion(iReligion,True,True,True)
			if pPlayer.isHuman():
				pReligion = GC.getReligionInfo(iReligion)
				strReligionName = pReligion.getText ()
				popup = PyPopup.PyPopup(-1)
				popup.setHeaderString(TRNSLTR.getText("TXT_REAL_FAVORITE_RELIGION_HEADER",()))
				popup.setBodyString(TRNSLTR.getText("TXT_REAL_FAVORITE_RELIGION_TEXT",(strReligionName,strReligionName)))
				popup.launch(True, PopupStates.POPUPSTATE_IMMEDIATE)
###real favorite religion end


def onImprovementBuilt(argsList):
	iImprovement, iX, iY = argsList
###Militia Start ###
	BugUtil.debug("The_J's mods:- Milita mod.")
	if iImprovement == giImprovementForMilitia:
		BugUtil.debug("The_J's mods:- Milita mod - Farm built.")
		pPlot = CyMap().plot(iX, iY)
		iPlayer = pPlot.getOwner()
		pPlayer = GC.getPlayer(iPlayer)
		if (iPlayer> -1 and pPlayer.isAlive() and pPlayer.isCivic(giCivicForMilitia)):
			iEra = pPlayer.getCurrentEra ()
			BugUtil.debug("Milita mod - Farm built, Civic is Caste System, Era is %s.",  iEra)
			if iEra in gaiEraToMilitiaUnit:
				pNewUnit = pPlayer.initUnit( gaiEraToMilitiaUnit[iEra], iX, iY, UnitAITypes.UNITAI_RESERVE, DirectionTypes.NO_DIRECTION )
				CyInterface().addMessage(iPlayer,False,15,TRNSLTR.getText("TXT_RECRUITED",()),'',0,'Art/Interface/Buttons/Civics/Serfdom.dds',ColorTypes(44), iX, iY, True,True)
###Militia End###


def onCombatResult(argsList):
	CyUnitW, CyUnitL = argsList
	iWinner = CyUnitW.getOwner()
	iLooser = CyUnitL.getOwner()
	CyPlayerW = GC.getPlayer(iWinner)
	CyPlayerL = GC.getPlayer(iLooser)
	CyTeamW = None
	X = Y = -1
	if not CyPlayerL.isNPC():
		iTeamW = CyPlayerW.getTeam()
		iTeamL = CyPlayerL.getTeam()
		CyTeamW = GC.getTeam(iTeamW)
		CyTeamL = GC.getTeam(iTeamL)

		bHumanW = CyPlayerW.isHuman()
		bHumanL = CyPlayerL.isHuman()

		fHandicapFactor = 1
		if bHumanL or bHumanW:
			X = CyUnitW.getX()
			Y = CyUnitW.getY()
			if bHumanL:
				if CyUnitW.isHiddenNationality():
					szLooser = TRNSLTR.getText("TXT_KEY_SNEAK_HIDDEN",())
				else:
					szLooser = CyPlayerW.getName()
			if bHumanW:
				if CyUnitL.isHiddenNationality():
					szWinner = TRNSLTR.getText("TXT_KEY_SNEAK_HIDDEN",())
				else:
					szWinner = CyPlayerL.getName()

			if bHumanL and bHumanW:
				iHandicapFactorW = GC.getHandicapInfo(CyPlayerW.getHandicapType()).getCivicUpkeepPercent()
				iHandicapFactorL = GC.getHandicapInfo(CyPlayerL.getHandicapType()).getCivicUpkeepPercent()
			elif bHumanW:
				iHandicapFactorW = GC.getHandicapInfo(CyPlayerW.getHandicapType()).getCivicUpkeepPercent()
				iHandicapFactorL = 100
			else:
				iHandicapFactorW = 100
				iHandicapFactorL = 100
			if iHandicapFactorW > iHandicapFactorL:
				fHandicapFactor = (iHandicapFactorW - iHandicapFactorL + 100) / 100.0

		# Sneak promo
		if CyUnitW.isHasPromotion(giSneakPromotion):

			iStolen = CyTeamL.getEspionagePointsAgainstTeam(iTeamW) * 2 - CyTeamW.getEspionagePointsAgainstTeam(iTeamL)
			if iStolen > 1:
				iStolen = int((iStolen ** 0.5) / fHandicapFactor)
			if iStolen > 0:
				CyTeamW.changeEspionagePointsAgainstTeam(iTeamL, iStolen)
				CyTeamL.changeEspionagePointsAgainstTeam(iTeamW,-iStolen)
				if bHumanW:
					szText = TRNSLTR.getText("TXT_KEY_SNEAK_YOU", (szWinner,iStolen))
					artPath = ',Art/Interface/Buttons/Process/ProcessCulture.dds,Art/Interface/Buttons/Beyond_the_Sword_Atlas.dds,8,16'
					CyInterface().addMessage(iWinner, False, 15, szText, '', 0, artPath, ColorTypes(44), X, Y, True, True)
				if bHumanL:
					szText = TRNSLTR.getText("TXT_KEY_SNEAK_FROM",(szLooser,iStolen))
					artPath = ',Art/Interface/Buttons/Process/ProcessCulture.dds,Art/Interface/Buttons/Beyond_the_Sword_Atlas.dds,8,16'
					CyInterface().addMessage(iLooser, False, 15, szText, '', 0, artPath, ColorTypes(44), X, Y, True, True)

		# Marauder promo
		if CyUnitW.isHasPromotion(giMarauderPromot):

			iStolen = int(((CyPlayerL.getEffectiveGold() / (CyPlayerL.getNumUnits() + 1)) ** .3) / fHandicapFactor)
			if iStolen > 0:
				CyPlayerL.changeGold(-iStolen)
				CyPlayerW.changeGold(iStolen)
				if bHumanW:
					szText = TRNSLTR.getText("TXT_KEY_MARAUDER_YOU", (szWinner,iStolen))
					artPath = ',Art/Interface/Buttons/TechTree/Banking.dds,Art/Interface/Buttons/TechTree_Atlas.dds,8,1'
					CyInterface().addMessage(iWinner, False, 15, szText, '', 0, artPath, ColorTypes(44), X, Y, True, True)
				if bHumanL:
					szText = TRNSLTR.getText("TXT_KEY_MARAUDER_FROM",(szLooser,iStolen))
					artPath = ',Art/Interface/Buttons/TechTree/Banking.dds,Art/Interface/Buttons/TechTree_Atlas.dds,8,1'
					CyInterface().addMessage(iLooser, False, 15, szText, '', 0, artPath, ColorTypes(44), X, Y, True, True)

		# Industry Espionage promo
		if CyUnitW.isHasPromotion(giIndEpionagePro) and GC.getPlayer(iLooser).getCurrentResearch()>=0:

			iTechW = CyPlayerW.getCurrentResearch()
			iTechL = CyPlayerL.getCurrentResearch()
			if CyTeamL.isHasTech(iTechW) or not CyTeamW.isHasTech(iTechL):
				iStolen = int((CyPlayerL.calculateBaseNetResearch() ** 0.5)/fHandicapFactor)
				if iStolen:
					CyTeamW.changeResearchProgress(iTechW, iStolen, iWinner)
					CyTeamL.changeResearchProgress(iTechL,-iStolen, iLooser)
					if bHumanW:
						szText = TRNSLTR.getText("TXT_KEY_INDUSTRYESPIONAGE_YOU", (szWinner,iStolen))
						artPath = 'Art/Interface/Buttons/Process/ProcessResearch.dds'
						CyInterface().addMessage(iWinner, False, 15, szText, '', 0, artPath, ColorTypes(44), X, Y, True, True)
					if bHumanL:
						szText = TRNSLTR.getText("TXT_KEY_INDUSTRYESPIONAGE_FROM",(szLooser,iStolen))
						artPath = 'Art/Interface/Buttons/Process/ProcessResearch.dds'
						CyInterface().addMessage(iLooser, False, 15, szText, '', 0, artPath, ColorTypes(44), X, Y, True, True)

	iUnitW = CyUnitW.getUnitType()
	## WarriorsOfGod Monk ##
	if iUnitW == GC.getInfoTypeForString("UNIT_MONK"):
		if X == -1 or Y == -1:
			X = CyUnitW.getX()
			Y = CyUnitW.getY()
		CyPlot = CyMap().plot(X, Y)
		if CyPlot.isCity():
			CyCity = CyPlot.getPlotCity()
			iReligion = CyPlayerW.getStateReligion()
			if iReligion != -1 and not CyCity.isHasReligion(iReligion):
				CyCity.setHasReligion(iReligion, True, True, False)
	## WarriorsOfGod Fanatic ##
	elif iUnitW == GC.getInfoTypeForString("UNIT_FANATIC"):
		iReligion = CyPlayerW.getStateReligion()
		if iReligion != -1:
			X = CyUnitL.getX()
			Y = CyUnitL.getY()
			CyPlot = CyMap().plot(X, Y)
			if CyPlot.isCity():
				CyCity = CyPlot.getPlotCity()
				if not CyCity.isHasReligion(iReligion):
					if not CyTeamW:
						iTeamW = CyPlayerW.getTeam()
						CyTeamW = GC.getTeam(iTeamW)
					if CyTeamW.isAtWar(GC.getPlayer(CyCity.getOwner()).getTeam()):
						NumDef = 0
						for i in range (GC.getMAX_PLAYERS()):
							if i == iWinner: continue
							CyPlayer = GC.getPlayer(i)
							iTeam = CyPlayer.getTeam()
							if iTeam == iTeamW: continue
							if CyTeamW.isAtWar(iTeam):
								NumDef += CyPlot.getNumDefenders(i)
								if NumDef > 1:
									break
						if NumDef <= 1:
							CyCity.setHasReligion(i, False, False, False)

	## Barbar hunter ##
	if CyUnitL.isHominid():
		if not CyUnitL.isAnimal():
			if CyUnitW.isHasPromotion(GC.getInfoTypeForString("PROMOTION_BARBARIAN_HUNTER")):
				iBarbXP = GC.getDefineINT("BARBARIAN_MAX_XP_VALUE") 
				if CyUnitW.getExperience() >= iBarbXP:
					CyUnitW.changeExperience(1, 999, True, False, gb_BarbarianGenerals)

	## Hunter
	if CyUnitL.isAnimal():
		if CyUnitW.isHasPromotion(GC.getInfoTypeForString("PROMOTION_ANIMAL_HUNTER")) or CyUnitW.isHasPromotion(GC.getInfoTypeForString("PROMOTION_SEA_ANIMAL_HUNTER")):
			if CyUnitW.getExperience() >= GC.getDefineINT("ANIMAL_MAX_XP_VALUE"):
				CyUnitW.changeExperience(1, 999, True, False, gb_BarbarianGenerals)


def onUnitBuilt(argsList):
	'Unit Completed'
	city = argsList[0]
	unit = argsList[1]
###WarriorsOfGod Fanatic Part2 Start ###
	strUnit = GC.getUnitInfo(unit.getUnitType()).getType()
	CurrentUnit = GC.getInfoTypeForString(strUnit)
	if (CurrentUnit == GC.getInfoTypeForString("UNIT_FANATIC")):
		iPlayer = city.getOwner()
		pPlayer = GC.getPlayer(iPlayer)
		iReligion = pPlayer.getStateReligion()
		NumReligions = GC.getNumReligionInfos ()
		for i in range (NumReligions):
			if ((city.isHasReligion(i)==True) and (i<>iReligion)):
				unit.changeExperience(2,100,False,False,False)
###WarriorsOfGod Fanatic Part2 End ###

###WarriorsOfGod Monk Part2 Start ###
	elif (CurrentUnit == GC.getInfoTypeForString("UNIT_MONK")):
		iPlayer = city.getOwner()
		pPlayer = GC.getPlayer(iPlayer)
		iReligion = pPlayer.getStateReligion()
		if iReligion<0:return
		MaxNumRelBuildings = 3
		CountBuildings = 0
		for i in range(GC.getNumBuildingInfos ()):
			thisbuilding = GC.getBuildingInfo (i)
			thisreligion = thisbuilding.getPrereqReligion ()
			if thisbuilding.getHolyCity ()==iReligion:
				if (city.getNumRealBuilding(i)==True) :
					unit.changeExperience(4,100,False,False,False)
			if thisreligion == iReligion:
				if (city.getNumRealBuilding(i)==True) :
					unit.changeExperience(2,100,False,False,False)
					CountBuildings = CountBuildings+1
					if CountBuildings>=MaxNumRelBuildings:
						break

		ApostolicPalace = GC.getInfoTypeForString("DIPLOVOTE_POPE")
		if ((pPlayer.isFullMember(ApostolicPalace)==True)and (GAME.isDiploVote(ApostolicPalace)==True)):
		    unit.changeExperience(4,100,False,False,False)
###sOfGod Monk Part2 End ###


def onUnitPromoted(argsList):
	'Unit Promoted'
	CyUnit, iPromotion = argsList
	CyPlayer = GC.getPlayer(CyUnit.getOwner())

	# AI promotion redirection
	if not CyPlayer.isHuman():
		iDomainType = CyUnit.getDomainType()
		if iDomainType == GC.getInfoTypeForString('DOMAIN_LAND') and CyUnit.isHasUnitCombat(GC.getInfoTypeForString("UNITCOMBAT_HUNTER")):
			# Hunter
			for KEY in ("PROMOTION_HUNTER1", "PROMOTION_HUNTER2", "PROMOTION_HUNTER3", "PROMOTION_HUNTER_GREAT"):
				iTemp = GC.getInfoTypeForString(KEY)
				if iPromotion == iTemp: return
				if CyUnit.canAcquirePromotion(iTemp):
					CyUnit.setHasPromotion(iPromotion, False)
					CyUnit.setHasPromotion(iTemp, True)
					return
		elif iDomainType == GC.getInfoTypeForString('DOMAIN_SEA') and CyUnit.isHasUnitCombat(GC.getInfoTypeForString("UNITCOMBAT_RECON")):
			# Sea Hunter
			for KEY in ("PROMOTION_SEA_HUNTER1", "PROMOTION_SEA_HUNTER2", "PROMOTION_SEA_HUNTER3", "PROMOTION_SEA_HUNTER_GREAT"):
				iTemp = GC.getInfoTypeForString('PROMOTION_SEA_HUNTER1')
				if iPromotion == iTemp: return
				if CyUnit.canAcquirePromotion(iTemp):
					CyUnit.setHasPromotion(iPromotion, False)
					CyUnit.setHasPromotion(iTemp, True)
					return
		# Sneak
		if iPromotion != giSneakPromotion:
			if CyUnit.canAcquirePromotion(giSneakPromotion):
				if not GAME.getSorenRandNum(4, "Spy"):
					CyUnit.setHasPromotion(iPromotion, False)
					CyUnit.setHasPromotion(giSneakPromotion, True)
					return
		# Marauder 
		if iPromotion != giMarauderPromot:
			if CyUnit.canAcquirePromotion(giMarauderPromot):
				if not GAME.getSorenRandNum(4, "Gold"):
					CyUnit.setHasPromotion(iPromotion, False)
					CyUnit.setHasPromotion(giMarauderPromot, True)
					return
		# Industry Espionage
		if iPromotion != giIndEpionagePro:
			if CyUnit.canAcquirePromotion(giIndEpionagePro):
				if not GAME.getSorenRandNum(4, "Research"):
					CyUnit.setHasPromotion(iPromotion, False)
					CyUnit.setHasPromotion(giIndEpionagePro, True)
					return
		# Barbarian Hunter
		if not GAME.isOption(GameOptionTypes.GAMEOPTION_NO_BARBARIANS):
			iTemp = GC.getInfoTypeForString('PROMOTION_BARBARIAN_HUNTER')
			if iPromotion != iTemp:
				if CyUnit.canAcquirePromotion(iTemp):
					if GAME.isOption(GameOptionTypes.GAMEOPTION_RAGING_BARBARIANS):
						iDec = 3
					else:
						iDec = 5
					if not GAME.getSorenRandNum(iDec, "BarbHunt"):
						CyUnit.setHasPromotion(iPromotion, False)
						CyUnit.setHasPromotion(iTemp, True)
						return


def onCityRazed(argsList):
	pCity, iPlayer = argsList

	# messages - wonder destroyed
	if pCity.getNumWorldWonders() > 0:
		for i in range(GC.getNumBuildingInfos()):
			if pCity.getNumBuilding(i)>0:
				thisbuilding = GC.getBuildingInfo(i)
				if GC.getBuildingClassInfo(thisbuilding.getBuildingClassType()).getMaxGlobalInstances() == 1:
					ConquerPlayer = GC.getPlayer(iPlayer)
					iConquerTeam = ConquerPlayer.getTeam()
					ConquerName = ConquerPlayer.getName()
					WonderName = thisbuilding.getDescription()
					iX = pCity.getX()
					iY = pCity.getY()
					for iPlayerX in range (GC.getMAX_PC_PLAYERS()):
						ThisPlayer = GC.getPlayer(iPlayerX)
						iThisTeam = ThisPlayer.getTeam()
						ThisTeam = GC.getTeam(iThisTeam)
						if ThisTeam.isHasMet(iConquerTeam):
							if iPlayerX == iPlayer:
								CyInterface().addMessage(iPlayerX,False,15,TRNSLTR.getText("TXT_KEY_YOU_DESTROYED_WONDER",(ConquerName,WonderName)),'',0,'Art/Interface/Buttons/General/warning_popup.dds',ColorTypes(GC.getInfoTypeForString("COLOR_RED")), iX, iY, True,True)
							else:
								CyInterface().addMessage(iPlayerX,False,15,TRNSLTR.getText("TXT_KEY_DESTROYED_WONDER",(ConquerName,WonderName)),'',0,'Art/Interface/Buttons/General/warning_popup.dds',ColorTypes(GC.getInfoTypeForString("COLOR_RED")), iX, iY, True,True)


def onCityAcquiredAndKept(argsList):
	iPlayer, pCity = argsList

	# messages - wonder captured
	if pCity.getNumWorldWonders() > 0:
		for i in range(GC.getNumBuildingInfos()):
			if pCity.getNumBuilding(i) > 0:
				thisbuilding = GC.getBuildingInfo(i)
				if GC.getBuildingClassInfo(thisbuilding.getBuildingClassType()).getMaxGlobalInstances() == 1:
					ConquerPlayer = GC.getPlayer(iPlayer)
					iConquerTeam = ConquerPlayer.getTeam()
					ConquerName = ConquerPlayer.getName()
					WonderName = thisbuilding.getDescription()
					iX = pCity.getX()
					iY = pCity.getY()
					for iPlayerX in range (GC.getMAX_PC_PLAYERS()):
						ThisPlayer = GC.getPlayer(iPlayerX)
						iThisTeam = ThisPlayer.getTeam()
						ThisTeam = GC.getTeam(iThisTeam)
						if ThisTeam.isHasMet(iConquerTeam):
							if iPlayerX == iPlayer:
								CyInterface().addMessage(iPlayerX,False,15,TRNSLTR.getText("TXT_KEY_YOU_CAPTURED_WONDER",(ConquerName,WonderName)),'',0,'Art/Interface/Buttons/General/happy_person.dds',ColorTypes(GC.getInfoTypeForString("COLOR_GREEN")), iX, iY, True,True)
							else:
								CyInterface().addMessage(iPlayerX,False,15,TRNSLTR.getText("TXT_KEY_CAPTURED_WONDER",(ConquerName,WonderName)),'',0,'Art/Interface/Buttons/General/warning_popup.dds',ColorTypes(GC.getInfoTypeForString("COLOR_RED")), iX, iY, True,True)
