# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005

#
# Sevopedia 2.3
#   sevotastic.blogspot.com
#   sevotastic@yahoo.com
#
# additional work by Gaurav, Progor, Ket, Vovan, Fitchn, LunarMongoose
# see ReadMe for details
#

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import SevoScreenEnums

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaHero:

	def __init__(self, main):
		self.iHero = -1
		self.top = main
		
		self.X_UNIT_PANE = self.top.X_PEDIA_PAGE
		self.Y_UNIT_PANE = self.top.Y_PEDIA_PAGE
		self.W_UNIT_PANE = 255
		self.H_UNIT_PANE = 255

		self.W_ICON = 240
		self.H_ICON = 240
		self.X_ICON = self.X_UNIT_PANE + (self.W_UNIT_PANE - self.W_ICON) / 2
		self.Y_ICON = self.Y_UNIT_PANE + (self.H_UNIT_PANE - self.H_ICON) / 2 + 3

		self.ICON_SIZE = 64
		self.BUTTON_SIZE = 64
		self.PROMOTION_ICON_SIZE = 32

		self.X_UNIT_ANIMATION = self.X_UNIT_PANE + self.W_UNIT_PANE + 10
		self.W_UNIT_ANIMATION = self.top.R_PEDIA_PAGE - self.X_UNIT_ANIMATION
		self.Y_UNIT_ANIMATION = self.Y_UNIT_PANE + 7
		self.H_UNIT_ANIMATION = 119
		self.X_ROTATION_UNIT_ANIMATION = -20
		self.Z_ROTATION_UNIT_ANIMATION = 30
		self.SCALE_ANIMATION = 1.0

		self.X_STATS_PANE = self.X_UNIT_ANIMATION
		self.Y_STATS_PANE = self.Y_UNIT_ANIMATION + self.H_UNIT_ANIMATION + 10
		self.W_STATS_PANE = 150
		self.H_STATS_PANE = 119

		self.X_CIV_PANE = self.X_STATS_PANE + self.W_STATS_PANE + 10
		self.Y_CIV_PANE = self.Y_STATS_PANE
		self.W_CIV_PANE = self.W_UNIT_ANIMATION - 250
		self.H_CIV_PANE = 119

		self.X_BELIEF_PANE = self.X_CIV_PANE + self.W_CIV_PANE + 10
		self.Y_BELIEF_PANE = self.Y_CIV_PANE
		self.W_BELIEF_PANE = self.W_UNIT_ANIMATION - self.W_CIV_PANE - self.W_STATS_PANE - 20
		self.H_BELIEF_PANE = 119

		self.X_UNITCOMBAT_PANE = self.X_UNIT_PANE
		self.Y_UNITCOMBAT_PANE = self.Y_UNIT_PANE + self.H_UNIT_PANE + 10
		self.W_UNITCOMBAT_PANE = 280
		self.H_UNITCOMBAT_PANE = 110

		self.X_SPECIAL_PANE = self.X_UNIT_PANE
		self.Y_SPECIAL_PANE = self.Y_UNITCOMBAT_PANE + self.H_UNITCOMBAT_PANE + 10
		self.W_SPECIAL_PANE = 280
		self.H_SPECIAL_PANE = 110

		self.X_PROMO_PANE = self.X_UNIT_PANE
		self.Y_PROMO_PANE = self.Y_SPECIAL_PANE + self.H_SPECIAL_PANE + 10
		self.W_PROMO_PANE = 280
		self.H_PROMO_PANE = self.top.B_PEDIA_PAGE - self.Y_PROMO_PANE

		self.X_HISTORY_PANE = self.X_UNITCOMBAT_PANE + self.W_UNITCOMBAT_PANE + 10
		self.Y_HISTORY_PANE = self.Y_UNITCOMBAT_PANE
		self.W_HISTORY_PANE = self.top.R_PEDIA_PAGE - self.X_HISTORY_PANE
		self.H_HISTORY_PANE = self.top.B_PEDIA_PAGE - self.Y_HISTORY_PANE



	def interfaceScreen(self, iHero):
		self.iHero = iHero
		screen = self.top.getScreen()

		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_UNIT_PANE, self.Y_UNIT_PANE, self.W_UNIT_PANE, self.H_UNIT_PANE, PanelStyles.PANEL_STYLE_BLUE50)
##		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getHeroInfo(self.iHero).getPortrait(), self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addUnitGraphicGFC(self.top.getNextWidgetName(), gc.getHeroInfo(self.iHero).getUnitType(), self.X_UNIT_ANIMATION, self.Y_UNIT_ANIMATION, self.W_UNIT_ANIMATION, self.H_UNIT_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_UNIT_ANIMATION, self.Z_ROTATION_UNIT_ANIMATION, self.SCALE_ANIMATION, True)

		self.placeStatsAndCivAndBelief()
		self.placeUnitCombatLevel()
		self.placeSpecial()
		self.placePromotions()
		self.placeHistory()



##	def placeStats(self):
##		screen = self.top.getScreen()
##		panelName = self.top.getNextWidgetName()
##		iCombatType = gc.getUnitInfo(gc.getHeroInfo(self.iHero).getUnitType()).getUnitCombatType()
##		if (iCombatType != -1):
##			screen.setImageButton(self.top.getNextWidgetName(), gc.getUnitCombatInfo(iCombatType).getButton(), self.X_STATS_PANE, self.Y_STATS_PANE - 35, 32, 32, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iCombatType, 0)
##			screen.setText(self.top.getNextWidgetName(), "", u"<font=3>" + gc.getUnitCombatInfo(iCombatType).getDescription() + u"</font>", CvUtil.FONT_LEFT_JUSTIFY, self.X_STATS_PANE + 37, self.Y_STATS_PANE - 30, 0, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, iCombatType, 0)
##		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
##		screen.enableSelect(panelName, False)
##		if (gc.getUnitInfo(gc.getHeroInfo(self.iHero).getUnitType()).getAirCombat() > 0 and gc.getUnitInfo(gc.getHeroInfo(self.iHero).getUnitType()).getCombat() == 0):
##			iStrength = gc.getUnitInfo(gc.getHeroInfo(self.iHero).getUnitType()).getAirCombat()
##		else:
##			iStrength = gc.getUnitInfo(gc.getHeroInfo(self.iHero).getUnitType()).getCombat()
##		szName = self.top.getNextWidgetName()
##		szStrength = localText.getText("TXT_KEY_PEDIA_STRENGTH", (iStrength,))
##		screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szStrength.upper() + u"%c" % CyGame().getSymbolID(FontSymbols.STRENGTH_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
##		szName = self.top.getNextWidgetName()
##		szMovement = localText.getText("TXT_KEY_PEDIA_MOVEMENT", (gc.getUnitInfo(gc.getHeroInfo(self.iHero).getUnitType()).getMoves(),))
##		screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szMovement.upper() + u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
##		if (gc.getUnitInfo(gc.getHeroInfo(self.iHero).getUnitType()).getProductionCost() >= 0 and not gc.getUnitInfo(gc.getHeroInfo(self.iHero).getUnitType()).isFound()):
##			szName = self.top.getNextWidgetName()
##			if self.top.iActivePlayer == -1:
##				szCost = localText.getText("TXT_KEY_PEDIA_COST", ((gc.getUnitInfo(gc.getHeroInfo(self.iHero).getUnitType()).getProductionCost() * gc.getDefineINT("UNIT_PRODUCTION_PERCENT"))/100,))
##			else:
##				szCost = localText.getText("TXT_KEY_PEDIA_COST", (gc.getActivePlayer().getUnitProductionNeeded(gc.getHeroInfo(self.iHero).getUnitType()),))
##			screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szCost.upper() + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_PRODUCTION).getChar() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
##		if (gc.getUnitInfo(gc.getHeroInfo(self.iHero).getUnitType()).getAirRange() > 0):
##			szName = self.top.getNextWidgetName()
##			szRange = localText.getText("TXT_KEY_PEDIA_RANGE", (gc.getUnitInfo(gc.getHeroInfo(self.iHero).getUnitType()).getAirRange(),))
##			screen.appendListBoxStringNoUpdate(panelName, u"<font=4>" + szRange.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
##		screen.updateListBox(panelName)


	def placeStatsAndCivAndBelief(self):
		screen = self.top.getScreen()

		# Stats
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_STATS", ()), "", False, True, self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		screen.setTextAt(self.top.getNextWidgetName(), panelName, localText.changeTextColor(gc.getHeroInfo(self.iHero).getDescription(), gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT")), CvUtil.FONT_CENTER_JUSTIFY, 5, 5, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setTextAt(self.top.getNextWidgetName(), panelName, localText.getText("TXT_KEY_RECRUIT_HERO_LEADERSHIP", (gc.getHeroInfo(self.iHero).getLeadership(), )), CvUtil.FONT_CENTER_JUSTIFY, 5, 25, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setTextAt(self.top.getNextWidgetName(), panelName, localText.getText("TXT_KEY_RECRUIT_HERO_MIGHT", (gc.getHeroInfo(self.iHero).getMight(), )), CvUtil.FONT_CENTER_JUSTIFY, 5, 45, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		
		# Historical Civilizations
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_DEFAULT_CIVILIZATION", ()), "", False, True, self.X_CIV_PANE, self.Y_CIV_PANE, self.W_CIV_PANE, self.H_CIV_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		
		HistoricalCivs = {}
		for i in range (gc.getNumCivilizationInfos()):
			if gc.getHeroInfo(self.iHero).getDefaultCivilizationEndYear(i) > 0:
				HistoricalCivs[gc.getHeroInfo(self.iHero).getDefaultCivilizationEndYear(i)] = i

		TempList = HistoricalCivs.keys()
		TempList.sort()

		iCount = 0
		iIncrement = 9
		iButtonSize = 64
		for iValue in TempList:
			screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getCivilizationInfo(HistoricalCivs[iValue]).getButton(), iIncrement * (iCount + 1) + iButtonSize * iCount, 5, iButtonSize, iButtonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_CIV, HistoricalCivs[iValue], 1)
			iXIncrement = 2
			if iCount > 0:
				szText = str(gc.getHeroInfo(self.iHero).getCivilizationLoyalty(HistoricalCivs[iValue]))
				iXIncrement = 30
			else:
				szText = localText.getText("TXT_KEY_PEDIA_HERO_CIV_LOYALTY", (gc.getHeroInfo(self.iHero).getCivilizationLoyalty(HistoricalCivs[iValue]), ))
			#szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"))
			screen.setTextAt(self.top.getNextWidgetName(), panelName, szText, CvUtil.FONT_CENTER_JUSTIFY, iIncrement * iCount + iButtonSize * iCount + iXIncrement, iButtonSize + 5, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			iCount += 1

		# Belief
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_HERO_BELIEF", ()), "", False, True, self.X_BELIEF_PANE, self.Y_BELIEF_PANE, self.W_BELIEF_PANE, self.H_BELIEF_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")

		iBelief = gc.getHeroInfo(self.iHero).getBelief()
		if iBelief != -1:
			screen.setImageButtonAt(self.top.getNextWidgetName(), panelName, gc.getReligionInfo(iBelief).getButton(), (self.W_BELIEF_PANE - iButtonSize) / 2, 5, iButtonSize, iButtonSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_RELIGION, iBelief, -1)
			szText = localText.getText("TXT_KEY_PEDIA_HERO_BELIEF_STRENGTH", (gc.getHeroInfo(self.iHero).getBeliefStrength(), ))
			#szText = localText.changeTextColor(szText, gc.getInfoTypeForString("COLOR_HIGHLIGHT_TEXT"))
			screen.setTextAt(self.top.getNextWidgetName(), panelName, szText, CvUtil.FONT_CENTER_JUSTIFY, 2, iButtonSize  + 5, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			

	def placeUnitCombatLevel(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_HERO_UNITCOMBAT_LEVEL", ()), "", False, True, self.X_UNITCOMBAT_PANE, self.Y_UNITCOMBAT_PANE, self.W_UNITCOMBAT_PANE, self.H_UNITCOMBAT_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		
		iY_Text = 62
		if CyGame().getCurrentLanguage() == 5:
			iY_Text = 55
		screen.setText(self.top.getNextWidgetName(), "", localText.getText("TXT_KEY_PEDIA_HERO_STARTING", ()), CvUtil.FONT_LEFT_JUSTIFY, self.X_UNITCOMBAT_PANE + 5, self.Y_UNITCOMBAT_PANE + iY_Text, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.setText(self.top.getNextWidgetName(), "", localText.getText("TXT_KEY_PEDIA_HERO_POTENTIAL", ()), CvUtil.FONT_LEFT_JUSTIFY, self.X_UNITCOMBAT_PANE + 5, self.Y_UNITCOMBAT_PANE + iY_Text + 20, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		UnitCombatEnum = {'MELEE'    :    gc.getInfoTypeForString("UNITCOMBAT_MELEE"),
				  'MOUNTED'  :    gc.getInfoTypeForString("UNITCOMBAT_MOUNTED"),
				  'ARCHER'   :    gc.getInfoTypeForString("UNITCOMBAT_ARCHER"),
				  'SIEGE'    :    gc.getInfoTypeForString("UNITCOMBAT_SIEGE"),
				  'NAVAL'    :    gc.getInfoTypeForString("UNITCOMBAT_NAVAL")}

		UnitCombatInfo = {'MELEE'    :    gc.getUnitCombatInfo(gc.getInfoTypeForString("UNITCOMBAT_MELEE")),
				  'MOUNTED'  :    gc.getUnitCombatInfo(gc.getInfoTypeForString("UNITCOMBAT_MOUNTED")),
				  'ARCHER'   :    gc.getUnitCombatInfo(gc.getInfoTypeForString("UNITCOMBAT_ARCHER")),
				  'SIEGE'    :    gc.getUnitCombatInfo(gc.getInfoTypeForString("UNITCOMBAT_SIEGE")),
				  'NAVAL'    :    gc.getUnitCombatInfo(gc.getInfoTypeForString("UNITCOMBAT_NAVAL"))}

		CombatLevelSign = {0 : '/',
				   1 : 'D',
				   2 : 'C',
				   3 : 'B',
				   4 : 'A',
				   5 : 'S',
				   -1: '/'}

		startingLevels = {'MELEE'    :    gc.getHeroInfo(self.iHero).getUnitCombatLevel(UnitCombatEnum['MELEE']),
				  'MOUNTED'  :    gc.getHeroInfo(self.iHero).getUnitCombatLevel(UnitCombatEnum['MOUNTED']),
				  'ARCHER'   :    gc.getHeroInfo(self.iHero).getUnitCombatLevel(UnitCombatEnum['ARCHER']),
				  'SIEGE'    :    gc.getHeroInfo(self.iHero).getUnitCombatLevel(UnitCombatEnum['SIEGE']),
				  'NAVAL'    :    gc.getHeroInfo(self.iHero).getUnitCombatLevel(UnitCombatEnum['NAVAL'])}

		potentialLevels ={'MELEE'    :    gc.getHeroInfo(self.iHero).getPotentialUnitCombatLevel(UnitCombatEnum['MELEE']),
				  'MOUNTED'  :    gc.getHeroInfo(self.iHero).getPotentialUnitCombatLevel(UnitCombatEnum['MOUNTED']),
				  'ARCHER'   :    gc.getHeroInfo(self.iHero).getPotentialUnitCombatLevel(UnitCombatEnum['ARCHER']),
				  'SIEGE'    :    gc.getHeroInfo(self.iHero).getPotentialUnitCombatLevel(UnitCombatEnum['SIEGE']),
				  'NAVAL'    :    gc.getHeroInfo(self.iHero).getPotentialUnitCombatLevel(UnitCombatEnum['NAVAL'])}

		iX = 90
		iY = 5
		iIncrement = 4
		iTextSize = 20
		iIconSize = 32

		screen.setImageButtonAt( "MeleeButton", panelName, UnitCombatInfo['MELEE'].getButton(), iX, iY, iIconSize, iIconSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, UnitCombatEnum['MELEE'], -1)
		screen.setTextAt( "MeleeLevel1", panelName, CombatLevelSign[ startingLevels['MELEE'] ], CvUtil.FONT_CENTER_JUSTIFY, iX + 8, iY + iIconSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if gc.getHeroInfo(self.iHero).isRandom() and startingLevels['MELEE'] < potentialLevels['MELEE']:
			screen.setTextAt( "MeleeLevel2", panelName, '?', CvUtil.FONT_CENTER_JUSTIFY, iX + 8, iY + iIconSize + iTextSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setTextAt( "MeleeLevel2", panelName, CombatLevelSign[ potentialLevels.get('MELEE') ], CvUtil.FONT_CENTER_JUSTIFY, iX + 8, iY + iIconSize + iTextSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setImageButtonAt( "MountedButton", panelName, UnitCombatInfo['MOUNTED'].getButton(), iX + iIncrement + iIconSize, iY, iIconSize, iIconSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, UnitCombatEnum['MOUNTED'], -1)
		screen.setTextAt( "MountedLevel1", panelName, CombatLevelSign[ startingLevels['MOUNTED'] ], CvUtil.FONT_CENTER_JUSTIFY, iX + iIncrement + iIconSize + 8, iY + iIconSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if gc.getHeroInfo(self.iHero).isRandom() and startingLevels['MOUNTED'] < potentialLevels['MOUNTED']:
			screen.setTextAt( "MountedLevel2", panelName, '?', CvUtil.FONT_CENTER_JUSTIFY, iX + iIncrement + iIconSize + 8, iY + iIconSize + iTextSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setTextAt( "MountedLevel2", panelName, CombatLevelSign[ potentialLevels.get('MOUNTED') ], CvUtil.FONT_CENTER_JUSTIFY, iX + iIncrement + iIconSize + 8, iY + iIconSize + iTextSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setImageButtonAt( "ArcherButton", panelName, UnitCombatInfo['ARCHER'].getButton(), iX + iIncrement * 2 + iIconSize * 2, iY, iIconSize, iIconSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, UnitCombatEnum['ARCHER'], -1)
		screen.setTextAt( "ArcherLevel1", panelName, CombatLevelSign[ startingLevels['ARCHER'] ], CvUtil.FONT_CENTER_JUSTIFY, iX + iIncrement * 2 + iIconSize * 2 + 8, iY + iIconSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if gc.getHeroInfo(self.iHero).isRandom() and startingLevels['ARCHER'] < potentialLevels['ARCHER']:
			screen.setTextAt( "ArcherLevel2", panelName, '?', CvUtil.FONT_CENTER_JUSTIFY, iX + iIncrement * 2 + iIconSize * 2 + 8, iY + iIconSize + iTextSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setTextAt( "ArcherLevel2", panelName, CombatLevelSign[ potentialLevels.get('ARCHER') ], CvUtil.FONT_CENTER_JUSTIFY, iX + iIncrement * 2 + iIconSize * 2 + 8, iY + iIconSize + iTextSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
			
		screen.setImageButtonAt( "SiegeButton", panelName, UnitCombatInfo['SIEGE'].getButton(), iX + iIncrement * 3 + iIconSize * 3, iY, iIconSize, iIconSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, UnitCombatEnum['SIEGE'], -1)
		screen.setTextAt( "SiegeLevel1", panelName, CombatLevelSign[ startingLevels['SIEGE'] ], CvUtil.FONT_CENTER_JUSTIFY, iX + iIncrement * 3 + iIconSize * 3 + 8, iY + iIconSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if gc.getHeroInfo(self.iHero).isRandom() and startingLevels['SIEGE'] < potentialLevels['SIEGE']:
			screen.setTextAt( "SiegeLevel2", panelName, '?', CvUtil.FONT_CENTER_JUSTIFY, iX + iIncrement * 3 + iIconSize * 3 + 8, iY + iIconSize + iTextSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setTextAt( "SiegeLevel2", panelName, CombatLevelSign[ potentialLevels.get('SIEGE') ], CvUtil.FONT_CENTER_JUSTIFY, iX + iIncrement * 3 + iIconSize * 3 + 8, iY + iIconSize + iTextSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

		screen.setImageButtonAt( "NavalButton", panelName, UnitCombatInfo['NAVAL'].getButton(), iX + iIncrement * 4 + iIconSize * 4, iY, iIconSize, iIconSize, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT_COMBAT, UnitCombatEnum['NAVAL'], -1)
		screen.setTextAt( "NavalLevel1", panelName, CombatLevelSign[ startingLevels['NAVAL'] ], CvUtil.FONT_CENTER_JUSTIFY, iX + iIncrement * 4 + iIconSize * 4 + 8, iY + iIconSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		if gc.getHeroInfo(self.iHero).isRandom() and startingLevels['NAVAL'] < potentialLevels['NAVAL']:
			screen.setTextAt( "NavalLevel2", panelName, '?', CvUtil.FONT_CENTER_JUSTIFY, iX + iIncrement * 4 + iIconSize * 4 + 8, iY + iIconSize + iTextSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		else:
			screen.setTextAt( "NavalLevel2", panelName, CombatLevelSign[ potentialLevels.get('NAVAL') ], CvUtil.FONT_CENTER_JUSTIFY, iX + iIncrement * 4 + iIconSize * 4 + 8, iY + iIconSize + iTextSize, 0, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

	def placeSpecial(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_SPECIAL_ABILITIES", ()), "", True, False, self.X_SPECIAL_PANE, self.Y_SPECIAL_PANE, self.W_SPECIAL_PANE, self.H_SPECIAL_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		listName = self.top.getNextWidgetName()
		szSpecialText = CyGameTextMgr().getUnitHelp(gc.getNumUnitInfos() + self.iHero, True, False, False, None)[1:]
		screen.addMultilineText(listName, szSpecialText, self.X_SPECIAL_PANE+5, self.Y_SPECIAL_PANE+30, self.W_SPECIAL_PANE-10, self.H_SPECIAL_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeHistory(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_HISTORY", ()), "", True, True, self.X_HISTORY_PANE, self.Y_HISTORY_PANE, self.W_HISTORY_PANE, self.H_HISTORY_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		textName = self.top.getNextWidgetName()
		szText = u""
		if len(gc.getHeroInfo(self.iHero).getStrategy()) > 0:
			szText += localText.getText("TXT_KEY_CIVILOPEDIA_STRATEGY", ())
			szText += gc.getHeroInfo(self.iHero).getStrategy()
			szText += u"\n\n"
		szText += localText.getText("TXT_KEY_CIVILOPEDIA_BACKGROUND", ())
		szText += gc.getHeroInfo(self.iHero).getCivilopedia()
		screen.addMultilineText(textName, szText, self.X_HISTORY_PANE + 15, self.Y_HISTORY_PANE + 40, self.W_HISTORY_PANE - (15 * 2), self.H_HISTORY_PANE - (15 * 2) - 25, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)


	def placeHeroes(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_PROMOTION_HERO", ()), "", True, True, self.X_HERO_PANE, self.Y_UNIT_GROUP_PANE, self.W_HERO_PANE, self.top.B_PEDIA_PAGE - self.Y_UNIT_GROUP_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")

		rowListName = self.top.getNextWidgetName()
		screen.addMultiListControlGFC(rowListName, "", self.X_HERO_PANE+15, self.Y_UNIT_GROUP_PANE+40, self.W_HERO_PANE-20, self.top.B_PEDIA_PAGE - self.Y_UNIT_GROUP_PANE -40, 1, 48, 48, TableStyles.TABLE_STYLE_STANDARD)
		for k in range(gc.getNumHeroInfos()):
			if (isPromotionValid(self.iPromotion, gc.getHeroInfo(k).getUnitType(), False) and not gc.getPromotionInfo(self.iPromotion).isGraphicalOnly()):
				if (gc.getHeroInfo(k).getUnitPromotionStatus(self.iPromotion) > 0):
					screen.appendMultiListButton(rowListName, gc.getHeroInfo(k).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_HERO, k, -1, False)



	def placePromotions(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_PROMOTION", ()), "", True, True, self.X_PROMO_PANE, self.Y_PROMO_PANE, self.W_PROMO_PANE, self.H_PROMO_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		rowListName = self.top.getNextWidgetName()
		screen.addMultiListControlGFC(rowListName, "", self.X_PROMO_PANE+15, self.Y_PROMO_PANE+40, self.W_PROMO_PANE-20, self.H_PROMO_PANE-40, 1, self.PROMOTION_ICON_SIZE, self.PROMOTION_ICON_SIZE, TableStyles.TABLE_STYLE_STANDARD)
		for k in range(gc.getNumPromotionInfos()):
			# if (isPromotionValid(k, gc.getHeroInfo(self.iHero).getUnitType(), False) and not gc.getPromotionInfo(k).isGraphicalOnly()):
			# if (isPromotionValid(k, self.iUnit, False) and not gc.getPromotionInfo(k).isGraphicalOnly()):
			if gc.getUnitInfo(self.iHero).isQualifiedPromotionType(k) and not gc.getPromotionInfo(k).isGraphicalOnly():
				if (gc.getHeroInfo(self.iHero).getUnitPromotionStatus(k) > 0):
					screen.appendMultiListButton(rowListName, gc.getPromotionInfo(k).getButton(), 0, WidgetTypes.WIDGET_PEDIA_JUMP_TO_PROMOTION, k, -1, False)



	def handleInput (self, inputClass):
		return 0
