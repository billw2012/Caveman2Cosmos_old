##Basic Damaged Land v1.0 by modifieda4 2011

from CvPythonExtensions import *
import BugUtil


gc = CyGlobalContext()
localText = CyTranslator()

# Globals
iFeatureFallout = -1
aiInvalidTerrain = None

iImprovementDamagedLand = -1
iImprovementWilderness = -1
iImprovementYoungForest = -1
iImprovementPlantForest = -1
iImprovementPlantBamboo = -1
iImprovementPlantSavanna = -1
iImprovementTreeNursery = -1

iFeatureForest = -1
iFeatureBamboo = -1
iFeatureNewForest = -1
iFeatureSavanna = -1

def init():
	global iFeatureFallout, aiInvalidTerrain, iFeatureSavanna, iFeatureForest, iFeatureNewForest, iFeatureBamboo
	global iImprovementDamagedLand, iImprovementWilderness, iImprovementYoungForest,  iImprovementTreeNursery, iImprovementYoungForest
	global iImprovementPlantForest, iImprovementPlantBamboo, iImprovementPlantSavanna

	iFeatureFallout = gc.getInfoTypeForString('FEATURE_FALLOUT')
	iFeatureNewForest = gc.getInfoTypeForString('FEATURE_FOREST_NEW')
	iFeatureForest = gc.getInfoTypeForString('FEATURE_FOREST')
	iFeatureBamboo = gc.getInfoTypeForString('FEATURE_BAMBOO')
	iFeatureSavanna = gc.getInfoTypeForString('FEATURE_SAVANNA')
	
	iImprovementDamagedLand = gc.getInfoTypeForString('IMPROVEMENT_DAMAGED_LAND')
	iImprovementWilderness = gc.getInfoTypeForString('IMPROVEMENT_WILDERNESS')
	iImprovementTreeNursery = gc.getInfoTypeForString('IMPROVEMENT_TREE_NURSERY')
	iImprovementYoungForest = gc.getInfoTypeForString('IMPROVEMENT_YOUNG_FOREST')
	iImprovementPlantForest = gc.getInfoTypeForString('IMPROVEMENT_PLANT_FOREST')
	iImprovementPlantBamboo = gc.getInfoTypeForString('IMPROVEMENT_PLANT_BAMBOO')
	iImprovementPlantSavanna = gc.getInfoTypeForString('IMPROVEMENT_PLANT_SAVANNA')

	aiInvalidTerrain = [gc.getInfoTypeForString('TERRAIN_DESERT'), 
				 gc.getInfoTypeForString('TERRAIN_DUNES'),
				 gc.getInfoTypeForString('TERRAIN_SALT_FLATS'),
				 gc.getInfoTypeForString('TERRAIN_ICE')
				 ]


def onPlotFeatureRemoved(argsList):
	'Plot Feature Removed'
	pPlot = argsList[0]
	iFeatureType = argsList[1]
	pCity = argsList[2] # This can be null

	iTerrain=pPlot.getTerrainType()
	#~ terrainvalid = 1
	iOwner = pPlot.getOwner()
	iX = pPlot.getX()
	iY = pPlot.getY()
	#BugUtil.alert("%s feature removed by %s",iFeatureType,iOwner)
	
	if (iFeatureType==iFeatureFallout):
		if (not iTerrain in aiInvalidTerrain):
			if (not iOwner==-1):
				pPlot.setImprovementType(iImprovementDamagedLand)
				if (iOwner==CyGame().getActivePlayer()):
					CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_DAMAGED_LAND",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Fallout.dds',ColorTypes(8),iX,iY,True,True)

def onImprovementBuilt(argsList):
	'Improvement Built'
	iImprovement, iX, iY = argsList
	pPlot = CyMap().plot(iX,iY)
	iowner = pPlot.getOwner()
	
	#BugUtil.alert("%s improvement built",iImprovement)
	irandom=0
	if iImprovement == iImprovementWilderness:
		irandom = gc.getGame().getSorenRandNum(100,"")
		if irandom > 50:
			pPlot.setFeatureType(iImprovementForest,0)
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WILDERNESS",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),iX,iY,True,True)				
		else:
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_WILDERNESS",()),'AS2D_REVOLTEND',1,'Art/Interface/PlotPicker/Warning.dds',ColorTypes(8),iX,iY,True,True)
		pPlot.setImprovementType(-1)

	
	if(iImprovement==iImprovementTreeNursery):
		pPlot.setFeatureType(iFeatureNewForest, 0)
	if(iImprovement==iImprovementYoungForest):
		if pPlot.getHasFeature(iFeatureNewForest):
			plot.setHasFeature(iFeatureNewForest, False)
		if (iowner==CyGame().getActivePlayer()):
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_YOUNG_FOREST",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),iX,iY,True,True)				

		chance=CyGame().getSorenRandNum(99, "modifieda4")
		lat=pPlot.getLatitude()

		if  lat > 60 or -60 > lat: ## region=="POLAR":
			if (pPlot.getTerrainType()==gc.getInfoTypeForString('TERRAIN_TAIGA')):
				pPlot.setHasfeature(iFeatureForest, True, 2) ##snowy forest
			else:
				pPlot.setHasfeature(iFeatureForest, True, 1) ##evergreen forest
		elif lat > 25 or -25 > lat : ## region=="TEMPERATE":
			if chance <= 50:
				pPlot.setHasfeature(iFeatureForest, True, 0) ##leafy forest
			else:
				pPlot.setFeatureType(iFeatureForest, 1) ##evergreen forest
		else: ## region=="EQUATOR":
			if chance <= 30:
				pPlot.setFeatureType(iFeatureForest, 0) ##leafy forest
			elif chance <= 60:
				pPlot.setFeatureType(iFeatureForest, 1) ##evergreen forest
			else:
				if (pPlot.getTerrainType()==gc.getInfoTypeForString('TERRAIN_GRASS')):
					pPlot.setFeatureType(gc.getInfoTypeForString('FEATURE_JUNGLE'), 0) ##jungle
				else:
					pPlot.setFeatureType(iFeatureForest, 0) ##leafy forest
		pPlot.setImprovementType(-1)
	if (iImprovement==iImprovementPlantForest):
		if pPlot.getHasFeature(iFeatureNewForest):
			plot.setHasFeature(iFeatureNewForest, False)
		if (iowner==CyGame().getActivePlayer()):
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PLANT_FOREST",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),iX,iY,True,True)				
		pPlot.setFeatureType(iFeatureForest, 0)
		pPlot.setImprovementType(-1)
	if (iImprovement==iImprovementPlantBamboo):
		if (iowner==CyGame().getActivePlayer()):
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PLANT_BAMBOO",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),iX,iY,True,True)				
		pPlot.setFeatureType(iFeatureBamboo, 0)
		pPlot.setImprovementType(-1)
	if (iImprovement==iImprovementPlantSavanna):
		if (iowner==CyGame().getActivePlayer()):
			CyInterface().addMessage(CyGame().getActivePlayer(),True,25,CyTranslator().getText("TXT_KEY_MESSAGE_PLANT_SAVANNA",()),'AS2D_DISCOVERBONUS',1,'Art/Interface/Buttons/TerrainFeatures/Forest.dds',ColorTypes(8),iX,iY,True,True)				
		pPlot.setFeatureType(iFeaureSavanna, 0)
		pPlot.setImprovementType(-1)
