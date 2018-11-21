# include <iostream>
# include <vector>
using namespace std;


template <class SomeType>
SomeType sum (SomeType a, SomeType b)
{
  return a+b;
}


// int main() {
// 	cout << sum<int>(10,20) << endl;
// }

struct Load_Interface;

struct Loader
{
	virtual void visit(Load_Interface&) = 0;
};

struct Load_Interface
{
	virtual void accept_loader(Loader& l)
	{
		l.visit(*this);
	}
};

class Integer : Load_Interface {

};

int main() {
	Integer a;
	a = 9; 
}