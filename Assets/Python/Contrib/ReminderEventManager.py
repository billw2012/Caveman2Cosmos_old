##-------------------------------------------------------------------
## Modified from reminder by eotinb
## by Ruff and EF
##-------------------------------------------------------------------
## Reorganized to work via CvCustomEventManager
## using Civ4lerts as template.
## CvCustomEventManager & Civ4lerts by Gillmer J. Derge
##-------------------------------------------------------------------
## EF: Turned into a real queue, can be disabled
##-------------------------------------------------------------------

from CvPythonExtensions import *
import CvUtil
import SdToolKit
import ScreenResolution as SR

STORE_EVENT_ID = CvUtil.getNewEventID("Reminder.Store")
RECALL_EVENT_ID = CvUtil.getNewEventID("Reminder.Recall")
RECALL_AGAIN_EVENT_ID = CvUtil.getNewEventID("Reminder.RecallAgain")

GC = CyGlobalContext()
GAME = GC.getGame()
TRNSLTR = CyTranslator()

g_reminders = None

# Used to display flashing end-of-turn text
g_turnReminderTexts = ""

# Used to receive network messages
g_hasNetMessage = hasattr(CyPlayer, "addReminder")

def hasNetMessage():
	return g_hasNetMessage

def netAddReminder(args):
	playerID, turn, message = args
	g_reminders.push(playerID, Reminder(turn, message))

# Shortcut - Create Reminder
def createReminder(argsList):
	g_eventMgr.beginEvent(STORE_EVENT_ID)

class ReminderEventManager:

	def __init__(self, eventManager):

		global g_eventMgr, g_autolog, ReminderOpt
		g_eventMgr = eventManager
		import autolog
		g_autolog = autolog.autologInstance()
		import BugCore
		ReminderOpt = BugCore.game.Reminder
		# expose to DLL
		import CvAppInterface
		CvAppInterface.netAddReminder = netAddReminder

		self.initReminders()
		eventManager.addEventHandler("BeginActivePlayerTurn", self.onBeginActivePlayerTurn)
		eventManager.addEventHandler("EndGameTurn", self.onEndGameTurn)
		eventManager.addEventHandler("endTurnReady", self.onEndTurnReady)
		eventManager.addEventHandler("GameStart", self.onGameStart)
		eventManager.addEventHandler("OnLoad", self.onLoadGame)
		eventManager.addEventHandler("PythonReloaded", self.onLoadGame)
		eventManager.addEventHandler("OnPreSave", self.onPreSave)
		eventManager.addEventHandler("SwitchHotSeatPlayer", self.onSwitchHotSeatPlayer)
		eventManager.setPopupHandlers(STORE_EVENT_ID, 'Reminder.Store', self.__eventReminderStoreBegin, self.__eventReminderStoreApply)
		eventManager.setPopupHandlers(RECALL_EVENT_ID, 'Reminder.Recall', self.__eventReminderRecallBegin, self.__eventReminderRecallApply)
		eventManager.setPopupHandlers(RECALL_AGAIN_EVENT_ID, 'Reminder.RecallAgain', self.__eventReminderRecallAgainBegin, self.__eventReminderRecallAgainApply)

	def __eventReminderStoreBegin(self, argsList):
		if SR.x > 2500:
			w = 520
			h = 232
		elif SR.x > 1700:
			w = 480
			h = 224
		elif SR.x > 1400:
			w = 440
			h = 216
		else:
			w = 400
			h = 210
		prompt = SR.aFontList[2] + TRNSLTR.getText("TXT_KEY_REMINDER_HEADER", ()) + "\n"
		prompt += SR.aFontList[5] + TRNSLTR.getText("TXT_KEY_REMINDER_PROMPT", ())
		ok = TRNSLTR.getText("TXT_KEY_MAIN_MENU_OK", ())
		cancel = TRNSLTR.getText("TXT_KEY_POPUP_CANCEL", ())

		popup = CyPopup(STORE_EVENT_ID, EventContextTypes.EVENTCONTEXT_SELF, True)
		popup.setSize(w, h)
		popup.setPosition(SR.x/2 - w/2, SR.y/2 - h/2)
		popup.setBodyString(prompt, 1<<0)
		popup.createSpinBox(0, "", 1, 1, 999, 0)
		popup.createEditBox("", 1)
		popup.addButton(ok)
		popup.addButton(cancel)
		popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)

	def __eventReminderStoreApply(self, playerID, userData, popupReturn):
		if popupReturn.getButtonClicked() != 1:
			reminderText = popupReturn.getEditBoxString(1)
			if reminderText:
				turns = popupReturn.getSpinnerWidgetValue(0)
				reminderTurn = turns + GAME.getGameTurn()
				self.addReminder(playerID, Reminder(reminderTurn, reminderText))
				if g_autolog.isLogging() and ReminderOpt.isAutolog():
					g_autolog.writeLog("Reminder: On Turn %d, %s" % (reminderTurn, reminderText))

	def __eventReminderRecallBegin(self, argsList):
		self.showReminders(False)

	def __eventReminderRecallApply(self, playerID, userData, popupReturn):
		if popupReturn.getButtonClicked() != 1:
			if self.reminder:
				self.reminder.turn = GAME.getGameTurn()
				self.addReminder(playerID, self.reminder)
				self.reminder = None

	def __eventReminderRecallAgainBegin(self, argsList):
		self.showReminders(True)

	def __eventReminderRecallAgainApply(self, playerID, userData, popupReturn):
		if popupReturn.getButtonClicked() != 1:
			if self.reminder:
				# Put it back into the queue for next turn
				self.reminder.turn += 1
				self.addReminder(playerID, self.reminder)
				self.reminder = None

	def showReminders(self, endOfTurn):
		global g_turnReminderTexts
		if not endOfTurn:
			g_turnReminderTexts = ""

		iPlayer = GAME.getActivePlayer()
		queue = self.reminders.get(iPlayer)
		if queue:
			iTurn = GAME.getGameTurn()
			yes = TRNSLTR.getText("TXT_KEY_POPUP_YES", ())
			no = TRNSLTR.getText("TXT_KEY_POPUP_NO", ())
			bLogging = g_autolog.isLogging() and ReminderOpt.isAutolog()
			bShowMsg = ReminderOpt.isShowMessage()
			bShowPop = ReminderOpt.isShowPopup()
			if bShowPop:
				if endOfTurn:
					prompt = TRNSLTR.getText("TXT_KEY_REMIND_NEXT_TURN_PROMPT", ())
					eventId = RECALL_AGAIN_EVENT_ID
				else:
					prompt = TRNSLTR.getText("TXT_KEY_REMIND_END_TURN_PROMPT", ())
					eventId = RECALL_EVENT_ID

			while not queue.isEmpty():
				nextTurn = queue.nextTurn()
				if nextTurn > iTurn:
					break
				elif nextTurn < iTurn:
					# invalid (lost) reminder
					reminder = queue.pop()
					print "[WARNING] Reminder - skipped turn %d: %s" %(reminder.turn, reminder.message)
				else:
					self.reminder = queue.pop()
					if bLogging:
						g_autolog.writeLog("Reminder: %s" % self.reminder.message)

					if not endOfTurn:
						if g_turnReminderTexts:
							g_turnReminderTexts += ", "
						g_turnReminderTexts += self.reminder.message

					if bShowMsg:
						CvUtil.sendMessage(self.reminder.message, iPlayer, 10, "", ColorTypes(8))

					if bShowPop:
						body = SR.aFontList[4] + self.reminder.message + "\n" + SR.aFontList[5] + prompt
						popup = CyPopup(eventId, EventContextTypes.EVENTCONTEXT_SELF, True)
						popup.setPosition(SR.x/3, SR.y/3)
						popup.setBodyString(body, 1<<0)
						popup.addButton(yes)
						popup.addButton(no)
						popup.launch(False, PopupStates.POPUPSTATE_IMMEDIATE)


	def initReminders(self):
		self.setReminders(Reminders())
		self.reminder = None

	def setReminders(self, queues):
		self.reminders = queues
		global g_reminders
		g_reminders = queues

	def clearReminders(self):
		self.reminders.clear()
		global g_turnReminderTexts
		g_turnReminderTexts = ""

	def addReminder(self, playerID, reminder):
		if hasNetMessage():
			player = GC.getPlayer(playerID)
			player.addReminder(reminder.turn, reminder.message)
		else:
			self.reminders.push(playerID, reminder)

	def createReminder(self):
		g_eventMgr.beginEvent(STORE_EVENT_ID)

	def onSwitchHotSeatPlayer(self, argsList):
		"""
		Clears the end turn text so hot seat players don't see each other's reminders.
		"""
		ePlayer = argsList[0]
		global g_turnReminderTexts
		g_turnReminderTexts = ""

	def onBeginActivePlayerTurn(self, argsList):
		"""
		Display the active player's reminders.
		"""
		iGameTurn = argsList[0]
		global g_turnReminderTexts
		g_turnReminderTexts = ""
		if (ReminderOpt.isEnabled()):
			g_eventMgr.beginEvent(RECALL_EVENT_ID)

	def onEndGameTurn(self, argsList):
		"""
		Clears reminders up to and including the turn that just ended for all players.
		"""
		iGameTurn = argsList[0]
		self.reminders.clearBefore(iGameTurn + 1)

	def onEndTurnReady(self, argsList):
		"""
		Display reminders set to repeat this turn.
		"""
		if ReminderOpt.isEnabled():
			g_eventMgr.beginEvent(RECALL_AGAIN_EVENT_ID)

	def onGameStart(self, argsList):
		"""
		Clear all reminders.
		"""
		self.clearReminders()

	def onLoadGame(self, argsList):
		"""
		Load saved reminders.
		"""
		self.clearReminders()
		queues = SdToolKit.sdGetGlobal("Reminders", "queues")
		if queues:
			self.setReminders(queues)

	def onPreSave(self, argsList):
		"""
		Save reminders.
		"""
		if self.reminders.isEmpty():
			SdToolKit.sdDelGlobal("Reminders", "queues")
		else:
			SdToolKit.sdSetGlobal("Reminders", "queues", self.reminders)


class Reminder(object):
	def __init__(self, turn, message):
		self.turn = turn
		self.message = message

class ReminderQueue(object):

	def __init__(self):
		self.clear()

	def clear(self):
		self.queue = []

	def clearBefore(self, turn, log=False):
		while not self.isEmpty() and self.nextTurn() < turn:
			reminder = self.pop()
			if log:
				print "Reminder - skipped turn %d: %s" %(reminder.turn, reminder.message)

	def size(self):
		return len(self.queue)

	def isEmpty(self):
		return self.size() == 0

	def nextTurn(self):
		reminder = self.peek()
		if reminder:
			return reminder.turn
		else: return -1

	def push(self, reminder):
		for i, r in enumerate(self.queue):
			if reminder.turn < r.turn:
				self.queue.insert(i, reminder)
				break
		else:
			self.queue.append(reminder)

	def pop(self):
		if self.isEmpty():
			return None
		else:
			return self.queue.pop(0)

	def peek(self):
		if self.isEmpty():
			return None
		else:
			return self.queue[0]


class Reminders(object):

	def __init__(self, queue=None):
		self.clear()
		if queue:
			self.queues[GAME.getActivePlayer()] = queue

	def clear(self):
		self.queues = {}

	def clearBefore(self, turn, log=False):
		for queue in self.queues.itervalues():
			queue.clearBefore(turn, log)

	def exists(self, playerID):
		return playerID in self.queues

	def get(self, playerID):
		if self.exists(playerID):
			return self.queues[playerID]

	def getForUpdate(self, playerID):
		if self.exists(playerID):
			return self.queues[playerID]
		else:
			queue = self.queues[playerID] = ReminderQueue()
			return queue

	def size(self, playerID=None):
		if playerID:
			queue = self.get(playerID)
			if queue:
				return queue.size()
			return 0
		else: return len(self.queues)

	def isEmpty(self, playerID=None):
		return self.size(playerID) == 0

	def nextTurn(self, playerID):
		queue = self.get(playerID)
		if queue:
			return queue.nextTurn()
		return -1

	def push(self, playerID, reminder):
		self.getForUpdate(playerID).push(reminder)

	def pop(self, playerID):
		queue = self.get(playerID)
		if queue:
			queue.pop()

	def peek(self, playerID):
		queue = self.get(playerID)
		if queue:
			return queue.peek()
