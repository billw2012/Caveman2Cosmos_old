## sdToolKit by Stone-D (Laga Mahesa)
## Copyright Laga Mahesa 2005
##
## laga@tbi.co.id
## lmahesa@(yahoo|hotmail|gmail).com
##
## Version 1.22
##
## Rewritten to use BugData by EmperorFool
## Merged with SdToolKitCustom by AIAndy (usage of both was conflicting with BugData)


from CvPythonExtensions import *
import BugUtil
import BugData

try:
  import cPickle as pickle
except:
  import pickle

GLOBALS_KEY = 'Global'
GAMEOBJECT_KEY = 'Game'

gc = CyGlobalContext()


################# SD-UTILITY-PACK ###################
#-=-=-=-=-=-=-=-= BASIC-UTILITIES =-=-=-=-=-=-=-=-=-#

def sdEcho( echoString ):
  BugUtil.debug("SdToolKit: %s" %(echoString))
  return 0

def sdGetTimeInt( turn ):
  TurnTable = CyGameTextMgr().getTimeStr(turn, False).split(' ')
  TurnInt   = int(TurnTable[0])
  if (TurnTable[1] == 'BC'):
    TurnInt = 0 - TurnInt
  return TurnInt

def sdGameYearsInt():
  yearsBC = sdGetTimeInt(gc.getGame().getStartTurn())
  if (yearsBC < 0):
    yearsBC = yearsBC - (yearsBC * 2)
  else:
    yearsBC = 0
  yearsAD = 0
  for i in range(gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getNumTurnIncrements()):
    yearsAD += gc.getGameSpeedInfo(gc.getGame().getGameSpeedType()).getGameTurnInfo(i).iNumGameTurnsPerIncrement
  yearsAD = sdGetTimeInt(yearsAD)
  if (yearsAD < sdGetTimeInt(gc.getGame().getGameTurn())):
    yearsAD = sdGetTimeInt(gc.getGame().getGameTurn())
  yearsAL = yearsBC + yearsAD
# sdEcho('yearsBC : %d, yearsAD : %d, All Years : %d' %(yearsBC, yearsAD, yearsAL))
  return yearsAL


#-=-=-=-=-=-=-=-= SD-DATA-STORAGE =-=-=-=-=-=-=-=-=-#
# Every variable is a string, except for the actual
# value you want to store, which can be anything.

#--------------- INTERNAL USE ONLY -----------------#

#   Initializes a central reservoir of custom variables for your mod's use. 'ModID' should be your mod's name.
def sdModInit( ModID ):
  return sdModLoad(ModID)

#   Loads previously initialized data from the central reservoir.
def sdModLoad( ModID ):
  return BugData.getTable(ModID).data

#   Saves a mod's entire variable data to the central reservoir.
def sdModSave( ModID, mTable ):
  table = BugData.getTable(ModID)
  table.setData(mTable)
  return 0


#----------------- MOD FUNCTIONS -------------------#

#   sdEntityInit( 'MyModName', 'UniqueName', Template_dictionary )
#   Initializes a unique data entity (city, unit, plot).
def sdEntityInit( ModID, entity, eTable ):
  table = BugData.getTable(ModID, entity)
  table.setData(eTable)
  return 0

#   sdEntityWipe( 'MyModName', 'UniqueName' )
#   Removes an entity that has been previously initialized by sdEntityInit.
#   Returns int 0 on failure, int 1 on success.
def sdEntityWipe( ModID, entity ):
  return BugData.deleteTable(ModID, entity)

#   sdEntityExists( 'MyModName', 'UniqueName' )
#   Checks whether or not an entity has been initialized by sdEntityInit.
#   Returns bool False on failure, bool True on success.
def sdEntityExists( ModID, entity ):
  return BugData.hasTable(ModID, entity)

#   sdGetVal( 'MyModName', 'UniqueName', 'VariableName' )
#   Fetches a specific variable's value from the entity's data set.
def sdGetVal( ModID, entity, var ):
  table = BugData.findTable(ModID, entity)
  if table:
    if var in table:
      return table[var]
  return None

#   sdSetVal( 'MyModName', 'UniqueName', 'VariableName', any_value )
#   Stores a specific variable's value within the entity's data set.
#   Returns bool False on failure, bool True on success.
def sdSetVal( ModID, entity, var, val ):
  table = BugData.findTable(ModID, entity)
  if table:
    table[var] = val
    return True
  return False

#   sdDelVal( 'MyModName', 'UniqueName', 'VariableName' )
#   Removes a specific variable from the entity's data set.
#   Returns bool False on failure, bool True on success.
def sdDelVal( ModID, entity, var ):
  table = BugData.findTable(ModID, entity)
  if table and var in table:
    del table[var]
    return True
  return False

#   sdGetGlobal( 'MyModName', 'GlobalVariableName' )
#   Fetches a specific variable's value from the mod's global data set.
def sdGetGlobal( ModID, var ):
  table = BugData.findTable(ModID, GLOBALS_KEY)
  if table and var in table:
    return table[var]
  return None

#   sdSetGlobal( 'MyModName', 'GlobalVariableName', any_value )
#   Stores a specific variable's value within the mod's global data set.
def sdSetGlobal( ModID, var, val ):
  BugData.getTable(ModID, GLOBALS_KEY)[var] = val

#   sdDelGlobal( 'MyModName', 'GlobalVariableName' )
#   Removes a specific variable from the mod's global data set.
#   Returns bool False on failure, bool True on success.
def sdDelGlobal( ModID, var ):
  table = BugData.findTable(ModID, GLOBALS_KEY)
  if table and var in table:
    del table[var]
    return True
  return False


## Modification by Teg Navanis. While SD-DATA-STORAGE stores
## values in the GameInstance - scriptdata, these functions can be used to store data
## in the scriptdata of an object (for instance a unit, a city or a plot)

## Further modifications by jdog5000

#-=-=-=-=-=-=-=-= SD-OBJECT-DATA-STORAGE =-=-=-=-=-=-=-=-=-#
# Every variable is a string, except for 'object' and the actual
# value you want to store, which can be anything.
# object can be one of the following:
# - CyCity object
# - CyGame object
# - CyPlayer object
# - CyPlot object
# - CyUnit object
# - PyCity object

# AIAndy: Using the CyGame object is now redirected to the functions above to use BugData

#--------------- INTERNAL USE ONLY -----------------#

#   Loads previously initialized data from the central reservoir. If no data is found, init it.
def sdLoad( object ):
  try:
    cyTable = pickle.loads(object.getScriptData())
  except:
    cyTable = {}

  if (cyTable == ""):
    cyTable = {}

  return cyTable

#   Loads previously initialized data from the central reservoir. If no data is found, init it.
def sdObjectGetDict( ModID, object ):
  cyTable = sdLoad( object )
  if( cyTable.has_key(ModID) ) :
      return cyTable[ModID]
  else :
      return {}

#   Loads previously initialized data from the central reservoir. If no data is found, init it.
def sdObjectSetDict( ModID, object, VarDictionary ):
  cyTable = sdLoad( object )
  cyTable[ModID] = VarDictionary
  object.setScriptData(pickle.dumps(cyTable))


#----------------- OBJECT FUNCTIONS -------------------#

#   sdObjectInit ( 'MyModName', object, Template_dictionary )
#   Fetches a specific variable's value from the object's data set.
def sdObjectInit (ModID, object, VarDictionary):
  if isinstance(object, CyGame):
    if not BugData.hasTable(ModID, GAMEOBJECT_KEY):
      sdEntityInit(ModID, GAMEOBJECT_KEY, VarDictionary)
  else:
    cyTable = sdLoad(object)
    if ( not cyTable.has_key(ModID) ):
      cyTable[ModID] = VarDictionary
      object.setScriptData(pickle.dumps(cyTable))
  return 0


#   sdObjectWipe( 'MyModName', object )
#   Removes an entity that has been previously initialized by sdObjectInit.
#   Returns False on failure, True on success.
def sdObjectWipe( ModID, object ):
  if isinstance(object, CyGame):
    sdEntityWipe(ModID, GAMEOBJECT_KEY)
  else:
    cyTable = sdLoad(object)
    if ( cyTable.has_key(ModID) ):
      del cyTable[ModID]
      object.setScriptData(pickle.dumps(cyTable))
      return True
  return False


#   sdObjectExists( 'MyModName', object )
#   Checks whether or not an object has been initialized by sdObjectInit.
#   Returns bool False on failure, bool True on success.
def sdObjectExists( ModID, object ):
  if isinstance(object, CyGame):
    if BugData.hasTable(ModID, GAMEOBJECT_KEY):
      return True
  else:
    cyTable = sdLoad(object)
    if ( cyTable.has_key(ModID) ):
      return True
  return False


#   sdObjectGetVal( 'MyModName', object, 'VariableName' )
#   Fetches a specific variable's value from the object's data set.
## Modded by jdog5000: returns None if not found
def sdObjectGetVal( ModID, object, var ):
  if isinstance(object, CyGame):
    return sdGetVal(ModID, GAMEOBJECT_KEY, var)
  else:
    cyTable = sdLoad(object)
    try:
      mTable = cyTable[ModID]
      if( var in mTable ) :
        return mTable[var]
      else :
        return None
    except:
      print "Error: initialize object first (getval)!"
      #assert False
      return None

#   sdObjectSetVal( 'MyModName', object, 'VariableName', any_value )
#   Stores a specific variable's value within the object's data set.
#   Returns bool False on failure, bool True on success.
## Modded by jdog5000 to allow creation of new dict elements
def sdObjectSetVal( ModID, object, var, val ):
  if isinstance(object, CyGame):
    return sdSetVal(ModID, GAMEOBJECT_KEY, var, val)
  else:
    cyTable = sdLoad( object )
    try:
      mTable = cyTable[ModID]
    except:
      print "Error: initialize object first (setval on %s)!"%(var)
      return False
    if ( mTable.has_key(var) ):
      mTable[var] = val
      object.setScriptData(pickle.dumps(cyTable))
      return True
    else :
      mTable[var] = val
      object.setScriptData(pickle.dumps(cyTable))
      return True

#   sdObjectChangeVal( 'MyModName', object, 'VariableName', change_in_value )
#   Updates an existing variable's value within the object's data set.
#   Returns bool False on failure, bool True on success.
def sdObjectChangeVal( ModID, object, var, delta ):
  if isinstance(object, CyGame):
    table = BugData.findTable(ModID, GAMEOBJECT_KEY)
    if table and var in table:
      table[var] += delta
      return True
    else:
      return False
  else:
    cyTable = sdLoad( object )
    try:
      mTable = cyTable[ModID]
    except:
      print "Error: initialize object first (changeval)!"
      return False
    prevVal = sdObjectGetVal( ModID, object, var )
    if ( mTable.has_key(var) and not prevVal == None ):
      mTable[var] = prevVal + delta
      object.setScriptData(pickle.dumps(cyTable))
      return True
    return False

#   sdObjectUpdateVal( 'MyModName', object, 'VariableName', any_value )
#   Updates an existing variable's value within the object's data set.
#   Returns bool False on failure, bool True on success.
def sdObjectUpdateVal( ModID, object, var, val ):
  if isinstance(object, CyGame):
    table = BugData.findTable(ModID, GAMEOBJECT_KEY)
    if table and var in table:
      table[var] = delta
      return True
    else:
      return False
  else:
    cyTable = sdLoad( object )
    try:
      mTable = cyTable[ModID]
    except:
      print "Error: initialize object first (updateval)!"
      return False
    if ( mTable.has_key(var) ):
      mTable[var] = val
      object.setScriptData(pickle.dumps(cyTable))
      return True
    else :
      print 'Error: object not initialized with var: %s'%(var)
    return False