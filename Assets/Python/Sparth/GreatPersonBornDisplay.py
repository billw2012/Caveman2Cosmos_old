## 
## Event Manager component of the Great Person is born Screen
##  by Sparth

from CvPythonExtensions import *
import CvUtil
import PyHelpers

## Great People ##
import GreatPeopleScreen
## Great People ##


def onGreatPersonBorn(argsList):
	'Unit Promoted'
	pUnit, iPlayer, pCity = argsList
	if pUnit.isNone() or pCity.isNone():
		return
## Great People Screen ##
	if not CyGame().isNetworkMultiPlayer() and iPlayer == CyGame().getActivePlayer():
		GreatPeopleScreen.GreatPeopleScreen().interfaceScreen(pUnit, iPlayer)
## Great People Screen ##
