# # Sid Meier's Civilization 4
# # Copyright Firaxis Games 2007
# # ImmigrationGameUtils

import CvUtil
from CvPythonExtensions import *
import CvEventInterface
import CvGameUtils
import Popup as PyPopup
import PyHelpers
import GodsOfOld
import Immigration

# globals
gc = CyGlobalContext()
PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo
PyCity = PyHelpers.PyCity
PyGame = PyHelpers.PyGame

# Immigration Mod By Orion Veteran
# Modular Python to eliminate Merging 
class ImmigrationGameUtils:
	#~ def canTrain(self,argsList):
		#~ # Requires the Can Train call back to be enabled in the PythonCallbackDefines.xml file
		#~ pCity = argsList[0]
		#~ eUnit = argsList[1]
		#~ bContinue = argsList[2]
		#~ bTestVisible = argsList[3]
		#~ bIgnoreCost = argsList[4]
		#~ bIgnoreUpgrades = argsList[5]
#~ # Immigration Mod
		#~ iOwner = pCity.getOwner()
		#~ pPlayer = gc.getPlayer(iOwner)
		#~ iImmigrant = gc.getInfoTypeForString("UNIT_IMMIGRANT")
		
		#~ if eUnit == iImmigrant:
			#~ if Immigration.cityCanTrainImmigrant(pCity):			
				#~ return True
#~ # End Immigration Mod
		
		#~ return False
		
	#~ def cannotTrain(self,argsList):
		#~ # Requires the Cannot Train call back to be enabled in the PythonCallbackDefines.xml file
		#~ pCity = argsList[0]
		#~ eUnit = argsList[1]
		#~ bContinue = argsList[2]
		#~ bTestVisible = argsList[3]
		#~ bIgnoreCost = argsList[4]
		#~ bIgnoreUpgrades = argsList[5]
#~ # Immigration Mod
		#~ iOwner = pCity.getOwner()
		#~ pPlayer = gc.getPlayer(iOwner)
		#~ iImmigrant = gc.getInfoTypeForString("UNIT_IMMIGRANT")
		
		#~ if eUnit == iImmigrant:
			#~ if not Immigration.cityCanTrainImmigrant(pCity):			
				#~ return True
#~ # End Immigration Mod
		
		#~ return False

	#~ def AI_chooseProduction(self,argsList):
		#~ pCity = argsList[0]
#~ # Immigration Mod	
		#~ iOwner = pCity.getOwner( )
		#~ AIpPlayer = gc.getPlayer(iOwner)		
		#~ ImmProdChance = Immigration.getImmigrantProductionChance(AIpPlayer)
		#~ iImmigrant = gc.getInfoTypeForString("UNIT_IMMIGRANT")
		#~ iUnitToProduce = iImmigrant
		#~ ProduceImmigrant = True
							
		#~ #CyInterface().addMessage(CyGame().getActivePlayer(),True,25,'Message 2','AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),0,0,False,False)
		#~ if pCity.canTrain(iUnitToProduce, 0, 0):			
			#~ lUnits = PyPlayer(AIpPlayer.getID()).getUnitList()
			#~ for iUnit in range(len(lUnits)):				
				#~ # if there are any iUnitToProduce, don't Build one
				#~ if AIpPlayer.getUnit(lUnits[iUnit].getID()).getUnitType() == iUnitToProduce:
					#~ #CyInterface().addImmediateMessage("A", "")
					#~ ProduceImmigrant = False
					#~ return False
			
			
			#~ if ProduceImmigrant:
				#~ if Immigration.doRandumChance(ImmProdChance):
					#~ # Makes the City produce the unit
					#~ pCity.pushOrder(OrderTypes.ORDER_TRAIN, iUnitToProduce, -1, False, False, False, True)
					#~ #CyInterface().addImmediateMessage("Order Successful", "")
					#~ #gc.getMap( ).plot( pCity.getX( ), pCity.getY( ) ).getPlotCity( ).pushOrder( OrderTypes.ORDER_TRAIN, iUnitToProduce, -1, False, False, False, True )
					#~ return True
#~ # End Immigration Mod

		#~ return False
	
	def AI_unitUpdate(self,argsList):
		pUnit = argsList[0]
# Orion's Inquisition Mod
		iOwner = pUnit.getOwner()
		AIpPlayer = gc.getPlayer(iOwner)
		pUnitType = pUnit.getUnitType()
		iImmigrant = gc.getInfoTypeForString("UNIT_IMMIGRANT")
		
		if pUnitType == iImmigrant:
			if AIpPlayer.isAlive() and not AIpPlayer.isHuman() and not AIpPlayer.isNPC():
				intCity = Immigration.getLeastPopulatedCity(iOwner)
				if intCity != -1:
					MigrationCity = AIpPlayer.getCity(intCity)
					Immigration.doImmigrantPlacementAI(pUnit, MigrationCity)
					return True
# End Immigration Mod

		return False
	
	
	#~ def getWidgetHelp(self, argsList):
		#~ eWidgetType, iData1, iData2, bOption = argsList
#~ # Immigration Mod
		
		#~ if iData1 == 680:
			#~ return CyTranslator().getText("TXT_KEY_JOIN_CITY_MOUSE_OVER", ())
		
		#~ return u""
		
#~ # End Immigration Mod









