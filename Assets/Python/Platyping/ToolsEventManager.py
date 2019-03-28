from CvPythonExtensions import *

import Forgetful
import TimeKeeper

class ToolsEventManager:
	def __init__(self, eventManager):
		self.EventKeyDown=6
		eventManager.addEventHandler("kbdEvent",self.onKbdEvent)
		self.eventManager = eventManager

	def onKbdEvent(self, argsList):
		'keypress handler - return 1 if the event was consumed'
		eventType,key,mx,my,px,py = argsList

		if ( eventType == self.EventKeyDown ):
			theKey=int(key)
## Forgetful Modder ##
			if theKey == int(InputTypes.KB_F1) and self.eventManager.bCtrl:
				Forgetful.Forgetful().interfaceScreen()
				return 1
## Forgetful Modder ##
## TimeKeeper ##
			if theKey == int(InputTypes.KB_F2) and self.eventManager.bCtrl:
				TimeKeeper.TimeKeeper().interfaceScreen()
				return 1
## TimeKeeper ##