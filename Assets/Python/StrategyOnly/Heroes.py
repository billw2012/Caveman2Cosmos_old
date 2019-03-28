## By StrategyOnly converted to BUG by Dancing Hoskuld

from CvPythonExtensions import *
import CvEventInterface
import CvUtil
import BugUtil
import PyHelpers
import Popup as PyPopup
import SdToolKit as SDTK

gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

giSparticus = -1
giGladiator = -1

def init():
	global giSparticus, giGladiator
	
	giSparticus = gc.getInfoTypeForString('UNITCLASS_SPARTACUS')
	giGladiator = CvUtil.findInfoTypeNum(gc.getUnitInfo,gc.getNumUnitInfos(),'UNIT_GLADIATOR')

def onUnitBuilt(self, argsList):
	'Unit Completed'
	city = argsList[0]
	unit = argsList[1]
	player = PyPlayer(city.getOwner())
	CvAdvisorUtils.unitBuiltFeats(city, unit)
## Hero Movies ##
	if not CyGame().isNetworkMultiPlayer() and city.getOwner() == CyGame().getActivePlayer() and isWorldUnitClass(unit.getUnitClassType()):
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
		popupInfo.setData1(unit.getUnitType())
		popupInfo.setData2(city.getID())
		popupInfo.setData3(4)
		popupInfo.setText(u"showWonderMovie")
		popupInfo.addPopup(city.getOwner())
## Hero Movies ##

def onCombatResult(argsList):
	'Combat Result'
	pWinner,pLoser = argsList
	playerX = PyPlayer(pWinner.getOwner())
	unitX = PyInfo.UnitInfo(pWinner.getUnitType())
	playerY = PyPlayer(pLoser.getOwner())
	unitY = PyInfo.UnitInfo(pLoser.getUnitType())

	pPlayer = gc.getPlayer(pWinner.getOwner())

## BTS HEROS - Spartacus Capture Event Start ##

	if pWinner.getUnitClassType() == giSparticus:

		## Capture % Random # 0 to 3 or 25% ##
		iNewGladiatorNumber = getRandomNumber( 3 )

		if iNewGladiatorNumber == 0:

			pClearPlot = findClearPlot(pLoser)

			if (pLoser.plot().getNumUnits() == 1 and pClearPlot != -1):
				pPlot = pLoser.plot()
				pLoser.setXY(pClearPlot.getX(), pClearPlot.getY(), False, True, True)
			else:
				pPlot = pWinner.plot()
				
			pPID = pPlayer.getID()
			newUnit = pPlayer.initUnit(giGladiator, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_NORTH)
			pLoser.setDamage(100000, False)
##			newUnit.convert(pLoser)
##			pLoser.setDamage(100, False)
			newUnit.finishMoves()

			iXa = pLoser.getX()
			iYa = pLoser.getY()

			CyInterface().addMessage(pPID,False,15,CyTranslator().getText("TXT_KEY_SPARTACUS_CAPTURE_SUCCESS",()),'',0,',Art/Interface/Buttons/Units/ICBM.dds,Art/Interface/Buttons/Warlords_Atlas_1.dds,3,11',ColorTypes(44), iXa, iYa, True,True)

## BTS HEROS - Spartacus Capture End ##

## Field Medic Start ##

	if pWinner.isHasPromotion(gc.getInfoTypeForString('PROMOTION_RETINUE_MESSENGER')):

		iHealChance = getRandomNumber( 9 )

		if iHealChance == 0:
			if ( not SDTK.sdObjectExists('Heroes', pWinner) ) :
				iHealTurn = -1
			else :
				iHealTurn = SDTK.sdObjectGetVal( 'Heroes', pWinner, 'HealTurn' )
			if( iHealTurn == None or gc.getGame().getGameTurn() > iHealTurn ) :
				pWinner.setDamage(0, False)
				if ( not SDTK.sdObjectExists('Heroes', pWinner) ) :
					SDTK.sdObjectInit('Heroes', pWinner, {})
				SDTK.sdObjectSetVal( 'Heroes', pWinner, 'HealTurn', gc.getGame().getGameTurn() )

## Field Medic End ##

def findClearPlot(pUnit):
	BestPlot = -1
	iBestPlot = 0
	pOldPlot = pUnit.plot()
	iX = pOldPlot.getX()
	iY = pOldPlot.getY()
	for iiX in range(iX-1, iX+2, 1):
		for iiY in range(iY-1, iY+2, 1):
			iCurrentPlot = 0
			pPlot = CyMap().plot(iiX,iiY)
			if pPlot.getNumUnits() == 0:
				iCurrentPlot = iCurrentPlot + 5
			if iCurrentPlot >= 1:
				iCurrentPlot = iCurrentPlot + CyGame().getSorenRandNum(5, "findClearPlot")
				if iCurrentPlot >= iBestPlot:
					BestPlot = pPlot
					iBestPlot = iCurrentPlot
	return BestPlot

def getRandomNumber(int):
	return CyGame().getSorenRandNum(int, "Gods")
