

#Load profile object
#	Load object -> name, energy
#	Profile -> season, hrly on/off
#System object -> allowable DoD, parasitic load
#	Battery object -> size, effiency, chemistry, voltage
#	Panel object -> size, efficiency
#	Location object -> name, lat, long, solar rad
#Autonomy object -> hrly autonomy, monthly avg, yr avg

class battery:
	def __init__(self,max_ah,efficiency,voltage):
		self.batsize = max_ah
		self.bateff = efficiency
		self.batvolt = voltage
	
	# Unchangeable properties
	def SetChem(self, chemistry):
		self.chem = chemistry
	def SetSize(self, max_ah):
		self.batsize = max_ah
	def SetEff(self, efficiency):
		self.eff = efficiency
	def SetVolt(self, voltage):
		self.volt = voltage

	# Changing properties
	def SetCapacity(self, curr_ah):
		self.capacity = curr_ah

	# Methods
	def AddEnergy(self, wh):
		self.capacity += (wh/self.volt)

class panel:
	def __init__(self, watts, efficiency):
		self.pansize = watts
		self.paneff = efficiency

	# Unchangeable properties
	def SetSize(self, watts):
		self.size = watts
	def SetEff(self, efficiency):
		self.eff = efficiency

class location:
	def __init__(self,name,lat,lngt):
		self.name = name
		self.latitude = lat
		self.longitude = lngt

	# Imports single column text file, radiation data from 12am 1/1 to 11pm 12/31
	def GetRadData(self, file_name):
		self.hrlyrad = []
		with open(file_name, 'r') as f:
			tmp = f.readlines()
			b = 0
			for i in tmp:
				tmp[b] = tmp[b].rstrip("\n")
				self.hrlyrad.append(int(tmp[b]))
				b+=1

class load:
	def __init__(self,name,watts):
		self.LoadName = name
		self.LoadWatts = watts

class ProfileDaily:
	def __init__(self,name,type):
		self.ProfileName = name

	def SetProfile(self, onoff_vals):
		self.vals = onoff_vals

class ProfileSeason(ProfileDaily):
	def __init__(self, name, start, end):
		self.monthStart = [0,31,59,90,120,151,181,212,243,273,304,334]
		self.start = self.monthStart[start["month"]]+start["date"]
		self.end   = self.monthStart[end["month"]]+end["date"]
		self.SeasonLength = self.end - self.start
		self.SeasonName = name

	def ChangeStart(self, start):
		self.start = self.monthStart[start["month"]]+start["date"]
		self.SeasonLength = self.end - self.start

	def ChangeEnd(self, end):
		self.end   = self.monthStart[end["month"]]+end["date"]
		self.SeasonLength = self.end - self.start

class ProfileAnnual(ProfileSeason):
	def __init__(self):
		self.season = {}

	def AddSeason(self, season):
		myseason = ProfileSeason(season.SeasonName,season.start,season.end)
		#self.season.append

class system(panel,battery,location):
	def __init__(self, blah):
		self.test = blah

mysys = system(12)
myseason = ProfileSeason("Rainy Season",{"month":1,"date":15},{"month":6,"date":15})
print(myseason.SeasonLength)
myseason.ChangeStart({"month":3,"date":15})
print(myseason.SeasonLength)
mysys.GetRadData("raddata")
print(mysys.hrlyrad[1]+mysys.hrlyrad[2]+mysys.hrlyrad[3])
myprofile = ProfileAnnual()
myprofile.AddSeason(myseason)


