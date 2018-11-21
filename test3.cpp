
#include "iostream"
// #include <map>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

#define __auto_reserved__(variable, value) std::decay<decltype(value)>::type variable = value


// template <typename T1, typename T2>
// auto mapp(T1 values, T2 fun) {
// 	std::vector<decltype(
// 		fun(std::declval<typename decltype(values)::value_type>()))> results{};
// 	for (auto v : values) {
// 		results.push_back(fun(v));
// 	}
// 	return results;
// }

template<typename T>
auto __List__() {
	vector <T> list;
	return list;
}

// class BufferToggle
// {
//     private:
//         struct termios t;

//     public:

//         /*
//          * Disables buffered input
//          */

//         void off(void)
//         {
//             tcgetattr(STDIN_FILENO, &t); //get the current terminal I/O structure
//             t.c_lflag &= ~ICANON; //Manipulate the flag bits to do what you want it to do
//             tcsetattr(STDIN_FILENO, TSCANOW, &t); //Apply the new settings
//         }


//         /*
//          * Enables buffered input
//          */

//         void on(void)
//         {
//             tcgetattr(STDIN_FILENO, &t); //get the current terminal I/O structure
//             t.c_lflag |= ICANON; //Manipulate the flag bits to do what you want it to do
//             tcsetattr(STDIN_FILENO, TSCANOW, &t); //Apply the new settings
//         }
// };

class Dog
{        
public:

	string name;
	__auto_reserved__(x, __List__<int>());

	template<typename T>
    Dog(T a) {
    	name = a;
    }

    void PrintName() {
    	cout << name << endl;
    }

};




// template<typename T>
// auto ReturnList() {
// 	vector <T> list;
// 	return list;
// }


auto range(int begin, int end)
{
	vector <int> r;
	for (int i = begin; i < end; i++)
	{
		r.push_back(i);
	}
	return r;
}



// template<typename T, typename T2>
// auto append(T *a, T2 b) {
// 	a.push_back(b);
// }


// auto returnChar()
// {

// 	stringstream ss;
// 	string a;
//     BufferToggle bt;
//     bt.off();
//     char b = getchar();
// 	ss << b;
// 	ss >> a;
//     return a;
// }

string get_char()
{
 	stringstream ss;
	char c;
	string s;
	cin.get(c);


 	ss << c;
 	ss >> s;

	return s;
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



int main()
{	
	int a = 10;
	cout << String(a+9) + " is gay lol" << endl;


	// string s = get_char();
	// cout<<s<<endl;
	// // x = (list [Dog])
	// __auto_reserved__(x, __List__<vector<int>>());
	// __auto_reserved__(y, __List__<int>());
	
	// y.append(0);


	// for (auto r : range(0,8))
	// {
	// 	x.push_back(y);
	// 	cout << "adding: " << r << endl;
	// }

	// // x.push_back(Dog("Hey there friend!"));

	// cout << "length: " << x.size() << endl;

	// // for (auto pup : x) // access by reference to avoid copying
	// // {  
	// // 	pup.PrintName();
	// // }

}