# MovieMod -- Play religion and Nat Wonder movies - 

from CvPythonExtensions import *

GC = CyGlobalContext()

def onBuildingBuilt(argsList):
	CyCity, iBuilding = argsList
	GAME = GC.getGame()
	iPlayer = CyCity.getOwner()

	if not GAME.isNetworkMultiPlayer() and iPlayer == GAME.getActivePlayer():
		if GC.getBuildingInfo(iBuilding).getMovie() and not isWorldWonderClass(GC.getBuildingInfo(iBuilding).getBuildingClassType()):
			if GC.getPlayer(iPlayer).countNumBuildings(iBuilding) == 1:

				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(iBuilding)
				popupInfo.setData2(CyCity.getID())
				popupInfo.setData3(0)
				popupInfo.setText("showWonderMovie")
				popupInfo.addPopup(iPlayer)