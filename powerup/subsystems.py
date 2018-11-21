

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

from ctre import *

from sensors import *

from controls import *

from networktables import *

class ChassisPIDs(RobotDrive):

	gyro = Gyro(scale_factor=6.744578313253012)
	gyroPID = PIDController(0.045,0.003,0.05,gyro.getAngle,lambda a: None)

	motors = []
	left_motors = []
	right_motors = []


	def __init__(this,lfm, lbm, rfm, rbm ):

		super().__init__(lfm, lbm, rfm, rbm)
		this.gyroPID.setOutputRange(Negative(0.8),0.8)
		this.gyroPID.enable()
		this.motors=append(this.motors,leftFrontMotor)
		this.motors=append(this.motors,leftRearMotor)
		this.motors=append(this.motors,rightFrontMotor)
		this.motors=append(this.motors,rightRearMotor)
		this.left_motors=append(this.left_motors,leftFrontMotor)
		this.left_motors=append(this.left_motors,leftRearMotor)
		this.right_motors=append(this.right_motors,rightFrontMotor)
		this.right_motors=append(this.right_motors,rightRearMotor)
		for motor in this.motors:

			motor.resetPostion()


		this.setSafetyEnabled(True)


	def goToAngle(this,angle ):

		this.gyroPID.setSetpoint(angle)
		print(this.gyroPID.getP())
		print(this.gyroPID.getI())
		print(this.gyroPID.getD())
		for i in range(0,150):

			timer.Timer.delay(Div(1,50))
			dashboard.putNumber("Angle",gyro.getAngle())
			this.arcadeDrive(0,this.gyroPID.get())




	def autoDrive(this,angle ):

		this.goToAngle(angle)


	def Out(this):

		pass




class Chassis(ChassisPIDs):

	shifter = DoubleSolenoid(20,0,1)

	currentGear = "Extended"



	def __init__(this,lfm, lbm, rfm, rbm ):

		super().__init__(lfm, lbm, rfm, rbm)


	def update(this,joystick, buttons ):

		dashboard.putNumber("RightFrontPosition",rightFrontMotor.getPosition())
		dashboard.putNumber("LeftFrontPosition",leftFrontMotor.getPosition())
		dashboard.putNumber("Gyro",gyro.getAngle())
		self.arcadeDrive(joystick.getRawAxis(controls.joystick['forward-axis']), joystick.getRawAxis(controls.joystick['turn-axis']) * 0.8)


	def shift(this):

		this.arcadeDrive(0,0)
		timer.Timer.delay(0.2)
		if (Is(this.currentGear,"Extended")):

			this.currentGear="Retracted"
			this.shifter.set(DoubleSolenoid.Value.kReverse)


		elif (Is(this.currentGear,"Retracted")):

			this.currentGear="Extended"
			this.shifter.set(DoubleSolenoid.Value.kReverse)




	def getLeftPosition(this):

		return leftFrontMotor.getRawPosition()


	def getRightPosition(this):

		return rightFrontMotor.getRawPosition()




class Launcher(RobotDrive):

	launchA = None

	liftA = None

	currentLifted = "Extended"

	locked = True

	cubeState = True

	wait = 0



	def __init__(this,launcherArms, lifterArms ):

		super().__init__(leftIntakeMotor, rightIntakeMotor)
		this.launchA=launcherArms
		this.liftA=lifterArms
		this.liftA.set(DoubleSolenoid.Value.kReverse)
		this.toggle()
		this.toggle()
		this.setSafetyEnabled(True)


	def update(this,joystick, buttons ):

		t = controls.joystick['intake']
		if (joystick.getRawButton(t)):

			intake()


		t = controls.joystick['outtake']
		if (joystick.getRawButton(t)):

			outtake()
			this.cubeState=False


		t = controls.joystick['launch']
		if (joystick.getRawButton(t)):

			launch()
			this.cubeState=False


		t = controls.joystick['toggle']
		if (And(joystick.getRawButton(t),Or(Less(this.wait,0),Is(this.wait,0)))):

			toggle()
			this.wait=25
			if (this.locked):

				this.locked=False
				close()


			else:

				this.locked=True




		else:

			this.wait=Sub(this.wait,1)


		t = buttons.getRawButton(controls.buttons['close']) or joystick.getRawButton(controls.joystick['close']) or self.locked
		if (t):

			close()


		else:

			open()


		if (cube()):

			dashboard.putNumber("HasCube",1)


		else:

			dashboard.putNumber("HasCube",0)




	def launch(this):

		this.arcadeDrive(Negative(1),0)


	def intake(this):

		this.arcadeDrive(0.8,0)


	def cube(this):

		t = leftIntakeMotor.getOutputCurrent() > 28 and rightIntakeMotor.getOutputCurrent() > 28
		return t


	def outtake(this):

		this.arcadeDrive(Negative(0.65),0)


	def cattywampus(this):

		this.arcadeDrive(0,Negative(0.7))


	def toggle(this):

		if (Is(this.currentLifted,"Extended")):

			this.currentLifted="Retracted"
			this.liftA.set(DoubleSolenoid.Value.kReverse)


		else:

			this.currentLifted="Extended"
			this.liftA.set(DoubleSolenoid.Value.kForward)




	def open(this):

		this.launchA.set(DoubleSolenoid.Value.kForward)


	def close(this):

		this.launchA.set(DoubleSolenoid.Value.kReverse)




class Elevator:

	state = "Descending"

	cycle = 0

	carriageL = None

	launcherArms = None

	lim = None

	rim = None



	def __init__(this,carriageLift, lA, LIM, RIM ):

		this.carriageL=carriageLift
		this.launcherArms=lA
		this.lim=LIM
		this.rim=RIM


	def getPosition(this):

		return this.carriageL.getPosition()


	def lift(this):

		this.state="Lifting"


	def descend(this):

		this.state="Descending"


	def exchange(this):

		this.carriageL.set(Negative(0.6))
		this.launcherArms.set(DoubleSolenoid.Value.kReverse)
		timer.Timer.delay(0.6)
		r=RobotDrive(this.lim,this.rim)
		r.arcadeDrive(Negative(1),0)
		this.carriageL.set(0)
		timer.Timer.delay(0.4)


	def update(this,joystick, buttons ):

		t = controls.joystick['lift']
		if (joystick.getRawButton(t)):

			this.lift()


		t = controls.joystick['descend']
		if (joystick.getRawButton(t)):

			this.descend()


		t = controls.joystick['exchange']
		if (joystick.getRawButton(t)):

			this.exchange()


		if (Is(this.state,"Descending")):

			this.carriageL.set(0)
			this.cycle=0


		elif (Is(this.state,"Lifting")):

			if (Less(this.cycle,30)):

				this.carriageL.set(Negative(1))
				this.cycle=Add(this.cycle,1)


			elif (Less(this.cycle,40)):

				this.carriageL.set(Negative(0.4))
				this.cycle=Add(this.cycle,1)


			else:

				this.carriageL.set(Negative(0.1))




		dashboard.putNumber("Elevator position",this.getPosition())




dashboard=NetworkTables.getTable("SmartDashboard")
def GetPosition():

	return(dashboard.getString("Auto Selector","Center"))



compressor=Compressor()
leftFrontMotor=DriveMotor(1)
leftCenterMotor=FollowMotor(3,leftFrontMotor)
leftRearMotor=DriveMotor(2)
rightFrontMotor=DriveMotor(4)
rightCenterMotor=FollowMotor(5,rightFrontMotor)
rightRearMotor=DriveMotor(6)
carriageLift=DriveMotor(7)
leftIntakeMotor=wpi_talonsrx.WPI_TalonSRX(8)
rightIntakeMotor=wpi_talonsrx.WPI_TalonSRX(9)
leftIntakeMotor.setInverted(True)
launcherArms=DoubleSolenoid(20,4,5)
lifterArms=DoubleSolenoid(20,2,3)
gyro = Gyro(scale_factor=6.744578313253012)
gyro.calibrate()
ultrasonic_sensor=UltraSonicSensor(2)
def HiroChassis():

	return(Chassis(leftFrontMotor,leftRearMotor,rightFrontMotor,rightRearMotor))



def HiroLauncher():

	return Launcher(launcherArms,lifterArms)



def HiroElevator():

	return Elevator(carriageLift,launcherArms,leftIntakeMotor,rightIntakeMotor)



dashboard.putStringArray('Auto List', ['Left', 'Right', 'Center'])
