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
# Modified for Caveman2Cosmos by Dancing Hoskuld
# - since C2C has so many units and buildings parse them once rather
#   than for each panel creating arrays for use by the panel

from CvPythonExtensions import *
import CvUtil
import ScreenInput
import SevoScreenEnums
import string

gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaBonus:

	def __init__(self, main):
		self.iBonus = -1
		self.top = main

		self.X_BONUS_PANE = self.top.X_PEDIA_PAGE
		self.Y_BONUS_PANE = self.top.Y_PEDIA_PAGE
		self.W_BONUS_PANE = self.top.W_PEDIA_PAGE / 2 - 5
		self.H_BONUS_PANE = 116

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_BONUS_PANE + (self.H_BONUS_PANE - self.H_ICON) / 2
		self.Y_ICON = self.Y_BONUS_PANE + (self.H_BONUS_PANE - self.H_ICON) / 2
		self.ICON_SIZE = 64

		self.X_STATS_PANE = self.X_BONUS_PANE + 110
		self.Y_STATS_PANE = self.Y_BONUS_PANE + 6
		self.W_STATS_PANE = self.W_BONUS_PANE - self.W_ICON - 3 ## 240
		self.H_STATS_PANE = self.H_BONUS_PANE - 6 ## 200

		self.X_BONUS_ANIMATION = self.X_BONUS_PANE + self.W_BONUS_PANE + 10
		self.Y_BONUS_ANIMATION = self.Y_BONUS_PANE + 7
		self.W_BONUS_ANIMATION = self.top.R_PEDIA_PAGE - self.X_BONUS_ANIMATION 
		self.H_BONUS_ANIMATION = self.H_BONUS_PANE
		self.X_ROTATION_BONUS_ANIMATION = -20
		self.Z_ROTATION_BONUS_ANIMATION = 30
		self.SCALE_ANIMATION = 0.7

		# Yield pane is used for Yields for Map Resources and Sources for manufactured and culture resources
		self.X_YIELD_PANE = self.X_BONUS_PANE
		self.W_YIELD_PANE = self.W_BONUS_PANE
		self.Y_YIELD_PANE = self.Y_BONUS_PANE + self.H_BONUS_PANE + 10
		self.H_YIELD_PANE = 110

		self.X_VICINITY_PANE = self.X_BONUS_ANIMATION
		self.W_VICINITY_PANE = self.W_BONUS_ANIMATION
		self.Y_VICINITY_PANE = self.Y_YIELD_PANE
		self.H_VICINITY_PANE = self.H_YIELD_PANE

		self.X_REQUIRES = self.X_BONUS_PANE
		self.W_REQUIRES = self.W_BONUS_PANE
		self.Y_REQUIRES = self.Y_YIELD_PANE + self.H_YIELD_PANE + 10
		self.H_REQUIRES = 110

		self.X_BUILDINGS = self.X_BONUS_ANIMATION
		self.W_BUILDINGS = self.W_BONUS_ANIMATION
		self.Y_BUILDINGS = self.Y_REQUIRES
		self.H_BUILDINGS = self.H_REQUIRES

		self.X_UNIT_REQUIRES_PANE = self.X_BONUS_PANE
		self.W_UNIT_REQUIRES_PANE = ((self.top.R_PEDIA_PAGE - self.X_UNIT_REQUIRES_PANE)/3) - 10
		self.Y_UNIT_REQUIRES_PANE = self.Y_REQUIRES + self.H_REQUIRES + 10
		self.H_UNIT_REQUIRES_PANE = 110

		self.X_UNIT_EFFECTS_PANE = self.X_BONUS_PANE + self.W_UNIT_REQUIRES_PANE + 5
		self.W_UNIT_EFFECTS_PANE = self.W_UNIT_REQUIRES_PANE
		self.Y_UNIT_EFFECTS_PANE = self.Y_UNIT_REQUIRES_PANE
		self.H_UNIT_EFFECTS_PANE = 110

		self.X_EFFECTS_PANE = self.X_UNIT_EFFECTS_PANE + self.W_UNIT_REQUIRES_PANE + 5
		self.W_EFFECTS_PANE = self.W_UNIT_REQUIRES_PANE
		self.Y_EFFECTS_PANE = self.Y_UNIT_REQUIRES_PANE
		self.H_EFFECTS_PANE = 110

		self.X_HISTORY_PANE = self.X_UNIT_REQUIRES_PANE
		self.W_HISTORY_PANE = self.top.R_PEDIA_PAGE - self.X_UNIT_REQUIRES_PANE
		self.Y_HISTORY_PANE = self.Y_UNIT_REQUIRES_PANE + self.H_UNIT_REQUIRES_PANE + 10
		self.H_HISTORY_PANE = self.top.B_PEDIA_PAGE - self.Y_HISTORY_PANE



	def interfaceScreen(self, iBonus):
		self.iBonus = iBonus
		screen = self.top.getScreen()

		screen.addPanel( self.top.getNextWidgetName(), "", "", False, False, self.X_BONUS_PANE, self.Y_BONUS_PANE, self.W_BONUS_PANE, self.H_BONUS_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getBonusInfo(self.iBonus).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )
		screen.addBonusGraphicGFC(self.top.getNextWidgetName(), self.iBonus, self.X_BONUS_ANIMATION, self.Y_BONUS_ANIMATION, self.W_BONUS_ANIMATION, self.H_BONUS_ANIMATION, WidgetTypes.WIDGET_GENERAL, -1, -1, self.X_ROTATION_BONUS_ANIMATION, self.Z_ROTATION_BONUS_ANIMATION, self.SCALE_ANIMATION, True)

		## The original code goes through the building list for each pane that has a building in it. 
		## Same for units. It is better to only go through once to create a set of lists of the relevant buildings and units.
		self.parsAllBuildings()
		self.parsAllUnits()
		
		self.placeStats()
		if gc.getBonusInfo(self.iBonus).getConstAppearance() > 0:
			self.placeYield()
		else:
			self.placeSource()
		self.placeRequires()
		if gc.getBonusInfo(self.iBonus).getConstAppearance() > 0:
			self.placeVicinityBuildings()
		self.placeBuildings()
		self.placeAllows()
		self.placeFasterUnits()
		self.placeEffects()
		self.placeHistory()

	def parsAllBuildings(self):
		bonusInfo = gc.getBonusInfo(self.iBonus)
		## Buildings and Units only show up once in this page even if they could be in each pane.
		## They only show in the most important to this context
		self.aVicinityBuildings = {}
		self.aRequiresBuildings = {}
		self.aEffectedBuildings = {}
		self.aSourceOfBonus = {}
				
		for iBuilding in range(gc.getNumBuildingInfos()):
			buildingInfo = gc.getBuildingInfo(iBuilding)

			if bonusInfo.getConstAppearance() == 0:
				if (buildingInfo.getFreeBonus() == self.iBonus):
					self.aSourceOfBonus[iBuilding] = iBuilding
				else:
					for i in range(buildingInfo.getNumExtraFreeBonuses()):
						if (buildingInfo.getExtraFreeBonus(i) == self.iBonus):
							self.aSourceOfBonus[iBuilding] = iBuilding
							break
			
			bShow = False
			if buildingInfo.getPrereqVicinityBonus() == self.iBonus :
				self.aVicinityBuildings[iBuilding] = iBuilding
				bShow = True
			else:
				if buildingInfo.getPrereqAndBonus() == self.iBonus :
					self.aRequiresBuildings[iBuilding] = iBuilding
					bShow = True
				else:
					j = 0
					while (not bShow and j < buildingInfo.getNumPrereqOrBonuses()):
						if (buildingInfo.getPrereqOrBonuses(j) == self.iBonus):
							self.aRequiresBuildings[iBuilding] = iBuilding
							bShow = True
						j += 1
			
			if (not bShow) and (buildingInfo.getBonusHealthChanges(self.iBonus) != 0 or buildingInfo.getBonusHappinessChanges(self.iBonus) != 0 or buildingInfo.getBonusProductionModifier(self.iBonus) != 0):
				self.aEffectedBuildings[iBuilding] = True
				bShow = True
			else:
				for eYield in range(YieldTypes.NUM_YIELD_TYPES):
					if (buildingInfo.getBonusYieldModifier(self.iBonus, eYield) != 0):
						self.aEffectedBuildings[iBuilding] = iBuilding
						bShow = True
						break
				
			# for eCommerce in range(YieldTypes.NUM_COMMERCE_TYPES):
				# if (buildingInfo.getBonusCommerceModifier(self.iBonus, eCommerce) > 0):
				
	
	def parsAllUnits(self):
		bonusInfo = gc.getBonusInfo(self.iBonus)
		## Buildings and Units only show up once in this page even if they could be in each pane.
		## They only show in the most important to this context
		self.aRequiresUnits = {}
		self.aEffectedUnits = {}

		bFound = False
		for eLoopUnit in range(gc.getNumUnitInfos()):
			unitInfo = gc.getUnitInfo(eLoopUnit)
			if (eLoopUnit >= 0):
				if (unitInfo.getPrereqAndBonus() == self.iBonus):
					self.aRequiresUnits[eLoopUnit] = eLoopUnit
					bFound = True	
				else:
					j = 0
					while (not bFound and j < gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
						if (unitInfo.getPrereqOrBonuses(j) == self.iBonus):
							self.aRequiresUnits[eLoopUnit] = eLoopUnit
							bFound = True
						j += 1
			if not bFound:
				if unitInfo.getBonusProductionModifier(self.iBonus) > 0:
					self.aEffectedUnits[eLoopUnit] = eLoopUnit
					

		
	def placeStats(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		bonusInfo = gc.getBonusInfo(self.iBonus)
		for k in range(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = bonusInfo.getYieldChange(k)
			if (iYieldChange != 0):
				if (iYieldChange > 0):
					sign = "+"
				else:
					sign = ""
				szYield = (u"%s: %s%i " % (gc.getYieldInfo(k).getDescription(), sign, iYieldChange))
				screen.appendListBoxString(panelName, u"<font=3>" + szYield.upper() + (u"%c" % gc.getYieldInfo(k).getChar()) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		iHappy = bonusInfo.getHappiness()
		iHealth = bonusInfo.getHealth()
		bSomeHappy = False
		bSomeHealth = False

		if not iHappy == 0:
			bSomeHappy = True
			iHappySign = "+"
			if iHappy < 0:
				iHappySign = ""

		if not iHealth == 0:
			bSomeHealth = True
			iHealthSign = "+"
			if iHealth < 0:
				iHealthSign = ""

		if bSomeHappy and bSomeHealth :
			if gc.getBonusInfo(self.iBonus).getConstAppearance() > 0:
				screen.appendListBoxString( panelName, u"%s%i%c " % (iHappySign, iHappy, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)) + u"%s%i%c " % (iHealthSign, iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR)) + localText.getText("TXT_KEY_PEDIA_WITH_IMPROVEMENT_AND_ROUTE", ()) + u"", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
			else:
				screen.appendListBoxString( panelName, u"%s%i%c " % (iHappySign, iHappy, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)) + u"%s%i%c " % (iHealthSign, iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR)) + u"", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		elif bSomeHappy:
			if gc.getBonusInfo(self.iBonus).getConstAppearance() > 0:
				screen.appendListBoxString( panelName, u"%s%i%c " % (iHappySign, iHappy, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)) + localText.getText("TXT_KEY_PEDIA_WITH_IMPROVEMENT_AND_ROUTE", ()) + u"", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
			else:
				screen.appendListBoxString( panelName, u"%s%i%c " % (iHappySign, iHappy, CyGame().getSymbolID(FontSymbols.HAPPY_CHAR)) + u"", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
		elif bSomeHealth:
			if gc.getBonusInfo(self.iBonus).getConstAppearance() > 0:
				screen.appendListBoxString( panelName, u"%s%i%c " % (iHealthSign, iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR)) + localText.getText("TXT_KEY_PEDIA_WITH_IMPROVEMENT_AND_ROUTE", ()) + u"", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )
			else:
				screen.appendListBoxString( panelName, u"%s%i%c " % (iHealthSign, iHealth, CyGame().getSymbolID(FontSymbols.HEALTHY_CHAR)) + u"", WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY )



	def placeYield(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_CATEGORY_IMPROVEMENT", ()), "", True, True, self.X_YIELD_PANE, self.Y_YIELD_PANE, self.W_YIELD_PANE, self.H_YIELD_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		bonusInfo = gc.getBonusInfo(self.iBonus)
		for j in range(gc.getNumImprovementInfos()):
			bFirst = True
			szYield = u""
			bEffect = False
			for k in range(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = gc.getImprovementInfo(j).getImprovementBonusYield(self.iBonus, k)
				if (iYieldChange != 0):
					bEffect = True
					iYieldChange += gc.getImprovementInfo(j).getYieldChange(k)
					if (bFirst):
						bFirst = False
					else:
						szYield += ", "
					if (iYieldChange > 0):
						sign = "+"
					else:
						sign = ""
					szYield += (u"%s%i%c" % (sign, iYieldChange, gc.getYieldInfo(k).getChar()))
			if (bEffect):
				childPanelName = self.top.getNextWidgetName()
				screen.attachPanel(panelName, childPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel(childPanelName, "", "  ")
				screen.attachImageButton(childPanelName, "", gc.getImprovementInfo(j).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, j, 1, False )
				screen.attachLabel(childPanelName, "", szYield)

	def placeSource(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_RESOURCE_SOURCE", ()), "", False, True, self.X_YIELD_PANE, self.Y_YIELD_PANE, self.W_YIELD_PANE, self.H_YIELD_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		bonusInfo = gc.getBonusInfo(self.iBonus)

		for iBuilding in self.aSourceOfBonus:
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, 1, False )



	def placeEffects(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_BONUS_EFFECTS_BUILDING", ()), "", False, True, self.X_EFFECTS_PANE, self.Y_EFFECTS_PANE, self.W_EFFECTS_PANE, self.H_EFFECTS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
			
		for iBuilding in self.aEffectedBuildings:
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, 1, False )



	def placeRequires(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True, self.X_REQUIRES, self.Y_REQUIRES, self.W_REQUIRES, self.H_REQUIRES, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panelName, "", "  ")
		iRevealTech = gc.getBonusInfo(self.iBonus).getTechReveal()
		iTradeTech = gc.getBonusInfo(self.iBonus).getTechCityTrade()

		if (iRevealTech == iTradeTech) and (iRevealTech > -1):
			screen.attachImageButton( panelName, "", gc.getTechInfo(iRevealTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iRevealTech, 1, False )
			screen.attachLabel(panelName, "", u"(" + localText.getText("TXT_KEY_PEDIA_BONUS_APPEARANCE_AND_TRADE", ()) + u")")
		else:
			if (iRevealTech > -1):
				screen.attachImageButton( panelName, "", gc.getTechInfo(iRevealTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iRevealTech, 1, False )
				screen.attachLabel(panelName, "", u"(" + localText.getText("TXT_KEY_PEDIA_BONUS_APPEARANCE", ()) + u")")
			if (iTradeTech > -1):
				screen.attachImageButton( panelName, "", gc.getTechInfo(iTradeTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTradeTech, 1, False )
				screen.attachLabel(panelName, "", u"(" + localText.getText("TXT_KEY_PEDIA_BONUS_TRADE", ()) + u")")

		iObsoleteTech = gc.getBonusInfo(self.iBonus).getTechObsolete()
		if (iObsoleteTech > -1):
			screen.attachImageButton( panelName, "", gc.getTechInfo(iObsoleteTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iObsoleteTech, 1, False )
			screen.attachLabel(panelName, "", u"(" + localText.getText("TXT_KEY_PEDIA_BONUS_OBSOLETE", ()) + u")")


	def placeHistory(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName,localText.getText("TXT_KEY_PEDIA_HISTORY", ()), "", True, True, self.X_HISTORY_PANE, self.Y_HISTORY_PANE, self.W_HISTORY_PANE, self.H_HISTORY_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.attachLabel(panelName, "", "  ")
		textName = self.top.getNextWidgetName()
		screen.addMultilineText( textName, gc.getBonusInfo(self.iBonus).getCivilopedia(), self.X_HISTORY_PANE + 15, self.Y_HISTORY_PANE + 40, self.W_HISTORY_PANE - (30), self.H_HISTORY_PANE - (15 * 2) - 25, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)



	def placeVicinityBuildings(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_BONUS_VICINITY_BUILDING", ()), "", False, True, self.X_VICINITY_PANE, self.Y_VICINITY_PANE, self.W_VICINITY_PANE, self.H_VICINITY_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panelName, "", "  ")

		for iBuilding in self.aVicinityBuildings:
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, 1, False )

				
	def placeBuildings(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_BONUS_REQUIRES_BUILDING", ()), "", False, True, self.X_BUILDINGS, self.Y_BUILDINGS, self.W_BUILDINGS, self.H_BUILDINGS, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panelName, "", "  ")

		bFirst = True
		for iBuilding in self.aRequiresBuildings:
			screen.attachImageButton( panelName, "", gc.getBuildingInfo(iBuilding).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BUILDING, iBuilding, 1, False )

				
	def placeAllows(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_BONUS_REQUIRES_UNIT", ()), "", False, True, self.X_UNIT_REQUIRES_PANE, self.Y_UNIT_REQUIRES_PANE, self.W_UNIT_REQUIRES_PANE, self.H_UNIT_REQUIRES_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panelName, "", "  ")

		for eLoopUnit in self.aRequiresUnits:
				screen.attachImageButton( panelName, "", gc.getUnitInfo(eLoopUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )

	def placeFasterUnits(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_BONUS_EFFECTS_UNIT", ()), "", False, True, self.X_UNIT_EFFECTS_PANE, self.Y_UNIT_EFFECTS_PANE, self.W_UNIT_EFFECTS_PANE, self.H_UNIT_EFFECTS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.attachLabel(panelName, "", "  ")

		for eLoopUnit in self.aEffectedUnits:
			screen.attachImageButton( panelName, "", gc.getUnitInfo(eLoopUnit).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_UNIT, eLoopUnit, 1, False )


	def handleInput (self, inputClass):
		return 0
