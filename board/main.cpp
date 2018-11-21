
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

class Board {
public:

	__auto_reserved__(board_list, __List__<vector<string>>());
	__auto_reserved__(empty_list, __List__<string>());
	__auto_reserved__(size, 0);
	
	auto empty_board() {
	
		board_list=empty(board_list);
		for (auto x:range(0,size)) {
		
			board_list=append(board_list,empty_list);
			
		}
		for (auto x:range(0,size)) {
		
			for (auto y:range(0,size)) {
			
				board_list[x]=append(board_list[x]," ");
				
			}
			
		}
		
	}
	auto print_board() {
	
		console("clear");
		for (auto y:range(0,size)) {
		
			for (auto x:range(0,size)) {
			
				print(board_list[y][x]);
				
			}
			println("");
			
		}
		
	}
	template<typename type0, typename type1, typename type2 >auto change_val(type0 x, type1 y, type2 val ) {
	
		board_list[y][x]=val;
		
	}
	template<typename type0 >auto add_wall(type0 wall ) {
	
		change_val(wall.x,wall.y,"W");
		
	}
	template<typename type0 >auto add_player(type0 player ) {
	
		change_val(player.x,player.y,"A");
		
	}
	template<typename type0 >
	Board (type0 _size ) {
	
		size=_size;
		empty_board();
		
	}
	
};

class Wall {
public:

	__auto_reserved__(x, 0);
	__auto_reserved__(y, 0);
	
	template<typename type0, typename type1 >
	Wall (type0 _x, type1 _y ) {
	
		x=_x;
		y=_y;
		
	}
	
};

class Player {
public:

	__auto_reserved__(x, 0);
	__auto_reserved__(y, 0);
	
	template<typename type0 >auto move(type0 movement ) {
	
		x=Add(x,movement[0]);
		y=Add(y,movement[1]);
		
	}
	template<typename type0, typename type1 >
	Player (type0 _x, type1 _y ) {
	
		x=_x;
		y=_y;
		
	}
	
};

class Controls {
public:

	string input="";
	__auto_reserved__(movement, __List__<int>());
	
	auto get_input() {
	
		auto m_length=len(movement);
		for (auto x:range(0,m_length)) {
		
			movement[x]=0;
			
		}
		input=get_char();
		if (inStr("w",input)) {
		
			movement[1]=-1;
			
		}
		else if (inStr("a",input)) {
		
			movement[0]=-1;
			
		}
		else if (inStr("s",input)) {
		
			movement[1]=1;
			
		}
		else if (inStr("d",input)) {
		
			movement[0]=1;
			
		}
		return movement;
		
	}
	
	Controls () {
	
		movement=append(movement,0);
		movement=append(movement,0);
		
	}
	
};

template<typename type0, typename type1, typename type2, typename type3 >auto build_wall(type0 x, type1 y, type2 _x, type3 _y ) {

	__auto_reserved__(store_walls, __List__<Wall>());
	for (auto i:range(x,_x)) {
	
		for (auto j:range(y,_y)) {
		
			auto w=Wall(i,j);
			store_walls=append(store_walls,w);
			
		}
		
	}
	return store_walls;
	
}

template<typename type0, typename type1, typename type2, typename type3 >auto draw_box(type0 x, type1 y, type2 _x, type3 _y ) {

	__auto_reserved__(ws, __List__<vector<Wall>>());
	auto store_walls=build_wall(x,y,Add(x,1),Sub(_y,1));
	ws=append(ws,store_walls);
	store_walls=build_wall(x,y,Sub(_x,1),Add(x,1));
	ws=append(ws,store_walls);
	store_walls=build_wall(x,Sub(_y,2),Sub(_y,1),Sub(_y,1));
	ws=append(ws,store_walls);
	store_walls=build_wall(Sub(_x,2),x,Sub(_x,1),Sub(_y,1));
	ws=append(ws,store_walls);
	return ws;
	
}

auto start() {

	int size=16;
	__auto_reserved__(ws, __List__<vector<Wall>>());
	auto b=Board(size);
	auto player=Player(Div(size,2),Div(size,2));
	__auto_reserved__(input, __List__<int>());
	auto controls=Controls();
	while (true) {
	
		for (auto wall_list:ws) {
		
			for (auto wall:wall_list) {
			
				b.add_wall(wall);
				
			}
			
		}
		b.add_player(player);
		b.print_board();
		b.change_val(player.x,player.y," ");
		input=controls.get_input();
		player.move(input);
		
	}
	
}



int main(int argc,char* __char_argv__[])
{

	string __file__ = *__char_argv__;
auto b=Board(16);
b.print_board();



start();

	return 0;

}

