## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
from CvPythonExtensions import *
import CvUtil
import ScreenInput
import SevoScreenEnums

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

class SevoPediaRoute:
	"Civilopedia Screen for tile Routes"

	def __init__(self, main):
		self.iRoute = -1
		self.top = main
		

		self.X_ROUTE_PANE = self.top.X_PEDIA_PAGE
		self.Y_ROUTE_PANE = self.top.Y_PEDIA_PAGE
		self.W_ROUTE_PANE = 323
		self.H_ROUTE_PANE = 116

		self.W_ICON = 100
		self.H_ICON = 100
		self.X_ICON = self.X_ROUTE_PANE + (self.H_ROUTE_PANE - self.H_ICON) / 2
		self.Y_ICON = self.Y_ROUTE_PANE + (self.H_ROUTE_PANE - self.H_ICON) / 2
		self.ICON_SIZE = 64
		self.BUTTON_SIZE = 64

		self.X_STATS_PANE = self.X_ROUTE_PANE + 125
		self.Y_STATS_PANE = self.Y_ROUTE_PANE + 10
		self.W_STATS_PANE = 300
		self.H_STATS_PANE = 200

		self.X_YIELDS_PANE = self.X_ROUTE_PANE + self.W_ROUTE_PANE +5
		self.Y_YIELDS_PANE = self.Y_ROUTE_PANE + 10
		self.W_YIELDS_PANE = 275 
		self.H_YIELDS_PANE = 106
		
		self.X_REQUIRES_PANE = self.X_ROUTE_PANE
		self.Y_REQUIRES_PANE = self.Y_ROUTE_PANE + self.H_ROUTE_PANE + 10
		self.W_REQUIRES_PANE = 600 
		self.H_REQUIRES_PANE = 110
		
		self.X_TECH_EFFECTS_PANE = self.X_REQUIRES_PANE
		self.Y_TECH_EFFECTS_PANE = self.Y_REQUIRES_PANE + self.H_REQUIRES_PANE + 10
		self.W_TECH_EFFECTS_PANE = 280
		self.H_TECH_EFFECTS_PANE = 195
		
		self.X_BONUS_YIELDS_PANE = self.X_TECH_EFFECTS_PANE
		self.Y_BONUS_YIELDS_PANE = self.Y_TECH_EFFECTS_PANE + self.H_TECH_EFFECTS_PANE + 10
		self.W_BONUS_YIELDS_PANE = 280
		self.H_BONUS_YIELDS_PANE = 195
		
		self.X_HISTORY_PANE = self.X_REQUIRES_PANE + self.W_TECH_EFFECTS_PANE + 10
		self.Y_HISTORY_PANE = self.Y_TECH_EFFECTS_PANE
		self.W_HISTORY_PANE = 300
		self.H_HISTORY_PANE = 385
		
	# Screen construction function
	def interfaceScreen(self, iRoute):	
		self.iRoute = iRoute
		screen = self.top.getScreen()
		
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ROUTE_PANE, self.Y_ROUTE_PANE, self.W_ROUTE_PANE, self.H_ROUTE_PANE, PanelStyles.PANEL_STYLE_BLUE50)
		screen.addPanel(self.top.getNextWidgetName(), "", "", False, False, self.X_ICON, self.Y_ICON, self.W_ICON, self.H_ICON, PanelStyles.PANEL_STYLE_MAIN)
		screen.addDDSGFC(self.top.getNextWidgetName(), gc.getRouteInfo(self.iRoute).getButton(), self.X_ICON + self.W_ICON/2 - self.ICON_SIZE/2, self.Y_ICON + self.H_ICON/2 - self.ICON_SIZE/2, self.ICON_SIZE, self.ICON_SIZE, WidgetTypes.WIDGET_GENERAL, -1, -1 )

		self.placeStats()
		self.placeRequires()
		self.placeYield()
		self.placeImprovementYield()
		self.placeTechEffects()
		# self.placeSpecial()
		self.placeHistory()

	def placeStats(self):
		screen = self.top.getScreen()
		panelName = self.top.getNextWidgetName()

		screen.addListBoxGFC(panelName, "", self.X_STATS_PANE, self.Y_STATS_PANE, self.W_STATS_PANE, self.H_STATS_PANE, TableStyles.TABLE_STYLE_EMPTY)
		screen.enableSelect(panelName, False)
		iFontSize = 3

		iMoveDenominator = gc.getMOVE_DENOMINATOR()
		RouteInfo = gc.getRouteInfo(self.iRoute)
		iMoveCost = RouteInfo.getMovementCost()
		iFlatMoveCost = RouteInfo.getFlatMovementCost()
		szName = self.top.getNextWidgetName()

		szMovement = localText.getText("TXT_KEY_PEDIA_ROUTE_MOVEMENT", ("",))
		szMovement = (u"%s %.1f" % (szMovement.upper(), float(iMoveDenominator)/iMoveCost))
		screen.appendListBoxString(panelName, u"<font=%d>" % iFontSize + szMovement + u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR) + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		if not iFlatMoveCost == 0:
			sText = u"%s: %.1f%s" % (localText.getText("TXT_KEY_PEDIA_ROUTE_FLAT_COST",()).upper(), float(iMoveDenominator) / iFlatMoveCost, CyTranslator().getText("[ICON_MOVES]", ()))
			screen.appendListBoxString(panelName, "<font=%d>" % iFontSize + sText + "</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		
		iMaxTime = 0
		iMaxCost = 0
		for iBuild in range(gc.getNumBuildInfos()):
			if (gc.getBuildInfo(iBuild).getRoute() == self.iRoute):	
				iTime = gc.getBuildInfo(iBuild).getTime()
				if iTime > iMaxTime:
					iMaxTime = iTime
				iCost = gc.getBuildInfo(iBuild).getCost()
				if iCost > iMaxCost:
					iMaxCost = iCost

		szName = self.top.getNextWidgetName()
		szCost = localText.getText("TXT_KEY_PEDIA_ROUTE_WORK_COST", (iMaxTime,))
		screen.appendListBoxStringNoUpdate(panelName, u"<font=%d>" % iFontSize + szCost.upper() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)
		szName = self.top.getNextWidgetName()
		szCost = localText.getText("TXT_KEY_PEDIA_COST", (iMaxCost,))
		screen.appendListBoxStringNoUpdate(panelName, u"<font=%d>" % iFontSize + szCost.upper() + u"%c" % gc.getYieldInfo(YieldTypes.YIELD_COMMERCE).getChar() + u"</font>", WidgetTypes.WIDGET_GENERAL, 0, 0, CvUtil.FONT_LEFT_JUSTIFY)

		screen.updateListBox(panelName)

	def placeYield(self):
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_PLOT_YIELD_CHANGE", ()), "", True, True,
				 self.X_YIELDS_PANE, self.Y_YIELDS_PANE, self.W_YIELDS_PANE, self.H_YIELDS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
	
		RouteInfo = gc.getRouteInfo(self.iRoute)
		
		szYield = u""
		bYieldChange = False
		comma = ""
		for k in range(YieldTypes.NUM_YIELD_TYPES):
			iYieldChange = RouteInfo.getYieldChange(k)
			if (iYieldChange != 0):	
				bYieldChange = True
				if (iYieldChange > 0):
					sign = "+"
				else:
					sign = ""
					
				szYield += (u"%s%s%i%c" % (comma, sign, iYieldChange, gc.getYieldInfo(k).getChar()))
				comma = ","
		
		if bYieldChange == False:
			szYield += localText.getText("TXT_KEY_PEDIA_NO_PLOT_YIELD_CHANGE", ())
			
		screen.attachLabel(panelName, "", u"<font=4>" + szYield + u"</font>")

	def placeImprovementYield(self):
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_ROUTE_IMPROVEMENT_YIELD_CHANGE", ()), "", True, True,
				 self.X_BONUS_YIELDS_PANE, self.Y_BONUS_YIELDS_PANE, self.W_BONUS_YIELDS_PANE, self.H_BONUS_YIELDS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
	
		szYield = u""
		bImprovementYieldChange = False
		for l in range(gc.getNumImprovementInfos()):
			bImprovementChange = False
			szImprovementYield  = u""
			for k in range(YieldTypes.NUM_YIELD_TYPES):
				iYieldChange = gc.getImprovementInfo(l).getRouteYieldChanges(self.iRoute, k)
				if (iYieldChange != 0):
					if bImprovementChange == True:
						szImprovementYield += (u",")
					szImprovementYield += (u" %i %c" % (iYieldChange, gc.getYieldInfo(k).getChar()))
					bImprovementYieldChange = True
					bImprovementChange = True
			if bImprovementChange:
				childPanelName = self.top.getNextWidgetName()
				screen.attachPanel(panelName, childPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel(childPanelName, "", "  ")
				screen.attachImageButton( childPanelName, "", gc.getImprovementInfo(l).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_IMPROVEMENT, l, 1, False )
				screen.attachLabel(childPanelName, "", u"<font=4>" + szImprovementYield + u"</font>")
				
		if bImprovementYieldChange == False:
			szYield += localText.getText("TXT_KEY_PEDIA_NO_PLOT_YIELD_CHANGE", ())

			listName = self.top.getNextWidgetName()
			screen.addMultilineText(listName, szYield, self.X_BONUS_YIELDS_PANE+5, self.Y_BONUS_YIELDS_PANE+30, self.W_BONUS_YIELDS_PANE-10, self.H_BONUS_YIELDS_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	
	
		return
	
	def placeRequires(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_REQUIRES", ()), "", False, True,
				 self.X_REQUIRES_PANE, self.Y_REQUIRES_PANE, self.W_REQUIRES_PANE, self.H_REQUIRES_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		
		screen.attachLabel(panelName, "", "  ")
		
		aTechList = []
		for iBuild in range(gc.getNumBuildInfos()):
			if (gc.getBuildInfo(iBuild).getRoute() == self.iRoute):	 
				iTech = gc.getBuildInfo(iBuild).getTechPrereq()
				if (iTech > -1):
					if not iTech in aTechList:
						aTechList.append(iTech)
		for i in aTechList:
			screen.attachImageButton( panelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )
			
		bFirst = True
		iPrereq = gc.getRouteInfo(self.iRoute).getPrereqBonus()
		if (iPrereq >= 0):
			bFirst = False
			screen.attachImageButton(panelName, "", gc.getBonusInfo(iPrereq).getButton(), GenericButtonSizes.BUTTON_SIZE_46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, iPrereq, -1, False)
		nOr = 0
		for j in range(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
			if (gc.getRouteInfo(self.iRoute).getPrereqOrBonus(j) > -1):
				nOr += 1
		szLeftDelimeter = ""
		szRightDelimeter = ""
		if (not bFirst):
			if (nOr > 1):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ()) + "("
				szRightDelimeter = ") "
			elif (nOr > 0):
				szLeftDelimeter = localText.getText("TXT_KEY_AND", ())
		if len(szLeftDelimeter) > 0:
			screen.attachLabel(panelName, "", szLeftDelimeter)
		bFirst = True
		for j in range(gc.getNUM_UNIT_PREREQ_OR_BONUSES()):
			eBonus = gc.getRouteInfo(self.iRoute).getPrereqOrBonus(j)
			if (eBonus > -1):
				if (not bFirst):
					screen.attachLabel(panelName, "", localText.getText("TXT_KEY_OR", ()))
				else:
					bFirst = False
				screen.attachImageButton(panelName, "", gc.getBonusInfo(eBonus).getButton(), GenericButtonSizes.BUTTON_SIZE_46, WidgetTypes.WIDGET_PEDIA_JUMP_TO_BONUS, eBonus, -1, False)
		if len(szRightDelimeter) > 0:
			screen.attachLabel(panelName, "", szRightDelimeter)

	def placeTechEffects(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel( panelName, localText.getText("TXT_KEY_PEDIA_TECH_CHANGES", ()), "", True, False,
				 self.X_TECH_EFFECTS_PANE, self.Y_TECH_EFFECTS_PANE, self.W_TECH_EFFECTS_PANE, self.H_TECH_EFFECTS_PANE, PanelStyles.PANEL_STYLE_BLUE50 )

		RouteInfo = gc.getRouteInfo(self.iRoute)
		iMoveDenominator = gc.getMOVE_DENOMINATOR()
		iMoveCost = RouteInfo.getMovementCost()
		iMovement = float(iMoveDenominator)/ iMoveCost
		bTechChange = False
		szSpecialText = u""
		for iTech in xrange(gc.getNumTechInfos()):
			iRouteChange = RouteInfo.getTechMovementChange(iTech)
			if not iRouteChange == 0:
				iNewMovement = float(iMoveDenominator)/ (iMoveCost + iRouteChange)

				childPanelName = self.top.getNextWidgetName()
				screen.attachPanel(panelName, childPanelName, "", "", False, False, PanelStyles.PANEL_STYLE_EMPTY)
				screen.attachLabel(childPanelName, "", "  ")
				screen.attachImageButton( childPanelName, "", gc.getTechInfo(iTech).getButton(), GenericButtonSizes.BUTTON_SIZE_CUSTOM, WidgetTypes.WIDGET_PEDIA_JUMP_TO_TECH, iTech, 1, False )
				screen.attachLabel(childPanelName, "", u"<font=4>%.1f" % (iNewMovement - iMovement) + u"%c" % CyGame().getSymbolID(FontSymbols.MOVES_CHAR) + u"</font>")

				iMovement = iNewMovement
				bTechChange = True
		
		if bTechChange == False:
			szSpecialText += localText.getText("TXT_KEY_PEDIA_NO_PLOT_YIELD_CHANGE", ())
		
			listName = self.top.getNextWidgetName()
			screen.addMultilineText(listName, szSpecialText, self.X_TECH_EFFECTS_PANE+5, self.Y_TECH_EFFECTS_PANE+30, self.W_TECH_EFFECTS_PANE-10, self.H_TECH_EFFECTS_PANE-35, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)	

	def placeHistory(self):
		
		screen = self.top.getScreen()
		
		panelName = self.top.getNextWidgetName()
		screen.addPanel(panelName, CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_CONCEPT", ()), "", True, False, self.X_HISTORY_PANE, self.Y_HISTORY_PANE, self.W_HISTORY_PANE, self.H_HISTORY_PANE, PanelStyles.PANEL_STYLE_BLUE50 )
		screen.addMultilineText(panelName, CyTranslator().getText("TXT_KEY_CONCEPT_MOVEMENT_PEDIA", ()), self.X_HISTORY_PANE+10, self.Y_HISTORY_PANE + 30, self.W_HISTORY_PANE -20, self.H_HISTORY_PANE- 55, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
			
	def placeLinks(self, bRedraw):

		screen = self.top.getScreen()

		if bRedraw:
			screen.clearListBoxGFC(self.top.LIST_ID)
		
		# sort Routes alphabetically
		rowListName=[(0,0)]*gc.getNumRouteInfos()
		for j in range(gc.getNumRouteInfos()):
			rowListName[j] = (gc.getRouteInfo(j).getDescription(), j)
		rowListName.sort()	
			
		iSelected = 0
		i = 0
		for iI in range(gc.getNumRouteInfos()):
			if (not gc.getRouteInfo(rowListName[iI][1]).isGraphicalOnly()):
				if bRedraw:
					screen.appendListBoxString(self.top.LIST_ID, rowListName[iI][0], WidgetTypes.WIDGET_HELP_MOVE_BONUS, rowListName[iI][1], 0, CvUtil.FONT_LEFT_JUSTIFY)
				if rowListName[iI][1] == self.iRoute:
					iSelected = i
				i += 1
					
		screen.setSelectedListBoxStringGFC(self.top.LIST_ID, iSelected)
			

	# Will handle the input for this screen...
	def handleInput (self, inputClass):
		return 0


