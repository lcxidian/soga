1、使用重载运算符
调用非成员函数的重载运算符：
	data1 + data2; // normal expression
	operator+(data1, data2); //
调用类成员函数的重载运算符：
	data1 += data2; // expression-based ''call''
	data1.operator+=(data2);
2、如何判断重载运算符是定义为成员函数还是非成员函数好
#	=、[]、()、->、*运算符必须是成员的
#	复合赋值运算符应该是成员的，如：+=，-=
#	递增、递减、解引用运算符应该是成员的
#	+、—、==、<、>、<=、>=运算符应该是非成员的

3、重载输出运算符
	第一个参数一般是非const ostream对象的引用————因为：ostream对象需要被写入，ostream对象不能拷贝
	第二个参数一般是const引用————因为：不用拷贝，输出操作不会改变其值
	重载输出运算符必须是非成员
如： 
ostream &operator<<(ostream &os, const Sales_data &item)
{
	os << item.isbn() << " " << item.units_sold << " "
	<< item.revenue << " " << item.avg_price();
	return os;
}
3、重载输入运算符
	第一个参数一般是const ostream对象的引用————因为：ostream对象只需被读出，ostream对象不能拷贝
	第二个参数一般是非const引用————因为：不用拷贝，输入操作会写入值
	重载输出运算符必须是非成员
如： 
istream &operator>>(istream &is, Sales_data &item)
{
	double price; // no need to initialize; 
	is >> item.bookNo >> item.units_sold >> price;#只有等所有数据输入完以后才能检查
	if (is) // check that the inputs succeeded
		item.revenue = item.units_sold * price;
	else
		item = Sales_data(); // input failed: give the object the default state
	return is;
}
5、算术运算符
Sales_data	operator+(const Sales_data &lhs, const Sales_data &rhs)
{
	Sales_data sum = lhs; // copy data members from lhs into sum
	sum += rhs; // add rhs into sum
	return sum;
}
6、==运算符
bool operator==(const Sales_data &lhs, const Sales_data &rhs)
{
	return lhs.isbn() == rhs.isbn() &&
	lhs.units_sold == rhs.units_sold &&
	lhs.revenue == rhs.revenue;
}
bool operator!=(const Sales_data &lhs, const Sales_data &rhs)
{
	return !(lhs == rhs);
}
7、关系运算符
8、赋值运算符(必须是成员的，第2条)
class StrVec {
public:
	StrVec &operator=(std::initializer_list<std::string>);
	// other members as in § 13.5 (p. 526)
};

StrVec &StrVec::operator=(initializer_list<string> il)
{
	auto data = alloc_n_copy(il.begin(), il.end());
	free(); // destroy the elements in this object and free the space
	elements = data.first; // update data members to point to the new space
	first_free = cap = data.second;
	return *this;
}
9、复合赋值运算符
Sales_data& Sales_data::operator+=(const Sales_data &rhs)
{
	units_sold += rhs.units_sold;
	revenue += rhs.revenue;
	return *this;
}
10、下标运算符(必须是成员的，第2条)
class StrVec {
public:
	std::string& operator[](std::size_t n)
	{ return elements[n]; }
	const std::string& operator[](std::size_t n) const
	{ return elements[n]; }
private:
	std::string *elements; // pointer to the first element in the array
};

const StrVec cvec = svec; // copy elements from svec into cvec
if (svec.size() && svec[0].empty()) {
	svec[0] = "zero"; // ok: subscript returns a reference to a string
	cvec[0] = "Zip"; // error: subscripting cvec returns a reference to const
}
分析：const对象自然需要“常”[]运算符，否则就会出现非const的svec[i],这样很奇怪，整体是const的，但局部却变成了非const的
11、递增、递减运算符
class StrBlobPtr {
public:
// increment and decrement
StrBlobPtr& operator++(); // prefix operators
StrBlobPtr& operator--();
// other members as before
};
如何区分是前置还是后置运算符呢？ 规定后置版本多一个额外的int类型参数，编译器自动为该形参赋值为0
如：前置运算符
	StrBlobPtr& StrBlobPtr::operator++()
	{
		check(curr, "increment past end of StrBlobPtr");
		++curr; // advance the current state
		return *this;
	}
	StrBlobPtr& StrBlobPtr::operator--()
	{
		--curr; // move the current state back one element
		check(-1, "decrement past begin of StrBlobPtr");
		return *this;
	}
如：后置运算符
	class StrBlobPtr {
	public:
		StrBlobPtr operator++(int); // postfix operators
		StrBlobPtr operator--(int);
	};
	StrBlobPtr StrBlobPtr::operator++(int)
	{
		StrBlobPtr ret = *this; // save the current value
		++*this; // advance one element; prefix ++ checks the increment
		return ret; // return the saved state
	}
	StrBlobPtr StrBlobPtr::operator--(int)
	{
		StrBlobPtr ret = *this; // save the current value
		--*this; // move backward one element; prefix -- checks the decrement
		return ret; // return the saved state
	}
显式调用后置运算符：
	StrBlobPtr p(a1); // p points to the vector inside a1
	p.operator++(0); // call postfix operator++
	p.operator++(); // call prefix operator++
12、成员访问运算符 *、->(成员的，且const函数)
因为是不需要改变其值，则写成常函数
class StrBlobPtr {
public:
	std::string& operator*() const
	{ 
		auto p = check(curr, "dereference past end");
		return (*p)[curr]; 
	}
	std::string* operator->() const
	{ 
		return & this->operator*();
	}
};
使用：
StrBlob a1 = {"hi", "bye", "now"};
StrBlobPtr p(a1); // p points to the vector inside a1
*p = "okay"; // assigns to the first element in a1
cout << p->size() << endl; // prints 4, the size of the first element in a1
cout << (*p).size() << endl; // equivalent to p->size()
13、函数调用运算符()
如果一个类重载了函数调用运算符，则我们可以像使用函数一样使用该类的对象，即函数对象
struct absInt {
	int operator()(int val) const {
		return val < 0 ? -val : val;
	}
};
函数对象类除了定义operator()之外，也可以包含其他成员函数：
class PrintString {
public:
	PrintString(ostream &o = cout, char c = ' '):
		os(o), sep(c) { }
	void operator()(const string &s) const { os << s << sep; }
private:
	ostream &os; // stream on which to write
	char sep; // character to print after each output
};
PrintString printer; // uses the defaults; prints to cout
printer(s); // prints s followed by a space on cout
PrintString errors(cerr, '\n');
errors(s); // prints s followed by a newline on cerr

注：函数对象常用于泛型算法的实参：
如： 
stable_sort(words.begin(), words.end(), ShorterString());

#分析lambla表达式————
	当我们编写一个lambla表达式后，编译器将该表达式翻译成一个未命名类的未命名对象，这个未命名类中含有一个函数调用运算符：
如： 
stable_sort(words.begin(), words.end(),
						[](const string &a, const string &b)
						{ return a.size() < b.size();});
编译器生成类似于： 
class ShorterString {
public:
	bool operator()(const string &s1, const string &s2) const
		{ return s1.size() < s2.size(); }
};
使用： 
stable_sort(words.begin(), words.end(), ShorterString());

再如： 
auto wc = find_if(words.begin(), words.end(),
							[sz](const string &a))
							{return a.size() >= sz}

编译器生成类似： #由于生成这样的类，并不给提供默认构造函数，想要使用这个类就必须提供sz参数的值
class SizeComp {
	SizeComp(size_t n): sz(n) { } // parameter for each captured variable
	bool operator()(const string &s) const
	{ return s.size() >= sz; }
private:
	size_t sz; // a data member for each variable captured by value
};
使用： 
auto wc = find_if(words.begin(), words.end(), SizeComp(sz));
15、标准库定义的函数对象类：算术运算符、关系运算符、逻辑运算符
16、可调用对象有哪些：
			函数
			函数指针
			lambda表达式
			bind创建的对象
			重载了函数调用运算符的类，即函数对象类
a：
什么是调用形式————函数的参数类型和返回值类型
两个不同类型的可调用对象可能共享同一个调用形式：
#函数
int add(int i, int j) { return i + j; }
#lambda表达式
auto mod = [](int i, int j) { return i % j; };
#函数对象类
struct div {
	int operator()(int denominator, int divisor) {
		return denominator / divisor;
	}
};
以上3者的调用形式都是int(int, int) 
b： 
如何把上述3者组合起来：函数表
	map<string, int(*)(int,int)> binops;
调用时：
	binops.insert({"+", add}); // {"+", add} is a pair § 11.2.3 (p. 426)
	binops.insert({"%", mod}); // error: mod is not a pointer to function
问题来了：mod，div不是函数指针，怎么办？
解决办法：标准库function类
function的操作：#T为调用形式
function<T> f;				隐式地构造一个存储可调用对象的空function
function<T> f(nullptr);		显式地构造一个存储可调用对象的空function
function<T> f(obj);			
f 							将f作为条件，若f中含有可调用对象，则为真					
f(args)						

定义为function<T>的成员的类型：
result_type					该function类型的可调用对象返回值的类型
argument_type
first_argument_type
second_argument_type

使用： 
function<int(int, int)> f1 = add; // function pointer
function<int(int, int)> f2 = div(); // object of a function-object class
function<int(int, int)> f3 = [](int i, int j){ return i * j; };
cout << f1(4,2) << endl; // prints 6
cout << f2(4,2) << endl; // prints 2
cout << f3(4,2) << endl; // prints

map<string, function<int(int, int)>> binops;

binops["+"](10, 5); // calls add(10, 5)
binops["-"](10, 5); // uses the call operator of the minus<int> object
binops["/"](10, 5); // uses the call operator of the div object
binops["*"](10, 5); // calls the lambda function object
binops["%"](10, 5); // calls the lambda function object
注：不能将重载函数存入function类对象中
int add(int i, int j) { return i + j; }
Sales_data add(const Sales_data&, const Sales_data&);#重载函数 
map<string, function<int(int, int)>> binops;
binops.insert( {"+", add} ); // 编译器搞不清: which add?
17、类类型转换运算符
string null_book = "9-9999-99"
item.combine(null_book);
#分析：实参非显式调用构造函数：将实参类型的对象转换成类类型。
同理：
#分析：类类型的类型转换，通过定义类类型转换运算符来完成。

引出了类类型转换运算符的概念：
	类类型转换运算符是类的一种特殊成员函数，它负责将类类型的值转换成其他类型
	其类类型运算符的形式：operator type() const; //没有参数
			#type表示要转换成的类型：只要type这种类型可做为函数的返回值，但不能是数组或函数类型，可以是数组指针或函数指针
如： 
class SmallInt {
public:
	SmallInt(int i = 0): val(i)#即定义了向类类型转换
	{
		if (i < 0 || i > 255)
			throw std::out_of_range("Bad SmallInt value");
	}
	//类类型转换运算符
	operator int() const { return val; }#又定义了类类型向其他类型转换
private:
	std::size_t val;
};
注：编译器只能对类类型转换走一步，但可以置于内置类型转换之前或之后都行
如： 
SmallInt si = 3.14; // 构造函数
si + 3.14; //类类型转换运算符->int内置类型->double类型

#类类型运算符可能会产生意外
在实践中，很少使用，但定义向bool的类类型转换比较常用：
int i = 42;
while (std::cin >> value)#cin被istream的类类型转换运算符隐式转换成了bool变量

#显式的类型转换运算符
class SmallInt {
public:
	explicit operator int() const { return val; }#表示编译器不会自动执行这一步，除非显式的类类型转换
};

SmallInt si = 3; // ok: the SmallInt constructor is not explicit
si + 3; # error: implicit is conversion required, but operator int is explicit
static_cast<int>(si) + 3; # ok: explicitly request the conversion
18、类型转换的二义性
如果一个类中包含一个或多个类类型转换，必须确保在类类型和目标类型之间只存在一种转换方式，否则会产生二义性
如： 
struct B;
struct A {
	A() = default;
	A(const B&); # B 转换成 A
};
struct B {
	operator A() const; # B 转换成 A
};
A f(const A&);
B b;
A a = f(b);#产生二义性

