## A New Dawn Mod Code
##

from CvPythonExtensions import *
gc = CyGlobalContext()
localText = CyTranslator()
import BugOptions
import BugCore
import BugUtil
import Popup as PyPopup
import CvUtil
import PlayerUtil
import BugOptionsScreen
ANewDawnOpt = BugCore.game.RoMSettings
MainOpt = BugCore.game.MainInterface
OPTIONS_POPUP_ID = CvUtil.getNewEventID("A New Dawn Options Popup")

def blankHandler( playerID, netUserData, popupReturn ) :
	# Dummy handler to take the second event for popup
	return

def optionHandler( iPlayerID, netUserData, popupReturn ) :

	if( popupReturn.getButtonClicked() == 0 ) :
		BugOptionsScreen.showOptionsScreen()
		ANewDawnOpt.setHasRunAND(True)
	elif( popupReturn.getButtonClicked() == 1 ) :
		ANewDawnOpt.setHasRunAND(False)
		BugCore.game.MainInterface.setShowOptionsKeyReminder(True)
	elif( popupReturn.getButtonClicked() == 2 ) :
		ANewDawnOpt.setHasRunAND(True)


class ANewDawnPopups:
	def __init__(self, eventManager):
		eventManager.addEventHandler("BeginPlayerTurn", self.onBeginPlayerTurn)
		eventManager.setPopupHandler(OPTIONS_POPUP_ID, ["OptionPopup", optionHandler, blankHandler])
		
	def onBeginPlayerTurn(self, argsList):
		iGameTurn, iPlayer = argsList
		if (iGameTurn > 5):
			pPlayer = gc.getPlayer(iPlayer)
			#BugUtil.debug("Stage 1")
			if (pPlayer.isHuman()):
				#BugUtil.debug("Stage 2, turn %d", iGameTurn)
				if (iGameTurn % 10 == 0):
					#BugUtil.debug("Stage 3")
					if (not ANewDawnOpt.isHasRunAND()):
						#BugUtil.debug("Stage 4")
						szTitle = localText.getText("TXT_KEY_SPLASH_TITLE", ())
						szBody = localText.getText("TXT_KEY_SPLASH_TEXT1", ())
						szBody += localText.getText("TXT_KEY_SPLASH_TEXT2", ())
						popup = PyPopup.PyPopup(OPTIONS_POPUP_ID, contextType = EventContextTypes.EVENTCONTEXT_ALL, bDynamic = True)
						popup.setHeaderString( szTitle)
						popup.setBodyString( szBody )
						popup.addSeparator()
						popup.addButton( localText.getText("TXT_KEY_SPLASH_BUTTON_SHOW", ()) )
						popup.addButton( localText.getText("TXT_KEY_SPLASH_BUTTON_REMIND", ()) )
						popup.addButton( localText.getText("TXT_KEY_SPLASH_BUTTON_NOTHANKS", ()) )
						#popup.setSize(400, 20) #220 is maximum for 1024x768 so as not to block the hints display and 640 so that help text is not covered.
						popup.setPosition(0, 0)
						popup.launch(bCreateOkButton = False)

