## MusicUpdate
##
## Adds music files in special directories to the respective sound registration files.
##
## Chooses a random file in a specific directory as title music
##

import BugUtil
import BugPath
import os
import os.path
import random
import re
import shutil
import string

def init():
  BugUtil.debug("MusicUpdate INIT.")

  soundtrackFolder = BugPath.getModDir() + '/Assets/Sounds/Soundtrack/'
  audioXMLFolder = BugPath.getModDir() + '/Assets/XML/Audio/'
  titleFolder = soundtrackFolder + '/Title/'
  
  eraNames = [ "Prehistoric", "Ancient", "Classical", "Medieval", "Renaissance", "Industrial", "Modern", "Transhuman", "Galactic", "Future" ]
  
  defineFilename = audioXMLFolder + 'AudioDefines.xml'
  scriptsFilename = audioXMLFolder + 'Audio2DScripts.xml'
  eraInfoFilename = BugPath.getModDir() + '/Assets/XML/GameInfo/CIV4EraInfos.xml'
  
  titleFilenames = os.listdir(titleFolder)
  if not titleFilenames:
    titleFile = random.choice(titleFilenames)
    titleFile = os.path.splitext(titleFile)[0]
    
    f = open(defineFilename, "r")
    content = f.read()
    f.close()
    content = re.sub(r'(<SoundID>SONG_OPENING_MENU</SoundID>\s*<Filename>)[^<]*',r'\1Sounds/Soundtrack/Title/'+titleFile,content) 
    f = open(defineFilename, "w")
    f.write(content)
    f.close()
  
  f = open(eraInfoFilename, 'r')
  infoFileContent = f.read()
  f.close()
  
  toInsertDef = ""
  toInsertScript = ""
  
  isChanged = False
  
  for era in eraNames:
    eraFolder = soundtrackFolder + era
    eraNewFolder = eraFolder + 'New'
    if os.path.isdir(eraNewFolder):
      newFiles = os.listdir(eraNewFolder)
      if newFiles:
        toInsert = ""
        for newFile in newFiles:
          if os.path.isdir(eraNewFolder + '/' + newFile):
            continue
          shutil.move(eraNewFolder + '/' + newFile, eraFolder + '/' + newFile)
          isChanged = True
          fileTag = os.path.splitext(newFile)[0]
          fileTagUpper = string.upper(fileTag)
          fileTagUpper = re.sub(r'\s', r'_', fileTagUpper)
          fileTagUpper = re.sub(r'[^A-Z0-9_]', r'', fileTagUpper)
          toInsert = toInsert + "\n<EraInfoSoundtrack>AS2D_"+fileTagUpper+"</EraInfoSoundtrack>"
          toInsertDef = toInsertDef + "<SoundData>\n<SoundID>SONG_"+fileTagUpper+"</SoundID>\n<Filename>Sounds/Soundtrack/"+era+"/"+fileTag+"</Filename>\n<LoadType>STREAMED</LoadType>\n<bIsCompressed>1</bIsCompressed>\n<bInGeneric>1</bInGeneric>\n</SoundData>\n"
          toInsertScript = toInsertScript + "<Script2DSound>\n<ScriptID>AS2D_"+fileTagUpper+"</ScriptID>\n<SoundID>SONG_"+fileTagUpper+"</SoundID>\n<SoundType>GAME_MUSIC</SoundType>\n<iMinVolume>80</iMinVolume>\n<iMaxVolume>80</iMaxVolume>\n<iPitchChangeDown>0</iPitchChangeDown>\n<iPitchChangeUp>0</iPitchChangeUp>\n<iMinLeftPan>-1</iMinLeftPan>\n<iMaxLeftPan>-1</iMaxLeftPan>\n<iMinRightPan>-1</iMinRightPan>\n<iMaxRightPan>-1</iMaxRightPan>\n<bLooping>0</bLooping>\n<iMinTimeDelay>0</iMinTimeDelay>\n<iMaxTimeDelay>0</iMaxTimeDelay>\n<bTaperForSoundtracks>0</bTaperForSoundtracks>\n<iLengthOfSound>0</iLengthOfSound>\n<fMinDryLevel>1.0</fMinDryLevel>\n<fMaxDryLevel>1.0</fMaxDryLevel>\n<fMinWetLevel>0.0</fMinWetLevel>\n<fMaxWetLevel>0.0</fMaxWetLevel>\n<iNotPlayPercent>0</iNotPlayPercent>\n</Script2DSound>\n"
        if toInsert:
          infoFileContent = re.sub(r'(\<Type\>ERA_'+string.upper(era)+r'(?:.|\n)*?\<EraInfoSoundtracks\>)', r'\1'+toInsert, infoFileContent)
  
  if isChanged:
    f = open(eraInfoFilename, 'w')
    f.write(infoFileContent)
    f.close()

  if toInsertDef:
    f = open(defineFilename, 'r')
    content = f.read()
    f.close()
    content = re.sub(r'(\</SoundDatas\>)', toInsertDef+r'\1', content)
    f = open(defineFilename, 'w')
    f.write(content)
    f.close()
    
    f = open(scriptsFilename, 'r')
    content = f.read()
    f.close()
    content = re.sub(r'(\</Script2DSounds\>)', toInsertScript+r'\1', content)
    f = open(scriptsFilename, 'w')
    f.write(content)
    f.close()
    
    
    
      
    