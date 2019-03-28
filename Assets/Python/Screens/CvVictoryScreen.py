## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import ScreenInput
import time

# BUG - start
import AttitudeUtil
import BugCore
import BugPath
import BugUtil
import ColorUtil
import GameUtil
import TechUtil

AdvisorOpt = BugCore.game.Advisors
# BUG - end

# BUFFY - start
import os
import GameSetUpCheck
import Buffy

BUFFYOpt = BugCore.game.BUFFY

worldWrapString = {
	'Flat': "TXT_KEY_MAP_WRAP_FLAT",
	'Cylindrical': "TXT_KEY_MAP_WRAP_CYLINDER",
	'Toroidal': "TXT_KEY_MAP_WRAP_TOROID"
}
# BUFFY - end

# BUG - Mac Support - start
BugUtil.fixSets(globals())
# BUG - Mac Support - end

# globals
GC = CyGlobalContext()
TRNSLTR = CyTranslator()

VICTORY_CONDITION_SCREEN = 0
GAME_SETTINGS_SCREEN = 1
UN_RESOLUTION_SCREEN = 2
UN_MEMBERS_SCREEN = 3

'''
FONT_CENTER_JUSTIFY	= 1<<2
FONT_RIGHT_JUSTIFY	= 1<<1
FONT_LEFT_JUSTIFY	= 1<<0
'''

class CvVictoryScreen:
	"Keeps track of victory conditions"

	def __init__(self, screenId):
		self.screenId = screenId
		self.SCREEN_NAME = "VictoryScreen"
		self.DEBUG_DROPDOWN_ID =  "VictoryScreenDropdownWidget"
		self.INTERFACE_ART_INFO = "TECH_BG"
		self.EXIT_AREA = "EXIT"
		self.EXIT_ID = "VictoryScreenExit"
		self.BACKGROUND_ID = "VictoryScreenBackground"
		self.HEADER_ID = "VictoryScreenHeader"
		self.WIDGET_ID = "VictoryScreenWidget"
		self.VC_TAB_ID = "VictoryTabWidget"
		self.SETTINGS_TAB_ID = "SettingsTabWidget"
		self.UN_RESOLUTION_TAB_ID = "VotingTabWidget"
		self.UN_MEMBERS_TAB_ID = "MembersTabWidget"
		self.SPACESHIP_SCREEN_BUTTON = 1234

		self.Z_BACKGROUND = -6.1
		self.Z_CONTROLS = self.Z_BACKGROUND - 0.2
		self.DZ = -0.2

		self.X_SCREEN = 500
		self.Y_SCREEN = 396
		self.W_SCREEN = 1024
		self.H_SCREEN = 768
		self.Y_TITLE = 12

		self.X_EXIT = 994
		self.Y_EXIT = 726

		self.X_AREA = 10
		self.Y_AREA = 60
		self.W_AREA = 1010
		self.H_AREA = 650

		self.TABLE_WIDTH_0 = 350
		self.TABLE_WIDTH_1 = 80
		self.TABLE_WIDTH_2 = 180
		self.TABLE_WIDTH_3 = 100
		self.TABLE_WIDTH_4 = 180
		self.TABLE_WIDTH_5 = 100

		self.TABLE2_WIDTH_0 = 740
		self.TABLE2_WIDTH_1 = 265

# BUG Additions Start
		self.TABLE3_WIDTH_0 = 450
		self.TABLE3_WIDTH_1 = 90
		self.TABLE3_WIDTH_2 = 90
		self.TABLE3_WIDTH_3 = 90
		self.TABLE3_WIDTH_4 = 90
		self.TABLE3_WIDTH_5 = 200

		self.Vote_Pope_ID = "BUGVotePope_Widget"
		self.Vote_DipVic_ID = "BUGVoteDiplomaticVictory_Widget"
		self.Vote_X = 20
		self.Vote_Y = 688
		self.VoteType = 1  # 1 = Pope or GenSec, 2 = Diplomatic Victory
		self.VoteBody = 1  # 1 = AP, 2 = UN

		self.Vote_AP_ID = "BUGVoteAP_Widget"
		self.Vote_UN_ID = "BUGVoteUN_Widget"
# BUG Additions End

		self.X_LINK = 100
		self.DX_LINK = 220
		self.Y_LINK = 726
		self.MARGIN = 20
		
		self.SETTINGS_PANEL_X1 = 50
		self.SETTINGS_PANEL_X2 = 355
		self.SETTINGS_PANEL_X3 = 660
		self.SETTINGS_PANEL_Y = 150
		self.SETTINGS_PANEL_WIDTH = 300
		self.SETTINGS_PANEL_HEIGHT = 500

		## Start HOF MOD V1.61.001  2/8
		self.HOF_WARNING_PANEL_X = 50
		self.HOF_WARNING_PANEL_Y = 50
		self.HOF_WARNING_PANEL_WIDTH = 910
		self.HOF_WARNING_PANEL_HEIGHT = 80
		self.BuffyWarningTextLoaded = False
		## End HOF MOD V1.61.001  2/8

		self.nWidgetCount = 0
		self.iActivePlayer = -1
		self.bVoteTab = False

		self.iScreen = VICTORY_CONDITION_SCREEN

		self.ApolloTeamsChecked = set()
		self.ApolloTeamCheckResult = {}

	def getScreen(self):
		return CyGInterfaceScreen(self.SCREEN_NAME, self.screenId)

	def hideScreen(self):
		screen = self.getScreen()
		screen.hideScreen()

	def interfaceScreen(self):

		# Create a new screen
		screen = self.getScreen()
		if screen.isActive():
			return
		screen.setRenderInterfaceOnly(True);
		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

		self.iActivePlayer = CyGame().getActivePlayer()
		if self.iScreen == -1:
			self.iScreen = VICTORY_CONDITION_SCREEN

		# Set the background widget and exit button
		screen.addDDSGFC(self.BACKGROUND_ID, CyArtFileMgr().getInterfaceArtInfo("MAINMENU_SLIDESHOW_LOAD").getPath(), 0, 0, self.W_SCREEN, self.H_SCREEN, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addPanel( "TechTopPanel", u"", u"", True, False, 0, 0, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_TOPBAR )
		screen.addPanel( "TechBottomPanel", u"", u"", True, False, 0, 713, self.W_SCREEN, 55, PanelStyles.PANEL_STYLE_BOTTOMBAR )
		screen.showWindowBackground( False )
		screen.setDimensions(screen.centerX(0), screen.centerY(0), self.W_SCREEN, self.H_SCREEN)
		screen.setText(self.EXIT_ID, "Background", u"<font=4>" + TRNSLTR.getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", 1<<1, self.X_EXIT, self.Y_EXIT, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1 )

		# Header...
		screen.setLabel(self.HEADER_ID, "Background", u"<font=4b>" + TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_TITLE", ()).upper() + u"</font>", 1<<2, self.X_SCREEN, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if self.iScreen == VICTORY_CONDITION_SCREEN:
			self.showVictoryConditionScreen()
		elif self.iScreen == GAME_SETTINGS_SCREEN:
			self.showGameSettingsScreen()
		elif self.iScreen == UN_RESOLUTION_SCREEN:
			self.showVotingScreen()
		elif self.iScreen == UN_MEMBERS_SCREEN:
			self.showMembersScreen()

	def drawTabs(self):
		screen = self.getScreen()

		xLink = self.X_LINK
		if (self.iScreen != VICTORY_CONDITION_SCREEN):
			screen.setText(self.VC_TAB_ID, "", u"<font=4>" + TRNSLTR.getText("TXT_KEY_MAIN_MENU_VICTORIES", ()).upper() + "</font>", 1<<2, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setText(self.VC_TAB_ID, "", u"<font=4>" + TRNSLTR.getColorText("TXT_KEY_MAIN_MENU_VICTORIES", (), GC.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", 1<<2, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		xLink += self.DX_LINK

		if (self.iScreen != GAME_SETTINGS_SCREEN):
			screen.setText(self.SETTINGS_TAB_ID, "", u"<font=4>" + TRNSLTR.getText("TXT_KEY_MAIN_MENU_SETTINGS", ()).upper() + "</font>", 1<<2, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setText(self.SETTINGS_TAB_ID, "", u"<font=4>" + TRNSLTR.getColorText("TXT_KEY_MAIN_MENU_SETTINGS", (), GC.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", 1<<2, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		xLink += self.DX_LINK

		if self.bVoteTab:
			if (self.iScreen != UN_RESOLUTION_SCREEN):
				screen.setText(self.UN_RESOLUTION_TAB_ID, "", u"<font=4>" + TRNSLTR.getText("TXT_KEY_VOTING_TITLE", ()).upper() + "</font>", 1<<2, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				screen.setText(self.UN_RESOLUTION_TAB_ID, "", u"<font=4>" + TRNSLTR.getColorText("TXT_KEY_VOTING_TITLE", (), GC.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", 1<<2, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			xLink += self.DX_LINK

			if (self.iScreen != UN_MEMBERS_SCREEN):
				screen.setText(self.UN_MEMBERS_TAB_ID, "", u"<font=4>" + TRNSLTR.getText("TXT_KEY_MEMBERS_TITLE", ()).upper() + "</font>", 1<<2, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			else:
				screen.setText(self.UN_MEMBERS_TAB_ID, "", u"<font=4>" + TRNSLTR.getColorText("TXT_KEY_MEMBERS_TITLE", (), GC.getInfoTypeForString("COLOR_YELLOW")).upper() + "</font>", 1<<2, xLink, self.Y_LINK, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			xLink += self.DX_LINK

	def showVotingScreen(self):
		self.deleteAllWidgets()

		CyPlayer = GC.getPlayer(self.iActivePlayer)
		iActiveTeam = CyPlayer.getTeam()
		CyTeam = GC.getTeam(iActiveTeam)

		aiVoteBuildingClass = []
		for i in xrange(GC.getNumBuildingInfos()):
			CvBuildingInfo = GC.getBuildingInfo(i)
			for j in xrange(GC.getNumVoteSourceInfos()):
				if CvBuildingInfo.getVoteSourceType() == j:
					iUNTeam = -1
					bUnknown = True

					for iPlayerX in xrange(GC.getMAX_PC_PLAYERS()):
						CyPlayerX = GC.getPlayer(iPlayerX)
						if CyPlayerX.isAlive() and not CyPlayerX.isMinorCiv() and CyPlayerX.countNumBuildings(i):
							iUNTeam = CyPlayerX.getTeam()
							if iUNTeam == iActiveTeam or GC.getGame().isDebugMode() or CyTeam.isHasMet(iUNTeam):
								bUnknown = False
							break

					aiVoteBuildingClass.append((CvBuildingInfo.getTextKey(), iUNTeam, bUnknown))

		if not aiVoteBuildingClass:
			return

		screen = self.getScreen()

		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-10, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+30, PanelStyles.PANEL_STYLE_BLUE50)
		szTable = self.getNextWidgetName()
		screen.addTableControlGFC(szTable, 2, self.X_AREA, self.Y_AREA, self.W_AREA, self.H_AREA, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(szTable, False)
		screen.setTableColumnHeader(szTable, 0, "", self.TABLE2_WIDTH_0)
		screen.setTableColumnHeader(szTable, 1, "", self.TABLE2_WIDTH_1)

		for TEXT_KEY, iUNTeam, bUnknown in aiVoteBuildingClass:
			iRow = screen.appendTableRow(szTable)
			screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_ELECTION", (TEXT_KEY,)), "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)
			if iUNTeam != -1:
				if bUnknown:
					szName = TRNSLTR.getText("TXT_KEY_TOPCIVS_UNKNOWN", ())
				else:
					szName = GC.getTeam(iUNTeam).getName()
				screen.setTableText(szTable, 1, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_BUILT", (szName, )), "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)
			else:
				screen.setTableText(szTable, 1, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_NOT_BUILT", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

		for i in xrange(GC.getNumVoteSourceInfos()):
			if (GC.getGame().canHaveSecretaryGeneral(i) and -1 != GC.getGame().getSecretaryGeneral(i)):
				iRow = screen.appendTableRow(szTable)
				screen.setTableText(szTable, 0, iRow, GC.getVoteSourceInfo(i).getSecretaryGeneralText(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)
				screen.setTableText(szTable, 1, iRow, GC.getTeam(GC.getGame().getSecretaryGeneral(i)).getName(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

			for iLoop in xrange(GC.getNumVoteInfos()):
				if GC.getGame().countPossibleVote(iLoop, i) > 0:
					info = GC.getVoteInfo(iLoop)
					if GC.getGame().isChooseElection(iLoop):
						iRow = screen.appendTableRow(szTable)
						screen.setTableText(szTable, 0, iRow, info.getDescription(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)
						if GC.getGame().isVotePassed(iLoop):
							screen.setTableText(szTable, 1, iRow, TRNSLTR.getText("TXT_KEY_POPUP_PASSED", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)
						else:
							screen.setTableText(szTable, 1, iRow, TRNSLTR.getText("TXT_KEY_POPUP_ELECTION_OPTION", (u"", GC.getGame().getVoteRequired(iLoop, i), GC.getGame().countPossibleVote(iLoop, i))), "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

		self.drawTabs()


# BUG Additions Start
	def showMembersScreen(self):
		iRelVote, iRelVoteIdx, iUNVote, iUNVoteIdx  = self.getVoteAvailable()

		if AdvisorOpt.isMembers():
			if  iRelVote == -1: self.VoteBody = 2 # AP Not active
			elif iUNVote == -1: self.VoteBody = 1 # UN Not active

			if self.VoteBody == 1:
				iVoteBody = iRelVote
				iVoteIdx = iRelVoteIdx
			else:
				iVoteBody = iUNVote
				iVoteIdx = iUNVoteIdx

			self.showMembersScreen_BUG(iRelVote, iUNVote, iVoteBody, iVoteIdx)
		else:
			self.showMembersScreen_NonBUG()

		self.drawTabs()

	def getVoteAvailable(self):

		iRelVote = -1
		iRelVoteIdx = -1
		iUNVote = -1
		iUNVoteIdx = -1

		for i in xrange(GC.getNumVoteSourceInfos()):
			if GC.getGame().isDiploVote(i):
				if (GC.getGame().getVoteSourceReligion(i) != -1):
					iRelVote = i
				else:
					iUNVote = i

			if (GC.getGame().canHaveSecretaryGeneral(i)
			and GC.getGame().getSecretaryGeneral(i) != -1):
				for j in xrange(GC.getNumVoteInfos()):
					if GC.getVoteInfo(j).isVoteSourceType(i):
						if GC.getVoteInfo(j).isSecretaryGeneral():
							if (GC.getGame().getVoteSourceReligion(i) != -1):
								iRelVoteIdx = j
							else:
								iUNVoteIdx = j

							break

		BugUtil.debug("CvVictoryScreen: Rel Vote %i, UN Vote %i, Rel Vote Idx %i, UN Vote Idx %i", iRelVote, iRelVoteIdx, iUNVote, iUNVoteIdx)

		return iRelVote, iRelVoteIdx, iUNVote, iUNVoteIdx

	def showMembersScreen_BUG(self, iRelVote, iUNVote, iActiveVote, iVoteIdx):
		self.deleteAllWidgets()

		if iRelVote == -1 and iUNVote == -1: return  # neither AP or UN are active

		GAME = GC.getGame()
		activePlayer = GC.getPlayer(self.iActivePlayer)
		iActiveTeam = activePlayer.getTeam()

		screen = self.getScreen()

		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-10, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+30, PanelStyles.PANEL_STYLE_BLUE50)

		# set up the header row
		szHeading = self.getNextWidgetName()
		screen.addTableControlGFC(szHeading, 3, self.X_AREA, self.Y_AREA, self.W_AREA, 30, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(szHeading, 0, "", self.TABLE3_WIDTH_0)
		screen.setTableColumnHeader(szHeading, 1, "", self.TABLE3_WIDTH_1 + self.TABLE3_WIDTH_2)
		screen.setTableColumnHeader(szHeading, 2, "", self.TABLE3_WIDTH_3 + self.TABLE3_WIDTH_4)
		iRow = screen.appendTableRow(szHeading)

		# heading
		kVoteSource = GC.getVoteSourceInfo(iActiveVote)
		sTableHeader = "<font=4b>" + kVoteSource.getDescription().upper() + "</font>"
		if GAME.getVoteSourceReligion(iActiveVote) != -1:
			sTableHeader += " (" + GC.getReligionInfo(GAME.getVoteSourceReligion(iActiveVote)).getDescription() + ")"

		screen.setTableText(szHeading, 0, iRow, sTableHeader, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

		# determine the two candidates, add to header
		iCandTeam1 = -1
		iCandTeam2 = -1
		for j in xrange(GC.getMAX_TEAMS()):
			BugUtil.debug("CvVictoryScreen: Team %i", j)

			if GC.getTeam(j).isAlive() and GAME.isTeamVoteEligible(j, iActiveVote):
				BugUtil.debug("CvVictoryScreen: Team %i, %s <- vote eligible ", j, GC.getTeam(j).getName())
				if iCandTeam1 == -1:
					iCandTeam1 = j
				else:
					iCandTeam2 = j

		# get the first player for each team
		# going to use that to calculation attitude - too hard to calc attitude for team
		iCandPlayer1 = self.getPlayerOnTeam(iCandTeam1)
		iCandPlayer2 = self.getPlayerOnTeam(iCandTeam2)

		# candidate known returns -1 if there is no candidate, 0 if not known or 1 if known
		iCand1Known, sCand1Name = self.getCandStatusName(iCandTeam1)
		iCand2Known, sCand2Name = self.getCandStatusName(iCandTeam2)

		screen.setTableText(szHeading, 1, iRow, sCand1Name, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<2)
		screen.setTableText(szHeading, 2, iRow, sCand2Name, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<2)

		# set up the member table
		szTable = self.getNextWidgetName()
		screen.addTableControlGFC(szTable, 6, self.X_AREA, self.Y_AREA + 30, self.W_AREA, self.H_AREA-20-30, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(szTable, False)
		screen.setTableColumnHeader(szTable, 0, "", self.TABLE3_WIDTH_0)
		screen.setTableColumnHeader(szTable, 1, "", self.TABLE3_WIDTH_1)
		screen.setTableColumnHeader(szTable, 2, "", self.TABLE3_WIDTH_2)
		screen.setTableColumnHeader(szTable, 3, "", self.TABLE3_WIDTH_3)
		screen.setTableColumnHeader(szTable, 4, "", self.TABLE3_WIDTH_4)
		screen.setTableColumnHeader(szTable, 5, "", self.TABLE3_WIDTH_5)
		iRow = screen.appendTableRow(szTable)

		# set up the vote selection texts
		iX = self.X_EXIT
		sText = GC.getVoteSourceInfo(iActiveVote).getSecretaryGeneralText()
		if self.VoteType == 1: sText = BugUtil.colorText(sText, "COLOR_YELLOW")
		screen.setText(self.Vote_Pope_ID, "", sText, 1<<1, iX, self.Vote_Y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		iX -= 10 + CyInterface().determineWidth(sText)
		sText = TRNSLTR.getText("TXT_KEY_BUG_VICTORY_DIPLOMATIC", ())
		if self.VoteType == 2:
			sText = BugUtil.colorText(sText, "COLOR_YELLOW")
		screen.setText(self.Vote_DipVic_ID, "", sText, 1<<1, iX, self.Vote_Y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		if iRelVote != -1 and iUNVote != -1:  # both AP and UN are active
			iX = self.Vote_X
			sText = GC.getVoteSourceInfo(iRelVote).getDescription()
			if iActiveVote == iRelVote: sText = BugUtil.colorText(sText, "COLOR_YELLOW")
			screen.setText(self.Vote_AP_ID, "", sText, 1<<0, iX, self.Vote_Y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

			iX += 10 + CyInterface().determineWidth(sText)
			sText = GC.getVoteSourceInfo(iUNVote).getDescription()
			if iActiveVote == iUNVote: sText = BugUtil.colorText(sText, "COLOR_YELLOW")
			screen.setText(self.Vote_UN_ID, "", sText, 1<<0, iX, self.Vote_Y, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.hide(self.Vote_AP_ID)
			screen.hide(self.Vote_UN_ID)

		# initialize the candidate votes and total vote counter
		iVoteTotal = [0] * 2
		iVoteCand = [0] * 2

		lMembers = []
		iAPUNTeam = self.getAP_UN_OwnerTeam()

		for j in xrange(GC.getMAX_PLAYERS()):
			pPlayer = GC.getPlayer(j)
			if pPlayer.isAlive() and not pPlayer.isNPC():
				iPlayer = j
				lPlayerName = pPlayer.getName()
				lPlayerVotes = 10000 - pPlayer.getVotes(iVoteIdx, iActiveVote) # so that it sorts from most votes to least

				if GAME.canHaveSecretaryGeneral(iActiveVote) and iAPUNTeam == pPlayer.getTeam() and GAME.getSecretaryGeneral(iActiveVote) == -1:
					lPlayerStatus = 0
					lPlayerLabel = GC.getVoteSourceInfo(iActiveVote).getSecretaryGeneralText()
				elif GAME.canHaveSecretaryGeneral(iActiveVote) and GAME.getSecretaryGeneral(iActiveVote) == pPlayer.getTeam():
					lPlayerStatus = 1
					lPlayerLabel = GC.getVoteSourceInfo(iActiveVote).getSecretaryGeneralText()
				elif pPlayer.isFullMember(iActiveVote):
					lPlayerStatus = 2
					lPlayerLabel = TRNSLTR.getText("TXT_KEY_VOTESOURCE_FULL_MEMBER", ())
				elif pPlayer.isVotingMember(iActiveVote):
					lPlayerStatus = 3
					lPlayerLabel = TRNSLTR.getText("TXT_KEY_VOTESOURCE_VOTING_MEMBER", ())
				else:
					lPlayerStatus = 4
					lPlayerLabel = TRNSLTR.getText("TXT_KEY_VOTESOURCE_NON_VOTING_MEMBER", ())

				lMembers.append([lPlayerStatus, lPlayerVotes, iPlayer, lPlayerLabel])

		lMembers.sort()

		for lMember in lMembers:
			lMemberStatus = lMember[0]
			lMemberVotes = 10000 - lMember[1]
			iMember = lMember[2]
			lMemberLabel = lMember[3]

			# player name
			bKnown, szPlayerText = self.getPlayerStatusName(iMember)

			if lMemberVotes > 0 and bKnown:
				szPlayerText += TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_PLAYER_VOTES", (lMemberVotes, iActiveVote),)

			iRow = screen.appendTableRow(szTable)
			screen.setTableText(szTable, 0, iRow, szPlayerText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

			if iMember != self.iActivePlayer:
				# player attitude to candidate #1
				szText = AttitudeUtil.getAttitudeText (iMember, iCandPlayer1, True, True, False, False)
				if szText and iCand1Known == 1 and bKnown:
					screen.setTableText(szTable, 1, iRow, szText, "", WidgetTypes.WIDGET_LEADERHEAD, iMember, iCandPlayer1, 1<<2)

				# player attitude to candidate #2
				szText = AttitudeUtil.getAttitudeText (iMember, iCandPlayer2, True, True, False, False)
				if szText and iCand2Known == 1 and bKnown:
					screen.setTableText(szTable, 3, iRow, szText, "", WidgetTypes.WIDGET_LEADERHEAD, iMember, iCandPlayer2, 1<<2)

			iVote = self.getVotesForWhichCandidate(iMember, iCandTeam1, iCandTeam2, self.VoteType)
			iVote_Column = -1

			if iVote != -1:
				sVote = str(lMemberVotes)
				iVoteTotal[iVote - 1] += lMemberVotes

				# number of votes for Candidate #1
				if iVote == 1 and lMemberVotes > 0 and iCand1Known == 1:
					screen.setTableText(szTable, 2, iRow, sVote, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<2)

				# number of votes for Candidate #2
				if iVote == 2 and lMemberVotes > 0 and iCand2Known == 1:
					screen.setTableText(szTable, 4, iRow, sVote, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<2)

			# player status
			if bKnown:
				screen.setTableText(szTable, 5, iRow, lMemberLabel, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<1)

			# store the candidates own votes
			if iCandTeam1 == GC.getPlayer(iMember).getTeam() and iCand1Known == 1:
				iVoteCand[0] = lMemberVotes
			if iCandTeam2 == GC.getPlayer(iMember).getTeam() and iCand2Known == 1:
				iVoteCand[1] = lMemberVotes

		# calculate the maximum number of votes
		iMaxVotes = 0
		for iLoop in xrange(GC.getNumVoteInfos()):
			if GAME.countPossibleVote(iLoop, iActiveVote) > 0:
				iMaxVotes = GAME.countPossibleVote(iLoop, iActiveVote)
				break

		iRow = screen.appendTableRow(szTable)
		iVoteReq = self.getVoteReq(iActiveVote, self.VoteType)
		sVoteReq = "%i" % (iVoteReq)
		sString = "<font=3b>" + TRNSLTR.getText("TXT_KEY_BUG_VICTORY_VOTES_TOTAL", ()) + "</font> "
		if iCand1Known and iCand2Known:
			sString +=  TRNSLTR.getText("TXT_KEY_BUG_VICTORY_VOTES_REQUIRED", (sVoteReq,))
		screen.setTableText(szTable, 0, iRow, sString, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

		if iCand1Known == 1:
			# color code the totals
			sVoteTotal = str(iVoteTotal[0])
			iColor = self.getVoteTotalColor(iVoteReq, iVoteTotal[0], iVoteCand[0], iVoteTotal[0] > iVoteTotal[1], self.VoteType == 2)
			if iColor != -1:
				sVoteTotal = TRNSLTR.changeTextColor(sVoteTotal, iColor)
			screen.setTableText(szTable, 2, iRow, sVoteTotal, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<2)

		if iCand2Known == 1:
			sVoteTotal = str(iVoteTotal[1])
			iColor = self.getVoteTotalColor(iVoteReq, iVoteTotal[1], iVoteCand[1], iVoteTotal[1] > iVoteTotal[0], self.VoteType == 2)
			if iColor != -1:
				sVoteTotal = TRNSLTR.changeTextColor(sVoteTotal, iColor)
			screen.setTableText(szTable, 4, iRow, sVoteTotal, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<2)

		# add a blank row
		iRow = screen.appendTableRow(szTable)

		# SecGen vote prediction
		if iVoteTotal[0] > iVoteTotal[1]:
			iWinner = 0
			sWin = sCand1Name
		else:
			iWinner = 1
			sWin = sCand2Name
		iLoser = 1 - iWinner

		fVotePercent = 100.0 * iVoteTotal[iWinner] / iMaxVotes
		fMargin = 100.0 * (iVoteTotal[iWinner] - iVoteTotal[iLoser]) / iMaxVotes

		if self.VoteType == 1:
			sSecGen = GC.getVoteSourceInfo(iActiveVote).getSecretaryGeneralText()
		else:
			sSecGen = TRNSLTR.getText("TXT_KEY_BUG_VICTORY_DIPLOMATIC", ())

		# display SecGen vote prediction
		if iCand1Known != 0 and iCand2Known != 0:
			sString = sSecGen + ":"
			iRow = screen.appendTableRow(szTable)
			screen.setTableText(szTable, 0, iRow, sString, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

			sString = "     " + TRNSLTR.getText("TXT_KEY_BUG_VICTORY_BUG_POLL_RESULT", (sWin, self.formatPercent(fVotePercent), self.formatPercent(fMargin)))
			iRow = screen.appendTableRow(szTable)
			screen.setTableText(szTable, 0, iRow, sString, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

			# BUG Poll statistical error
			iRandError = 3.5 + GC.getASyncRand().get(10, "Election Results Statistical Error") / 10.0
			sString = TRNSLTR.getText("TXT_KEY_BUG_VICTORY_BUG_POLL_ERROR", (self.formatPercent(iRandError), ))
			iRow = screen.appendTableRow(szTable)
			screen.setTableText(szTable, 0, iRow, sString, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

		iRow = screen.appendTableRow(szTable)

		# add info about vote timing
		iRow = screen.appendTableRow(szTable)
		iVoteTimer = GAME.getVoteTimer(iActiveVote)
		sString = TRNSLTR.getText("TXT_KEY_BUG_VICTORY_TURNS_NEXT_VOTE", (iVoteTimer,))
		sString = "<font=2>" + sString + "</font>"
		screen.setTableText(szTable, 0, iRow, sString, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

		iRow = screen.appendTableRow(szTable)
		iSecGenTimer = GAME.getSecretaryGeneralTimer(iActiveVote)
		sString = TRNSLTR.getText("TXT_KEY_BUG_VICTORY_VOTES_NEXT_ELECTION", (iSecGenTimer,))
		sString = "<font=2>" + sString + "</font>"
		screen.setTableText(szTable, 0, iRow, sString, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)


	def showMembersScreen_NonBUG(self):
		self.deleteAllWidgets()

		iActiveTeam = GC.getPlayer(self.iActivePlayer).getTeam()

		screen = self.getScreen()

		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-10, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+30, PanelStyles.PANEL_STYLE_BLUE50)
		szTable = self.getNextWidgetName()
		screen.addTableControlGFC(szTable, 2, self.X_AREA, self.Y_AREA, self.W_AREA, self.H_AREA, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.enableSelect(szTable, False)
		screen.setTableColumnHeader(szTable, 0, "", self.TABLE2_WIDTH_0)
		screen.setTableColumnHeader(szTable, 1, "", self.TABLE2_WIDTH_1)

		for i in xrange(GC.getNumVoteSourceInfos()):
			if GC.getGame().isDiploVote(i):
				kVoteSource = GC.getVoteSourceInfo(i)
				iRow = screen.appendTableRow(szTable)
				screen.setTableText(szTable, 0, iRow, u"<font=4b>" + kVoteSource.getDescription().upper() + u"</font>", "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)
				if GC.getGame().getVoteSourceReligion(i) != -1:
					screen.setTableText(szTable, 1, iRow, GC.getReligionInfo(GC.getGame().getVoteSourceReligion(i)).getDescription(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

				iSecretaryGeneralVote = -1
				if GC.getGame().canHaveSecretaryGeneral(i) and -1 != GC.getGame().getSecretaryGeneral(i):
					for j in xrange(GC.getNumVoteInfos()):
						print j
						if GC.getVoteInfo(j).isVoteSourceType(i):
							print "votesource"
							if GC.getVoteInfo(j).isSecretaryGeneral():
								print "secgen"
								iSecretaryGeneralVote = j
								break

				print iSecretaryGeneralVote
				for j in xrange(GC.getMAX_PLAYERS()):
					if GC.getPlayer(j).isAlive() and not GC.getPlayer(j).isNPC() and GC.getTeam(iActiveTeam).isHasMet(GC.getPlayer(j).getTeam()):
						szPlayerText = GC.getPlayer(j).getName()
						if (-1 != iSecretaryGeneralVote):
							szPlayerText += TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_PLAYER_VOTES", (GC.getPlayer(j).getVotes(iSecretaryGeneralVote, i), )) 
						if (GC.getGame().canHaveSecretaryGeneral(i) and GC.getGame().getSecretaryGeneral(i) == GC.getPlayer(j).getTeam()):
							iRow = screen.appendTableRow(szTable)
							screen.setTableText(szTable, 0, iRow, szPlayerText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)
							screen.setTableText(szTable, 1, iRow, GC.getVoteSourceInfo(i).getSecretaryGeneralText(), "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)
						elif (GC.getPlayer(j).isFullMember(i)):
							iRow = screen.appendTableRow(szTable)
							screen.setTableText(szTable, 0, iRow, szPlayerText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)
							screen.setTableText(szTable, 1, iRow, TRNSLTR.getText("TXT_KEY_VOTESOURCE_FULL_MEMBER", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)
						elif (GC.getPlayer(j).isVotingMember(i)):
							iRow = screen.appendTableRow(szTable)
							screen.setTableText(szTable, 0, iRow, szPlayerText, "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)
							screen.setTableText(szTable, 1, iRow, TRNSLTR.getText("TXT_KEY_VOTESOURCE_VOTING_MEMBER", ()), "", WidgetTypes.WIDGET_GENERAL, -1, -1, 1<<0)

				iRow = screen.appendTableRow(szTable)

	def formatPercent(self, f):
		return "%.1f%%" % f

	def getVoteReq(self, i, iVote):
		iMaxVotes = 0
		iMinVotes = 999999
		for iLoop in xrange(GC.getNumVoteInfos()):
			iVoteReq = GC.getGame().getVoteRequired(iLoop, i)
			if iVoteReq > 0:
				if iVoteReq > iMaxVotes:
					iMaxVotes = iVoteReq
				if iVoteReq < iMinVotes:
					iMinVotes = iVoteReq

		if iVote == 1:
			return iMinVotes
		else:
			return iMaxVotes

	def getCandStatusName(self, iTeam):
		if iTeam == -1: # there is no candidate
			return -1, "-"

		iTeamActive = GC.getPlayer(self.iActivePlayer).getTeam()

		if iTeamActive == iTeam:
			return 1, GC.getTeam(iTeam).getName()

		if GC.getTeam(iTeamActive).isHasMet(iTeam):
			return 1, GC.getTeam(iTeam).getName()
		else:
			return 0, TRNSLTR.getText("TXT_KEY_TOPCIVS_UNKNOWN", ())

	def getPlayerStatusName(self, iPlayer):
		if iPlayer == -1: # there is no player
			return False, "-"

		CyPlayer = GC.getPlayer(iPlayer)
		iTeam = CyPlayer.getTeam()
		iTeamActive = GC.getPlayer(self.iActivePlayer).getTeam()

		if iTeamActive == iTeam:
			return True, CyPlayer.getName()

		if GC.getTeam(iTeamActive).isHasMet(iTeam):
			return True, CyPlayer.getName()
		else:
			return False, TRNSLTR.getText("TXT_KEY_TOPCIVS_UNKNOWN", ())

	def getVoteTotalColor(self, iVoteReq, iVoteTotal, iVoteCand, bWinner, bVictoryVote):
		print "%i %i %i" % (iVoteReq, iVoteTotal, iVoteCand)
		if not bWinner:
			return -1
		if (iVoteCand > iVoteReq
		and bVictoryVote):
			return ColorUtil.keyToType("COLOR_RED")
		if iVoteTotal > iVoteReq:
			return ColorUtil.keyToType("COLOR_GREEN")
		return -1

	def showGameSettingsScreen(self):
		self.deleteAllWidgets()
		GAME = GC.getGame()
		screen = self.getScreen()
		iWidGen = WidgetTypes.WIDGET_GENERAL

		## Start HOF MOD V1.61.001  3/8
		failedHOFChecks = False
		showHOFSettingChecks = BUFFYOpt.isWarningsSettings()
		self.getBuffyWarningText()

		# EF: Mac only?
		if showHOFSettingChecks and GameSetUpCheck.isXOTMScenario():
			showHOFSettingChecks = False
		## End HOF MOD V1.61.001  3/8

		CyPlayer = GC.getPlayer(self.iActivePlayer)

		szSettingsPanel = self.getNextWidgetName()
		screen.addPanel(szSettingsPanel, TRNSLTR.getText("TXT_KEY_MAIN_MENU_SETTINGS", ()).upper(), "", True, True, self.SETTINGS_PANEL_X1, self.SETTINGS_PANEL_Y - 10, self.SETTINGS_PANEL_WIDTH, self.SETTINGS_PANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN)
		szSettingsTable = self.getNextWidgetName()
		screen.addListBoxGFC(szSettingsTable, "", self.SETTINGS_PANEL_X1 + self.MARGIN, self.SETTINGS_PANEL_Y + self.MARGIN, self.SETTINGS_PANEL_WIDTH - 2*self.MARGIN, self.SETTINGS_PANEL_HEIGHT - 2*self.MARGIN, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(szSettingsTable, False)

		if showHOFSettingChecks and BugPath.isMac():
			failedHOFChecks = True
			showHOFSettingChecks = False
			screen.appendListBoxStringNoUpdate(szSettingsTable, self.BuffyWarningMac, iWidGen, -1, -1, 1<<0)

		screen.appendListBoxStringNoUpdate(szSettingsTable, TRNSLTR.getText("TXT_KEY_LEADER_CIV_DESCRIPTION", (CyPlayer.getNameKey(), CyPlayer.getCivilizationShortDescriptionKey())), iWidGen, -1, -1, 1<<0)
		szText = CyGameTextMgr().parseLeaderTraits(CyPlayer.getLeaderType(), CyPlayer.getCivilizationType(), True, False)
		if szText:
			screen.appendListBoxStringNoUpdate(szSettingsTable, "	(" + szText + ")", iWidGen, -1, -1, 1<<0)
		screen.appendListBoxStringNoUpdate(szSettingsTable, " ", iWidGen, -1, -1, 1<<0)
		#Afforess Difficulty Can Change
		screen.appendListBoxString(szSettingsTable, TRNSLTR.getText("TXT_KEY_SETTINGS_DIFFICULTY", (GC.getHandicapInfo(CyPlayer.getHandicapType()).getTextKey(), )), iWidGen, -1, -1, 1<<0)
		#Afforess End
		screen.appendListBoxStringNoUpdate(szSettingsTable, " ", iWidGen, -1, -1, 1<<0 )

		## Start HOF MOD V1.61.001  4/8
		if showHOFSettingChecks and not GameSetUpCheck.isMapScriptOK():
			screen.appendListBoxStringNoUpdate(szSettingsTable, GC.getMap().getMapScriptName() + " " + self.BuffyWarningNotAllowed, iWidGen, -1, -1, 1<<0)
			failedHOFChecks = True
		else:
			screen.appendListBoxStringNoUpdate(szSettingsTable, GC.getMap().getMapScriptName(), iWidGen, -1, -1, 1<<0)

		if showHOFSettingChecks and GameSetUpCheck.getBalanced():
			screen.appendListBoxStringNoUpdate(szSettingsTable, self.BuffyWarningBalancedResoucesNotAllowed, iWidGen, -1, -1, 1<<0)
			failedHOFChecks = True

		if showHOFSettingChecks and not GameSetUpCheck.getWorldWrapSettingOK():
			szText = TRNSLTR.getText(worldWrapString[GameSetUpCheck.getWorldWrap()],())
			szText += " " + self.BuffyWarningNotAllowed
			screen.appendListBoxStringNoUpdate(szSettingsTable, szText, iWidGen, -1, -1, 1<<0 )
			failedHOFChecks = True
		else:
			szText = TRNSLTR.getText(worldWrapString[GameSetUpCheck.getWorldWrap()],())
			screen.appendListBoxStringNoUpdate(szSettingsTable, szText, iWidGen, -1, -1, 1<<0 )
		## End HOF MOD V1.61.001  4/8

		screen.appendListBoxStringNoUpdate(szSettingsTable, TRNSLTR.getText("TXT_KEY_SETTINGS_MAP_SIZE", (GC.getWorldInfo(GC.getMap().getWorldSize()).getTextKey(), )), iWidGen, -1, -1, 1<<0 )
		screen.appendListBoxStringNoUpdate(szSettingsTable, TRNSLTR.getText("TXT_KEY_SETTINGS_CLIMATE", (GC.getClimateInfo(GC.getMap().getClimate()).getTextKey(), )), iWidGen, -1, -1, 1<<0 )
		screen.appendListBoxStringNoUpdate(szSettingsTable, TRNSLTR.getText("TXT_KEY_SETTINGS_SEA_LEVEL", (GC.getSeaLevelInfo(GC.getMap().getSeaLevel()).getTextKey(), )), iWidGen, -1, -1, 1<<0 )
		screen.appendListBoxStringNoUpdate(szSettingsTable, " ", iWidGen, -1, -1, 1<<0 )
		screen.appendListBoxStringNoUpdate(szSettingsTable, TRNSLTR.getText("TXT_KEY_SETTINGS_STARTING_ERA", (GC.getEraInfo(GAME.getStartEra()).getTextKey(), )), iWidGen, -1, -1, 1<<0 )
		screen.appendListBoxStringNoUpdate(szSettingsTable, TRNSLTR.getText("TXT_KEY_SETTINGS_GAME_SPEED", (GC.getGameSpeedInfo(GAME.getGameSpeedType()).getTextKey(), )), iWidGen, -1, -1, 1<<0 )

		## Start HOF MOD V1.61.001  5/8
		if showHOFSettingChecks:
			szText = ""
			for iVCLoop in xrange(GC.getNumVictoryInfos()):
				if not GAME.isVictoryValid(iVCLoop):
					if szText:
						szText += ", "
					else:
						szText = self.BuffyWarningVictoryConditions + " "
					szText += GC.getVictoryInfo(iVCLoop).getDescription()
			if szText:
				failedHOFChecks = True
				screen.appendListBoxStringNoUpdate(szSettingsTable, " ", iWidGen, -1, -1, 1<<0)
				screen.appendListBoxStringNoUpdate(szSettingsTable, szText, iWidGen, -1, -1, 1<<0)

			if GameSetUpCheck.crcResult != 0:
				failedHOFChecks = True
				if GameSetUpCheck.crcResult==1:
					szText = self.BuffyWarningCheckSumMissing
				elif GameSetUpCheck.crcResult==2:
					szText = self.BuffyWarningCheckSumDifferent
				else:
					szText = self.BuffyWarningCheckSumFailed
				screen.appendListBoxStringNoUpdate(szSettingsTable, " ", iWidGen, -1, -1, 1<<0)
				screen.appendListBoxStringNoUpdate(szSettingsTable, BugUtil.colorText(szText, "COLOR_WARNING_TEXT"), iWidGen, -1, -1, 1<<0)
		## End HOF MOD V1.61.001  5/8

		screen.updateListBox(szSettingsTable)

		szOptionsPanel = self.getNextWidgetName()
		screen.addPanel(szOptionsPanel, TRNSLTR.getText("TXT_KEY_MAIN_MENU_CUSTOM_SETUP_OPTIONS", ()).upper(), "", True, True, self.SETTINGS_PANEL_X2, self.SETTINGS_PANEL_Y - 10, self.SETTINGS_PANEL_WIDTH, self.SETTINGS_PANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN)
		szOptionsTable = self.getNextWidgetName()
		screen.addListBoxGFC(szOptionsTable, "", self.SETTINGS_PANEL_X2 + self.MARGIN, self.SETTINGS_PANEL_Y + self.MARGIN, self.SETTINGS_PANEL_WIDTH - 2*self.MARGIN, self.SETTINGS_PANEL_HEIGHT - 2*self.MARGIN, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(szOptionsTable, False)

		## Start HOF MOD V1.61.001  6/8
		if (showHOFSettingChecks and GAME.isGameMultiPlayer()):
			screen.appendListBoxStringNoUpdate(szOptionsTable, self.BuffyWarningMultiPlayerNotAllowed, iWidGen, -1, -1, 1<<0)
			failedHOFChecks = True

		if showHOFSettingChecks:
			invalidOptions = GameSetUpCheck.getInvalidGameOptions()
			if len(invalidOptions) > 0:
				failedHOFChecks = True
				for i in xrange(GC.getNumGameOptionInfos()):
					szDescription = GC.getGameOptionInfo(i).getDescription()
					if i not in invalidOptions:
						if GAME.isOption(i):
							screen.appendListBoxStringNoUpdate(szOptionsTable, szDescription, iWidGen, -1, -1, 1<<0)
					else:
						if invalidOptions[i]:
							screen.appendListBoxStringNoUpdate(szOptionsTable, BugUtil.colorText(szDescription, "COLOR_YELLOW") + u" " + self.BuffyWarningRequired, iWidGen, -1, -1, 1<<0)
						else:
							screen.appendListBoxStringNoUpdate(szOptionsTable, szDescription + u" " + self.BuffyWarningNotAllowed, iWidGen, -1, -1, 1<<0)
			else:
				for i in xrange(GC.getNumGameOptionInfos()):
					screen.appendListBoxStringNoUpdate(szOptionsTable, GC.getGameOptionInfo(i).getDescription(), iWidGen, -1, -1, 1<<0)
		else:
			for i in xrange(GC.getNumGameOptionInfos()):
				if GAME.isOption(i):
					screen.appendListBoxStringNoUpdate(szOptionsTable, GC.getGameOptionInfo(i).getDescription(), iWidGen, -1, -1, 1<<0)

		if showHOFSettingChecks and not Buffy.isDllPresent():
			failedHOFChecks = True
			screen.appendListBoxStringNoUpdate(szOptionsTable, "\n" + self.BuffyWarningNoDll, iWidGen, -1, -1, 1<<0 )

		if showHOFSettingChecks and not Buffy.isDllInCorrectPath():
			failedHOFChecks = True
			szText = "\n" + self.BuffyWarningInstallLocation + "\n" + GAME.getExePath() + "\Mods"
			screen.appendListBoxStringNoUpdate(szOptionsTable, szText, iWidGen, -1, -1, 1<<0 )

		if GAME.isOption(GameOptionTypes.GAMEOPTION_ADVANCED_START):
			szNumPoints = u"%s %d" % (TRNSLTR.getText("TXT_KEY_ADVANCED_START_POINTS", ()), GAME.getNumAdvancedStartPoints())
			screen.appendListBoxStringNoUpdate(szOptionsTable, szNumPoints, iWidGen, -1, -1, 1<<0)

		if GAME.isGameMultiPlayer():
			for i in xrange(GC.getNumMPOptionInfos()):
				if GAME.isMPOption(i):
					screen.appendListBoxStringNoUpdate(szOptionsTable, GC.getMPOptionInfo(i).getDescription(), iWidGen, -1, -1, 1<<0)

			if GAME.getMaxTurns() > 0:
				szMaxTurns = u"%s %d" % (TRNSLTR.getText("TXT_KEY_TURN_LIMIT_TAG", ()), GAME.getMaxTurns())
				screen.appendListBoxStringNoUpdate(szOptionsTable, szMaxTurns, iWidGen, -1, -1, 1<<0)

			if GAME.getMaxCityElimination() > 0:
				szMaxCityElimination = u"%s %d" % (TRNSLTR.getText("TXT_KEY_CITY_ELIM_TAG", ()), GAME.getMaxCityElimination())
				screen.appendListBoxStringNoUpdate(szOptionsTable, szMaxCityElimination, iWidGen, -1, -1, 1<<0)

		if GAME.hasSkippedSaveChecksum():
			screen.appendListBoxStringNoUpdate(szOptionsTable, self.BuffyWarningSkippedCheckSum, iWidGen, -1, -1, 1<<0)

		screen.updateListBox(szOptionsTable)

		szCivsPanel = self.getNextWidgetName()
		screen.addPanel(szCivsPanel, TRNSLTR.getText("TXT_KEY_RIVALS_MET", ()).upper(), "", True, True, self.SETTINGS_PANEL_X3, self.SETTINGS_PANEL_Y - 10, self.SETTINGS_PANEL_WIDTH, self.SETTINGS_PANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN)

		szCivsTable = self.getNextWidgetName()
		screen.addListBoxGFC(szCivsTable, "", self.SETTINGS_PANEL_X3 + self.MARGIN, self.SETTINGS_PANEL_Y + self.MARGIN, self.SETTINGS_PANEL_WIDTH - 2*self.MARGIN, self.SETTINGS_PANEL_HEIGHT - 2*self.MARGIN, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(szCivsTable, False)

		## Start HOF MOD V1.61.001  7/8
		if showHOFSettingChecks:
			civCounts = [0] * GC.getNumLeaderHeadInfos()
			opponentCount = -1

			for iPlayerX in range(GC.getMAX_PC_PLAYERS()):
				CyPlayerX = GC.getPlayer(iPlayerX)
				if CyPlayerX.isEverAlive() and not CyPlayerX.isMinorCiv():
					civCounts[iPlayerX.getLeaderType()] += 1
					opponentCount += 1

			if GameSetUpCheck.isMapSizeOK() and not GameSetUpCheck.isOpponentCountOK(opponentCount):
				failedHOFChecks = True
				zsMapSize = TRNSLTR.getText("TXT_KEY_SETTINGS_MAP_SIZE", (GC.getWorldInfo(GC.getMap().getWorldSize()).getTextKey(),))
				minOpponents, maxOpponents = GameSetUpCheck.getValidOpponentCountRange()
				if opponentCount < minOpponents:
					szText = BugUtil.getText("TXT_KEY_BUFFYWARNING_TOO_FEW_OPPONENTS", (minOpponents, zsMapSize))
				elif opponentCount > maxOpponents:
					szText = BugUtil.getText("TXT_KEY_BUFFYWARNING_TOO_MANY_OPPONENTS", (maxOpponents, zsMapSize))
				screen.appendListBoxStringNoUpdate(szCivsTable, szText, iWidGen, -1, -1, 1<<0)

			for iLoopCivs, count in enumerate(civCounts):
				if count > 1:
					failedHOFChecks = True
					zsLeader = GC.getLeaderHeadInfo(iLoopCivs).getText()
					szText = BugUtil.getText("TXT_KEY_BUFFYWARNING_MULT_LEADERS", (zsLeader, count))
					screen.appendListBoxStringNoUpdate(szCivsTable, szText, iWidGen, -1, -1, 1<<0)

			if GAME.isTeamGame():
				failedHOFChecks = True
				screen.appendListBoxStringNoUpdate(szCivsTable, self.BuffyWarningNoTeams, iWidGen, -1, -1, 1<<0)
		## End HOF MOD V1.61.001  7/8

		iTeam = CyPlayer.getTeam()
		for iPlayerX in xrange(GC.getMAX_PC_PLAYERS()):
			if iPlayerX == self.iActivePlayer:
				continue
			CyPlayerX = GC.getPlayer(iPlayerX)
			if not CyPlayerX.isEverAlive() or CyPlayerX.isMinorCiv():
				continue
			if GC.getTeam(CyPlayerX.getTeam()).isHasMet(iTeam) or GAME.isDebugMode():
				szText = TRNSLTR.getText("TXT_KEY_LEADER_CIV_DESCRIPTION", (CyPlayerX.getNameKey(), CyPlayerX.getCivilizationShortDescriptionKey()))
				screen.appendListBoxStringNoUpdate(szCivsTable, szText, iWidGen, -1, -1, 1<<0)
				szText = CyGameTextMgr().parseLeaderTraits(CyPlayerX.getLeaderType(), CyPlayerX.getCivilizationType(), True, False)
				if szText:
					screen.appendListBoxStringNoUpdate(szCivsTable, "     (" + szText + ")", iWidGen, -1, -1, 1<<0)
				screen.appendListBoxStringNoUpdate(szCivsTable, " ", iWidGen, -1, -1, 1<<0 )

		screen.updateListBox(szCivsTable)

		## Start HOF MOD V1.61.001  8/8
		if failedHOFChecks:
			szHOFWarningPanel = self.getNextWidgetName()
			screen.addPanel(szHOFWarningPanel, self.BuffyWarning, "", True, True, self.HOF_WARNING_PANEL_X, self.HOF_WARNING_PANEL_Y, self.HOF_WARNING_PANEL_WIDTH, self.HOF_WARNING_PANEL_HEIGHT, PanelStyles.PANEL_STYLE_MAIN)
			szHOFWarningBox = self.getNextWidgetName()
			screen.addListBoxGFC(szHOFWarningBox, "", self.HOF_WARNING_PANEL_X + 20, self.HOF_WARNING_PANEL_Y + 37, self.HOF_WARNING_PANEL_WIDTH, self.HOF_WARNING_PANEL_HEIGHT, TableStyles.TABLE_STYLE_EMPTY)
			screen.enableSelect(szHOFWarningBox, False)
			screen.appendListBoxString(szHOFWarningBox, self.BuffyWarningNotValid, iWidGen, -1, -1, 1<<0 )
		## End HOF MOD V1.61.001  8/8

		self.drawTabs()


	def getBuffyWarningText(self):
		if self.BuffyWarningTextLoaded:
			return
		else:
			self.BuffyWarningTextLoaded = True

		self.BuffyWarning = BugUtil.getText("TXT_KEY_BUFFYWARNING")
		self.BuffyWarningNotValid = BugUtil.getText("TXT_KEY_BUFFYWARNING_NOT_VALID")
		self.BuffyWarningNoTeams = BugUtil.getText("TXT_KEY_BUFFYWARNING_NO_TEAMS")
		self.BuffyWarningMac = BugUtil.getText("TXT_KEY_BUFFYWARNING_MAC")
		self.BuffyWarningInstallLocation = BugUtil.getText("TXT_KEY_BUFFYWARNING_INSTALL_LOCATION")
		self.BuffyWarningMultiPlayerNotAllowed = BugUtil.getText("TXT_KEY_BUFFYWARNING_MULTI_PLAYER_NOT_ALLOWED")
		self.BuffyWarningNoDll = BugUtil.getText("TXT_KEY_BUFFYWARNING_DLL_MISSING")
		self.BuffyWarningSkippedCheckSum = BugUtil.getText("TXT_KEY_BUFFYWARNING_CHECKSUM_SKIPPED")
		self.BuffyWarningCheckSumMissing = BugUtil.getText("TXT_KEY_BUFFYWARNING_CHECKSUM_MISSING")
		self.BuffyWarningCheckSumDifferent = BugUtil.getText("TXT_KEY_BUFFYWARNING_CHECKSUM_DIFFERENT")
		self.BuffyWarningCheckSumFailed = BugUtil.getText("TXT_KEY_BUFFYWARNING_CHECKSUM_FAILED")
		self.BuffyWarningVictoryConditions = BugUtil.getText("TXT_KEY_BUFFYWARNING_VICTORY_CONDITIONS")
		self.BuffyWarningRequired = BugUtil.getText("TXT_KEY_BUFFYWARNING_REQUIRED")
		self.BuffyWarningNotAllowed = BugUtil.getText("TXT_KEY_BUFFYWARNING_NOT_ALLOWED")
		self.BuffyWarningBalancedResoucesNotAllowed = BugUtil.getText("TXT_KEY_BUFFYWARNING_BALANCED_RESOUCES_NOT_ALLOWED")

#Sevo--VCM
# The entire function has been redone.  
	def showVictoryConditionScreen(self):
		GAME = GC.getGame()
		iActivePlayer = self.iActivePlayer
		CyPlayer = GC.getPlayer(iActivePlayer)
		iActiveTeam = CyPlayer.getTeam()
		CyTeam = GC.getTeam(iActiveTeam)

		# checking if apollo has been built - clear arrays / lists / whatever they are called
		self.ApolloTeamsChecked = set()
		self.ApolloTeamCheckResult = {}

		# Conquest
		nRivals = 0
		nknown = 0
		nVassaled = 0
		for iTeamX in xrange(GC.getMAX_PC_TEAMS()):
			if iTeamX == iActiveTeam: continue
			CyTeamX = GC.getTeam(iTeamX)
			if CyTeamX.isAlive() and not CyTeamX.isMinorCiv():
				nRivals += 1
				if CyTeamX.isHasMet(iActiveTeam):
					nknown += 1
				if CyTeamX.isVassal(iActiveTeam):
					nVassaled += 1

		# Population
		totalPop = GAME.getTotalPopulation()
		ourPop = CyTeam.getTotalPopulation()
		if totalPop > 0:
			popPercent = ourPop * 100.0 / totalPop
		else:
			popPercent = 0.0
# Prevents division by zero at beginning of game; picky, I know.
			TotalPop = 1


		iBestPopTeam = -1
		bestPop = 0
		for iTeamX in xrange(GC.getMAX_PC_TEAMS()):
			if iTeamX == iActiveTeam:
				continue
			CyTeamX = GC.getTeam(iTeamX)
			if CyTeamX.isAlive() and not CyTeamX.isMinorCiv():
				if CyTeam.isHasMet(iTeamX) or GAME.isDebugMode():
					teamPop = CyTeamX.getTotalPopulation()
					if teamPop > bestPop:
						bestPop = teamPop
						iBestPopTeam = iTeamX

		# Score
		ourScore = GAME.getTeamScore(iActiveTeam)

		iBestScoreTeam = -1
		bestScore = 0
		for iTeamX in xrange(GC.getMAX_PC_TEAMS()):
			if iTeamX == iActiveTeam: continue
			CyTeamX = GC.getTeam(iTeamX)
			if CyTeamX.isAlive() and not CyTeamX.isMinorCiv():
				if CyTeam.isHasMet(iTeamX) or GAME.isDebugMode():
					teamScore = GAME.getTeamScore(iTeamX)
					if teamScore > bestScore:
						bestScore = teamScore
						iBestScoreTeam = iTeamX

		# Land Area
		totalLand = GC.getMap().getLandPlots()
		ourLand = CyTeam.getTotalLand()
		if totalLand > 0:
			landPercent = ourLand * 100.0 / totalLand
		else:
			landPercent = 0.0

		iBestLandTeam = -1
		bestLand = 0

		ownedLand = 0
		for iTeamX in xrange(GC.getMAX_PC_TEAMS()):
			CyTeamX = GC.getTeam(iTeamX)
			ownedLand += CyTeamX.getTotalLand()
			if iTeamX == iActiveTeam:
				continue
			if CyTeamX.isAlive() and not CyTeamX.isMinorCiv():
				if CyTeam.isHasMet(iTeamX) or GAME.isDebugMode():
					teamLand = CyTeamX.getTotalLand()
					if teamLand > bestLand:
						bestLand = teamLand
						iBestLandTeam = iTeamX
		if ownedLand < 1:
			ownedLand = 1
		TVLand = ourLand * 100.0 / totalLand


		# Religion
		iOurReligion = -1
		ourReligionPercent = 0
		for iLoopReligion in xrange(GC.getNumReligionInfos()):
			if CyTeam.hasHolyCity(iLoopReligion):
				religionPercent = GAME.calculateReligionPercent(iLoopReligion)
				if religionPercent > ourReligionPercent:
					ourReligionPercent = religionPercent
					iOurReligion = iLoopReligion

		iBestReligion = -1
		bestReligionPercent = 0
		for iLoopReligion in xrange(GC.getNumReligionInfos()):
			if iLoopReligion != iOurReligion:
				religionPercent = GAME.calculateReligionPercent(iLoopReligion)
				if religionPercent > bestReligionPercent:
					bestReligionPercent = religionPercent
					iBestReligion = iLoopReligion

		# Total Culture
		iBestCultureTeam = -1
		bestCulture = 0
		worldCulture = 0

		for iTeamX in xrange(GC.getMAX_PC_TEAMS()):
			CyTeamX = GC.getTeam(iTeamX)
			worldCulture += CyTeamX.countTotalCulture()
			if iTeamX == iActiveTeam:
				continue
			if CyTeamX.isAlive() and not CyTeamX.isMinorCiv():
				if CyTeam.isHasMet(iTeamX) or GAME.isDebugMode():
					teamCulture = CyTeamX.countTotalCulture()
					if teamCulture > bestCulture:
						bestCulture = teamCulture
						iBestCultureTeam = iTeamX
		if worldCulture < 1:
			worldCulture = 1

		# Vote
		aiVoteBuildingClass = []
		for i in xrange(GC.getNumBuildingInfos()):
			CvBuildingInfo = GC.getBuildingInfo(i)
			for j in xrange(GC.getNumVoteSourceInfos()):
				if CvBuildingInfo.getVoteSourceType() == j:
					iUNTeam = -1
					bUnknown = True

					for iPlayerX in xrange(GC.getMAX_PC_PLAYERS()):
						CyPlayerX = GC.getPlayer(iPlayerX)
						if CyPlayerX.isAlive() and not CyPlayerX.isMinorCiv() and CyPlayerX.countNumBuildings(i):
							iUNTeam = CyPlayerX.getTeam()
							if iUNTeam == iActiveTeam or GAME.isDebugMode() or CyTeam.isHasMet(iUNTeam):
								bUnknown = False
							break

					aiVoteBuildingClass.append((CvBuildingInfo.getBuildingClassType(), iUNTeam, bUnknown))

		self.bVoteTab = (len(aiVoteBuildingClass) > 0)

		self.deleteAllWidgets()
		screen = self.getScreen()
		iWidGen = WidgetTypes.WIDGET_GENERAL

#################################################################################################
	# Get Best Team
		iBestTeam = GC.getPlayer(0).getTeam() # The first turn of the game, everyone's score starts at 0, so there is no best team. 
		iBestTeamScore = 0
		iTVScore = 0
		for iPlayerX in xrange(GC.getMAX_PC_PLAYERS()):
			if iPlayerX == iActivePlayer:
				continue
			CyPlayerX = GC.getPlayer(iPlayerX)
			if CyPlayerX.isAlive():
				iTeamX = CyPlayerX.getTeam()
				iTVScore = GC.getTeam(iTeamX).getTotalVictoryScore()
				if iTVScore > iBestTeamScore:
					iBestTeamScore = iTVScore
					iBestTeam = iTeamX
		CyTeamBest = GC.getTeam(iBestTeam)
		bMetHuman = CyTeamBest.hasMetHuman()

	# Power History
		ourPower = 0;
		worldPower = 0;
		bestPower = 0;

		for iPlayerX in xrange(GC.getMAX_PC_PLAYERS()):
			CyPlayerX = GC.getPlayer(iPlayerX)
			if CyPlayerX.isAlive():
				iTeamX = CyPlayerX.getTeam()
				for i in xrange(GAME.getGameTurn()):
					worldPower += CyPlayerX.getPowerHistory(i);

					if iActiveTeam == iTeamX:
						ourPower += CyPlayerX.getPowerHistory(i);
					elif iBestTeam == iTeamX:
						bestPower += CyPlayerX.getPowerHistory(i);
		if worldPower < 1:
			worldPower = 1;

		ourCulture = CyTeam.countTotalCulture()

		for iLoopVC in xrange(GC.getNumVictoryInfos()):
			victory = GC.getVictoryInfo(iLoopVC)
			if victory.isTotalVictory():
				if GAME.isVictoryValid(iLoopVC):

					self.deleteAllWidgets()

					self.drawTabs()
					# Start filling in the table below
					screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-10, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+30, PanelStyles.PANEL_STYLE_BLUE50)
					szTable = self.getNextWidgetName()
					screen.addTableControlGFC(szTable, 5, self.X_AREA, self.Y_AREA, self.W_AREA, self.H_AREA, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
					screen.setTableColumnHeader(szTable, 0, "", 430)
					screen.setTableColumnHeader(szTable, 1, "", 180)
					screen.setTableColumnHeader(szTable, 2, "", int(180 * 0.5) + 100)
					screen.setTableColumnHeader(szTable, 3, "", int(180 * 0.5) + 100)
					screen.appendTableRow(szTable)

					szVictoryType = "<font=4b>" + victory.getDescription().upper() + "</font>"
					if (GAME.getMaxTurns() > GAME.getElapsedGameTurns() and GAME.getMaxTurns()/8 < GAME.getElapsedGameTurns()) or GAME.cheatCodesEnabled():
						iNumRows = screen.getTableNumRows(szTable)
						szVictoryType += "    (" + TRNSLTR.getText("TXT_KEY_MISC_TURNS_LEFT", (GAME.getMaxTurns() - GAME.getElapsedGameTurns(), )) + ")"
						screen.setTableText(szTable, 0, iNumRows - 1, szVictoryType, "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 1, iNumRows - 1, "<font=4b>" + CyPlayer.getName(), "", iWidGen, -1, -1, 1<<2)
						if bMetHuman:
							screen.setTableText(szTable, 3, iNumRows - 1, "<font=4b>" + CyTeamBest.getName(), "", iWidGen, -1, -1, 1<<0)

					elif GAME.getMaxTurns()/8 > GAME.getElapsedGameTurns():
						iRow = screen.appendTableRow(szTable)
						iRow = screen.appendTableRow(szTable)
						screen.setTableText(szTable, 0, iRow, u"<font=3b>" + TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_TOOEARLY", ())  + u"</font>", "", iWidGen, -1, -1, 1<<0)
						return

					iRow = screen.appendTableRow(szTable)

				# Headings
					screen.setTableText(szTable, 0, iRow, "<font=3b>" + TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_CONDITION", ()), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 1, iRow, "<font=3b>" + TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_PERCENTAGE", ()), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, "<font=3b>" + TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_POINTS", ()), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 3, iRow, "<font=2b>" + "(" + TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_RIVAL_CIV", ()) + ")", "", iWidGen, -1, -1, 1<<0)

					screen.appendTableRow(szTable)
					iRow = screen.appendTableRow(szTable)

				# Population
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_WORLD_POP", ()), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 1, iRow, (u"%i%%" % popPercent), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, (u"%i" % popPercent), "", iWidGen, -1, -1, 1<<0)
					if iBestTeam != -1 and bMetHuman:
						screen.setTableText(szTable, 3, iRow, (u"%i%%" % (CyTeamBest.getTotalPopulation() * 100 / totalPop)), "", iWidGen, -1, -1, 1<<0)
					else:
						screen.setTableText(szTable, 3, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_UNKNOWN", ()), "", iWidGen, -1, -1, 1<<0)

				# Land
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_WORLD_LAND", ()), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 1, iRow, (u"%i%%" % TVLand), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, (u"%i" % TVLand), "", iWidGen, -1, -1, 1<<0)
					if iBestTeam != -1 and bMetHuman:
						screen.setTableText(szTable, 3, iRow, (u"%i%%" % (CyTeamBest.getTotalLand() * 100 / totalLand)), "", iWidGen, -1, -1, 1<<0)
					else:
						screen.setTableText(szTable, 3, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_UNKNOWN", ()), "", iWidGen, -1, -1, 1<<0)
				# Culture
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_CONCEPT_CULTURE", ()), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 1, iRow, u"%i%%" %(ourCulture * 100/worldCulture), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, u"%i" %(ourCulture * 100/worldCulture), "", iWidGen, -1, -1, 1<<0)
					if iBestTeam != -1 and bMetHuman:
						screen.setTableText(szTable, 3, iRow, u"%i%%" %(CyTeamBest.countTotalCulture() * 100 / worldCulture), "", iWidGen, -1, -1, 1<<0)
					else:
						screen.setTableText(szTable, 3, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_UNKNOWN", ()), "", iWidGen, -1, -1, 1<<0)
				# Power
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_POWER", ()), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 1, iRow, u"%i" %(ourPower), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, u"%i" %(ourPower * 100/worldPower), "", iWidGen, -1, -1, 1<<0)
					if iBestTeam != -1 and bMetHuman:
						screen.setTableText(szTable, 3, iRow, u"%i" %(bestPower), "", iWidGen, -1, -1, 1<<0)
					else:
						screen.setTableText(szTable, 3, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_UNKNOWN", ()), "", iWidGen, -1, -1, 1<<0)

				# WonderScores

					iTeamWonderScore = self.getTeamWonderScore(iActiveTeam)
					iRivalWonderScore = self.getTeamWonderScore(iBestTeam)
					iTotalWorldWondersBuilt = GC.getPlayer(0).getSevoWondersScore(1)
					iTotalWorldWondersPossible = GC.getPlayer(0).getSevoWondersScore(2)
					if iTotalWorldWondersPossible == 0:
						iTotalWorldWondersPossible = -1

					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_CONCEPT_WONDERS", ()), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 1, iRow, u"%i  (%i of %i built)" %(iTeamWonderScore, iTotalWorldWondersBuilt, iTotalWorldWondersPossible), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, u"%i" %(iTeamWonderScore * 100 /iTotalWorldWondersPossible), "", iWidGen, -1, -1, 1<<0)
					if iBestTeam != -1 and bMetHuman:
						screen.setTableText(szTable, 3, iRow, u"%i" %(iRivalWonderScore), "", iWidGen, -1, -1, 1<<0)
					else:
						screen.setTableText(szTable, 3, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_UNKNOWN", ()), "", iWidGen, -1, -1, 1<<0)

				# Religion
					iRow = screen.appendTableRow(szTable)
					iRefRow = iRow
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_CONCEPT_RELIGION",()), "", iWidGen, -1, -1, 1<<0)

					if iOurReligion != -1:
						for iLoopReligion in xrange(GC.getNumReligionInfos()):
							if CyTeam.hasHolyCity(iLoopReligion):
								religionPercent = GAME.calculateReligionPercent(iLoopReligion)

								iRow = screen.appendTableRow(szTable)
								screen.setTableText(szTable, 0, iRow, GC.getReligionInfo(iLoopReligion).getDescription(), "", iWidGen, -1, -1, 1<<1)
								screen.setTableText(szTable, 1, iRow, (u"%d%%" % religionPercent), "", iWidGen, -1, -1, 1<<0)

								#Only get points for the TOP religion score.
								if iLoopReligion == iOurReligion:
									screen.setTableText(szTable, 2, iRow, (u"%d" % religionPercent), "", iWidGen, -1, -1, 1<<0)

					else:
						iRow = screen.appendTableRow(szTable)
						screen.setTableText(szTable, 1, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_NO_HOLY", ()), "", iWidGen, -1, -1, 1<<0)

					iReligionFound = 0;
					if iBestTeam != -1 and bMetHuman:
						for iLoopReligion in xrange(GC.getNumReligionInfos()):
							if (CyTeamBest.hasHolyCity(iLoopReligion)):
								iReligionFound = 1;
								religionPercent = GAME.calculateReligionPercent(iLoopReligion)

								iRefRow += 1
								if (iRefRow > iRow):
									iRow = screen.appendTableRow(szTable)
								screen.setTableText(szTable, 3, iRefRow, (u"%s: %i%%" %(GC.getReligionInfo(iLoopReligion).getDescription(), religionPercent)), "", iWidGen, -1, -1, 1<<0)
						if not iReligionFound:
							iRefRow += 1
							screen.setTableText(szTable, 3, iRefRow, u"No Holy City", "", iWidGen, -1, -1, 1<<0)
					else:
						screen.setTableText(szTable, 3, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_UNKNOWN", ()), "", iWidGen, -1, -1, 1<<0)


					# Legendary Cultural Cities

					(iPlayerLegendaryCities, iWorldLegendaryCities) = self.getLegendaryCities(iActiveTeam)
					(iBestTeamLegendaryCities, iWorldLegendaryCities) = self.getLegendaryCities(iBestTeam)

					ourBestCities = self.getListCultureCitiesTeam(iActiveTeam)[0:(iPlayerLegendaryCities + 3)]
					theirBestCities = self.getListCultureCitiesTeam(iBestTeam)[0:(iBestTeamLegendaryCities+3)]

					iRow = screen.appendTableRow(szTable)
					iRefRow = iRow
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_CITIES", ()), "", iWidGen, -1, -1, 1<<0)

					for i in xrange(len(ourBestCities)):
						iRow = screen.appendTableRow(szTable)
						screen.setTableText(szTable, 0, iRow, ourBestCities[i][1].getName() + ":", "", iWidGen, -1, -1, 1<<1)
						screen.setTableText(szTable, 1, iRow, str(ourBestCities[i][0]), "", iWidGen, -1, -1, 1<<0)
						if iPlayerLegendaryCities >= i + 1:
							screen.setTableText(szTable, 2, iRow, u"%s" %(30), "", iWidGen, -1, -1, 1<<0)

					if iBestTeam != -1 and bMetHuman:
						for i in xrange(len(theirBestCities)):
							iRefRow += 1
							if iRefRow > iRow:
								iRow = screen.appendTableRow(szTable)
							screen.setTableText(szTable, 3, iRefRow, u"%s : %i" %(theirBestCities[i][1].getName() + ":", theirBestCities[i][0]), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 3, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_UNKNOWN", ()), "", iWidGen, -1, -1, 1<<0)


				# Starship Launch Data
					iRow = screen.appendTableRow(szTable)
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_CONCEPT_SPACESHIP", ()), "", iWidGen, -1, -1, 1<<0)

					if iBestTeam != -1:
						iRivalLaunched = self.teamLaunchedShip(iBestTeam)

					iNeedParts = 0


					if self.teamLaunchedShip(iActiveTeam) == 1:
						screen.setTableText(szTable, 1, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_LAUNCHED", ()), "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 2, iRow, u"%i" %(100), "", iWidGen, -1, -1, 1<<0)
					else:
						screen.setTableText(szTable, 1, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_NOTLAUNCHED", ()), "", iWidGen, -1, -1, 1<<0)
						if CyTeam.getProjectCount(GC.getInfoTypeForString("PROJECT_APOLLO_PROGRAM")) > 0:
							iNeedParts = 1

					if iBestTeam != -1 and bMetHuman and iRivalLaunched == 1:
						screen.setTableText(szTable, 3, iRow, u"%s" %(TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_LAUNCHED", ())), "", iWidGen, -1, -1, 1<<0)
					elif iBestTeam != -1 and bMetHuman:
						screen.setTableText(szTable, 3, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_NOTLAUNCHED", ()), "", iWidGen, -1, -1, 1<<0)

					#add spaceship button
					iSpaceshipButtonRow = screen.getTableNumRows(szTable)
					screen.appendTableRow(szTable)
					screen.setButtonGFC("SpaceShipButton" + str(iLoopVC), TRNSLTR.getText("TXT_KEY_GLOBELAYER_STRATEGY_VIEW", ()), "", 0, 0, 15, 10, iWidGen, self.SPACESHIP_SCREEN_BUTTON, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
					screen.attachControlToTableCell("SpaceShipButton" + str(iLoopVC), szTable, iSpaceshipButtonRow, 1)

					if iNeedParts == 1:
						for i in xrange(GC.getNumProjectInfos()):
							for iL in xrange(GC.getNumVictoryInfos()):
								if (GC.getProjectInfo(i).getVictoryThreshold(iL) > 0):
									if (GC.getProjectInfo(i).isSpaceship()):
										iRow = screen.appendTableRow(szTable)
										screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_BUILDING", (GC.getProjectInfo(i).getVictoryThreshold(iL), GC.getProjectInfo(i).getTextKey())), "", iWidGen, -1, -1, 1<<1)

										if self.teamLaunchedShip(iActiveTeam) != 1:
											screen.setTableText(szTable, 1, iRow, str(CyTeam.getProjectCount(i)), "", iWidGen, -1, -1, 1<<0)


				# Score Totals
					iRow = screen.appendTableRow(szTable)
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, u"<font=4b>" + TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_TOTALS", ()) + "</font>", "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, u"<font=4b>%i</font>" %(CyTeam.getTotalVictoryScore()), "", iWidGen, -1, -1, 1<<0)


					if iBestTeam != -1 and bMetHuman:
						screen.setTableText(szTable, 3, iRow, u"<font=4b>%i</font>" %(CyTeamBest.getTotalVictoryScore()), "", iWidGen, -1, -1, 1<<0)
					iRow = screen.appendTableRow(szTable)
					iRow = screen.appendTableRow(szTable)
					iRow = screen.appendTableRow(szTable)
				
				# The rest of the scores
					screen.setTableText(szTable, 0, iRow, "<font=4b>" + TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_OTHER_CIV_SCORE",()) + "</font>", "", iWidGen, -1, -1, 1<<0)
					iRow = screen.appendTableRow(szTable)
					for iTeamX in xrange(GC.getMAX_PC_TEAMS()):
						if iTeamX == iActiveTeam: continue
						CyTeamX = GC.getTeam(iTeamX)
						if CyTeamX.isAlive() and not CyTeamX.isMinorCiv():
							if iTeamX != iActiveTeam and iTeamX != iBestTeam and CyTeam.isHasMet(iTeamX) or GAME.isDebugMode():
								iRow = screen.appendTableRow(szTable)
								screen.setTableText(szTable, 0, iRow, "<font=3b>" + CyTeamX.getName() + ":", "", iWidGen, -1, -1, 1<<0)
								screen.setTableText(szTable, 1, iRow, "<font=3b>" + str(CyTeamX.getTotalVictoryScore()), "", iWidGen, -1, -1, 1<<0)


				# civ picker dropdown
					if CyGame().isDebugMode():
						self.szDropdownName = self.DEBUG_DROPDOWN_ID
						screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, iWidGen, -1, -1, FontTypes.GAME_FONT)
						for j in xrange(GC.getMAX_PLAYERS()):
							if GC.getPlayer(j).isAlive():
								screen.addPullDownString(self.szDropdownName, GC.getPlayer(j).getName(), j, j, False)

					return

	# End of check to see if Total Victory is enabled
#End VCM
		# Start filling in the table below
		screen.addPanel(self.getNextWidgetName(), "", "", False, False, self.X_AREA-10, self.Y_AREA-15, self.W_AREA+20, self.H_AREA+30, PanelStyles.PANEL_STYLE_BLUE50)
		szTable = self.getNextWidgetName()
		screen.addTableControlGFC(szTable, 6, self.X_AREA, self.Y_AREA, self.W_AREA, self.H_AREA, False, False, 32,32, TableStyles.TABLE_STYLE_STANDARD)
		screen.setTableColumnHeader(szTable, 0, "", self.TABLE_WIDTH_0)
		screen.setTableColumnHeader(szTable, 1, "", self.TABLE_WIDTH_1)
		screen.setTableColumnHeader(szTable, 2, "", self.TABLE_WIDTH_2)
		screen.setTableColumnHeader(szTable, 3, "", self.TABLE_WIDTH_3)
		screen.setTableColumnHeader(szTable, 4, "", self.TABLE_WIDTH_4)
		screen.setTableColumnHeader(szTable, 5, "", self.TABLE_WIDTH_5)
		screen.appendTableRow(szTable)

		szTeamName = CyTeam.getName()

		for iLoopVC in xrange(GC.getNumVictoryInfos()):
			victory = GC.getVictoryInfo(iLoopVC)
			CvVictoryInfo = GC.getVictoryInfo(iLoopVC)
			if GAME.isVictoryValid(iLoopVC):

				iNumRows = screen.getTableNumRows(szTable)
				szVictoryType = "<font=4b>" + CvVictoryInfo.getDescription().upper() + "</font>"
				if CvVictoryInfo.isEndScore() and GAME.getMaxTurns() > GAME.getElapsedGameTurns():
					szVictoryType += "    (" + TRNSLTR.getText("TXT_KEY_MISC_TURNS_LEFT", (GAME.getMaxTurns() - GAME.getElapsedGameTurns(), )) + ")"

				iVictoryTitleRow = iNumRows - 1
				screen.setTableText(szTable, 0, iVictoryTitleRow, szVictoryType, "", iWidGen, -1, -1, 1<<0)
				bSpaceshipFound = False

				bEntriesFound = False

				if CvVictoryInfo.isTargetScore() and GAME.getTargetScore():

					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_TARGET_SCORE", (GAME.getTargetScore(), )), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, szTeamName + ":", "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 3, iRow, (u"%d" % ourScore), "", iWidGen, -1, -1, 1<<0)

					if (iBestScoreTeam != -1):
						screen.setTableText(szTable, 4, iRow, GC.getTeam(iBestScoreTeam).getName() + ":", "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 5, iRow, (u"%d" % bestScore), "", iWidGen, -1, -1, 1<<0)

					bEntriesFound = True

				if CvVictoryInfo.isEndScore():

					szText1 = TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_HIGHEST_SCORE", (CyGameTextMgr().getTimeStr(GAME.getStartTurn() + GAME.getMaxTurns(), False), ))

					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, szText1, "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, szTeamName + ":", "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 3, iRow, (u"%d" % ourScore), "", iWidGen, -1, -1, 1<<0)

					if iBestScoreTeam != -1:
						screen.setTableText(szTable, 4, iRow, GC.getTeam(iBestScoreTeam).getName() + ":", "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 5, iRow, (u"%d" % bestScore), "", iWidGen, -1, -1, 1<<0)

					bEntriesFound = True

				if CvVictoryInfo.isConquest():
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_ELIMINATE_ALL", ()), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_RIVALS_LEFT", ()), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 3, iRow, unicode(nRivals), "", iWidGen, -1, -1, 1<<0)
					bEntriesFound = True
# BUG Additions Start
					if AdvisorOpt.isVictories():
						if nVassaled != 0:
							sString = TRNSLTR.getText("TXT_KEY_BUG_VICTORY_VASSALED", (nVassaled, ))
							screen.setTableText(szTable, 4, iRow, sString, "", iWidGen, -1, -1, 1<<0)
						if nRivals - nknown != 0:
							sString = TRNSLTR.getText("TXT_KEY_BUG_VICTORY_UNKNOWN", (nRivals - nknown, ))
							screen.setTableText(szTable, 5, iRow, sString, "", iWidGen, -1, -1, 1<<0)
# BUG Additions End

				if GAME.getAdjustedPopulationPercent(iLoopVC) > 0:
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_PERCENT_POP", (GAME.getAdjustedPopulationPercent(iLoopVC), )), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, szTeamName + ":", "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 3, iRow, (u"%.2f%%" % popPercent), "", iWidGen, -1, -1, 1<<0)
					if (iBestPopTeam != -1):
						screen.setTableText(szTable, 4, iRow, GC.getTeam(iBestPopTeam).getName() + ":", "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 5, iRow, (u"%.2f%%" % (bestPop * 100 / totalPop)), "", iWidGen, -1, -1, 1<<0)
					bEntriesFound = True


				if GAME.getAdjustedLandPercent(iLoopVC) > 0:
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_PERCENT_LAND", (GAME.getAdjustedLandPercent(iLoopVC), )), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, szTeamName + ":", "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 3, iRow, (u"%.2f%%" % landPercent), "", iWidGen, -1, -1, 1<<0)
					if (iBestLandTeam != -1):
						screen.setTableText(szTable, 4, iRow, GC.getTeam(iBestLandTeam).getName() + ":", "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 5, iRow, (u"%.2f%%" % (bestLand * 100 / totalLand)), "", iWidGen, -1, -1, 1<<0)
					bEntriesFound = True

				if CvVictoryInfo.getReligionPercent() > 0:
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_PERCENT_RELIGION", (CvVictoryInfo.getReligionPercent(), )), "", iWidGen, -1, -1, 1<<0)
					if iOurReligion != -1:
						screen.setTableText(szTable, 2, iRow, GC.getReligionInfo(iOurReligion).getDescription() + ":", "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 3, iRow, (u"%d%%" % ourReligionPercent), "", iWidGen, -1, -1, 1<<0)
					else:
						screen.setTableText(szTable, 2, iRow, szTeamName + ":", "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 3, iRow, u"No Holy City", "", iWidGen, -1, -1, 1<<0)
					if iBestReligion != -1:
						screen.setTableText(szTable, 4, iRow, GC.getReligionInfo(iBestReligion).getDescription() + ":", "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 5, iRow, (u"%d%%" % religionPercent), "", iWidGen, -1, -1, 1<<0)
					bEntriesFound = True

				if CvVictoryInfo.getTotalCultureRatio() > 0:
					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_PERCENT_CULTURE", (int((100.0 * bestCulture) / CvVictoryInfo.getTotalCultureRatio()), )), "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 2, iRow, szTeamName + ":", "", iWidGen, -1, -1, 1<<0)
					screen.setTableText(szTable, 3, iRow, unicode(ourCulture), "", iWidGen, -1, -1, 1<<0)
					if iBestLandTeam != -1:
						screen.setTableText(szTable, 4, iRow, GC.getTeam(iBestCultureTeam).getName() + ":", "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 5, iRow, unicode(bestCulture), "", iWidGen, -1, -1, 1<<0)
					bEntriesFound = True

				iBestBuildingTeam = -1
				bestBuilding = 0
				for iTeamX in xrange(GC.getMAX_PC_TEAMS()):
					if iTeamX == iActiveTeam: continue
					CyTeamX = GC.getTeam(iTeamX)
					if CyTeamX.isAlive() and not CyTeamX.isMinorCiv():
						if CyTeam.isHasMet(iTeamX) or GAME.isDebugMode():
							teamBuilding = 0
							for i in xrange(GC.getNumBuildingClassInfos()):
								if GC.getBuildingClassInfo(i).getVictoryThreshold(iLoopVC) > 0:
									teamBuilding += CyTeamX.getBuildingClassCount(i)
							if teamBuilding > bestBuilding:
								bestBuilding = teamBuilding
								iBestBuildingTeam = iTeamX

				for i in xrange(GC.getNumBuildingClassInfos()):
					if GC.getBuildingClassInfo(i).getVictoryThreshold(iLoopVC) > 0:
						iRow = screen.appendTableRow(szTable)
						szNumber = unicode(GC.getBuildingClassInfo(i).getVictoryThreshold(iLoopVC))
						screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_BUILDING", (szNumber, GC.getBuildingClassInfo(i).getTextKey())), "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 2, iRow, szTeamName + ":", "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 3, iRow, str(CyTeam.getBuildingClassCount(i)), "", iWidGen, -1, -1, 1<<0)
						if iBestBuildingTeam != -1:
							screen.setTableText(szTable, 4, iRow, GC.getTeam(iBestBuildingTeam).getName() + ":", "", iWidGen, -1, -1, 1<<0)
							screen.setTableText(szTable, 5, iRow, str(GC.getTeam(iBestBuildingTeam).getBuildingClassCount(i)), "", iWidGen, -1, -1, 1<<0)
						bEntriesFound = True

				iBestProjectTeam = -1
				bestProject = -1
				for iTeamX in xrange(GC.getMAX_PC_TEAMS()):
					if iTeamX == iActiveTeam: continue
					CyTeamX = GC.getTeam(iTeamX)
					if CyTeamX.isAlive() and not CyTeamX.isMinorCiv():
						if (CyTeam.isHasMet(iTeamX) or GAME.isDebugMode()) and self.isApolloBuiltbyTeam(CyTeamX):
							teamProject = 0
							for i in xrange(GC.getNumProjectInfos()):
								if GC.getProjectInfo(i).getVictoryThreshold(iLoopVC) > 0:
									teamProject += CyTeamX.getProjectCount(i)
							if teamProject > bestProject:
								bestProject = teamProject
								iBestProjectTeam = iTeamX

# BUG Additions Start
				if AdvisorOpt.isVictories():
					bApolloShown = False
					for i in xrange(GC.getNumProjectInfos()):
						CvProjectInfo = GC.getProjectInfo(i)
						iVictoryThreshold = CvProjectInfo.getVictoryThreshold(iLoopVC)
						if iVictoryThreshold > 0:
							if not self.isApolloBuilt():
								iRow = screen.appendTableRow(szTable)
								screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_PROJECT_APOLLO_PROGRAM", ()), "", iWidGen, -1, -1, 1<<0)
								screen.setTableText(szTable, 2, iRow, szTeamName + ":", "", iWidGen, -1, -1, 1<<0)
								screen.setTableText(szTable, 3, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_NOT_BUILT", ()), "", iWidGen, -1, -1, 1<<0)
								bEntriesFound = True
								break
							else:
								bApolloBuiltByActiveTeam = self.isApolloBuiltbyTeam(CyTeam)
								if not bApolloShown:
									bApolloShown = True
									iRow = screen.appendTableRow(szTable)
									screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_PROJECT_APOLLO_PROGRAM", ()), "", iWidGen, -1, -1, 1<<0)

									if bApolloBuiltByActiveTeam:
										screen.setTableText(szTable, 2, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_BUILT", (szTeamName, )), "", iWidGen, -1, -1, 1<<0)
									else:
										screen.setTableText(szTable, 2, iRow, szTeamName + ":", "", iWidGen, -1, -1, 1<<0)
										screen.setTableText(szTable, 3, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_NOT_BUILT", ()), "", iWidGen, -1, -1, 1<<0)

									if iBestProjectTeam != -1:
										screen.setTableText(szTable, 4, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_BUILT", (GC.getTeam(iBestProjectTeam).getName(), )), "", iWidGen, -1, -1, 1<<0)

								iRow = screen.appendTableRow(szTable)
								iReqTech = CvProjectInfo.getTechPrereq()

								if CvProjectInfo.getVictoryMinThreshold(iLoopVC) == iVictoryThreshold:
									szNumber = unicode(iVictoryThreshold)
								else:
									szNumber = unicode(CvProjectInfo.getVictoryMinThreshold(iLoopVC)) + u"-" + unicode(iVictoryThreshold)

								sSSPart = TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_BUILDING", (szNumber, CvProjectInfo.getTextKey()))
								screen.setTableText(szTable, 0, iRow, sSSPart, "", iWidGen, -1, -1, 1<<0)

								if bApolloBuiltByActiveTeam:
									bOwnProject = CyTeam.getProjectCount(i)

									bHasTech = CyTeam.isHasTech(iReqTech)
									sSSPlayer = szTeamName + ":"
									sSSCount = "%i [+%i]" % (bOwnProject, CyTeam.getProjectMaking(i))

									iHasTechColor = -1
									iSSColor = 0
									if bOwnProject == iVictoryThreshold:
										sSSCount = "%i" % (bOwnProject)
										iSSColor = ColorUtil.keyToType("COLOR_GREEN")
									elif bOwnProject >= CvProjectInfo.getVictoryMinThreshold(iLoopVC):
										iSSColor = ColorUtil.keyToType("COLOR_YELLOW")

									if iSSColor > 0:
										sSSPlayer = TRNSLTR.changeTextColor(sSSPlayer, iSSColor)
										sSSCount = TRNSLTR.changeTextColor(sSSCount, iSSColor)

									screen.setTableText(szTable, 2, iRow, sSSPlayer, "", iWidGen, -1, -1, 1<<0)
									if bHasTech:
										screen.setTableText(szTable, 3, iRow, sSSCount, "", iWidGen, -1, -1, 1<<0)

									#check if spaceship
									if CvProjectInfo.isSpaceship():
										bSpaceshipFound = True

								# add AI space ship info
								if iBestProjectTeam != -1:
									pTeam = GC.getTeam(iBestProjectTeam)
									bOwnProject = pTeam.getProjectCount(i)
									sSSPlayer = GC.getTeam(iBestProjectTeam).getName() + ":"
									sSSCount = "%i" % (bOwnProject)

									Techs = TechUtil.getVisibleKnownTechs(pTeam.getLeaderID(), iActivePlayer)
									bHasTech = iReqTech in Techs

									iHasTechColor = -1
									iSSColor = 0
									if bOwnProject == iVictoryThreshold:
										iSSColor = ColorUtil.keyToType("COLOR_GREEN")
									elif bOwnProject >= CvProjectInfo.getVictoryMinThreshold(iLoopVC):
										iSSColor = ColorUtil.keyToType("COLOR_YELLOW")
									elif bHasTech:
										iSSColor = ColorUtil.keyToType("COLOR_PLAYER_ORANGE")

									if iSSColor > 0:
										sSSPlayer = TRNSLTR.changeTextColor(sSSPlayer, iSSColor)
										sSSCount = TRNSLTR.changeTextColor(sSSCount, iSSColor)

									screen.setTableText(szTable, 4, iRow, sSSPlayer, "", iWidGen, -1, -1, 1<<0)
									screen.setTableText(szTable, 5, iRow, sSSCount, "", iWidGen, -1, -1, 1<<0)

								bEntriesFound = True

				else: # vanilla BtS SShip display
					for i in xrange(GC.getNumProjectInfos()):
						CvProjectInfo = GC.getProjectInfo(i)
						iVictoryThreshold = CvProjectInfo.getVictoryThreshold(iLoopVC)
						if iVictoryThreshold > 0:
							iRow = screen.appendTableRow(szTable)
							if CvProjectInfo.getVictoryMinThreshold(iLoopVC) == iVictoryThreshold:
								szNumber = unicode(iVictoryThreshold)
							else:
								szNumber = unicode(CvProjectInfo.getVictoryMinThreshold(iLoopVC)) + "-" + unicode(iVictoryThreshold)
							screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_BUILDING", (szNumber, CvProjectInfo.getTextKey())), "", iWidGen, -1, -1, 1<<0)
							screen.setTableText(szTable, 2, iRow, szTeamName + ":", "", iWidGen, -1, -1, 1<<0)
							screen.setTableText(szTable, 3, iRow, str(CyTeam.getProjectCount(i)), "", iWidGen, -1, -1, 1<<0)

							#check if spaceship
							if CvProjectInfo.isSpaceship():
								bSpaceshipFound = True

							if iBestProjectTeam != -1:
								screen.setTableText(szTable, 4, iRow, GC.getTeam(iBestProjectTeam).getName() + ":", "", iWidGen, -1, -1, 1<<0)
								screen.setTableText(szTable, 5, iRow, unicode(GC.getTeam(iBestProjectTeam).getProjectCount(i)), "", iWidGen, -1, -1, 1<<0)

							bEntriesFound = True
# BUG Additions End

				#add spaceship button
				if bSpaceshipFound:
					screen.setButtonGFC("SpaceShipButton" + str(iLoopVC), TRNSLTR.getText("TXT_KEY_GLOBELAYER_STRATEGY_VIEW", ()), "", 0, 0, 15, 10, iWidGen, self.SPACESHIP_SCREEN_BUTTON, -1, ButtonStyles.BUTTON_STYLE_STANDARD )
					screen.attachControlToTableCell("SpaceShipButton" + str(iLoopVC), szTable, iVictoryTitleRow, 1)

					victoryDelay = GC.getTeam(iActiveTeam).getVictoryCountdown(iLoopVC)
					if victoryDelay > 0 and GAME.getGameState() != GameStateTypes.GAMESTATE_EXTENDED:
						victoryDate = CyGameTextMgr().getTimeStr(GAME.getGameTurn() + victoryDelay, False)
						screen.setTableText(szTable, 2, iVictoryTitleRow, TRNSLTR.getText("TXT_KEY_SPACE_SHIP_SCREEN_ARRIVAL", ()) + ":", "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 3, iVictoryTitleRow, victoryDate, "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 4, iVictoryTitleRow, TRNSLTR.getText("TXT_KEY_REPLAY_SCREEN_TURNS", ()) + ":", "", iWidGen, -1, -1, 1<<0)
						screen.setTableText(szTable, 5, iVictoryTitleRow, str(victoryDelay), "", iWidGen, -1, -1, 1<<0)

				if CvVictoryInfo.isDiploVote() and not GAME.isOption(GameOptionTypes.GAMEOPTION_UNITED_NATIONS):
					for (iVoteBuildingClass, iUNTeam, bUnknown) in aiVoteBuildingClass:
						iRow = screen.appendTableRow(szTable)
						screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_ELECTION", (GC.getBuildingClassInfo(iVoteBuildingClass).getTextKey(), )), "", iWidGen, -1, -1, 1<<0)
						if iUNTeam != -1:
							if bUnknown:
								szName = TRNSLTR.getText("TXT_KEY_TOPCIVS_UNKNOWN", ())
							else:
								szName = GC.getTeam(iUNTeam).getName()
							screen.setTableText(szTable, 2, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_BUILT", (szName, )), "", iWidGen, -1, -1, 1<<0)
						else:
							screen.setTableText(szTable, 2, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_NOT_BUILT", ()), "", iWidGen, -1, -1, 1<<0)
						bEntriesFound = True

				if CvVictoryInfo.getCityCulture() != CultureLevelTypes.NO_CULTURELEVEL and CvVictoryInfo.getNumCultureCities() > 0:
					ourBestCities = self.getListCultureCities(iActivePlayer, CvVictoryInfo)[0:CvVictoryInfo.getNumCultureCities()]

					iBestCulturePlayer = -1
					bestCityCulture = 0
					maxCityCulture = GameUtil.getCultureThreshold(CvVictoryInfo.getCityCulture())

					for iPlayerX in xrange(GC.getMAX_PLAYERS()):
						CyPlayerX = GC.getPlayer(iPlayerX)
						if CyPlayerX.isAlive() and not CyPlayerX.isMinorCiv() and not CyPlayerX.isNPC():
							if iPlayerX != iActivePlayer and (CyTeam.isHasMet(CyPlayerX.getTeam()) or GAME.isDebugMode()):
								theirBestCities = self.getListCultureCities(iPlayerX, CvVictoryInfo)[0:CvVictoryInfo.getNumCultureCities()]

								iTotalCulture = 0
								for loopCity in theirBestCities:
									if loopCity[0] >= maxCityCulture:
										iTotalCulture += maxCityCulture
									else:
										iTotalCulture += loopCity[0]

								if iTotalCulture >= bestCityCulture:
									bestCityCulture = iTotalCulture
									iBestCulturePlayer = iPlayerX

					if iBestCulturePlayer != -1:
						theirBestCities = self.getListCultureCities(iBestCulturePlayer, CvVictoryInfo)[0:(CvVictoryInfo.getNumCultureCities())]
					else:
						theirBestCities = []

					iRow = screen.appendTableRow(szTable)
					screen.setTableText(szTable, 0, iRow, TRNSLTR.getText("TXT_KEY_VICTORY_SCREEN_CITY_CULTURE", (CvVictoryInfo.getNumCultureCities(), GC.getCultureLevelInfo(CvVictoryInfo.getCityCulture()).getTextKey())), "", iWidGen, -1, -1, 1<<0)

					for i in xrange(CvVictoryInfo.getNumCultureCities()):
						if len(ourBestCities) > i:
							screen.setTableText(szTable, 2, iRow, ourBestCities[i][1].getName() + ":", "", iWidGen, -1, -1, 1<<0)
# BUG Additions Start
							if AdvisorOpt.isVictories():
								if ourBestCities[i][2] == -1:
									sString = "%i (-)" % (ourBestCities[i][0])
								elif ourBestCities[i][2] > 100:
									sString = "%i (100+)" % (ourBestCities[i][0])
								elif ourBestCities[i][2] < 1:
									sString = "%i (L)" % (ourBestCities[i][0])
								else:
									sString = "%i (%i)" % (ourBestCities[i][0], ourBestCities[i][2])
							else:
								sString = "%i" % (ourBestCities[i][0])

							screen.setTableText(szTable, 3, iRow, sString, "", iWidGen, -1, -1, 1<<0)
# BUG Additions End

						if len(theirBestCities) > i:
							screen.setTableText(szTable, 4, iRow, theirBestCities[i][1].getName() + ":", "", iWidGen, -1, -1, 1<<0)

# BUG Additions Start
							if AdvisorOpt.isVictories():
								if theirBestCities[i][2] == -1:
									sString = "%i (-)" % (theirBestCities[i][0])
								elif theirBestCities[i][2] > 100:
									sString = "%i (100+)" % (theirBestCities[i][0])
								elif theirBestCities[i][2] < 1:
									sString = "%i (L)" % (theirBestCities[i][0])
								else:
									sString = "%i (%i)" % (theirBestCities[i][0], theirBestCities[i][2])
							else:
								sString = "%i" % (theirBestCities[i][0])

							screen.setTableText(szTable, 5, iRow, sString, "", iWidGen, -1, -1, 1<<0)
# BUG Additions End

						if i < CvVictoryInfo.getNumCultureCities()-1:
							iRow = screen.appendTableRow(szTable)
					bEntriesFound = True

				if bEntriesFound:
					screen.appendTableRow(szTable)
					screen.appendTableRow(szTable)

		# civ picker dropdown
		if CyGame().isDebugMode():
			self.szDropdownName = self.DEBUG_DROPDOWN_ID
			screen.addDropDownBoxGFC(self.szDropdownName, 22, 12, 300, iWidGen, -1, -1, FontTypes.GAME_FONT)
			for j in xrange(GC.getMAX_PLAYERS()):
				if GC.getPlayer(j).isAlive():
					screen.addPullDownString(self.szDropdownName, GC.getPlayer(j).getName(), j, j, False )

		self.drawTabs()


	def getListCultureCities(self, iPlayer, CvVictoryInfo):

		if iPlayer != -1:
			CyPlayer = GC.getPlayer(iPlayer)
			if CyPlayer.isAlive():
				iThreshold = GameUtil.getCultureThreshold(CvVictoryInfo.getCityCulture())
				aList = []

				CyCity, i = CyPlayer.firstCity(False)
				while CyCity:
					iRate = CyCity.getCommerceRateTimes100(CommerceTypes.COMMERCE_CULTURE)
					if not iRate:
						iTurns = -1
					else:
						iCultureLeftTimes100 = 100 * iThreshold - CyCity.getCultureTimes100(CyCity.getOwner())
						iTurns = int((iCultureLeftTimes100 + iRate - 1) / iRate)
					aList.append((CyCity.getCulture(iPlayer), CyCity, iTurns))
					CyCity, i = CyPlayer.nextCity(i, False)

				aList.sort()
				aList.reverse()
				return aList
		return []

# Sevo--VCM
	def getListCultureCitiesTeam(self, iTeam):
		aList = []

		for iPlayerX in xrange(GC.getMAX_PLAYERS()):
			CyPlayerX = GC.getPlayer(iPlayerX)
			if CyPlayerX.isAlive() and CyPlayerX.getTeam() == iTeam:
				CyCity, i = CyPlayerX.firstCity(False)
				while CyCity:
					aList.append((CyCity.getCulture(iPlayerX), CyCity))
					CyCity, i = CyPlayerX.nextCity(i, False)

		if aList:
			aList.sort()
			aList.reverse()
			return aList
		return []


	def getLegendaryCities(self, iTeam):
		iLegendaryCities = 0
		iTeamCities = 0
		iThreshold = GC.getCultureLevelInfo(GC.getNumCultureLevelInfos()-1).getSpeedThreshold(GC.getGame().getGameSpeedType())

		for iPlayerX in xrange(GC.getMAX_PLAYERS()):
			CyPlayerX = GC.getPlayer(iPlayerX)
			if CyPlayerX.isAlive():
				iTeamX = CyPlayerX.getTeam()
				if iTeamX == iTeam:
					bTeam = True
				else:
					bTeam = False
				CyCity, i = CyPlayerX.firstCity(False)
				while CyCity:
					if CyCity.getCulture(iPlayerX) > iThreshold:
						iLegendaryCities += 1
						if bTeam:
							iTeamCities += 1
					CyCity, i = CyPlayerX.nextCity(i, False)

		return [iTeamCities, iLegendaryCities]

# END VCM

# BUG Additions Start
	def getVotesForWhichCandidate(self, iPlayer, iCand1, iCand2, iVote):
		# returns are 1 = vote for candidate 1
		#             2 = vote for candidate 2
		#            -1 = abstain

		# iVote = 1 means vote for SecGen or Pope
		# iVote = 2 means vote for diplomatic victory

		# candidates are teams!!!

		# * AI votes for itself if it can
		# * AI votes for a team member if it can
		# * AI votes for its master, if it is a vassal
		# * if the AI attitude to one of the candidates is 'friendly' and the other is 'pleased' or less, AI votes for 'friend'
		# * if both candidates are at 'friendly' status, votes for one with highest attitude
		# * if neither candidate is at 'friendly', abstains

		iPTeam = GC.getPlayer(iPlayer).getTeam()
		iPCand1 = self.getPlayerOnTeam(iCand1)
		iPCand2 = self.getPlayerOnTeam(iCand2)

		# * player votes for its own team if it can
		if iPTeam == iCand1: return 1
		if iPTeam == iCand2: return 2

		# if player is human, votes for self or abstains
		if iPlayer == self.iActivePlayer: return -1

		# * AI votes for its master, if it is a vassal
		if GC.getTeam(iPTeam).isVassal(iCand1): return 1
		if GC.getTeam(iPTeam).isVassal(iCand2): return 2

		# get player category (friendly) to candidates
		iC1Cat = AttitudeUtil.getAttitudeCategory(iPlayer, iPCand1)
		iC2Cat = AttitudeUtil.getAttitudeCategory(iPlayer, iPCand2)

		# the cut-off for SecGen votes is pleased (3)
		# the cut-off for Diplo victory votes is friendly (4)
		if iVote == 1:  # vote for SecGen or Pope
			iCutOff = 3
		else:
			iCutOff = 4

		# * if neither candidate is at 'friendly', abstains
		# assumes friendly = 4, pleased = 3, etc
		if (iC1Cat < iCutOff
		and iC2Cat < iCutOff):
			return -1

		# * if the AI attitude to one of the candidates is 'friendly' and the other is 'pleased' or less, AI votes for 'friend'
		if (iC1Cat >= iCutOff
		and iC1Cat > iC2Cat):
			return 1

		if (iC2Cat >= iCutOff
		and iC2Cat > iC1Cat):
			return 2

		# if the code gets to here, then both candidates are at or above the cutoff
		# and they are both at the same category (ie both friendly)
		# need to decide on straight attitude (visible only)

		# get player attitude to candidates
		iC1Att = AttitudeUtil.getAttitudeCount(iPlayer, iPCand1)
		iC2Att = AttitudeUtil.getAttitudeCount(iPlayer, iPCand2)

		# * if both candidates are at 'friendly' status, votes for one with highest attitude
		if iC2Att < iC1Att: # ties go to Candidate #1
			return 1
		else:
			return 2

		return -1

	def getPlayerOnTeam(self, iTeam):
		for i in xrange(GC.getMAX_PLAYERS()):
			if iTeam == GC.getPlayer(i).getTeam():
				return i

		return -1

	def getAP_UN_OwnerTeam(self):
		for i in xrange(GC.getNumBuildingInfos()):
			CvBuildingInfo = GC.getBuildingInfo(i)
			for j in xrange(GC.getNumVoteSourceInfos()):
				if CvBuildingInfo.getVoteSourceType() == j:
					for iPlayerX in xrange(GC.getMAX_PC_PLAYERS()):
						CyPlayerX = GC.getPlayer(iPlayerX)
						if CyPlayerX.isAlive() and not CyPlayerX.isMinorCiv() and CyPlayerX.countNumBuildings(i):
							return CyPlayerX.getTeam()
		return -1

	def canBuildSSComponent(self, vTeam, vComponent):
		if(not vTeam.isHasTech(vComponent.getTechPrereq())):
			return False
		else:
			for j in xrange(GC.getNumProjectInfos()):
				if(vTeam.getProjectCount(j) < vComponent.getProjectsNeeded(j)):
					return False
		return True

	def isApolloBuilt(self):
		iTeam = GC.getPlayer(self.iActivePlayer).getTeam()
		CyTeam = GC.getTeam(iTeam)

		# check if anyone has built the apollo project (PROJECT_APOLLO_PROGRAM)
		for iTeamX in xrange(GC.getMAX_PC_TEAMS()):
			CyTeamX = GC.getTeam(iTeamX)
			if CyTeamX.isAlive() and not CyTeamX.isMinorCiv():
				if iTeamX == iTeam:
					bContact = True
				elif CyTeam.isHasMet(iTeamX) or GC.getGame().isDebugMode():
					bContact = True
				else:
					bContact = False

				if bContact and self.isApolloBuiltbyTeam(CyTeamX):
					return True
		return False

	def isApolloBuiltbyTeam(self, CyTeam):
		iTeam = CyTeam.getID()

		if iTeam in self.ApolloTeamsChecked:
			sString = "1: %s" % (self.ApolloTeamCheckResult[iTeam])

		for i in xrange(GC.getNumProjectInfos()):
			component = GC.getProjectInfo(i)
			if component.isSpaceship():
				bApollo = True
				for j in xrange(GC.getNumProjectInfos()):
					if CyTeam.getProjectCount(j) < component.getProjectsNeeded(j):
						bApollo = False
				if bApollo:
					self.ApolloTeamCheckResult[iTeam] = True
					self.ApolloTeamsChecked.add(iTeam)
					return True
				break

		self.ApolloTeamCheckResult[iTeam] = False
		self.ApolloTeamsChecked.add(iTeam)
		return False
# BUG Additions End

	# returns a unique ID for a widget in this screen
	def getNextWidgetName(self):
		szName = self.WIDGET_ID + str(self.nWidgetCount)
		self.nWidgetCount += 1
		return szName

	def deleteAllWidgets(self):
		screen = self.getScreen()
		i = self.nWidgetCount - 1
		while (i >= 0):
			self.nWidgetCount = i
			screen.deleteWidget(self.getNextWidgetName())
			i -= 1

		self.nWidgetCount = 0

		screen.deleteWidget(self.Vote_Pope_ID)
		screen.deleteWidget(self.Vote_DipVic_ID)
		screen.deleteWidget(self.Vote_AP_ID)
		screen.deleteWidget(self.Vote_UN_ID)

	# handle the input for this screen...
	def handleInput (self, inputClass):
		sWidget = inputClass.getFunctionName()
		if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_LISTBOX_ITEM_SELECTED):
			if (sWidget == self.DEBUG_DROPDOWN_ID):
				szName = self.DEBUG_DROPDOWN_ID
				iIndex = self.getScreen().getSelectedPullDownID(szName)
				self.iActivePlayer = self.getScreen().getPullDownData(szName, iIndex)
				self.iScreen = VICTORY_CONDITION_SCREEN
				self.showVictoryConditionScreen()
		elif (inputClass.getNotifyCode() == NotifyCode.NOTIFY_CLICKED):
			if (sWidget == self.VC_TAB_ID):
				self.iScreen = VICTORY_CONDITION_SCREEN
				self.showVictoryConditionScreen()
			elif (sWidget == self.SETTINGS_TAB_ID):
				self.iScreen = GAME_SETTINGS_SCREEN
				self.showGameSettingsScreen()
			elif (sWidget == self.UN_RESOLUTION_TAB_ID):
				self.iScreen = UN_RESOLUTION_SCREEN
				self.showVotingScreen()
			elif (sWidget == self.UN_MEMBERS_TAB_ID):
				self.iScreen = UN_MEMBERS_SCREEN
				self.showMembersScreen()

			elif (sWidget == self.Vote_Pope_ID and self.VoteType == 2):
				self.VoteType = 1
				self.iScreen = UN_MEMBERS_SCREEN
				self.showMembersScreen()

			elif (sWidget == self.Vote_DipVic_ID and self.VoteType == 1):
				self.VoteType = 2
				self.iScreen = UN_MEMBERS_SCREEN
				self.showMembersScreen()

			elif (sWidget == self.Vote_AP_ID and self.VoteBody == 2):
				self.VoteBody = 1
				self.iScreen = UN_MEMBERS_SCREEN
				self.showMembersScreen()

			elif (sWidget == self.Vote_UN_ID and self.VoteBody == 1):
				self.VoteBody = 2
				self.iScreen = UN_MEMBERS_SCREEN
				self.showMembersScreen()

			elif (inputClass.getData1() == self.SPACESHIP_SCREEN_BUTTON):
				#close screen
				screen = self.getScreen()
				screen.setDying(True)
				CyInterface().clearSelectedCities()

				#popup spaceship screen
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_PYTHON_SCREEN)
				popupInfo.setData1(-1)
				popupInfo.setText(u"showSpaceShip")
				popupInfo.addPopup(self.iActivePlayer)

	def update(self, fDelta):
		return

#Sevo--VCM
	def getTeamWonderScore(self, iTeam):
		teamWonderScore = 0

		for iPlayerX in xrange(GC.getMAX_PC_PLAYERS()):
			CyPlayerX = GC.getPlayer(iPlayerX)
			if CyPlayerX.isAlive() and not CyPlayerX.isMinorCiv() and CyPlayerX.getTeam() == iTeam:
				teamWonderScore += CyPlayerX.getSevoWondersScore(0)
		return teamWonderScore


	def getTeamTotalCulture(self, iTeam):
		teamCulture = 0

		for iPlayerX in xrange(GC.getMAX_PC_PLAYERS()):
			CyPlayerX = GC.getPlayer(iPlayerX)
			if CyPlayerX.isAlive() and not CyPlayerX.isMinorCiv() and CyPlayerX.getTeam() == iTeam:
				teamCulture += CyPlayerX.countTotalCulture()
		return teamCulture


	def teamLaunchedShip(self, iTeam):
		for iPlayerX in xrange(GC.getMAX_PC_PLAYERS()):
			CyPlayerX = GC.getPlayer(iPlayerX)
			if CyPlayerX.isAlive() and not CyPlayerX.isMinorCiv() and CyPlayerX.getTeam() == iTeam:
				if GC.getGame().getStarshipLaunched(iPlayerX):
					return 1
		return -1
