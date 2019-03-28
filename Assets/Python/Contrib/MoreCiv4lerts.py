## MoreCiv4lerts
## From HOF MOD V1.61.001
## Based upon Gillmer J. Derge's Civ4lerts.py

from CvPythonExtensions import *
import BugCore
import PlayerUtil
import TradeUtil

# BUG - Mac Support - start
import BugUtil
BugUtil.fixSets(globals())
# BUG - Mac Support - end

GC = CyGlobalContext()
localText = CyTranslator()

class MoreCiv4lerts:

	def __init__(self, eventManager):
		## Init event handlers
		MoreCiv4lertsEvent(eventManager)

class AbstractMoreCiv4lertsEvent(object):

	def __init__(self, eventManager, *args, **kwargs):
		super(AbstractMoreCiv4lertsEvent, self).__init__(*args, **kwargs)

	def _addMessageNoIcon(self, iPlayer, message, iColor=-1):
		#Displays an on-screen message with no popup icon.
		self._addMessage(iPlayer, message, None, -1, -1, False, False, iColor)

	def _addMessage(self, iPlayer, szString, szIcon, iFlashX, iFlashY, bOffArrow, bOnArrow, iColor):
		#Displays an on-screen message.
		eventMessageTimeLong = GC.getDefineINT("EVENT_MESSAGE_TIME_LONG")
		CyInterface().addMessage(iPlayer, True, eventMessageTimeLong, szString, None, 0, szIcon, ColorTypes(iColor), iFlashX, iFlashY, bOffArrow, bOnArrow)

class MoreCiv4lertsEvent(AbstractMoreCiv4lertsEvent):

	def __init__(self, eventManager, *args, **kwargs):
		super(MoreCiv4lertsEvent, self).__init__(eventManager, *args, **kwargs)

		eventManager.addEventHandler("BeginActivePlayerTurn", self.onBeginActivePlayerTurn)
		eventManager.addEventHandler("cityAcquired", self.OnCityAcquired)
		eventManager.addEventHandler("cityBuilt", self.OnCityBuilt)
		eventManager.addEventHandler("cityRazed", self.OnCityRazed)
		eventManager.addEventHandler("cityLost", self.OnCityLost)
		eventManager.addEventHandler("GameStart", self.reset)
		eventManager.addEventHandler("OnLoad", self.reset)

		self.eventMgr = eventManager
		self.options = BugCore.game.MoreCiv4lerts
		self.reset()

	def reset(self, argsList=None):
		self.CurrAvailTechTrades = {}
		self.PrevAvailTechTrades = {}
		self.PrevAvailBonusTrades = {}
		self.PrevAvailOpenBordersTrades = set()
		self.PrevAvailMapTrades = set()
		self.PrevAvailDefensivePactTrades = set()
		self.PrevAvailPermanentAllianceTrades = set()
		self.PrevAvailVassalTrades = set()
		self.PrevAvailSurrenderTrades = set()
		self.PrevAvailPeaceTrades = set()
		self.lastPopCount = 0
		self.lastLandCount = 0

	def getCheckForDomVictory(self):
		return self.options.isShowDomPopAlert() or self.options.isShowDomLandAlert()

	def onBeginActivePlayerTurn(self, argsList):
		"Called when the active player can start making their moves."
		iGameTurn = argsList[0]
		iPlayer = GC.getGame().getActivePlayer()
		self.CheckForAlerts(iPlayer, True)

	def OnCityAcquired(self, argsList):
		owner, playerType, city, bConquest, bTrade = argsList
		iPlayer = city.getOwner()
		if not self.getCheckForDomVictory(): return
		if iPlayer == GC.getGame().getActivePlayer():
			self.CheckForAlerts(iPlayer, False)

	def OnCityBuilt(self, argsList):
		CyCity = argsList[0]
		iOwner = CyCity.getOwner()
		iPlayerAct = GC.getGame().getActivePlayer()
		if self.getCheckForDomVictory():
			if iOwner == iPlayerAct:
				self.CheckForAlerts(iOwner, False)
		if self.options.isShowCityFoundedAlert():
			if iOwner != iPlayerAct:
				bRevealed = CyCity.isRevealed(GC.getActivePlayer().getTeam(), False)
				if bRevealed or PlayerUtil.canSeeCityList(iOwner):
					CyPlayer = GC.getPlayer(iOwner)
					iColor = GC.getInfoTypeForString("COLOR_MAGENTA")
					if bRevealed:
						msg = localText.getText("TXT_KEY_MORECIV4LERTS_CITY_FOUNDED", (CyPlayer.getName(), CyCity.getName()))
						iTime = GC.getDefineINT("EVENT_MESSAGE_TIME_LONG")
						icon = "Art/Interface/Buttons/Actions/foundcity.dds"
						CyInterface().addMessage(iPlayerAct, True, iTime, msg, None, 0, icon, ColorTypes(iColor), CyCity.getX(), CyCity.getY(), True, True)
					else:
						msg = localText.getText("TXT_KEY_MORECIV4LERTS_CITY_FOUNDED_UNSEEN", (CyPlayer.getName(), CyCity.getName()))
						self._addMessageNoIcon(iPlayerAct, msg, iColor)

	def OnCityRazed(self, argsList):
		city, iPlayer = argsList
		if not self.getCheckForDomVictory(): return
		if iPlayer == GC.getGame().getActivePlayer():
			self.CheckForAlerts(iPlayer, False)

	def OnCityLost(self, argsList):
		city = argsList[0]
		iPlayer = city.getOwner()
		if not self.getCheckForDomVictory(): return
		if iPlayer == GC.getGame().getActivePlayer():
			self.CheckForAlerts(iPlayer, False)

	def CheckForAlerts(self, iPlayer, bBeginTurn):
		GAME = GC.getGame()
		CyPlayer = GC.getPlayer(iPlayer)
		CyTeam = GC.getTeam(CyPlayer.getTeam())
		iGrowthCount = 0

		bCheck1 = self.options.isShowDomPopAlert()
		if bBeginTurn and self.options.isShowCityPendingExpandBorderAlert():
			bCheck2 = True
		else:
			bCheck2 = False

		if bCheck1 or bCheck2:
			# Check for cultural expansion and population growth
			iTime = GC.getDefineINT("EVENT_MESSAGE_TIME_LONG")
			icon = "Art/Interface/Buttons/General/Warning_popup.dds"
			iActiveTeam = GAME.getActiveTeam()
			for iPlayerX in xrange(GC.getMAX_PC_PLAYERS()):
				CyPlayerX = GC.getPlayer(iPlayerX)
				if CyPlayerX.isAlive() and CyPlayerX.getTeam() == iActiveTeam:
					CyCity, i = CyPlayerX.firstCity(False)
					while CyCity:
						if CyCity.getFoodTurnsLeft() == 1 and not CyCity.isFoodProduction() and not CyCity.AI_isEmphasize(5):
							iGrowthCount += 1
						if bCheck2 and CyCity.getCultureLevel() != GC.getNumCultureLevelInfos() - 1:
							if CyCity.getCulture(iPlayerX) + CyCity.getCommerceRate(CommerceTypes.COMMERCE_CULTURE) >= CyCity.getCultureThreshold():
								msg = localText.getText("TXT_KEY_MORECIV4LERTS_CITY_TO_EXPAND",(CyCity.getName(),))
								CyInterface().addMessage(iPlayerX, True, iTime, msg, None, 0, icon, -1, CyCity.getX(), CyCity.getY(), True, True)
						CyCity, i = CyPlayerX.nextCity(i, False)

		# Check Domination Limit
		if self.getCheckForDomVictory() and GAME.isVictoryValid(3):
			# Population Limit
			if bCheck1 and iGrowthCount:
				iTotalPop = GAME.getTotalPopulation()
				if iTotalPop > 10:
					iTeamPop = CyTeam.getTotalPopulation()
					fPercent = iTeamPop * 100.0 / iTotalPop
					fPercentNext = (iTeamPop + iGrowthCount) * 100.0 / iTotalPop

					if iTeamPop + iGrowthCount != self.lastPopCount:
						fVictoryPercent = GAME.getAdjustedPopulationPercent(3) * 1.0
						iLimitPop = int(iTotalPop * fVictoryPercent / 100)

						if fPercent >= fVictoryPercent:
							msg = localText.getText("TXT_KEY_MORECIV4LERTS_POP_EXCEEDS_LIMIT", (iTeamPop, (u"%.2f%%" % fPercent), iLimitPop, (u"%.2f%%" % fVictoryPercent)))
							self._addMessageNoIcon(iPlayer, msg)

						elif fPercentNext >= fVictoryPercent:
							msg = localText.getText("TXT_KEY_MORECIV4LERTS_POP_GROWTH_EXCEEDS_LIMIT", (iTeamPop, iGrowthCount, (u"%.2f%%" % fPercentNext), iLimitPop, (u"%.2f%%" % fVictoryPercent)))
							self._addMessageNoIcon(iPlayer, msg)

						elif fVictoryPercent - fPercentNext < self.options.getDomPopThreshold():
							msg = localText.getText("TXT_KEY_MORECIV4LERTS_POP_GROWTH_CLOSE_TO_LIMIT", (iTeamPop, iGrowthCount, (u"%.2f%%" % fPercentNext), iLimitPop, (u"%.2f%%" % fVictoryPercent)))
							self._addMessageNoIcon(iPlayer, msg)

						elif fVictoryPercent - fPercent < self.options.getDomPopThreshold():
							msg = localText.getText("TXT_KEY_MORECIV4LERTS_POP_CLOSE_TO_LIMIT", (iTeamPop, (u"%.2f%%" % fPercent), iLimitPop, (u"%.2f%%" % fVictoryPercent)))
							self._addMessageNoIcon(iPlayer, msg)

						self.lastPopCount = iTeamPop + iGrowthCount
			# Land Limit
			if self.options.isShowDomLandAlert():
				iTeamLand = CyTeam.getTotalLand()
				if iTeamLand > 40 and iTeamLand != self.lastLandCount:
					iTotalLand = GC.getMap().getLandPlots()
					fVictoryPercent = GAME.getAdjustedLandPercent(3) * 1.0
					iLimitLand = int(iTotalLand * fVictoryPercent / 100)
					fPercent = (iTeamLand * 100.0) / iTotalLand

					if fPercent > fVictoryPercent:
						msg = localText.getText("TXT_KEY_MORECIV4LERTS_LAND_EXCEEDS_LIMIT", (iTeamLand, (u"%.2f%%" % fPercent), iLimitLand, (u"%.2f%%" % fVictoryPercent)))
						self._addMessageNoIcon(iPlayer, msg)

					elif fVictoryPercent - fPercent < self.options.getDomLandThreshold():
						msg = localText.getText("TXT_KEY_MORECIV4LERTS_LAND_CLOSE_TO_LIMIT", (iTeamLand, (u"%.2f%%" % fPercent), iLimitLand, (u"%.2f%%" % fVictoryPercent)))
						self._addMessageNoIcon(iPlayer, msg)

					self.lastLandCount = iTeamLand

		if not bBeginTurn: return
		#********#
		# Trades #
		# | || | #
		tradeData = TradeData()
		# Bonus
		if self.options.isShowBonusTradeAlert():
			desiredBonuses = TradeUtil.getDesiredBonuses(CyPlayer)
			tradesByPlayer = {}
			for CyPlayerX in TradeUtil.getBonusTradePartners(CyPlayer):
				will, wont = TradeUtil.getTradeableBonuses(CyPlayerX, CyPlayer)
				tradesByPlayer[CyPlayerX.getID()] = will

			for iLoopPlayer, currentTrades in tradesByPlayer.iteritems():
				#Did he have trades avail last turn
				if self.PrevAvailBonusTrades.has_key(iLoopPlayer):
					previousTrades = self.PrevAvailBonusTrades[iLoopPlayer]
				else:
					previousTrades = set()
				#Determine new bonuses
				newTrades = currentTrades.difference(previousTrades).intersection(desiredBonuses)
				if newTrades:
					szNewTrades = self.buildBonusString(newTrades)
					msg = localText.getText("TXT_KEY_MORECIV4LERTS_NEW_BONUS_AVAIL", (GC.getPlayer(iLoopPlayer).getName(), szNewTrades))
					self._addMessageNoIcon(iPlayer, msg)
				#Determine removed bonuses
				removedTrades = previousTrades.difference(currentTrades).intersection(desiredBonuses)
				if removedTrades:
					szRemovedTrades = self.buildBonusString(removedTrades)
					msg = localText.getText("TXT_KEY_MORECIV4LERTS_BONUS_NOT_AVAIL", (GC.getPlayer(iLoopPlayer).getName(), szRemovedTrades))
					self._addMessageNoIcon(iPlayer, msg)
			#save curr trades for next time
			self.PrevAvailBonusTrades = tradesByPlayer
		# Tech
		if self.options.isShowTechTradeAlert():
			techsByPlayer = {}
			researchTechs = set()
			iTotalTechs = GC.getNumTechInfos()
			tradeData.ItemType = TradeableItems.TRADE_TECHNOLOGIES
			bCheck1 = True
			for CyPlayerX in TradeUtil.getTechTradePartners(CyPlayer):
				techsToTrade = set()
				for iTech in range(iTotalTechs):
					if bCheck1 and CyPlayer.canResearch(iTech, True):
						researchTechs.add(iTech)
					tradeData.iData = iTech
					if CyPlayerX.canTradeItem(iPlayer, tradeData, False):
						if CyPlayerX.getTradeDenial(iPlayer, tradeData) == DenialTypes.NO_DENIAL: # will trade
							techsToTrade.add(iTech)
				bCheck1 = False
				techsByPlayer[CyPlayerX.getID()] = techsToTrade

			for iLoopPlayer, currentTechs in techsByPlayer.iteritems():
				#Did he have trades avail last turn
				if self.PrevAvailTechTrades.has_key(iLoopPlayer):
					previousTechs = self.PrevAvailTechTrades[iLoopPlayer]
				else:
					previousTechs = set()
				#Determine new techs
				newTechs = currentTechs.difference(previousTechs).intersection(researchTechs)
				if newTechs:
					szNewTechs = self.buildTechString(newTechs)
					msg = localText.getText("TXT_KEY_MORECIV4LERTS_NEW_TECH_AVAIL", (GC.getPlayer(iLoopPlayer).getName(), szNewTechs))
					self._addMessageNoIcon(iPlayer, msg)
				#Determine removed techs
				removedTechs = previousTechs.difference(currentTechs).intersection(researchTechs)
				if removedTechs:
					szRemovedTechs = self.buildTechString(removedTechs)
					msg = localText.getText("TXT_KEY_MORECIV4LERTS_TECH_NOT_AVAIL", (GC.getPlayer(iLoopPlayer).getName(), szRemovedTechs))
					self._addMessageNoIcon(iPlayer, msg)
			#save curr trades for next time
			self.PrevAvailTechTrades = techsByPlayer
		# Map
		if self.options.isShowMapTradeAlert():
			tradeData.ItemType = TradeableItems.TRADE_MAPS
			oldSet = self.PrevAvailMapTrades
			TXT_KEY = "TXT_KEY_MORECIV4LERTS_MAP"
			willTrade = self.getTrades(TradeUtil.getMapTradePartners(CyPlayer), iPlayer, tradeData, oldSet, TXT_KEY)
			if willTrade != oldSet:
				self.PrevAvailMapTrades = willTrade
		# Open Borders
		if self.options.isShowOpenBordersTradeAlert():
			tradeData.ItemType = TradeableItems.TRADE_OPEN_BORDERS
			oldSet = self.PrevAvailOpenBordersTrades
			TXT_KEY = "TXT_KEY_MORECIV4LERTS_OPEN_BORDERS"
			willTrade = self.getTrades(TradeUtil.getOpenBordersTradePartners(CyPlayer), iPlayer, tradeData, oldSet, TXT_KEY)
			if willTrade != oldSet:
				self.PrevAvailOpenBordersTrades = willTrade
		# Defensive Pact
		if self.options.isShowDefensivePactTradeAlert():
			tradeData.ItemType = TradeableItems.TRADE_DEFENSIVE_PACT
			oldSet = self.PrevAvailDefensivePactTrades
			TXT_KEY = "TXT_KEY_MORECIV4LERTS_DEFENSIVE_PACT"
			willTrade = self.getTrades(TradeUtil.getDefensivePactTradePartners(CyPlayer), iPlayer, tradeData, oldSet, TXT_KEY)
			if willTrade != oldSet:
				self.PrevAvailDefensivePactTrades = willTrade
		# Alliance
		if self.options.isShowPermanentAllianceTradeAlert():
			tradeData.ItemType = TradeableItems.TRADE_PERMANENT_ALLIANCE
			oldSet = self.PrevAvailPermanentAllianceTrades
			TXT_KEY = "TXT_KEY_MORECIV4LERTS_PERMANENT_ALLIANCE"
			willTrade = self.getTrades(TradeUtil.getPermanentAllianceTradePartners(CyPlayer), iPlayer, tradeData, oldSet, TXT_KEY)
			if willTrade != oldSet:
				self.PrevAvailPermanentAllianceTrades = willTrade
		# Vassalage
		if self.options.isShowVassalTradeAlert():
			tradeData.ItemType = TradeableItems.TRADE_VASSAL
			oldSet = self.PrevAvailVassalTrades
			TXT_KEY = "TXT_KEY_MORECIV4LERTS_VASSAL"
			willTrade = self.getTrades(TradeUtil.getVassalTradePartners(CyPlayer), iPlayer, tradeData, oldSet, TXT_KEY)
			if willTrade != oldSet:
				self.PrevAvailVassalTrades = willTrade
		# Capitulate
		if self.options.isShowSurrenderTradeAlert():
			tradeData.ItemType = TradeableItems.TRADE_SURRENDER
			oldSet = self.PrevAvailSurrenderTrades
			TXT_KEY = "TXT_KEY_MORECIV4LERTS_SURRENDER"
			willTrade = self.getTrades(TradeUtil.getCapitulationTradePartners(CyPlayer), iPlayer, tradeData, oldSet, TXT_KEY)
			if willTrade != oldSet:
				self.PrevAvailSurrenderTrades = willTrade
		# Peace Treaty
		if self.options.isShowPeaceTradeAlert():
			tradeData.ItemType = TradeableItems.TRADE_PEACE_TREATY
			tradeData.iData = GC.getDefineINT("PEACE_TREATY_LENGTH")
			oldSet = self.PrevAvailPeaceTrades
			TXT_KEY = "TXT_KEY_MORECIV4LERTS_PEACE_TREATY"
			willTrade = self.getTrades(TradeUtil.getPeaceTradePartners(CyPlayer), iPlayer, tradeData, oldSet, TXT_KEY)
			if willTrade != oldSet:
				self.PrevAvailPeaceTrades = willTrade

	def getTrades(self, aList, iPlayer, tradeData, oldSet, TXT_KEY):
		aSet = set()
		for CyPlayerX in aList:
			if CyPlayerX.canTradeItem(iPlayer, tradeData, False):
				if CyPlayerX.getTradeDenial(iPlayer, tradeData) == DenialTypes.NO_DENIAL:
					aSet.add(CyPlayerX.getID())
		newSet = aSet.difference(oldSet)
		if newSet:
			self._addMessageNoIcon(iPlayer, localText.getText(TXT_KEY, (self.buildPlayerString(newSet),)))
		return aSet

	def buildTechString(self, techs):
		return self.buildItemString(techs, GC.getTechInfo, CvTechInfo.getDescription)

	def buildBonusString(self, bonuses):
		return self.buildItemString(bonuses, GC.getBonusInfo, CvBonusInfo.getDescription)

	def buildPlayerString(self, players):
		return self.buildItemString(players, GC.getPlayer, CyPlayer.getName)

	def buildItemString(self, items, getItemFunc, getNameFunc):
		names = [getNameFunc(getItemFunc(eItem)) for eItem in items]
		names.sort()
		return u", ".join(names)
