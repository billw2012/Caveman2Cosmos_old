## Cleopatra's Needle Great Wonder
##  by Platyping
##  converted to BUG by Dancing Hoskuld


from CvPythonExtensions import *
import CvUtil
# import CvScreensInterface
import CvDebugTools
# import CvWBPopups
# import PyHelpers
# import Popup as PyPopup
# import CvCameraControls
# import CvTopCivs
# import sys
# import CvWorldBuilderScreen
# import CvAdvisorUtils
# import CvTechChooser

gc = CyGlobalContext()

# globals
###################################################

def onBuildingBuilt(argsList):
	'Building Completed'
	pCity, iBuildingType = argsList
	game = gc.getGame()
## Cleopatra's Needle Start ##
	if iBuildingType == gc.getInfoTypeForString("BUILDING_CLEOPATRA_NEEDLE"):
		iPlayer = pCity.getOwner()
		pPlayer = gc.getPlayer(iPlayer)
		Cities = []
		(loopCity, iter) = pPlayer.firstCity(false)
		while(loopCity):
			if loopCity.getID() != pCity.getID():
				Cities.append(loopCity)
			(loopCity, iter) = pPlayer.nextCity(iter, false)
		while(len(Cities) > 2):
			if Cities[0].getCulture(iPlayer) < Cities[1].getCulture(iPlayer) and Cities[0].getCulture(iPlayer) < Cities[2].getCulture(iPlayer):
				del Cities[0]
			elif Cities[1].getCulture(iPlayer) < Cities[0].getCulture(iPlayer) and Cities[1].getCulture(iPlayer) < Cities[2].getCulture(iPlayer):
				del Cities[1]
			else:
				del Cities[2]
		Cities[0].setNumRealBuilding(gc.getInfoTypeForString("BUILDING_CLEOPATRA_NEEDLE"), 1)
		Cities[1].setNumRealBuilding(gc.getInfoTypeForString("BUILDING_CLEOPATRA_NEEDLE"), 1)
## Cleopatra's Needle End ##
