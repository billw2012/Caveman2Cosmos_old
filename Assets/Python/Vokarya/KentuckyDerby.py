## Sid Meier's Civilization 4
## Copyright Firaxis Games 2006
##
## Kentucky Derby
## Adapted from PlatyPing's Montreal Biodome by Vokarya

from CvPythonExtensions import *
import CvUtil
import BugUtil
import PyHelpers
import sys

gc = CyGlobalContext()
localText = CyTranslator()

def onEndPlayerTurn(argsList):
	iGameTurn, iPlayer = argsList

	pPlayer = gc.getPlayer(iPlayer)
	if not pPlayer.isAlive():
		return

## Derby Start ##
	if iGameTurn % 10 == 0:
		b_KDerby = gc.getInfoTypeForString("BUILDING_KENTUCKY_DERBY")
		if b_KDerby > -1:
			(loopCity, iter) = pPlayer.firstCity(False)
			while(loopCity):
				if loopCity.getNumActiveBuilding(b_KDerby) > 0:
					iX = loopCity.getX()
					iY = loopCity.getY()
					u_horse = gc.getInfoTypeForString("UNIT_SUBDUED_HORSE")
					pNewUnit = pPlayer.initUnit( u_horse, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION )
					CyInterface().addMessage(iPlayer,True,20,CyTranslator().getText("TXT_NEW_HORSE",(pNewUnit.getName(),)),'',0,pNewUnit.getButton(),ColorTypes(11), iX, iY, True,True)
				break
			(loopCity, iter) = pPlayer.nextCity(iter, False)
## Derby End ##