## Sid Meier's Civilization 4
## Copyright Firaxis Games 2006
## 
## CvEventManager
## This class is passed an argsList from CvAppInterface.onEvent
## The argsList can contain anything from mouse location to key info
## The EVENTLIST that are being notified can be found 


from CvPythonExtensions import *
import CvUtil
import CvDebugTools
import sys

## Natural Wonders ##
import NaturalWonders
## Natural Wonders ##


gc = CyGlobalContext()
localText = CyTranslator()

def onPlotRevealed(argsList):
	'Plot Revealed'
	pPlot = argsList[0]
	iTeam = argsList[1]
	
## Natural Wonders Start ##
	NaturalWonders.NaturalWonders().checkReveal(pPlot, iTeam)
## Natural Wonders End ##
		
		
# def onCityBuilt(argsList):
	# 'City Built'
	# city = argsList[0]

# Natural Wonders Start ##
	# NaturalWonders.NaturalWonders().placeWonderBuilding(city)
# Natural Wonders End ##
		
# def onCityRazed(argsList):
	# 'City Razed'
	# city, iPlayer = argsList
	# iOwner = city.findHighestCulture()
# Natural Wonders Start ##
	# NaturalWonders.NaturalWonders().findNewCity(city)
# Natural Wonders End ##
