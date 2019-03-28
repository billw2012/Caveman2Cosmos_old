## Code for Process Upgrade Chains
##
## If a process such as Culture, or Wealth or Research have upgrade paths
## for example Meger Research = 1/3 Research
##                       -> Lesser Research = 2/3 Research is available at tech X
##                       -> Research is available at tech
##
## The XML does not have any way to obsolete the earlier process so this code does it.
##
## Only the most advanced available process is displayed in the city list.

from CvPythonExtensions import *
#import BugUtil

# globals
gc = CyGlobalContext()

gai_ProcessUpgrades = None  # Process which obsoletes a given process
gai_TechProcessOn = None    # The tech that switches the process on

def init():
	print "ProcessUpgrades.init"

	## Define the globals
	global gai_ProcessUpgrades, gai_TechProcessOn

	## Define the upgrade chains 
	##    [ number of elements in the chain, earliest, next, ..., most advanced]
	##  Note that the number is the human count
	##
	asProcessUpgrades = [
	[3, 'PROCESS_WEALTH_MEAGER', 'PROCESS_WEALTH_LESSER', 'PROCESS_WEALTH'],
	[3, 'PROCESS_RESEARCH_MEAGER', 'PROCESS_RESEARCH_LESSER', 'PROCESS_RESEARCH'],
	[3, 'PROCESS_CULTURE_MEAGER', 'PROCESS_CULTURE_LESSER', 'PROCESS_CULTURE'],
	[3, 'PROCESS_SPY_MEAGER', 'PROCESS_SPY_LESSER', 'PROCESS_SPY']
	]

	## Identify which process are prequsite another procese.
	gai_ProcessUpgrades = {}

	for i in range(asProcessUpgrades.__len__()):
		iNumber =asProcessUpgrades[i][0]

		j = 1
		while j < iNumber :
			iOldProcess = gc.getInfoTypeForString(asProcessUpgrades[i][j])
			iNewProcess = gc.getInfoTypeForString(asProcessUpgrades[i][j+1])
			#BugUtil.debug("Process %s (%d) upgrades to proces %s (%d).",  asProcessUpgrades[i][j],  iOldProcess ,  asProcessUpgrades[i][j+1], iNewProcess )

			gai_ProcessUpgrades[iOldProcess] = iNewProcess

			j = j + 1

	## Identify which process are active with which tech
	gai_TechProcessOn = {}

	for i in range( gc.getNumProcessInfos() ):
		iPrereqTech = gc.getProcessInfo(i).getTechPrereq()
		gai_TechProcessOn[i] = iPrereqTech

		if iPrereqTech == -1:
			iAtTech = "None"
		else:
			iAtTech =  gc.getTechInfo(iPrereqTech).getDescription()

		#BugUtil.debug("Process %s (%d) active at tech %s (%d).",  gc.getProcessInfo(i).getDescription(),  i , iAtTech, gai_TechProcessOn[i] )



def canSelectProcess(iOwner, iProcess):
	pPlayer = gc.getPlayer(iOwner)
	team = gc.getTeam(pPlayer.getTeam())

	# Note that iOwner may be NULL (-1) and not a refer to a player object
	if iOwner == -1:
		return False
	'''
	BugUtil.debug("Process Update/Oboslete canSelectProcess. For Process %d", iProcess)

	if iProcess in gai_ProcessUpgrades:
		BugUtil.debug("Trace 2: Process %d upgrades to proces %d.",  iProcess,  gai_ProcessUpgrades[iProcess] )

	if iProcess in gai_TechProcessOn:
		BugUtil.debug("Trace 2: Process %d active at tech %d.",  iProcess, gai_TechProcessOn[iProcess] )
	'''

	iPrereqTech = gai_TechProcessOn[iProcess]
	#BugUtil.debug("   Process %d has prereq tech %d.", iProcess , iPrereqTech)

	processActive = False
	if iPrereqTech == -1 or team.isHasTech(iPrereqTech):
		processActive = True

		#BugUtil.debug("   Team has prereq tech %d.", iPrereqTech)
		# If this process is upgraded and the team has the tech for the upgraded tech then this tech is off
		if iProcess in gai_ProcessUpgrades:
			#BugUtil.debug("   Process has an upgrade %d.", gai_ProcessUpgrades[iProcess])
			iUpgradePrereqTech = gai_TechProcessOn[gai_ProcessUpgrades[iProcess]]
			if iUpgradePrereqTech == -1 or team.isHasTech(iUpgradePrereqTech):
				processActive = False
				#BugUtil.debug("   Team has ugrade prereq tech %d.", iUpgradePrereqTech)
	'''
	if processActive:
		BugUtil.debug("   Process %d is active.", iProcess)
	else:
		BugUtil.debug("   Process %d is not active.", iProcess)
	'''

	return processActive

