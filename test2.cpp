// constructing maps
#include <iostream>
#include <map>
using namespace std;


class Variable
{	
public:
	int numbers;
	bool boolean;
	string string;

	template <class T>
	T create(T a) {
		// switch(typeid(a).name())
		// {
		// 	case :

		// }
		cout << typeid(a).name() << endl;
	}
};


int main ()
{

	Variable a = Variable.create<int>(9);
	return 0;
}