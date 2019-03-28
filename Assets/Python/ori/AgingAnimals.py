
# AgingAnimals

from CvPythonExtensions import *

GC = CyGlobalContext()
GAME = CyGame()

def onBeginPlayerTurn(argsList):
	# Called at the beginning of a players turn.
	iGameTurn, iPlayer = argsList
	CyPlayer = GC.getPlayer(iPlayer)
	if not CyPlayer.isNPC() or CyPlayer.isHominid():
		return
	CvGameSpeedInfo = GC.getGameSpeedInfo(GAME.getGameSpeedType())
	fModGS = CvGameSpeedInfo.getVictoryDelayPercent() / 100.0
	iMinorIncrement = 16 * fModGS
	iMajorIncrement = 128 * fModGS
	bMinor = not iGameTurn % iMinorIncrement
	bMajor = not iGameTurn % iMajorIncrement

	if bMinor or bMajor:
		CyUnit, i = CyPlayer.firstUnit(False)
		while CyUnit:
			if not CyUnit.isDead() and CyUnit.isAnimal():
				if not GAME.getSorenRandNum(15 - bMajor*10, "Aging"): # 1 in 15
					if not CyUnit.isHasPromotion(GC.getInfoTypeForString("PROMOTION_COMBAT1")):
						CyUnit.setHasPromotion(GC.getInfoTypeForString("PROMOTION_COMBAT1"), True)
					elif not CyUnit.isHasPromotion(GC.getInfoTypeForString("PROMOTION_COMBAT2")):
						CyUnit.setHasPromotion(GC.getInfoTypeForString("PROMOTION_COMBAT2"), True)
					elif not CyUnit.isHasPromotion(GC.getInfoTypeForString("PROMOTION_COMBAT3")):
						CyUnit.setHasPromotion(GC.getInfoTypeForString("PROMOTION_COMBAT3"), True)
					elif not CyUnit.isHasPromotion(GC.getInfoTypeForString("PROMOTION_COMBAT4")):
						CyUnit.setHasPromotion(GC.getInfoTypeForString("PROMOTION_COMBAT4"), True)
					elif not CyUnit.isHasPromotion(GC.getInfoTypeForString("PROMOTION_COMBAT5")):
						CyUnit.setHasPromotion(GC.getInfoTypeForString("PROMOTION_COMBAT5"), True)
					elif not CyUnit.isHasPromotion(GC.getInfoTypeForString("PROMOTION_COMBAT6")):
						CyUnit.setHasPromotion(GC.getInfoTypeForString("PROMOTION_COMBAT6"), True)
					elif bMajor:
						CyUnit.setBaseCombatStr(CyUnit.baseCombatStr() + 1)
					else:
						CyUnit.setExperience(CyUnit.getExperience() + 3, -1)
			CyUnit, i = CyPlayer.nextUnit(i, False)

