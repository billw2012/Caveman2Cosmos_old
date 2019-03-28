## espionage event manager
## by ruff_hi
##
## Required to store the prior players EP Value against the other players
## This information is used in the Espionage Screen to show EP spending per turn

from CvPythonExtensions import *

gc = CyGlobalContext()

import SdToolKit
sdEcho			= SdToolKit.sdEcho
sdModInit		= SdToolKit.sdModInit
sdModLoad		= SdToolKit.sdModLoad
sdModSave		= SdToolKit.sdModSave
sdEntityInit	= SdToolKit.sdEntityInit
sdEntityExists	= SdToolKit.sdEntityExists
sdEntityWipe	= SdToolKit.sdEntityWipe
sdGetVal		= SdToolKit.sdGetVal
sdSetVal		= SdToolKit.sdSetVal
sdGroup			= "EspionagePoints"

class EspionageEventManager:

	def __init__(self, eventManager):
		EspionageEvent(eventManager)


class AbstractEspionageEvent(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractEspionageEventEvent, self).__init__(*args, **kwargs)


class EspionageEventEvent(AbstractEspionageEventEvent):

	def __init__(self, eventManager, *args, **kwargs):
		super(AutoLogEvent, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)


	def onBeginPlayerTurn(self, argsList):
		'Called at the beginning of a players turn'
		iGameTurn, iPlayer = argsList

		if iPlayer != CyGame().getActivePlayer():
			return

		# check to see if we have already done this turn...
		iCurrentTurn = gc.getGame().getGameTurn()
		zsSDKey = "Turn"
		if not sdEntityExists(sdGroup, zsSDKey):
			# Create a record
			zDic = {'Turn':0}
			sdEntityInit(sdGroup, zsSDKey, zDic)

		if sdGetVal(sdGroup, zsSDKey, "Turn") == iCurrentTurn:
			return

		# save the current turn
		sdSetVal(sdGroup, zsSDKey, "Turn", iCurrentTurn)

		# loop through all the players, recording their EP against the other players
		for iPlayerX in range(gc.getMAX_PC_PLAYERS()):
			CyPlayerX = gc.getPlayer(iPlayerX)
			iTeamX = CyPlayerX.getTeam()
			CyTeamX = gc.getTeam(iTeamX)
			for iPlayerY in range(gc.getMAX_PC_PLAYERS()):
				if iPlayerX == iPlayerY:
					continue

				zsSDKey = "%i-%i" %(iPlayerX, iPlayerY)
				if not sdEntityExists(sdGroup, zsSDKey):
					#create a record
					zDic = {'Prior':0}
					sdEntityInit(sdGroup, zsSDKey, zDic)

				CyPlayerY = gc.getPlayer(iPlayerY)
				iTeamY = CyPlayerY.getTeam()

				iPrior = 0
				if iTeamX != iTeamY:
					if CyPlayerX.isAlive() and CyPlayerY.isAlive():
						if CyTeamX.isHasMet(iTeamY):
							iPrior = CyTeamX.getEspionagePointsAgainstTeam(iTeamY)

				sdSetVal(sdGroup, zsSDKey, "Prior", iPrior)
