import wpilib
import ctre
import time
# NetworkTables.initialize(server='roborio-6517-frc.local')

"""
by deanna :) start
"""

# points = [
#     # Waypoint @ x=-4, y=-1, exit angle=-45 degrees
#     pf.Waypoint(-4, -1, radians(-45.0)),
#     # Waypoint @ x=-2, y=-2, exit angle=0 radians
#     pf.Waypoint(-2, -2, 0),
#     # Waypoint @ x=0, y=0,   exit angle=0 radians
#     pf.Waypoint(0, 0, 0),
# ]
#
# info, trajectory = pf.generate(points, pf.FIT_HERMITE_CUBIC,
#                                pf.SAMPLES_HIGH, 0.05, 1.7, 2.0, 60.0)
#
# modifier = pf.modifiers.TankModifier(trajectory).modify(0.5)
# pickle_file = os.path.join(os.path.dirname(__file__), 'trajectory.pickle')
#
# if wpilib.RobotBase.isSimulation():
#     with open(pickle_file, 'wb') as fp:
#         pickle.dump(trajectory, fp)
# else:
#     with open('fname', 'rb') as fp:
#         trajectory = pickle.load(fp)


class Gyro(wpilib.adxrs450_gyro.ADXRS450_Gyro):
    def __init__(self, **kwargs):
        self.scale_factor = kwargs["scale_factor"]
        super().__init__()

    def getAngle(self):
        return super().getAngle() * self.scale_factor

    def reset(self):
        self.calibrate()


class UltraSonicSensor():
    def __init__(self, channel):
        self.analog_input = wpilib.analoginput.AnalogInput(channel)
        self.inches_away = 8.5714 * 9.8 * self.analog_input.getAverageVoltage()
        self.cycle_limit = 4

        self.PID = wpilib.PIDController(
            0.03, 0, 0.1, self.AvgInchesAway, self.Out)
        self.PID.setSetpoint(0)
        self.PID.enable()

    def AvgInchesAway(self):
        self.inches_away *= (self.cycle_limit - 1) / self.cycle_limit
        self.inches_away += (8.5714 * 9.8 *
                             self.analog_input.getAverageVoltage()) / self.cycle_limit

        return self.inches_away

    def InchesAway(self):
        return 8.5714 * 9.8 * self.analog_input.getAverageVoltage()

    def returnSpeed(self):
        return self.PID.get()

    def setTarget(self, distance):
        self.PID.setSetpoint(distance)

    def Out(self, input):
        pass


class DriveMotor(ctre.wpi_talonsrx.WPI_TalonSRX):
    def __init__(self, CAN_Id):
        super().__init__(CAN_Id)
        self.inverted = 1
        self.PID = wpilib.PIDController(
            0.22, 0, 0.33, self.getPosition, self.Out)
        self.PID.setSetpoint(0)
        self.PID.enable()

    # def set(self, value):
    #     super().set(value)

    def invert(self):
        self.inverted = -1

    def getSpeed(self):
        return self.inverted * (self.getPulseWidthVelocity() / 4096) * 10 * (6 * 3.14159) / 12

    def getPosition(self):
        return self.inverted * (self.getQuadraturePosition() / 4096) * 6 * 3.14159

    def getRawPosition(self):
        return self.getQuadraturePosition()

    def resetPostion(self):
        self.setQuadraturePosition(0, 0)

    def setTarget(self, distance):
        self.PID.setSetpoint(distance)

    def posReturnSpeed(self):
        return self.PID.get()

    def auto(self):
        self.set(self.posReturnSpeed())

    def Out(self, input):
        pass


class FollowMotor(DriveMotor):
    def __init__(self, CAN_Id, motor):
        super().__init__(CAN_Id)
        self.follow(motor)


class SensorMotor(ctre.wpi_talonsrx.WPI_TalonSRX):
    def __init__(self):
        self.starting_check = True
        self.time_held = 0

    def underLoad(self):
        if self.getOutputCurrent() > 2:
            if self.starting_check:
                self.time_held = time.time()
            self.starting_check = True

        if self.getOutputCurrent() > 2 and (time.time() - self.time_held) > 0.25:
            return True
        else:
            return False
