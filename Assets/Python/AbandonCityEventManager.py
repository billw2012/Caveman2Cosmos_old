##-------------------------------------------------------------------
## Modified from Abandon Raze City by unknown, Bhruic, Nemo, OrionVetran
##  by Dancing Hoskuld with a great deal of help from EmperorFool and Zappara
##  to work in, with and under BUG
##-------------------------------------------------------------------
##
## Things that could be done to improve this mod making it interact with the main mod in a more generic fashon.
## 1. replace the English language stuff with the correct language translations in the text file.
##-------------------------------------------------------------------
##
## To get this working in any mod you need to
## 1. put 	<load mod="Abandon City Mod"/>	in the init.xml in the Python/Config directory
##
## Modders:- If you want any special events when a city is abandoned add them to your OnCityRazed event.
##		This mod calls that event.
##  In RoM Holy Shrines are not world wonders a fix to reflect this is in the code it should have no effect
##    on other mods but the test can be commented out if needs be.
##
##-------------------------------------------------------------------
##
## Changes
##  April 2009
##	A moders section of this code now allows a single place for the setting of the "parameters"
##	 - produce just workers or settlers and workers
##	 - produce 1 worker for every X popuation in the city
##	 - produce 1 settler fo every X population in the city with 1 worker for every Y in the remainder
##   Sell buildings rather than demolish them.  Thanks Zappara
##   Unhappiness from selling religious buildings +1 unhappy for x turns.  Where x depends on game speed.
##   Can not abandon last city.
##   Can not sell free buildings however they need to appear in the list for this program to work.
##
##   Note. If you only have one city and it has no buildings then Ctrl-A will appear not to work.  This was
##   done to to stop a CDT which could be caused otherwise.  Besides there is nothing to sell and you can't
##   abandon your only city.
##   - I had made a typo in the check for this - it is now fixed - thanks Zappara
##
## Late April 2009
##  Civ specific unique units for workers and settlers are now produced when appropriate. - thanks Zappara
##  Percentage of building production cost is now in the parameter section so modders can change it
##    currently set at the Rise of mankind default of 20%.  Popup header text now reflects this percentage.
##  More of the text supports language even if I have not put the language stuff there yet.
##  Fixed to support modular buildings. - thanks Zappara
##
## September 2009
## 	Minor coding changes to make the code cleaner.
##		Includes removing excess coments, define globals once, and put parameter for obsolete reduction.
##	Stopped putting free buildings in the list.  
##		The way the popup works is it puts the items in the list in the order supplied (text and index).
##		It displays (text) and returns (index) for the selected item.
##
##-------------------------------------------------------------------
##
## Potential changes
## 1. has an .ini file (AbandonCity.INI) to hold parameters
##	 - mod is active/inactive
##     - only abandon city (no selling of buildings)
##
## 2. buildings in albhabetical order in the list.
##	
##
## ------------------------------------------
## Decided not to generate upgraded settler units as these could then be settled and the free buildings sold off.
##	- obsolete decision now that selling free buildings gives no money.
##	- further obsolete since now we do not present free buildings to be sold :)
##
## Decided to have the population parameters in the code for modders rather than letting the player change them ad hoc.
##
## Decided that you can sell obsolete buildings.  Just because they are obsolete does not mean that they are not having an effect.



from CvPythonExtensions import *
import CvUtil
import CvEventInterface
import Popup as PyPopup
import BugCore
import BugUtil
import SdToolKit
import string

# BUG - Mac Support - start
BugUtil.fixSets(globals())
# BUG - Mac Support - end

# globals

SD_MOD_ID = "AbandonCity"

ABANDON_CITY_DEMOLISH_BUILDING_EVENT_ID = CvUtil.getNewEventID("AbandonCity.Active")

gc = CyGlobalContext()
localText = CyTranslator()

#AbandonCityOpt = BugCore.game.AbandonCity
g_modEventManager = None
g_eventMgr = None

# parameters for modders.
bSettlersAndWorkers = True	# True means settlers and workers. False for just workers.
iPopulationForSettlers = 10	# If producing settlers then produce 1 per each full city population of iPopulationForSettlers
iPopulationForWorkers = 3	# produce 1 per each full city population of iPopulationForWorkers. This is left over population after producing settlers.
g_CostFraction = 0.14		# Percentage of building cost converted to money.
g_ReductionForObsolete = 2	# Amount the gold being returned is divided by if the building is obsolete.

def onStartAbandonCity(argsList):
	g_modEventManager.onStartAbandonCity(argsList)

class AbandonCityEventManager:
	def __init__(self, eventManager):
		eventManager.addEventHandler("StartAbandonCity", self.onStartAbandonCity)
		eventManager.addEventHandler("ModNetMessage", self.onModNetMessage)

		global g_modEventManager
		g_modEventManager = self

		global g_eventMgr
		g_eventMgr = eventManager
		self.eventManager = eventManager

		eventManager.setPopupHandler(ABANDON_CITY_DEMOLISH_BUILDING_EVENT_ID, ("AbandonCity.Active", self.__eventAbandonCityDestroyBuildingApply, self.__eventAbandonCityDestroyBuildingBegin))

	def onModNetMessage(self, argsList):
		protocol, data1, data2, data3, data4 = argsList
		if protocol == 900:
			pPlayer = gc.getPlayer(data4)
			pCity = pPlayer.getCity(data1)
			iX = pCity.getX()
			iY = pCity.getY()
			pPlayer.initUnit(data2, iX, iY, UnitAITypes.NO_UNITAI, DirectionTypes.NO_DIRECTION)
		elif protocol == 901:
			pPlayer = gc.getPlayer(data4)
			pCity = pPlayer.getCity(data1)
			pCity.kill()
		elif protocol == 902:
			pPlayer = gc.getPlayer(data4)
			pCity = pPlayer.getCity(data1)
			pCity.setNumRealBuilding(data2, 0)
			pPlayer.changeGold(data3)
			CyInterface().setDirty(InterfaceDirtyBits.CityScreen_DIRTY_BIT, True)
			CyInterface().setDirty(InterfaceDirtyBits.SelectionButtons_DIRTY_BIT, True)
			if (gc.getBuildingInfo(data2).getReligionType() >= 0):
				pCity.changeHurryAngerTimer(pCity.flatHurryAngerLength())
				if (not gc.getGame().isOption(GameOptionTypes.GAMEOPTION_NO_REVOLUTION)):
					pCity.changeRevolutionIndex(100)

	def onStartAbandonCity(self, argsList):
		# Have keypress from handler - return 1 if the event was consumed
		# Get the player details and game options.

		if CyInterface().isCityScreenUp():
			pHeadSelectedCity = CyInterface().getHeadSelectedCity()
			iOwner = pHeadSelectedCity.getOwner()
			if iOwner == gc.getGame().getActivePlayer():
				pPlayer = gc.getPlayer(iOwner)
				## if player only has one city and that city has no buildings then do not display popup as it can cause a CDT
				if not pHeadSelectedCity.getNumBuildings() and pPlayer.getNumCities() == 1:
					return 0
				g_eventMgr.beginEvent(ABANDON_CITY_DEMOLISH_BUILDING_EVENT_ID)
				return 1
		return 0


	def __eventAbandonCityDestroyBuildingBegin(self, argsList):
		# Get player and city details. Set up headings etc.
		# Display appropriate dialogue.
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()
		pPlayer = gc.getPlayer(pHeadSelectedCity.getOwner())

		szheader = BugUtil.getPlainText("TXT_KEY_ABANDON_CITY_HEADER1")
		szheader += " " + u"%d" %(g_CostFraction * 100) + BugUtil.getPlainText("TXT_KEY_ABANDON_CITY_HEADER2")

		abandoncity = BugUtil.getPlainText("TXT_KEY_ABANDON_CITY")
		ok = BugUtil.getPlainText("TXT_KEY_MAIN_MENU_OK")
		cancel = BugUtil.getPlainText("TXT_KEY_POPUP_CANCEL")
		popup = PyPopup.PyPopup(ABANDON_CITY_DEMOLISH_BUILDING_EVENT_ID, EventContextTypes.EVENTCONTEXT_ALL)
		popup.setHeaderString(szheader)
		popup.createPullDown()

		# find out what the gamespeed building cost modifier is
		# and adjust construct modifier also with building production percent game define
		fConstructModifier = gc.getDefineINT("BUILDING_PRODUCTION_PERCENT")/100.0
		fConstructModifier *= gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getConstructPercent()/100.0
		fConstructModifier *= gc.getHandicapInfo(pPlayer.getHandicapType()).getConstructPercent()/100.0
		fConstructModifier *= gc.getEraInfo(pPlayer.getCurrentEra()).getConstructPercent()/100.0
		self.fConstructModifier = fConstructModifier

		#Find out how many valid buildings exist
		iNumValidBuildings = 0
		for iBuilding in range(gc.getNumBuildingClassInfos()):
			iType = gc.getBuildingClassInfo(iBuilding).getDefaultBuildingIndex()
			if (iType > -1 and pHeadSelectedCity.getNumRealBuilding(iType) > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iType).getBuildingClassType()) and not gc.getBuildingInfo(iType).getGlobalReligionCommerce() > 0):
				# Only put non-free buildings in the list
				if (not pPlayer.isBuildingFree(iType) and gc.getBuildingInfo(iType).getProductionCost() != -1 and not gc.getBuildingInfo(iType).isAutoBuild() ):
					iNumValidBuildings += 1
		#create the list
		buildingList = [(0,0)] * iNumValidBuildings
		i = 0
		for iBuilding in range(gc.getNumBuildingClassInfos()):
			iType = gc.getBuildingClassInfo(iBuilding).getDefaultBuildingIndex()
			# RoM 2.7 added check for Holy Shrines so that player can't demolish them, those aren't Great Wonders in RoM
			if (iType > -1 and pHeadSelectedCity.getNumRealBuilding(iType) > 0 and not isLimitedWonderClass(gc.getBuildingInfo(iType).getBuildingClassType()) and not gc.getBuildingInfo(iType).getGlobalReligionCommerce() > 0):
				# Only put non-free buildings in the list
				if (not pPlayer.isBuildingFree(iType) and gc.getBuildingInfo(iType).getProductionCost() != -1  and not gc.getBuildingInfo(iType).isAutoBuild()):
					buildingList[i] = (gc.getBuildingInfo(iType).getDescription(), iType)
					i += 1
		#sort alphabetically
		buildingList.sort()

		# Populate list box with non-free buildings
		CyTeam = gc.getTeam(pPlayer.getTeam())
		for item in buildingList:
			iType = item[1]
			# Figure out the gold to be paid for the building.
			# Note that this code is repeated when the building is actually sold.
			iGoldBack = int(gc.getBuildingInfo(iType).getProductionCost() * fConstructModifier * g_CostFraction)

			# If building is obsolete, give only half sum back
			obsoleteTech = gc.getBuildingInfo(iType).getObsoleteTech()
			if CyTeam.isHasTech(obsoleteTech):
				iGoldBack = int(iGoldBack/g_ReductionForObsolete)

			# Build up text to display in the list box
			szBuilding = gc.getBuildingInfo(iType).getDescription()
			szBuilding += " (" + u"%d " %(iGoldBack) + localText.getText("TXT_KEY_COMMERCE_GOLD", ())
			# Add unhappiness text here
			if gc.getBuildingInfo(iType).getReligionType() >= 0 : # religious building
				szBuilding += ", " + localText.getText("TXT_KEY_ABANDON_UNHAPPINESS", ()) #+  u"%c" % CyGame().getSymbolID(FontSymbols.UNHAPPY_CHAR)
			szBuilding += ")"

			popup.addPullDownString(szBuilding, iType)

		# Only allow abandonment of city if there is more than one city
		if pPlayer.getNumCities() > 1 :
			popup.addPullDownString(abandoncity, gc.getNumBuildingInfos())

		popup.addButton(ok)
		popup.addButton(cancel)
		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)
		return

	def __eventAbandonCityDestroyBuildingApply(self, playerID, userData, popupReturn):
		pPlayer = gc.getPlayer(playerID)
		CyTeam = gc.getTeam(pPlayer.getTeam())
		pHeadSelectedCity = CyInterface().getHeadSelectedCity()

		if not popupReturn.getButtonClicked():
			if popupReturn.getSelectedPullDownValue(0) == gc.getNumBuildingInfos():
				ix = pHeadSelectedCity.getX()
				iy = pHeadSelectedCity.getY()
				iPopulation = pHeadSelectedCity.getPopulation()

				# Generate the units
				iWorker = gc.getInfoTypeForString("UNIT_GATHERER")
				iSettler = gc.getInfoTypeForString("UNIT_TRIBE")
				if CyTeam.isHasTech(gc.getInfoTypeForString("TECH_SEDENTARY_LIFESTYLE")):
					iWorker = gc.getInfoTypeForString("UNIT_WORKER")
					iSettler = gc.getInfoTypeForString("UNIT_SETTLER")

				iUniqueWorkerUnit = iWorker
				iUniqueSettlerUnit = iSettler

				# if settlers and workers
				if bSettlersAndWorkers:
					isettlers = iPopulation/iPopulationForSettlers
					iworkers = (iPopulation - iPopulationForSettlers * isettlers)/iPopulationForWorkers
				else:
					isettlers = 0
					iworkers = iPopulation/iPopulationForWorkers

				for i in range(0,iworkers):
					CyMessageControl().sendModNetMessage(900, pHeadSelectedCity.getID(), iUniqueWorkerUnit, 0, playerID)
				for i in range(0,isettlers):
					CyMessageControl().sendModNetMessage(900, pHeadSelectedCity.getID(), iUniqueSettlerUnit, 0, playerID)

				# Abandon the City
				CyMessageControl().sendModNetMessage(901, pHeadSelectedCity.getID(), 0, 0, playerID)
				CyAudioGame().Play2DSound("AS2D_DISCOVERBONUS")

			else:
				iBuildingType = popupReturn.getSelectedPullDownValue(0)
				civ = gc.getCivilizationInfo(pHeadSelectedCity.getCivilizationType())
				iType = civ.getCivilizationBuildings(gc.getBuildingInfo(iBuildingType).getBuildingClassType())

				iGoldBack = int(gc.getBuildingInfo(iType).getProductionCost() * self.fConstructModifier * g_CostFraction)

				if CyTeam.isHasTech(gc.getBuildingInfo(iType).getObsoleteTech()):
					iGoldBack = int(iGoldBack/g_ReductionForObsolete)

				CyMessageControl().sendModNetMessage(902, pHeadSelectedCity.getID(), iType, iGoldBack, playerID)
				CyAudioGame().Play2DSound("AS2D_DISCOVERBONUS")
