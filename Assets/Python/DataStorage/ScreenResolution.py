# Data storage python
# The screen resolution for the game will be set by CvScreensInterface.py once when you launch the game.
# When you change resolutions the storage here will change accordingly, this happens in CvOptionsScreenCallbackInterface.py
# Some python code may need to know the screen resolution, there is no need to ask the dll about it if this file has been imported.

x = 0
y = 0

def init(dir):
	global x, y
	print "ScreenResolution.init\nSet custom resolution from CivilizationIV.ini if found."
	import ConfigParser
	Config = ConfigParser.ConfigParser()
	Config.read(dir + "\CivilizationIV.ini")
	#Config.sections()
	X0 = Config.get("DEBUG", "ScreenWidth")
	Y0 = Config.get("DEBUG", "ScreenHeight")
	if X0.isdigit() and Y0.isdigit():
		X0 = int(X0)
		Y0 = int(Y0)
		if X0 > 0 and Y0 > 0:
			if X0 < 1024:
				X0 = 1024
			if Y0 < 768:
				Y0 = 768
			x = X0
			y = Y0
			print "Resolution: %dx%d\nScreenResolution.init - END" %(x, y)
			return
	print "No custom resolution found.\nValue stored in profileName.pfl will be used instead.\nScreenResolution.init - END"