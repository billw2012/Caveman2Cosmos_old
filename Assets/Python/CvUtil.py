#
# CvUtil
#
import traceback # for error reporting
import sys # for file ops

# For Civ game code access
from CvPythonExtensions import *

# globals
GC = CyGlobalContext()
localText = CyTranslator()

# For exception handling
SHOWEXCEPTIONS = 1

# Popup context enums, values greater than 999 are reserved for events
#
# DEBUG TOOLS
PopupTypeEntityEventTest = 4
PopupTypeEffectViewer = 5
# HELP SCREENS
PopupTypeMilitaryAdvisor = 103
PopupTypePlayerSelect = 104
# EVENT ID VALUES (also used in popup contexts)
EventEditCity = 5001
EventPlaceObject = 5002
EventAwardTechsAndGold = 5003
EventCityWarning = 5007
EventWBAllPlotsPopup = 5008
EventWBLandmarkPopup = 5009
EventWBScriptPopup = 5010
EventWBStartYearPopup = 5011
EventShowWonder = 5012

# List of unreported Events
SilentEvents = []

# Event IDs
g_nextEventID = 5050
def getNewEventID(name=None, silent=True):
	"""
	Defines a new event and returns its unique ID
	to be passed to BugEventManager.beginEvent(id).
	"""
	global g_nextEventID
	id = g_nextEventID
	g_nextEventID += 1
	if silent:
		addSilentEvent(id)
	return id

def addSilentEvent(id):
	if id not in SilentEvents:
		SilentEvents.append(id)

# Screen IDs
BUG_FIRST_SCREEN = 1000
g_nextScreenID = BUG_FIRST_SCREEN
def getNewScreenID():
	global g_nextScreenID
	id = g_nextScreenID
	g_nextScreenID += 1
	return id

# Popup defines
FONT_CENTER_JUSTIFY=1<<2
FONT_RIGHT_JUSTIFY=1<<1
FONT_LEFT_JUSTIFY=1<<0

def convertToUnicode(s):
	"if the string is non unicode, convert it to unicode by decoding it using 8859-1, latin_1"
	if (isinstance(s, str)):
		return s.decode("latin_1")
	return s

def convertToStr(s):
	"if the string is unicode, convert it to str by encoding it using 8859-1, latin_1"
	if (isinstance(s, unicode)):
		try:
			return s.encode("latin_1")
		except:
			return s
	return s

class RedirectDebug:
	"""Send Debug Messages to Civ Engine"""
	def __init__(self):
		self.m_PythonMgr = CyPythonMgr()
	def write(self, stuff):
		# if str is non unicode and contains encoded unicode data, supply the right encoder to encode it into a unicode object
		if isinstance(stuff, unicode):
			self.m_PythonMgr.debugMsgWide(stuff)
		else:
			self.m_PythonMgr.debugMsg(stuff)

class RedirectError:
	"""Send Error Messages to Civ Engine"""
	def __init__(self):
		self.m_PythonMgr = CyPythonMgr()
	def write(self, stuff):
		# if str is non unicode and contains encoded unicode data, supply the right encoder to encode it into a unicode object
		if isinstance(stuff, unicode):
			self.m_PythonMgr.errorMsgWide(stuff)
		else:
			self.m_PythonMgr.errorMsg(stuff)

def myExceptHook(type, value, tb):
	lines = traceback.format_exception(type, value, tb)
	sys.stderr.write("\n".join(lines))

def pyPrint(stuff):
	# < Revolution Mod Start >
	# Attempt to silence encoding errors for some city names after Python reload
	stuff = 'PY:' + stuff + "\n"
	# < Revolution Mod End >
	sys.stdout.write(stuff)

def pyAssert(cond, msg):
	if cond == False:
		sys.stderr.write(msg)
	assert(cond, msg)

def getOppositeCardinalDirection(dir):
	return (dir + 2) % CardinalDirectionTypes.NUM_CARDINALDIRECTION_TYPES

def shuffle(num, rand):
	"returns a tuple of size num of shuffled numbers"
	piShuffle = [0]*num
	shuffleList(num, rand, piShuffle)	# implemented in C for speed
	return piShuffle

def spawnUnit(iUnit, pPlot, pPlayer):
	pPlayer.initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
	return 1

def findInfoTypeNum(infoGetter, numInfos, typeStr):
	if typeStr == 'NONE':
		return -1
	idx = GC.getInfoTypeForString(typeStr)
	pyAssert(idx != -1, "Can't find type enum for type tag %s" %(typeStr,))
	return idx

def combatDetailMessageBuilder(cdUnit, ePlayer, iChange):
	if cdUnit.iExtraCombatPercent:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_EXTRA_COMBAT_PERCENT",(cdUnit.iExtraCombatPercent * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iAnimalCombatModifierTA:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_ANIMAL_COMBAT",(cdUnit.iAnimalCombatModifierTA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iAIAnimalCombatModifierTA:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_AI_ANIMAL_COMBAT",(cdUnit.iAIAnimalCombatModifierTA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iAnimalCombatModifierAA:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_ANIMAL_COMBAT",(cdUnit.iAnimalCombatModifierAA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iAIAnimalCombatModifierAA:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_AI_ANIMAL_COMBAT",(cdUnit.iAIAnimalCombatModifierAA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iBarbarianCombatModifierTB:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_BARBARIAN_COMBAT",(cdUnit.iBarbarianCombatModifierTB * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iAIBarbarianCombatModifierTB:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_BARBARIAN_AI_COMBAT",(cdUnit.iAIBarbarianCombatModifierTB * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iBarbarianCombatModifierAB:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_BARBARIAN_COMBAT",(cdUnit.iBarbarianCombatModifierAB * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iAIBarbarianCombatModifierAB:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_BARBARIAN_AI_COMBAT",(cdUnit.iAIBarbarianCombatModifierAB * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iPlotDefenseModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_PLOT_DEFENSE",(cdUnit.iPlotDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iFortifyModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_FORTIFY",(cdUnit.iFortifyModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iCityDefenseModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CITY_DEFENSE",(cdUnit.iCityDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iHillsAttackModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_HILLS_ATTACK",(cdUnit.iHillsAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iHillsDefenseModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_HILLS",(cdUnit.iHillsDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iFeatureAttackModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_FEATURE_ATTACK",(cdUnit.iFeatureAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iFeatureDefenseModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_FEATURE",(cdUnit.iFeatureDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iTerrainAttackModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_TERRAIN_ATTACK",(cdUnit.iTerrainAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iTerrainDefenseModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_TERRAIN",(cdUnit.iTerrainDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iCityAttackModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CITY_ATTACK",(cdUnit.iCityAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iDomainDefenseModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CITY_DOMAIN_DEFENSE",(cdUnit.iDomainDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iCityBarbarianDefenseModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CITY_BARBARIAN_DEFENSE",(cdUnit.iCityBarbarianDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iClassDefenseModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_DEFENSE",(cdUnit.iClassDefenseModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iClassAttackModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_ATTACK",(cdUnit.iClassAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iCombatModifierT:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_COMBAT",(cdUnit.iCombatModifierT * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iCombatModifierA:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_COMBAT",(cdUnit.iCombatModifierA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iDomainModifierA:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_DOMAIN",(cdUnit.iDomainModifierA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iDomainModifierT:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_DOMAIN",(cdUnit.iDomainModifierT * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iAnimalCombatModifierA:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_ANIMAL_COMBAT",(cdUnit.iAnimalCombatModifierA * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iAnimalCombatModifierT:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_ANIMAL_COMBAT",(cdUnit.iAnimalCombatModifierT * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iRiverAttackModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_RIVER_ATTACK",(cdUnit.iRiverAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

	if cdUnit.iAmphibAttackModifier:
		msg=localText.getText("TXT_KEY_COMBAT_MESSAGE_CLASS_AMPHIB_ATTACK",(cdUnit.iAmphibAttackModifier * iChange,))
		CyInterface().addCombatMessage(ePlayer,msg)

def combatMessageBuilder(cdAttacker, cdDefender, iCombatOdds):
	combatMessage = ""
	if cdAttacker.eOwner == cdAttacker.eVisualOwner:
		combatMessage += "%s's " %(GC.getPlayer(cdAttacker.eOwner).getName(),)
	combatMessage += "%s (%.2f)" %(cdAttacker.sUnitName,cdAttacker.iCurrCombatStr/100.0,)
	combatMessage += " " + localText.getText("TXT_KEY_COMBAT_MESSAGE_VS", ()) + " "
	if cdDefender.eOwner == cdDefender.eVisualOwner:
		combatMessage += "%s's " %(GC.getPlayer(cdDefender.eOwner).getName(),)
	combatMessage += "%s (%.2f)" %(cdDefender.sUnitName,cdDefender.iCurrCombatStr/100.0,)
	CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
	CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
	combatMessage = "%s %.1f%%" %(localText.getText("TXT_KEY_COMBAT_MESSAGE_ODDS", ()),iCombatOdds/10.0,)
	CyInterface().addCombatMessage(cdAttacker.eOwner,combatMessage)
	CyInterface().addCombatMessage(cdDefender.eOwner,combatMessage)
	combatDetailMessageBuilder(cdAttacker,cdAttacker.eOwner,-1)
	combatDetailMessageBuilder(cdDefender,cdAttacker.eOwner,1)
	combatDetailMessageBuilder(cdAttacker,cdDefender.eOwner,-1)
	combatDetailMessageBuilder(cdDefender,cdDefender.eOwner,1)

def stripLiterals(txt, literal):
	# The literal argument can be: "font", "color", "link", etc. Caps lock does matter.
	start = "<%s=" % literal
	txt = txt.replace("</%s>" % literal, "")
	i1 = txt.find(start)
	if i1 > -1:
		while i1 > -1:
			i2 = txt.find(">", i1)
			txt = txt[:i1] + txt[i2+1:]
			i1 = txt.find(start)
	return txt