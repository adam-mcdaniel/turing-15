

import os
# import _ctypes

def inStr(s1, s2):
	return (s1 in s2)

def read():
	return input()

def write(a):
	print(a, end='')

def writeln(a):
	print(a)

def get_char():
	return input()[0]

def Add(a, b):
	return a+b

def Sub(a, b):
	return a-b

def Negative(a):
	return -a

def Mul(a, b):
	return a*b

def Div(a, b):
	return int(a/b)

def Int(a):
	return int(a)

def String(a):
	return str(a)

def Is(a, b):
	return (a==b)

def In(a, b):
	return (a in b)

def Not(a):
	return (not a)

def And(a, b):
	return (a and b)

def Or(a, b):
	return (a or b)

def Greater(a, b):
	return (a > b)

def Less(a, b):
	return (a < b)

# def dereference(obj_id):
#     return _ctypes.PyObj_FromPtr(obj_id)

def append(a, b):
	c = list(a)
	c.append(b)
	return c

def empty(a):
	return []

def console(a):
	os.system(a)


from wpilib import *

from networktables import *

from sensors import *

from controls import *

from subsystems import *

class Hiro(IterativeRobot):

	buttons = Joystick(0)
	
	joystick = Joystick(1)
	
	chassis = HiroChassis()
	
	launcher = HiroLauncher()
	
	elevator = HiroElevator()
	
	
	recordedjoystick = RecordJoystick()
	
	FMS = None
	
	dashboard = NetworkTables.getTable("SmartDashboard")
	
	
	def robotInit(this):
	
		this.FMS=driverstation.DriverStation.getInstance()
		
	
	def autonomousInit(this):
	
		this.chassis.autoDrive(this.dashboard.getNumber("Setpoint",0))
		GameState=this.FMS.getGameSpecificMessage()
		HiroPosition=GetPosition()
		print(GameState)
		print(HiroPosition)
		if (Is(HiroPosition,"Left")):
		
			if (Is(GameState[1],"L")):
			
				this.recordedjoystick=this.recordedjoystick.load("ScaleLeft")
				
			
			elif (Is(GameState[0],"L")):
			
				this.recordedjoystick=this.recordedjoystick.load("SwitchLeft")
				
			
			else:
			
				this.recordedjoystick=RecordJoystick()
				
			
			
		
		elif (Is(HiroPosition,"Center")):
		
			if (Is(GameState,"L")):
			
				this.recordedjoystick=this.recordedjoystick.load("SwitchLeftCenter")
				
			
			else:
			
				this.recordedjoystick=this.recordedjoystick.load("SwitchRightCenter")
				
			
			
		
		else:
		
			this.recordedjoystick=RecordJoystick()
			
		
		
	
	def teleopInit(this):
	
		this.recordedjoystick=RecordJoystick()
		
	
	def teleopPeriodic(this):
	
		this.chassis.update(this.joystick,this.buttons)
		this.launcher.update(this.joystick,this.buttons)
		this.elevator.update(this.joystick,this.buttons)
		this.recordedjoystick.recordAxes(this.joystick)
		this.recordedjoystick.recordButtons(this.joystick)
		
	
	def testInit(this):
	
		this.recordedjoystick.finish("SwitchRightCenter")
		print(this.recordedjoystick)
		LiveWindow.run()
		
	
	

if (Is(__name__,"__main__")):

	run(Hiro)
	

