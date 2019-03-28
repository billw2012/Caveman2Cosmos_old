import CvUtil
import CvScreenEnums
from CvPythonExtensions import *
gc = CyGlobalContext()

class GreatPeopleScreen:

	def __init__(self):
		self.GreatPeople = {	"UNIT_PROPHET": "ART_DEF_BACKGROUND_PROPHET",
					"UNIT_ARTIST": "ART_DEF_BACKGROUND_ARTIST",
					"UNIT_SCIENTIST": "ART_DEF_BACKGROUND_SCIENTIST",
					"UNIT_MERCHANT": "ART_DEF_BACKGROUND_MERCHANT",
					"UNIT_ENGINEER": "ART_DEF_BACKGROUND_ENGINEER",
					"UNIT_GREAT_GENERAL": "ART_DEF_BACKGROUND_GGENERAL",
					"UNIT_GREAT_ADMIRAL": "ART_DEF_BACKGROUND_ADMIRAL",
					"UNIT_GREAT_HUNTER": "ART_DEF_BACKGROUND_HUNTER",
					"UNIT_GREAT_SPY": "ART_DEF_BACKGROUND_SPY",
					"UNIT_GREAT_STATESMAN": "ART_DEF_BACKGROUND_STATESMAN",					
					"UNIT_GREAT_DOCTOR": "ART_DEF_BACKGROUND_DOCTOR"}
				
	def interfaceScreen(self, pUnit, iPlayer):
		screen = CyGInterfaceScreen("Great People Screen", CvScreenEnums.GREAT_PEOPLE_SCREEN)
		if CyGame().isPitbossHost(): return
		sUnitName = pUnit.getNameNoDesc()
		if sUnitName == "": return

		self.W_MAIN_PANEL = 660
		self.H_MAIN_PANEL = 452
		self.X_MAIN_PANEL = (screen.getXResolution()/2) - (self.W_MAIN_PANEL/2)
		self.Y_MAIN_PANEL = 70
		
		self.iMarginSpace = 15
		
		self.W_EXIT = 120
		self.H_EXIT = 30
		self.X_EXIT = (screen.getXResolution() - self.W_EXIT) /2
		self.Y_EXIT = 466
		
		self.W_PERSON_PORTRAIT = 220
		self.H_PERSON_PORTRAIT = 360
		self.X_PERSON_PORTRAIT = self.X_MAIN_PANEL + self.iMarginSpace
		self.Y_PERSON_PORTRAIT =  self.Y_MAIN_PANEL + self.iMarginSpace

		self.W_BACKGROUND = 660
		self.H_BACKGROUND = 452
		self.X_BACKGROUND = self.X_MAIN_PANEL
		self.Y_BACKGROUND =  self.Y_MAIN_PANEL
		
		self.X_TEXT_PANEL = self.X_PERSON_PORTRAIT + self.W_PERSON_PORTRAIT + self.iMarginSpace
		self.Y_TEXT_PANEL = self.Y_PERSON_PORTRAIT + 95
		self.W_TEXT_PANEL = 355
		self.H_TEXT_PANEL = 250

		iType = pUnit.getUnitType()
		Info = gc.getUnitInfo(iType)
		sGreat = ""
		for i in xrange(Info.getNumUnitNames()):
			sName = Info.getUnitNames(i)
			if CyTranslator().getText(sName, ()) == sUnitName:
				sGreat = sName[8:]
				break

		if sGreat:
			sPortrait = ""
			sIcon = ""
			sArtDef = CyArtFileMgr().getInterfaceArtInfo("ART_DEF_" + sGreat)
			if sArtDef:
				sPortrait = sArtDef.getPath()
			sBack = ""
			sType = Info.getType()
			if sType in self.GreatPeople:
				sIcon = self.GreatPeople[sType]
			sArtDef= CyArtFileMgr().getInterfaceArtInfo(sIcon)
			if sArtDef:
				sBack = sArtDef.getPath()
			sQuote = CyTranslator().getText("TXT_KEY_" + sGreat + "_QUOTE", ())
			sText = "<color=136,94,43,255>" + u"<font=2b>" + CyTranslator().getText("TXT_KEY_" + sGreat + "_PEDIA", ())
		else:
			return

		screen.showScreen(PopupStates.POPUPSTATE_QUEUED, False)
		screen.showWindowBackground(False)
		screen.addPanel("MainPanel", "", "", true, true, self.X_MAIN_PANEL, self.Y_MAIN_PANEL, self.W_MAIN_PANEL, self.H_MAIN_PANEL, PanelStyles.PANEL_STYLE_MAIN )
		screen.addDDSGFC("ScreenBackground", sBack, self.X_BACKGROUND, self.Y_BACKGROUND, self.W_BACKGROUND, self.H_BACKGROUND, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addPanel("GreatPersonTextPanel", "", "", true, true, self.X_TEXT_PANEL, self.Y_TEXT_PANEL, self.W_TEXT_PANEL, self.H_TEXT_PANEL, PanelStyles.PANEL_STYLE_MAIN)
		screen.setStyle("GreatPersonTextPanel", "Panel_TechDiscover_Style")
		screen.addDDSGFC("GreatPersonPortrait", sPortrait, self.X_PERSON_PORTRAIT, self.Y_PERSON_PORTRAIT, self.W_PERSON_PORTRAIT, self.H_PERSON_PORTRAIT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		screen.addMultilineText("GreatPersonText", sText, self.X_TEXT_PANEL + self.iMarginSpace, self.Y_TEXT_PANEL, self.W_TEXT_PANEL - (self.iMarginSpace * 1), self.H_TEXT_PANEL - (self.iMarginSpace * 1), WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
		screen.setButtonGFC("Exit", CyTranslator().getText("TXT_KEY_SCREEN_CONTINUE", ()), "", self.X_EXIT, self.Y_EXIT, self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD )

	def handleInput( self, inputClass ):
		return 0
	
	def update(self, fDelta):
		return