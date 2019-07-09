## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
# Author - Jon Shafer
# Top Civilizations screen

import CvScreenEnums
import random
from CvPythonExtensions import *

GC = CyGlobalContext()
localText = CyTranslator()

class CvTopCivs:
	"The Greatest Civilizations screen"

	def __init__(self):

		self.X_SCREEN = 0
		self.Y_SCREEN = 0
		self.W_SCREEN = 1024
		self.H_SCREEN = 768

		self.X_MAIN_PANEL = 250
		self.Y_MAIN_PANEL = 70
		self.W_MAIN_PANEL = 550
		self.H_MAIN_PANEL = 500

		iMarginSpace = 15

		self.X_HEADER_PANEL = self.X_MAIN_PANEL + iMarginSpace
		self.Y_HEADER_PANEL = self.Y_MAIN_PANEL + iMarginSpace
		self.W_HEADER_PANEL = self.W_MAIN_PANEL - (iMarginSpace * 2)
		self.H_HEADER_PANEL = self.H_MAIN_PANEL - (iMarginSpace * 2)

		self.X_TEXT_PANEL = self.X_HEADER_PANEL + iMarginSpace
		self.Y_TEXT_PANEL = self.Y_HEADER_PANEL + 132
		self.W_TEXT_PANEL = self.W_HEADER_PANEL - (iMarginSpace * 2)
		self.H_TEXT_PANEL = 265#self.H_MAIN_PANEL - self.H_HEADER_PANEL - (iMarginSpace * 3) + 10 #10 is the fudge factor

		self.X_RANK_TEXT = 430
		self.Y_RANK_TEXT = 230
		self.W_RANK_TEXT = 300
		self.H_RANK_TEXT = 30

		self.X_EXIT = 460
		self.Y_EXIT = self.Y_MAIN_PANEL + 440
		self.W_EXIT = 120
		self.H_EXIT = 30


	def showScreen(self):

		if CyGame().isPitbossHost():
			return

		# Text
		self.HistorianList = [
			localText.getText("TXT_KEY_TOPCIVS_HISTORIAN1", ()),
			localText.getText("TXT_KEY_TOPCIVS_HISTORIAN2", ()),
			localText.getText("TXT_KEY_TOPCIVS_HISTORIAN3", ()),
			localText.getText("TXT_KEY_TOPCIVS_HISTORIAN4", ()),
			localText.getText("TXT_KEY_TOPCIVS_HISTORIAN5", ()),
			localText.getText("TXT_KEY_TOPCIVS_HISTORIAN6", ()),
			localText.getText("TXT_KEY_TOPCIVS_HISTORIAN7", ()),
			localText.getText("TXT_KEY_TOPCIVS_HISTORIAN8", ()),
			localText.getText("TXT_KEY_TOPCIVS_HISTORIAN9", ()),
			localText.getText("TXT_KEY_TOPCIVS_HISTORIAN10", ()),
			localText.getText("TXT_KEY_TOPCIVS_HISTORIAN11", ())
		]
		self.RankList = [
			localText.getText("TXT_KEY_TOPCIVS_RANK1", ()),
			localText.getText("TXT_KEY_TOPCIVS_RANK2", ()),
			localText.getText("TXT_KEY_TOPCIVS_RANK3", ()),
			localText.getText("TXT_KEY_TOPCIVS_RANK4", ()),
			localText.getText("TXT_KEY_TOPCIVS_RANK5", ()),
			localText.getText("TXT_KEY_TOPCIVS_RANK6", ()),
			localText.getText("TXT_KEY_TOPCIVS_RANK7", ()),
			localText.getText("TXT_KEY_TOPCIVS_RANK8", ())
		]
		self.TypeList = [
			localText.getText("TXT_KEY_TOPCIVS_WEALTH", ()),
			localText.getText("TXT_KEY_TOPCIVS_POWER", ()),
			localText.getText("TXT_KEY_TOPCIVS_TECH", ()),
			localText.getText("TXT_KEY_TOPCIVS_CULTURE", ()),
			localText.getText("TXT_KEY_TOPCIVS_SIZE", ()),
		]
		# Randomly choose what category and what historian will be used
		szTypeRand = random.choice(self.TypeList)
		szHistorianRand = random.choice(self.HistorianList)

		# Create screen

		self.screen = CyGInterfaceScreen("CvTopCivs", CvScreenEnums.TOP_CIVS)

		self.screen.setSound("AS2D_TOP_CIVS")
		self.screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
		self.screen.showWindowBackground(False)
		self.screen.setDimensions(self.screen.centerX(self.X_SCREEN), self.screen.centerY(self.Y_SCREEN), self.W_SCREEN, self.H_SCREEN)

		# Create panels
		self.screen.addPanel("TopCivsMainPanel", "", "", True, True, self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN)
		# Top
		self.screen.addPanel("TopCivsHeaderPanel", "", "", True, True, self.X_HEADER_PANEL, self.Y_HEADER_PANEL, self.W_HEADER_PANEL, self.H_HEADER_PANEL, PanelStyles.PANEL_STYLE_DAWNBOTTOM)
		# Bottom
		self.screen.addPanel("TopCivsTextPanel", "", "", True, True, self.X_TEXT_PANEL, self.Y_TEXT_PANEL, self.W_TEXT_PANEL, self.H_TEXT_PANEL, PanelStyles.PANEL_STYLE_DAWNTOP)

		szTxt = localText.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper()
		self.screen.setButtonGFC("Exit", szTxt, "", self.X_EXIT,self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

		# Title Text
		szTxt = u"<font=3>" + localText.getText("TXT_KEY_TOPCIVS_TITLE", ()).upper() + u"</font>"
		X_TITLE_TEXT = self.X_HEADER_PANEL + (self.W_HEADER_PANEL / 2)
		Y_TITLE_TEXT = self.Y_HEADER_PANEL + 15
		self.screen.setLabel("", "", szTxt, 1<<2, X_TITLE_TEXT, Y_TITLE_TEXT, -2.0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		# 1 Text
		X_INFO_TEXT = X_TITLE_TEXT - 260
		Y_INFO_TEXT = Y_TITLE_TEXT + 50
		W_INFO_TEXT = self.W_HEADER_PANEL
		H_INFO_TEXT = 70
		szTxt = localText.getText("TXT_KEY_TOPCIVS_TEXT1", (szHistorianRand, )) + u"\n" + localText.getText("TXT_KEY_TOPCIVS_TEXT2", (szTypeRand, ))
		self.screen.addMultilineText("InfoText1", szTxt, X_INFO_TEXT, Y_INFO_TEXT, W_INFO_TEXT, H_INFO_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<2)

		self.makeList(szTypeRand)

	def makeList(self, szType):

		# Determine the list of top civs

		# Will eventually Store [iValue, iPlayerID]
		self.aiTopCivsValues = []

		# Loop through all players
		for iPlayerLoop in range(GC.getMAX_PC_PLAYERS()):

			if GC.getPlayer(iPlayerLoop).isAlive():

				if (szType == localText.getText("TXT_KEY_TOPCIVS_WEALTH", ())):

					self.aiTopCivsValues.append([GC.getPlayer(iPlayerLoop).getGold(), iPlayerLoop])
					print("Player %d Num Gold: %d" %(iPlayerLoop, GC.getPlayer(iPlayerLoop).getGold()))

				if (szType == localText.getText("TXT_KEY_TOPCIVS_POWER", ())):

					self.aiTopCivsValues.append([GC.getPlayer(iPlayerLoop).getPower(), iPlayerLoop])

				if (szType == localText.getText("TXT_KEY_TOPCIVS_TECH", ())):

					iPlayerNumTechs = 0
					iNumTotalTechs = GC.getNumTechInfos()

					for iTechLoop in range(iNumTotalTechs):

						bPlayerHasTech = GC.getTeam(GC.getPlayer(iPlayerLoop).getTeam()).isHasTech(iTechLoop)

						if (bPlayerHasTech):
							iPlayerNumTechs = iPlayerNumTechs + 1

					self.aiTopCivsValues.append([iPlayerNumTechs, iPlayerLoop])

				if (szType == localText.getText("TXT_KEY_TOPCIVS_CULTURE", ())):

					self.aiTopCivsValues.append([GC.getPlayer(iPlayerLoop).countTotalCulture(), iPlayerLoop])

				if (szType == localText.getText("TXT_KEY_TOPCIVS_SIZE", ())):

					self.aiTopCivsValues.append([GC.getPlayer(iPlayerLoop).getTotalLand(), iPlayerLoop])

		# Lowest to Highest
		self.aiTopCivsValues.sort()
		# Switch it around - want the best to be first
		self.aiTopCivsValues.reverse()

		self.printList(szType)

	def printList(self, szType):

		# Print out the list
		for iRankLoop in range(8):

			if (iRankLoop > len(self.aiTopCivsValues)-1):
				return

			iPlayer = self.aiTopCivsValues[iRankLoop][1]
			iValue = self.aiTopCivsValues[iRankLoop][0]

			szPlayerName = GC.getPlayer(iPlayer).getNameKey()

			if (szPlayerName != ""):

				pActivePlayerTeam = GC.getTeam(GC.getPlayer(CyGame().getActivePlayer()).getTeam())
				iPlayerTeam = GC.getPlayer(iPlayer).getTeam()
				szCivText = ""

				# Does the Active player know this player exists?
				if (iPlayer == CyGame().getActivePlayer() or pActivePlayerTeam.isHasMet(iPlayerTeam)):
					szCivText = localText.getText("TXT_KEY_TOPCIVS_TEXT3", (szPlayerName, self.RankList[iRankLoop]))

				else:
					szCivText = localText.getText("TXT_KEY_TOPCIVS_UNKNOWN", ())

				szWidgetName = "Text" + str(iRankLoop)
				szWidgetDesc = "%d) %s" % (iRankLoop + 1, szCivText)
				iXLoc = self.X_RANK_TEXT
				iYLoc = self.Y_RANK_TEXT + (iRankLoop * self.H_RANK_TEXT)
				#self.screen.setText(szWidgetName, "Background", szWidgetDesc, 1<<0, iXLoc, iYLoc, TEXT_Z, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
				self.screen.addMultilineText( szWidgetName, unicode(szWidgetDesc), iXLoc, iYLoc, self.W_RANK_TEXT, self.H_RANK_TEXT, WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

	def turnChecker(self, iTurnNum):

		# Check to see if this is a turn when the screen should pop up (every 50 turns)
		if (not CyGame().isNetworkMultiPlayer() and CyGame().getActivePlayer()>=0):
			if (iTurnNum % 50 == 0 and iTurnNum > 0 and GC.getPlayer(CyGame().getActivePlayer()).isAlive()):
				self.showScreen()

	#####################################################################################################################################

	def handleInput( self, inputClass ):
		self.screen = CyGInterfaceScreen( "CvTopCivs", CvScreenEnums.TOP_CIVS )

		if ( inputClass.getFunctionName() == "Exit" and inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED ):
			self.screen.hideScreen()
			return 1
		elif ( inputClass.getData() == int(InputTypes.KB_RETURN) ):
			self.screen.hideScreen()
			return 1
		return 0

	def update(self, fDelta):
		return
