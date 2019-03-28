## Sid Meier's Civilization 4
## Copyright Firaxis Games 2006
## 
## PlatyPing Python Wonders and Projects
##   - 
##   - Cyrus Cylinder
##   - Lotus Temple
##   - Montreal Biodome
##   - Nazca Lines
##   + lots more
## 
## Converted to BUG/WoC format for caveman2Cosmos mod by DancingHoskuld

from CvPythonExtensions import *

# globals
GC = CyGlobalContext()
localText = CyTranslator()

agBiodomeAnimalList = None

# globals
###################################################
def init():
	global agBiodomeAnimalList
	agBiodomeAnimalList = []

	for iUnit in xrange(GC.getNumUnitInfos()):
		UnitInfo = GC.getUnitInfo(iUnit)
		sType = UnitInfo.getType()
		if sType.find("UNIT_SUBDUED") > -1:
			agBiodomeAnimalList.append(iUnit)


def onBeginPlayerTurn(argsList):
	'Called at the beginning of a players turn'
	iGameTurn, iPlayer = argsList

## Cyrus Cylinder
	CyPlayer = GC.getPlayer(iPlayer)
	if CyPlayer.isAlive():

		iTeam = CyPlayer.getTeam()
		KEY = GC.getInfoTypeForString("BUILDING_CYRUS_CYLINDER")
		if KEY > -1: # Make sure the building is in the game.
			obsoleteTech = GC.getBuildingInfo(KEY).getObsoleteTech()

			if GC.getTeam(iTeam).isHasTech(obsoleteTech) == False or obsoleteTech == -1:
				if CyPlayer.countNumBuildings(KEY) == 1:
					Value = 400 +iGameTurn
					for iPlayerX in range(GC.getMAX_PC_PLAYERS()):
						CyPlayerX = GC.getPlayer(iPlayerX)
						if CyPlayerX.isAlive():
							if GC.getTeam(CyPlayerX.getTeam()).isVassal(iTeam):
								Value = int( 0.9 *Value)
					GGpoint = int(CyGame().getPlayerScore(iPlayer)/Value)
					if GGpoint > 9:
						GGpoint = 10
					CyPlayer.changeCombatExperience(GGpoint)

	## Zizkov
		KEY = GC.getInfoTypeForString("BUILDING_ZIZKOV")
		if KEY > -1 and CyPlayer.countNumBuildings(KEY):
			for iPlayerX in range(GC.getMAX_PC_PLAYERS()):
				CyPlayerX = GC.getPlayer(iPlayerX)
				if not CyPlayerX.isAlive(): continue
				iTeamX = CyPlayerX.getTeam()
				if not GC.getTeam(iTeamX).isHasTech(GC.getInfoTypeForString("TECH_SATELLITES")):
					if iTeamX != iTeam and not GC.getTeam(iTeamX).isVassal(iTeam):
						concealchance = CyGame().getSorenRandNum(10, "Conceal")
						if concealchance ==0:
							CyMap().setRevealedPlots(iTeamX, False, False)
							for iCity2 in range(CyPlayerX.getNumCities()):
								pCity2 = CyPlayerX.getCity(iCity2)
								clevel = pCity2.getCultureLevel() + 2
								iX = pCity2.getX()
								iY = pCity2.getY()
								for x in range(iX - clevel, iX+clevel +1):
									for y in range(iY - clevel, iY+ clevel +1):
										pPlot = CyMap().plot(x,y)
										pPlot.setRevealed(iTeamX, True, False, -1)
							CyInterface().addMessage(iPlayer,True,20,localText.getText("TXT_ZIZKOV1",(CyPlayerX.getCivilizationDescription(iPlayerX),)),'',0,'',-1,-1,-1, False,False)
							CyInterface().addMessage(iPlayerX,True,20,localText.getText("TXT_ZIZKOV2",()),'',0,'',-1, -1,-1,False,False)


def onCityDoTurn(argsList):
	'City Production'
	pCity = argsList[0]
	iPlayer = argsList[1]

	pPlayer = GC.getPlayer(iPlayer)
	if not pPlayer.isAlive():
		return

## Biodome Start ##
	if CyGame().getGameTurn() % 5 ==0:
			
		b_Biodome = GC.getInfoTypeForString("BUILDING_BIODOME")
		if b_Biodome > -1 and len(agBiodomeAnimalList) > 0:
			if pCity.getNumActiveBuilding(b_Biodome) > 0:
			
				iX = pCity.getX()
				iY = pCity.getY()
				animal = agBiodomeAnimalList[CyGame().getSorenRandNum(len(agBiodomeAnimalList), "Which Animal")]

				pNewUnit = pPlayer.initUnit( animal, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION )

				pCity.addProductionExperience(pNewUnit, False)
				CyInterface().addMessage(iPlayer,True,20,localText.getText("TXT_NEW_ANIMAL",(pNewUnit.getName(),)),'',0,pNewUnit.getButton(),ColorTypes(11), iX, iY, True,True)

## Biodome End ##


def onEndPlayerTurn(argsList):
	'Called at the end of a players turn'
	iGameTurn, iPlayer = argsList

	CyPlayer = GC.getPlayer(iPlayer)
	if not CyPlayer.isAlive():
		return

## Wembley Stadium
	KEY = GC.getInfoTypeForString("BUILDING_WEMBLEY")
	if KEY > -1 and CyPlayer.countNumBuildings(KEY):
		ExcessHappy = CyPlayer.calculateTotalCityHappiness() - CyPlayer.calculateTotalCityUnhappiness()
		if ExcessHappy > 0:
			iNewGold = int(ExcessHappy * 2.5)
			CyPlayer.changeGold(iNewGold)


def onBuildingBuilt(argsList):
	CyCity, iBuildingType = argsList

## Lotus
	if iBuildingType == GC.getInfoTypeForString( 'BUILDING_LOTUS_TEMPLE' ):
		pPlayer = GC.getPlayer(CyCity.plot().getOwner())
		pID = pPlayer.getID()
		iTeam = pPlayer.getTeam()
		for iPlayer2 in range(GC.getMAX_PC_PLAYERS()):
			pPlayer2 = GC.getPlayer(iPlayer2)
			pID2 = pPlayer2.getID()
			iTeam2 = pPlayer2.getTeam()
			if (pPlayer2.isAlive()==True) and (pPlayer2.isNPC()==False) and pPlayer != pPlayer2:
				while pPlayer.AI_getAttitudeExtra(pID2) < GC.getInfoTypeForString("ATTITUDE_CAUTIOUS"):
					pPlayer.AI_changeAttitudeExtra(iTeam2, 1)
				while pPlayer2.AI_getAttitudeExtra(pID) < GC.getInfoTypeForString("ATTITUDE_CAUTIOUS"):
					pPlayer2.AI_changeAttitudeExtra(iTeam, 1)

## Nazca Lines
	elif iBuildingType == GC.getInfoTypeForString("BUILDING_NAZCA_LINES"):
		pPlayer = GC.getPlayer(CyCity.getOwner())
		KEY = GC.getInfoTypeForString("BUILDINGCLASS_NAZCA_LINES")
		currentEra = pPlayer.getCurrentEra()

		for i in range (currentEra + 1):
			nazcabenefits = CyGame().getSorenRandNum(8, "Nazca")
			if nazcabenefits == 0:
				change = CyCity.getBuildingCommerceChange(KEY, 0)
				CyCity.setBuildingCommerceChange(KEY, 0, change + 4)
			elif nazcabenefits == 1:
				change = CyCity.getBuildingCommerceChange(KEY, 1)
				CyCity.setBuildingCommerceChange(KEY, 1, change + 4)
			elif nazcabenefits == 2:
				change = CyCity.getBuildingCommerceChange(KEY, 2)
				CyCity.setBuildingCommerceChange(KEY, 2, change + 4)
			elif nazcabenefits == 3:
				change = CyCity.getBuildingCommerceChange(KEY, 3)
				CyCity.setBuildingCommerceChange(KEY, 3, change + 4)
			elif nazcabenefits == 4:
				change = CyCity.getBuildingYieldChange(KEY, 0)
				CyCity.setBuildingYieldChange(KEY, 0, change + 4)
			elif nazcabenefits == 5:
				change = CyCity.getBuildingYieldChange(KEY, 1)
				CyCity.setBuildingYieldChange(KEY, 1, change + 4)
			elif nazcabenefits == 6:
				change = CyCity.getBuildingHappyChange(KEY)
				CyCity.setBuildingHappyChange(KEY, change + 2)
			else:
				change = CyCity.getBuildingHealthChange(KEY)
				CyCity.setBuildingHealthChange(KEY, change + 2)

## Taipei 101
	elif iBuildingType == GC.getInfoTypeForString( 'BUILDING_TAIPEI_101' ):
		iPlayer = CyCity.getOwner()
		pPlayer = GC.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()

	#### Check for all players, alive and non-barbarian
		for iPlayerX in range(GC.getMAX_PC_PLAYERS()):
			pPlayerX = GC.getPlayer(iPlayerX)
			if pPlayerX.isAlive():
				pPlayerX.AI_changeAttitudeExtra(iTeam, 3)

## Empire State Building
	elif iBuildingType == GC.getInfoTypeForString("BUILDING_EMPIRE_STATE_BUILDING"):
		iPlayer = CyCity.getOwner()

		aInvalidBonusClasses = [
			GC.getInfoTypeForString("BONUSCLASS_RUSH"),
			GC.getInfoTypeForString("BONUSCLASS_MODERN"),
			GC.getInfoTypeForString("BONUSCLASS_WONDER"),
			GC.getInfoTypeForString("BONUSCLASS_FUEL")
		]
		#Find out how many valid bonuses exist
		aList = []
		for iBonus in range(GC.getNumBonusInfos()):
			CvBonus = GC.getBonusInfo(iBonus)
			if CvBonus.getPlacementOrder() < 0: continue
			if CvBonus.getBonusClassType() not in aInvalidBonusClasses and CvBonus.getTechObsolete() == -1:
				aList.append([iBonus, CvBonus])

		n = 0
		len = len(aList)
		while n < 3:
			i = CyGame().getSorenRandNum(len, "Freebie")
			iBonus, CvBonus = aList[i]
			CyCity.changeFreeBonus(iBonus, 1)
			szTxt = localText.getText("TXT_EMPIRE_BONUS",(CvBonus.getDescription(),))
			CyInterface().addMessage(iPlayer, True, 20, szTxt, '', 0, '', -1, -1, -1, False, False)
			n +=1

## Tsukiji
	elif iBuildingType == GC.getInfoTypeForString( 'BUILDING_TSUKIJI' ):
		iPlayer = CyCity.getOwner()
		pTeam = GC.getTeam(GC.getPlayer(iPlayer).getTeam())
		fish = GC.getInfoTypeForString("BONUS_FISH")
		clam = GC.getInfoTypeForString("BONUS_CLAM")
		crab = GC.getInfoTypeForString("BONUS_CRAB")
		fboat = GC.getInfoTypeForString("IMPROVEMENT_FISHING_BOATS")
		iX = CyCity.getX()
		iY = CyCity.getY()

		pTeam.changeImprovementYieldChange(fboat, 0, 1)
		pTeam.changeImprovementYieldChange(fboat, 2, 1)

		for x in range(iX - 2, iX + 3):
			for y in range(iY - 2, iY + 3):
				pPlot = CyMap().plot(x,y)
				if pPlot.isPlayerCityRadius(iPlayer):
					if pPlot.isWater() and  pPlot.getBonusType(-1)== -1:
						randBonus = CyGame().getSorenRandNum(10, "Freebie")
						if randBonus < 2:
							pPlot.setBonusType(fish)
							pPlot.setImprovementType(fboat)
							CyInterface().addMessage(iPlayer,True,20,localText.getText("TXT_TSUKIJI_BONUS",(GC.getBonusInfo(fish).getDescription(),)),'',0, GC.getBonusInfo(fish).getButton(),ColorTypes(11), iX, iY, True,True)
						elif randBonus == 2:
							pPlot.setBonusType(clam)
							pPlot.setImprovementType(fboat)
							CyInterface().addMessage(iPlayer,True,20,localText.getText("TXT_TSUKIJI_BONUS",(GC.getBonusInfo(clam).getDescription(),)),'',0, GC.getBonusInfo(fish).getButton(),ColorTypes(11), iX, iY, True,True)
						elif randBonus == 3:
							pPlot.setBonusType(crab)
							pPlot.setImprovementType(fboat)
							CyInterface().addMessage(iPlayer,True,20,localText.getText("TXT_TSUKIJI_BONUS",(GC.getBonusInfo(crab).getDescription(),)),'',0, GC.getBonusInfo(fish).getButton(),ColorTypes(11), iX, iY, True,True)

## Zizkov
	elif iBuildingType == GC.getInfoTypeForString("BUILDING_ZIZKOV"):
		pPlayer = GC.getPlayer(CyCity.getOwner())
		iTeam = pPlayer.getTeam()

	#### Reveals whole map for owner
		CyMap().setRevealedPlots(iTeam, True, False)

		for iPlayer2 in range(GC.getMAX_PC_PLAYERS()):
			pPlayer2 = GC.getPlayer(iPlayer2)
			if pPlayer2.isAlive():
				iTeam2 = pPlayer2.getTeam()
				if (iTeam2 != iTeam):
					if ( GC.getTeam(iTeam2).isVassal(iTeam) == False ):

					#### Covers whole map for other players
						CyMap().setRevealedPlots(iTeam2, False, False)

					#### Reveals plots around cities
						for iCity2 in range(pPlayer2.getNumCities()):
							pCity2 = pPlayer2.getCity(iCity2)
							clevel = pCity2.getCultureLevel() + 2
							iX = pCity2.getX()
							iY = pCity2.getY()
							for x in range(iX - clevel, iX+clevel +1):
								for y in range(iY - clevel, iY+ clevel +1):
									pPlot = CyMap().plot(x,y)
									pPlot.setRevealed(iTeam2, True, False, -1)
		CyInterface().addImmediateMessage( localText.getText("TXT_GLOBAL_JAM",()), None)



def onTechAcquired(argsList):
	iTechType, iTeam, iPlayer, bAnnounce = argsList
	# Note that iPlayer may be NULL (-1) and not a refer to a player object
	if iPlayer == -1: return

## Nazca Lines Start ##
	iBuilding = GC.getInfoTypeForString("BUILDING_NAZCA_LINES")
	CyPlayer = GC.getPlayer(iPlayer)
	if iBuilding > -1 and CyPlayer.countNumBuildings(iBuilding):
		CyTeam = GC.getTeam(iTeam)
		bNewEra = True
		for iTech in range(GC.getNumTechInfos()):
			if CyTeam.isHasTech(iTech) and iTech != iTechType:
				if GC.getTechInfo(iTech).getEra() >= GC.getTechInfo(iTechType).getEra():
					bNewEra = False
					break
		if bNewEra:
			iBuildingClass = GC.getInfoTypeForString("BUILDINGCLASS_NAZCA_LINES")
			CyCity, iter = CyPlayer.firstCity(False)
			while CyCity:
				if CyCity.getNumActiveBuilding(iBuilding) > 0:
					nazcabenefits = CyGame().getSorenRandNum(8, "Nazca")
					if nazcabenefits == 0:
						change = CyCity.getBuildingCommerceChange(iBuildingClass, 0)
						CyCity.setBuildingCommerceChange(iBuildingClass, 0, change + 4)
					elif nazcabenefits == 1:
						change = CyCity.getBuildingCommerceChange(iBuildingClass, 1)
						CyCity.setBuildingCommerceChange(iBuildingClass, 1, change + 4)
					elif nazcabenefits == 2:
						change = CyCity.getBuildingCommerceChange(iBuildingClass, 2)
						CyCity.setBuildingCommerceChange(iBuildingClass, 2, change + 4)
					elif nazcabenefits == 3:
						change = CyCity.getBuildingCommerceChange(iBuildingClass, 3)
						CyCity.setBuildingCommerceChange(iBuildingClass, 3, change + 4)
					elif nazcabenefits == 4:
						change = CyCity.getBuildingYieldChange(iBuildingClass, 0)
						CyCity.setBuildingYieldChange(iBuildingClass, 0, change + 4)
					elif nazcabenefits == 5:
						change = CyCity.getBuildingYieldChange(iBuildingClass, 1)
						CyCity.setBuildingYieldChange(iBuildingClass, 1, change + 4)
					elif nazcabenefits == 6:
						change = CyCity.getBuildingHappyChange(iBuildingClass)
						CyCity.setBuildingHappyChange(iBuildingClass, change + 2)
					else:
						change = CyCity.getBuildingHealthChange(iBuildingClass)
						CyCity.setBuildingHealthChange(iBuildingClass, change + 2)
					CyInterface().addImmediateMessage(localText.getText("TXT_NAZCA_LINES",()), None)
					break
				CyCity, iter = CyPlayer.nextCity(iter, False)


def onCombatResult(argsList):
	CyUnitW, CyUnitL = argsList

	iPlayerW = CyUnitW.getOwner()
	iPlayerL = CyUnitL.getOwner()
	CyPlayerW = GC.getPlayer(iPlayerW)
	CyPlayerL = GC.getPlayer(iPlayerL)

## Catacombs
	if CyUnitL.plot().isCity():
		KEY = GC.getInfoTypeForString("BUILDING_CATACOMBS")
		if KEY > -1 and CyPlayerL.countNumBuildings(KEY) == 1:
			obsoleteTech = GC.getBuildingInfo(KEY).getObsoleteTech()
			if obsoleteTech == -1 or not GC.getTeam(CyPlayerL.getTeam()).isHasTech(obsoleteTech):
				burialchance = CyGame().getSorenRandNum(10, "die together")
				if burialchance < int(CyUnitW.getDamage() / 25):
					CyUnitW.setDamage(100, False)
					szText = localText.getText("TXT_MASS_BURIAL", (CyUnitW.getName(),CyUnitL.getName(),))
					CyInterface().addMessage(iPlayerL, True, 20, szText, '', 0, '', -1, -1, -1, True, True)
					CyInterface().addMessage(iPlayerW, True, 20, szText, '', 0, '', -1, -1, -1, True, True)

## Pergamon Altar
	KEY = GC.getInfoTypeForString("BUILDING_PERGAMON")
	if KEY > -1 and CyPlayerW.countNumBuildings(KEY) and not CyPlayerL.isNPC():
		iGGChange = CyPlayerL.getCombatExperience() # Adjusted to only let you steal something they have. Dancing Hoskukd March 2012 ##
		if iGGChange > 0:
			if iGGChange > 2:
				iGGChange = 2
			CyPlayerW.changeCombatExperience(iGGChange)
			CyPlayerL.changeCombatExperience(-iGGChange)


def onUnitBuilt(argsList):
	CyCity = argsList[0]
	CyUnit = argsList[1]

## Fa Men Si
	FA_MEN_SI = GC.getInfoTypeForString("BUILDING_FA_MEN_SI")
	if FA_MEN_SI > -1 and GC.getPlayer(CyCity.getOwner()).countNumBuildings(FA_MEN_SI):
		if GC.getUnitInfo(CyUnit.getUnitType()).getPrereqReligion() > -1:
			CyUnit.setHasPromotion(GC.getInfoTypeForString("PROMOTION_FA_MEN_SI_INSPIRED"), True)


def onUnitKilled(argsList):
	'Unit Killed'
	unit, iAttacker = argsList

## Tomb of Cyrus
	iPlayer = unit.getOwner()
	pPlayer = GC.getPlayer(iPlayer)
	KEY = GC.getInfoTypeForString("BUILDING_CYRUS_TOMB")
	if KEY > -1 and pPlayer.countNumBuildings(KEY) == 1:
		if unit.isHasPromotion(GC.getInfoTypeForString("PROMOTION_LEADER")) or unit.getUnitType() == GC.getInfoTypeForString("UNIT_GREAT_GENERAL"):
			(loopCity, iter) = pPlayer.firstCity(False)
			while(loopCity):
				if loopCity.getNumActiveBuilding(KEY) > 0:
					pNewUnit = pPlayer.initUnit(GC.getInfoTypeForString("UNIT_GREAT_GENERAL"), loopCity.getX(), loopCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
					pNewUnit.setName(unit.getNameNoDesc())
					pNewUnit.setImmobileTimer(8)
					CyInterface().addMessage(iPlayer,True,15,localText.getText("TXT_GG_REVIVE",(unit.getNameNoDesc(),)),'',0,'Art/Cyrus_Tomb/cyrustomb_button.dds',ColorTypes(11),loopCity.getX(), loopCity.getY(), True,True)
					break
				(loopCity, iter) = pPlayer.nextCity(iter, False)



def onUnitSpreadReligionAttempt(argsList):
	'Unit tries to spread religion to a city'
	CyUnit, iReligion, bSuccess = argsList

## Fa Men Si
	if not bSuccess:
		FA_MEN_SI = GC.getInfoTypeForString("BUILDING_FA_MEN_SI")
		if FA_MEN_SI > -1 and GC.getPlayer(CyUnit.getOwner()).countNumBuildings(FA_MEN_SI):
			CyCity = CyMap().plot(CyUnit.getX(), CyUnit.getY()).getPlotCity()
			CyCity.setHasReligion(GC.getUnitInfo(CyUnit.getUnitType()).getPrereqReligion(), True, True, True)


def onCityRazed(argsList):
	'City Razed'
	city, iPlayer = argsList
	iOwner = city.findHighestCulture()
	
## Taipei 101 Start ##
	b_Taipei = GC.getInfoTypeForString("BUILDING_TAIPEI_101")
	if b_Taipei > -1 and city.getNumActiveBuilding(b_Taipei) > 0:
		pPlayer = GC.getPlayer(iPlayer)
		iTeam = pPlayer.getTeam()

		for iPlayerX in range(GC.getMAX_PC_PLAYERS()):
			pPlayerX = GC.getPlayer(iPlayerX)
			if pPlayerX.isAlive():
				pPlayerX.AI_changeAttitudeExtra(iTeam, -3)
## Taipei 101 End ##

## Tsukiji Start ##
	b_Tsukiji = GC.getInfoTypeForString("BUILDING_TSUKIJI")
	if b_Tsukiji > -1 and city.getNumActiveBuilding(b_Tsukiji) > 0:
		pPlayer = GC.getPlayer(iPlayer)
		pTeam = GC.getTeam(pPlayer.getTeam())
		fboat = GC.getInfoTypeForString( 'IMPROVEMENT_FISHING_BOATS' )

		pTeam.changeImprovementYieldChange(fboat, 0, -1)
		pTeam.changeImprovementYieldChange(fboat, 2, -1)
## Tsukiji End ##

def onCityAcquired(argsList):
	'City Acquired'
	iPreviousOwner,iNewOwner,pCity,bConquest,bTrade = argsList

## Taipei 101 Start ##
	b_Taipei = GC.getInfoTypeForString("BUILDING_TAIPEI_101")

#### If Taipei switches owner
	if b_Taipei > -1 and pCity.getNumActiveBuilding(b_Taipei) > 0:
		pPlayer = GC.getPlayer(iPreviousOwner)
		pPlayer2 = GC.getPlayer(iNewOwner)
		iTeam = pPlayer.getTeam()
		iTeam2 = pPlayer2.getTeam()

	#### Add for new owner
		for iPlayerX in range(GC.getMAX_PC_PLAYERS()):
			pPlayerX = GC.getPlayer(iPlayerX)
			if pPlayerX.isAlive():
				pPlayerX.AI_changeAttitudeExtra(iTeam2, 3)

	#### Reduce for old owner
		for iPlayerX in range(GC.getMAX_PC_PLAYERS()):
			pPlayerX = GC.getPlayer(iPlayerX)
			if pPlayerX.isAlive():
				pPlayerX.AI_changeAttitudeExtra(iTeam, -3)
## Taipei 101 End ##

## Empire State Building Start ##
	b_Empire = GC.getInfoTypeForString("BUILDING_EMPIRE_STATE_BUILDING")
	if b_Empire > -1 and pCity.getNumActiveBuilding(b_Empire) > 0:
		freebie = 0
		for i in range(400):
			randBonus = CyGame().getSorenRandNum(GC.getNumBonusInfos(), "Freebie")
			bonusinfo = GC.getBonusInfo(randBonus)
			if bonusinfo.getBonusClassType() < 3 and bonusinfo.getTechObsolete() == -1 and randBonus != GC.getInfoTypeForString("BONUS_COAL"):	## Coal, Rush, Modern, Wonder Types  and Obsolete ones Excluded
				pCity.changeFreeBonus(randBonus,1)
				CyInterface().addMessage(iNewOwner,True,20,localText.getText("TXT_EMPIRE_BONUS",(bonusinfo.getDescription(),)),'',0,'',-1,-1,-1, False,False)
				freebie +=1
			if freebie == 3:
				break
## Empire State Building End ##

## Tsukiji Start ##
	b_Tsukiji = GC.getInfoTypeForString("BUILDING_TSUKIJI")
	if b_Tsukiji > -1 and pCity.getNumActiveBuilding(b_Tsukiji) > 0:
		pPlayer = GC.getPlayer(iPreviousOwner)
		pPlayer2 = GC.getPlayer(iNewOwner)
		pTeam = GC.getTeam(pPlayer.getTeam())
		pTeam2 = GC.getTeam(pPlayer2.getTeam())
		fboat = GC.getInfoTypeForString( 'IMPROVEMENT_FISHING_BOATS' )

		pTeam.changeImprovementYieldChange(fboat, 0, -1)
		pTeam.changeImprovementYieldChange(fboat, 2, -1)
		pTeam2.changeImprovementYieldChange(fboat, 0, 1)
		pTeam2.changeImprovementYieldChange(fboat, 2, 1)
## Tsukiji End ##

def onNukeExplosion(argsList):
	'Nuke Explosion'
	pPlot, pNukeUnit = argsList

## NPT Start ##
	iPlayer = pNukeUnit.getOwner()
	pPlayer = GC.getPlayer(iPlayer)
	iTeam = pPlayer.getTeam()
	pTeam = GC.getTeam(iTeam)
	if CyGame().getProjectCreatedCount(GC.getInfoTypeForString("PROJECT_NPT")) == 1:
		for iPlayerX in range(GC.getMAX_PC_PLAYERS()):
			pPlayerX = GC.getPlayer(iPlayerX)
			if pPlayerX.isAlive() and iPlayerX != iPlayer:
				pPlayerX.AI_changeAttitudeExtra(iTeam, -1)
				if pPlayerX.AI_getAttitude(iPlayer) == GC.getInfoTypeForString("ATTITUDE_FURIOUS"):
					pTeamX = GC.getTeam(pPlayerX.getTeam())
					if pTeamX.canDeclareWar(iTeam):
						pTeamX.declareWar(iTeam, True, -1)
## NPT End ##
