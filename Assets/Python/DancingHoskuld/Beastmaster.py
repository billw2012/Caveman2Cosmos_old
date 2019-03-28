#
# Beastmaster - saibotlieh
#
from CvPythonExtensions import *

# globals
gc = CyGlobalContext()


def onLoadGame(argsList):
	return
	#~ for iPlayer in range(gc.getMAX_PLAYERS()):
		#~ player = gc.getPlayer(iPlayer)
		#~ if (player.isAlive()):
			#~ for iLoopUnit in range(player.getNumUnits()):
				#~ pLoopUnit = player.getUnit(iLoopUnit)
				#~ iUnitType = pLoopUnit.getUnitType()
				#~ if iUnitType > -1:
					#~ UnitInfo = gc.getUnitInfo(iUnitType)
					#~ sUnitType = UnitInfo.getType()

					#~ if sUnitType[:10] == 'UNIT_TAMED':	# A Beastmaster will be added to all units which first 10 letters of the UnitType are UNIT_TAMED
						#~ iRnd = CyGame().getSorenRandNum(100, "Female Beastmaster")
						#~ if iRnd < 15:
							#~ unit.setLeaderUnitType(gc.getInfoTypeForString("UNIT_FEMALE_BEASTMASTER"))
						#~ else:
							#~ unit.setLeaderUnitType(gc.getInfoTypeForString("UNIT_BEASTMASTER"))


def onUnitCreated(argsList):
	CyUnit = argsList[0]

	sUnitType = gc.getUnitInfo(CyUnit.getUnitType()).getType()
	# A Beastmaster will be added to all units which first 11 letters of the UnitType are UNIT_TAMED_
	if sUnitType[:11] == 'UNIT_TAMED_':
		iRnd = CyGame().getSorenRandNum(99, "Female Beastmaster")
		if iRnd < 16:
			CyUnit.setLeaderUnitType(gc.getInfoTypeForString("UNIT_FEMALE_BEASTMASTER"))
		else:
			CyUnit.setLeaderUnitType(gc.getInfoTypeForString("UNIT_BEASTMASTER"))


def onUnitKilled(argsList):
	CyUnit, iAttacker = argsList

# Beastmaster - saibotlieh
#	If the following two lines are activated, the beastmaster disappears if the unit will lose the combat. This will prevent a 'beastmaster lost' message to be triggered.

	if CyUnit.getLeaderUnitType() in (gc.getInfoTypeForString("UNIT_BEASTMASTER"), gc.getInfoTypeForString("UNIT_FEMALE_BEASTMASTER")):
		CyUnit.setLeaderUnitType(gc.getInfoTypeForString("NO_UNIT"))
