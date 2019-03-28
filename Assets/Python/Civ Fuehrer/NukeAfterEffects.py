### Advanced Nukes
from CvPythonExtensions import *
import CvUtil
import BugUtil
import Caveman2CosmosUtil

BugUtil.fixSets(globals())

gc = CyGlobalContext()

SD_MOD_ID = "Caveman2Cosmos"

g_modEventManager = None
g_eventMgr = None

class NukeAfterEffects:
	def __init__(self, eventManager):

		self.__LOG_IMPROVEMENT = 0

		eventManager.addEventHandler("nukeExplosion", self.onNukeExplosion)
		eventManager.addEventHandler("improvementBuilt", self.onImprovementBuilt)

		global g_modEventManager
		g_modEventManager = self

		global g_eventMgr
		g_eventMgr = eventManager
		self.eventManager = eventManager

	def onImprovementBuilt(self, argsList):
		iImprovement, iX, iY = argsList
		pPlot = CyMap().plot(iX,iY)
		if gc.getInfoTypeForStringWithHiddenAssert("IMPROVEMENT_SANITIZE_WATER") > 0:
			if iImprovement==gc.getInfoTypeForString('IMPROVEMENT_SANITIZE_WATER'):
				pPlot.setTerrainType(Caveman2CosmosUtil.getCoastalType(pPlot), 1, 1)
				pPlot.setImprovementType(-1)
			if self.__LOG_IMPROVEMENT:
				CvUtil.pyPrint('Improvement %s was built at %d, %d' %(gc.getImprovementInfo(iImprovement).getDescription(), iX, iY))

	def onNukeExplosion(self, argsList):
		pPlot, pNukeUnit = argsList
		if gc.getInfoTypeForStringWithHiddenAssert("UNIT_TURN") > 0:
			if pNukeUnit is not None and pNukeUnit.getUnitType() == gc.getInfoTypeForString('UNIT_TURN'):
				if pPlot.isCity():
					iPlayer = pNukeUnit.getOwner()
					pPlayer = gc.getPlayer(iPlayer)
					pCity = pPlot.getPlotCity()
					pPlayer.acquireCity(pCity,False,False)
					iX = pPlot.getX()
					iY = pPlot.getY()
					for iiX in range(iX-1, iX+2, 1):
						for iiY in range(iY-1, iY+2, 1):
							numUnits = pPlot.getNumUnits()
							for e in xrange(numUnits,0,-1):
									pUnit = pPlot.getUnit(e)
									pUnit.kill(False, -1)
							pNukedPlot = CyMap().plot(iiX,iiY)
							if (pNukedPlot.getFeatureType() == gc.getInfoTypeForString('FEATURE_FALLOUT')):
								pNukedPlot.setFeatureType(-1, -1)
			CvUtil.pyPrint('Nuke detonated at %d, %d' %(pPlot.getX(), pPlot.getY()))

		if (gc.getInfoTypeForStringWithHiddenAssert("UNIT_FUSION_NUKE") > 0):
			if (pNukeUnit is not None and pNukeUnit.getUnitType() == gc.getInfoTypeForString('UNIT_FUSION_NUKE')):


				iX = pPlot.getX()
				iY = pPlot.getY()

				for iXLoop in range(iX - 0, iX + 1, 1):
					for iYLoop in range(iY - 0, iY + 1, 1):
							pPlot = CyMap().plot(iXLoop, iYLoop)
							if pPlot.isPeak() or pPlot.isHills():
								pPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
							pPlot.setTerrainType(Caveman2CosmosUtil.getCoastalType(pPlot), 1, 1)

		if (gc.getInfoTypeForStringWithHiddenAssert("UNIT_FUSION_NOVA") > 0):
			if (pNukeUnit is not None and pNukeUnit.getUnitType() == gc.getInfoTypeForString('UNIT_FUSION_NOVA')):


				iX = pPlot.getX()
				iY = pPlot.getY()

				for iXLoop in range(iX - 1, iX + 2, 1):
					for iYLoop in range(iY - 1, iY + 2, 1):
							pPlot = CyMap().plot(iXLoop, iYLoop)
							if (( pPlot.isPeak()==True  ) or (pPlot.isHills()==True)):
								pPlot.setPlotType(PlotTypes.PLOT_LAND, True, True)
							pPlot.setTerrainType(Caveman2CosmosUtil.getCoastalType(pPlot), 1, 1)

		if (gc.getInfoTypeForStringWithHiddenAssert("UNIT_POISON_NUKE") > 0):
			if (pNukeUnit is not None and pNukeUnit.getUnitType() == gc.getInfoTypeForString('UNIT_POISON_NUKE')):
				iX = pPlot.getX()
				iY = pPlot.getY()
				for iXLoop in range(iX - 1, iX + 2, 1):
					for iYLoop in range(iY - 1, iY + 2, 1):
							pPlot = CyMap().plot(iXLoop, iYLoop)
							pPlot.setFeatureType(gc.getInfoTypeForString( "FEATURE_BIOGAS" ), 1)
							if ( pPlot.isWater()==True  ):
								pPlot.setTerrainType(gc.getInfoTypeForString( "TERRAIN_SLIMY_COAST" ), 1, 1)

		if (gc.getInfoTypeForStringWithHiddenAssert("UNIT_POISON_NOVA") > 0):
			if (pNukeUnit is not None and pNukeUnit.getUnitType() == gc.getInfoTypeForString('UNIT_POISON_NOVA')):
				iX = pPlot.getX()
				iY = pPlot.getY()
				for iXLoop in range(iX - 5, iX + 6, 1):
					for iYLoop in range(iY - 5, iY + 6, 1):
							pPlot = CyMap().plot(iXLoop, iYLoop)
							pPlot.setFeatureType(gc.getInfoTypeForString( "FEATURE_PLAGUEGAS" ), 1)
							if ( pPlot.isWater()==True  ):
								pPlot.setTerrainType(gc.getInfoTypeForString( "TERRAIN_SLIMY_OCEAN" ), 1, 1)
