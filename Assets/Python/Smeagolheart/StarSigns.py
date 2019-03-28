## Sid Meier's Civilization 4
## Copyright Firaxis Games 2005
##
## Star Sign Picker by Smeagolheart
##

from CvPythonExtensions import *
import sys
import PyHelpers
import CvUtil
import BugUtil
#~ import Popup as PyPopup
#import array

# globals
gc = CyGlobalContext()
localText = CyTranslator()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

gaiStarSigns= None
gasStarSignIcons = None

def init():
	BugUtil.debug("Initializing StarSigns")
	
	global gaiStarSigns, gasStarSignIcons
	
	gaiStarSigns = [gc.getInfoTypeForString("PROMOTION_AQUARIUS"),
				gc.getInfoTypeForString("PROMOTION_ARIES"),
				gc.getInfoTypeForString("PROMOTION_CANCER"),
				gc.getInfoTypeForString("PROMOTION_CAPRICORN"),
				gc.getInfoTypeForString("PROMOTION_GEMINI"),
				gc.getInfoTypeForString("PROMOTION_LEO"),
				gc.getInfoTypeForString("PROMOTION_LIBRA"),
				gc.getInfoTypeForString("PROMOTION_PISCES"),
				gc.getInfoTypeForString("PROMOTION_SAGITTARIUS"),
				gc.getInfoTypeForString("PROMOTION_SCORPIO"),
				gc.getInfoTypeForString("PROMOTION_TAURUS"),
				gc.getInfoTypeForString("PROMOTION_VIRGO"),
			]
	
	gasStarSignIcons = ["Art/Interface/Buttons/promotions/StarSigns/AQUARIUS.dds",
					"Art/Interface/Buttons/promotions/StarSigns/ARIES.dds",	
					"Art/Interface/Buttons/promotions/StarSigns/CANCER.dds",
					"Art/Interface/Buttons/promotions/StarSigns/CAPRICORN.dds",
					"Art/Interface/Buttons/promotions/StarSigns/GEMINI.dds",
					"Art/Interface/Buttons/promotions/StarSigns/LEO.dds",
					"Art/Interface/Buttons/promotions/StarSigns/LIBRA.dds",
					"Art/Interface/Buttons/promotions/StarSigns/PICES.dds",
					"Art/Interface/Buttons/promotions/StarSigns/SAGITTARIUS.dds",
					"Art/Interface/Buttons/promotions/StarSigns/SCORPIO.dds",
					"Art/Interface/Buttons/promotions/StarSigns/TAURUS.dds",
					"Art/Interface/Buttons/promotions/StarSigns/VIRGO.dds"
				]
			
def onUnitCreated(self, argsList):
	pUnit = argsList[0]

	BugUtil.debug("StarSigns - onUnitCreate")
	chance = CyGame().getSorenRandNum(99, "Random to get a Sign") #returns a number 0-100
		
	if chance == 7:  ### Lucky 7 Lol -> so 1% chance of getting a "sign promotion" ###
		chance2 = CyGame().getSorenRandNum(11, "Random Sign Picker") # returns a number 0-11
		pUnit.setHasPromotion(gaiStarSigns[chance2], True)
		
		pPlayer = PyPlayer(pUnit.getOwner())
		pPID = pPlayer.getID()
		iXa = pUnit.getX()
		iYa = pUnit.getY()

		strMessage = localText.getText("TXT_KEY_MESSAGE_STARSIGN_CREATE")
		szIcon = gasStarSignIcons[chance2]
		CyInterface().addMessage(pPID, False, 15, strMessage, "", 0, szIcon, ColorTypes(44), iXa, iYa, True,True)

def onUnitBuilt(argsList):
	'Unit Completed'
	pCity = argsList[0]
	pUnit = argsList[1]
	pPlayer = PyPlayer(pCity.getOwner())
	iplayer = gc.getPlayer(pCity.getOwner())
		
	BugUtil.debug("StarSigns - onUnitBuilt")
# Star Signs by Smeagolheart Start
	
	chance = CyGame().getSorenRandNum(99, "Random to get a Sign")
	
	if chance == 7:  ### Lucky 7 Lol -> so 1% chance of getting a "sign promotion" ###
		chance2 = CyGame().getSorenRandNum(11, "Random Sign Picker")

		pUnit.setHasPromotion(gaiStarSigns[chance2], True)
		szIcon = gasStarSignIcons[chance2]

		pPID = pPlayer.getID()
		iXa = pUnit.getX()
		iYa = pUnit.getY()

		strMessage = localText.getText("TXT_KEY_MESSAGE_STARSIGN_BUILD",(pCity.getName(),))
		szIcon = gasStarSignIcons[chance2]
		CyInterface().addMessage(pPID, False, 15, strMessage, "", 0, szIcon, ColorTypes(44), iXa, iYa, True,True)
			
# Star Signs by Smeagolheart End
				
			
