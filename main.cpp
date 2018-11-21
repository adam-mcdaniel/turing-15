
#include <iostream>
#include <vector>
#include <sstream>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
using namespace std;

#define __auto_reserved__(variable, value) std::decay<decltype(value)>::type variable = value

bool inStr(string s1, string s2)
{
    if (s1.find(s2) != string::npos)
    {
        return true;
    }
    else
    {
        return false;
    }
}

template<typename T>
auto __List__()
{
	vector <T> list;
	return list;
}

template<typename T>
auto __Type__()
{
	T a;
	return a;
}

auto range(int begin, int end)
{
	vector <int> r;
	for (int i = begin; i < end; i++)
	{
		r.push_back(i);
	}
	return r;
}


string read()
{
	string a;
	getline(cin, a);
	return a;
}


template<typename T>
void print(T a)
{
	cout<<a;
}

template<typename T>
void println(T a)
{
	cout<<a<<endl;
}

string get_char()
{
	string s;
 	stringstream ss;

	getline(cin, s);

	if (s.size() > 0)
	{
	 	ss << s.at(0);
	 	ss >> s;
	} else {
		s = " ";
	}

	return s;
}

template<typename T, typename T2>
auto Add(T a, T2 b)
{
	return a+b;
}

int Sub(int a, int b)
{
	return a-b;
}

int Negative(int a)
{
	return -a;
}

template<typename T, typename T2>
auto Mul(T a, T2 b)
{
	return a*b;
}

int Div(int a, int b)
{
	return a/b;
}


template<typename T>
auto Int(T a)
{
	int c = 0;
	stringstream b(a);
	b >> c;
	return c;
}

template<typename T>
auto String(T a)
{
	stringstream b;
	b << a;
	string c = b.str();
	return c;
}

template<typename T, typename T2>
auto Is(T a, T2 b)
{
	return (a==b);
}

template<typename T>
auto Not(T a)
{
	return (!a);
}

template<typename T, typename T2>
auto And(T a, T2 b)
{
	return (a&&b);
}

template<typename T, typename T2>
auto Or(T a, T2 b)
{
	return (a||b);
}

auto console(string a)
{
	system(a.c_str());
}

template<typename T, typename T2>
auto append(T a, T2 b)
{
	auto c = a;
	c.push_back(b);
	return c;
}

template<typename T>
auto len(T a)
{
	return a.size();
}

template<typename T>
auto empty(T a)
{
	a.empty();
	return a;
}

#include "wpilib"

#include "networktables"

#include "sensors"

#include "controls"

class Hiro: public IterativeRobot {
public:

	__auto_reserved__(buttons, Joystick(0));
	__auto_reserved__(joystick, Joystick(1));
	__auto_reserved__(chassis, HiroChassis());
	__auto_reserved__(launcher, HiroLauncher());
	__auto_reserved__(elevator, HiroElevator());
	;
	__auto_reserved__(recordedjoystick, RecordJoystick());
	__auto_reserved__(FMS, None);
	__auto_reserved__(dashboard, NetworkTables.getTable("SmartDashboard"));

	auto robotInit() {

		FMS=driverstation.DriverStation.getInstance();

	}
	auto autonomousInit() {

		chassis.autoDrive(dashboard.getNumber("Setpoint",0));
		auto GameState=FMS.getGameSpecificMessage();
		auto HiroPosition=GetPosition();
		print(GameState);
		print(HiroPosition);
		if (Is(HiroPosition,"Left")) {

			if (Is(GameState[1],"L")) {

				recordedjoystick=recordedjoystick.load("ScaleLeft");

			}
			else if (Is(GameState[0],"L")) {

				recordedjoystick=recordedjoystick.load("SwitchLeft");

			}
			else {

				recordedjoystick=RecordJoystick();

			}

		}
		else if (Is(HiroPosition,"Center")) {

			if (Is(GameState,"L")) {

				recordedjoystick=recordedjoystick.load("SwitchLeftCenter");

			}
			else {

				recordedjoystick=recordedjoystick.load("SwitchRightCenter");

			}

		}
		else {

			recordedjoystick=RecordJoystick();

		}

	}
	auto teleopInit() {

		recordedjoystick=RecordJoystick();

	}
	auto teleopPeriodic() {

		chassis.update(joystick,buttons);
		launcher.update(joystick,buttons);
		elevator.update(joystick,buttons);
		recordedjoystick.recordAxes(joystick);
		recordedjoystick.recordButtons(joystick);

	}
	auto testInit() {

		recordedjoystick.finish("SwitchRightCenter");
		print(recordedjoystick);
		LiveWindow.run();

	}

};



int main(int argc,char* __char_argv__[])
{

	string __file__ = *__char_argv__;
if (Is(__name__,"__main__")) {

	run(Hiro);
	
}

	return 0;

}
