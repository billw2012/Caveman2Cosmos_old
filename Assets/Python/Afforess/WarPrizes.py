from CvPythonExtensions import *
import BugUtil

GC = CyGlobalContext()

class WarPrizes:
	def __init__(self, eventManager):
		eventManager.addEventHandler("combatResult", self.onCombatResult)

	def onCombatResult(self, argsList):
		CyUnitW, CyUnitL = argsList # [W]inner and [L]oser

		if GC.getDefineINT("WAR_PRIZES") > 0:
			iPlayerW = CyUnitW.getOwner()
			CyPlayerW = GC.getPlayer(iPlayerW)
			if not CyPlayerW.isNPC():
				aList = (
				GC.getInfoTypeForString("UNITCOMBAT_WOODEN_SHIPS"),
				GC.getInfoTypeForString("UNITCOMBAT_STEAM_SHIPS"),
				GC.getInfoTypeForString("UNITCOMBAT_DIESEL_SHIPS"),
				GC.getInfoTypeForString("UNITCOMBAT_NUCLEAR_SHIPS")
				)
				if CyUnitW.getUnitCombatType() in aList and CyUnitL.getUnitCombatType() in aList:
					iUnitL = CyUnitL.getUnitType()
					if GC.getInfoTypeForString("UNIT_PRIVATEER") not in (CyUnitW.getUnitType(), iUnitL):
						if CyGame().getSorenRandNum(100, "Bob") <= 15:
							iPlayerL = CyUnitL.getOwner()
							X = CyUnitW.getX()
							Y = CyUnitW.getY()
							CyUnit = CyPlayerW.initUnit(iUnitL, X, Y, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
							CyUnit.finishMoves()
							CyUnit.setDamage(50, iPlayerW)
							if CyUnitW.isHiddenNationality():
								CyUnit.doHNCapture()
							CyPlayerL = GC.getPlayer(iPlayerL)
							bHumanW = CyPlayerW.isHuman()
							bHumanL = CyPlayerL.isHuman()
							if bHumanW or bHumanL:
								CvUnitInfoL = GC.getUnitInfo(iUnitL)
								szDescL = CvUnitInfoL.getDescription()
								if bHumanW:
									msg = BugUtil.getText("TXT_KEY_MISC_WARPRIZES_SUCCESS", szDescL)
									iClrG = ColorTypes(GC.getInfoTypeForString("COLOR_GREEN"))
									icon = CvUnitInfoL.getButton()
									CyInterface().addMessage(iPlayerW, False, 20, msg, '', 0, icon, iClrG, X, Y, True, True)
								if bHumanL:
									msg = BugUtil.getText("TXT_KEY_MISC_WARPRIZES_FAILURE", szDescL)
									iClrR = ColorTypes(GC.getInfoTypeForString("COLOR_RED"))
									icon = 'Art/Interface/Buttons/General/warning_popup.dds'
									CyInterface().addMessage(iPlayerL, False, 20, msg, '', 0, icon, iClrR, X, Y, True, True)
							aList = (
							GC.getInfoTypeForString("UNIT_GALLEY"),
							GC.getInfoTypeForString("UNIT_FLUYT"),
							GC.getInfoTypeForString("UNIT_GALLEON"),
							GC.getInfoTypeForString("UNIT_TRANSPORT")
							)
							if iUnitL in aList:
								Loot = CyGame().getSorenRandNum(100, "Loot")
								CyPlayerW.changeGold(Loot)
								if CyPlayerL.getGold() >= Loot:
									CyPlayerL.changeGold(-Loot)
									if bHumanL:
										msg = BugUtil.getText("TXT_KEY_MISC_WARPRIZES_FAILURE_GOLD_LOST", szDescL) + " (" + str(Loot) + ")"
										CyInterface().addMessage(iPlayerL, False, 20, msg, '', 0, icon, iClrR, X, Y, True, True)
								if bHumanW:
									msg = BugUtil.getText("TXT_KEY_MISC_WARPRIZES_SUCCESS_GOLD_GAINED", szDescL) + " (" + str(Loot) + ")"
									icon = 'Art/Interface/Buttons/process/processwealth.dds'
									CyInterface().addMessage(iPlayerW, False, 20, msg, '', 0, icon, iClrG, X, Y, True, True)
