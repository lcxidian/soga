1、默认构造函数的书写
类名() = default;
2、
切记———编译合成的默认构造函数中其内置类型或者数组，指针的值若没显式直接初始化，都将是随机值。自己书写的默认构造函数也是这样。

3、有些类，编译器无法合成默认构造函数，如：如果类中包含一个其他类，但这个其他类没有默认的构造函数，或这个默认构造函数是private的，这时编译不能合成默认的构造函数
4、封装的作用
作用一：确保用户代码不会无意间破坏类的结构
作用二：被封装类的具体实现细节可以随时改变，而无需调整用户级别的代码（即接口不变，实现可以变，采用的是动态库方式才可以办到无需调整用户级代码也无需重新编译）
5、关键字mutable
在一个const函数中，可以通过成员变量声明中添加mutable关键字来做到修改类中某个数据成员
如：
class Screen {
public:
	void some_member() const; 
private:
	mutable size_t access_ctr;
};
void Screen::some_member() const
{
	++access_ctr; 
}

6、
class Screen {
public:
    using pos = std::string::size_type;

    Screen() = default; // 1
    Screen(pos ht, pos wd):height(ht),width(wd),contents(ht*wd, ' '){} // 2
    Screen(pos ht, pos wd, char c):height(ht),width(wd),contents(ht*wd, c){} // 3

    char get() const { return contents[cursor]; }
    char get(pos r, pos c) const { return contents[r*width+c]; }
    inline Screen& move(pos r, pos c);
    inline Screen& set(char c);
    inline Screen& set(pos r, pos c, char ch);

    const Screen& display(std::ostream &os) const;
private:
    pos cursor = 0;
    pos height = 0, width = 0;
    std::string contents;
};
使用时，可以这样：myScreen.move(4,0).set('#');
但不可以这样：myScreen.display(cout).set('*'); #因为display返回的是一个const引用

改进：
重载一个display版本：
	const Screen& display(std::ostream &os) const { do_display(os); return *this; }
	Screen& display(std::ostream &os) { do_display(os); return *this; }

	void do_display(std::ostream &os) const { os << contents; }

应用时：
	Screen myScreen(5,3);
	const Screen blank(5, 3);
	myScreen.set('#').display(cout); 
	blank.display(cout);

7、const 类对象只能调用const成员函数（主题是const，局部也应该是const才对），而普通类对象即能调用非const成员函数又能调用const函数
注：这就体现了类设计的时候，const成员函数的重要用途。

8、类的友元
类可以作为另一个类的友元，类的某个成员函数也可以作为另一个类的友元
如：
class Screen {
	friend class Window_mgr;
};
如：
class Screen {
	friend void Window_mgr::clear(ScreenIndex);
};

注：友元函数可以直接在另一个类中定义，但在这个类的外面还对友元函数进行声明
如：
struct X {
friend void f() {  .... }
X() { f(); } #错误，在这之前，f还没有声明就不可以使用
void g();
void h();
};
void X::g() { return f(); } // //错误，在这之前，f还没有声明就不可以使用
void f(); // f 声明
void X::h() { return f(); } // //正确，在这之前，f声明了就可以使用
9、
class Screen {
public:
	void dummy_fcn(pos height) {#错误，Unknown type name 'pos'
		cursor = width * height; 
	}
	typedef std::string::size_type pos;
private:
	pos cursor = 0;
	pos height = 0, width = 0;
};
改进：
class Screen {
public:
	typedef std::string::size_type pos;
	void dummy_fcn(pos height) {
		cursor = width * height;
	}
private:
	pos cursor = 0;
	pos height = 0, width = 0;
};
10、
typedef string Type;
Type initVal(); # use `string`
class Exercise {
public:
    typedef double Type;
    Type setVal(Type); # use `double`
    Type initVal(); # use `double`
private:
    int val;
};

Type Exercise::setVal(Type parm) {  # first is `string`, second is `double`
    val = parm + initVal();     # Exercise::initVal()
    return val;
}
11、类的const成员和引用必须初始化，且必须用构造函数列表初始化
class ConstRef {
public:
	ConstRef(int ii);
private:
	int i;
	const int ci;
	int &ri;
};
ConstRef::ConstRef(int ii)
{ // assignments:
	i = ii; // ok
	ci = ii; // error: cannot assign to a const
	ri = i; // error: ri was never initialized
}
static成员变量都必须在类的外部初始化，如：double Account::interestRate = 5;
除非，该成员变量是const整型且为constexpr，这时可以在类内初始化
12、委托构造函数———即使用其他构造函数来执行自己的初始化
如：
class Sales_data {
public:
	Sales_data(std::string s, unsigned cnt, double price):bookNo(s), units_sold(cnt), revenue(cnt*price) { }
	Sales_data(): Sales_data("", 0, 0) {}
	Sales_data(std::string s): Sales_data(s, 0,0) {}
	Sales_data(std::istream &is): Sales_data() { read(is, *this); }
};

13、类类型的隐式转换
#特别注意：有且只能隐式转换一步，且隐式转换那一步必须有对应的构造函数才能隐式转换成功
如：
sales_data& combine(const sales_data &item)；
a
string null_book = "9-999-99999-9";
item.combine(null_book);#正确，一步转换：null_book转换成sales_data对象(隐式执行了其构造函数)
item.combine("9-999-99999-9");#错误，需要两步才能转换成sales_data对象:"9-999-99999-9"转成string，string转成sales_data对象

item.combine(string("9-999-99999-9"));#正确
item.combine(Sales_data("9-999-99999-9"));#正确
item.combine(cin);#正确
item.combine(Sales_data(null_book));
item.combine(static_cast<Sales_data>(cin));
14、关键字explicit————隐式转换不再可行
class Sales_data {
public:
	Sales_data() = default;
	Sales_data(const std::string &s, unsigned n, double p):
	bookNo(s), units_sold(n), revenue(p*n) { }
	#explici表示一步隐式转换都不再可以
	explicit Sales_data(const std::string &s): bookNo(s) { }
	explicit Sales_data(std::istream&);
}；
item.combine(null_book); #不再正确
item.combine(cin); #不再正确
item.combine(Sales_data(null_book));#正确
item.combine(static_cast<Sales_data>(cin));#正确
15、聚合类————都是public，没有构造函数，没有类内初始值，没有基类
struct Data {
	int ival;
	string s;
};
注：类成员的初始化顺序必须和声明顺序相同
16、字面值常量类
有两个情况：
情况一：聚合类的成员变量都是字面值类型，这种聚合类属于字面值常量类
情况二：类的成员变量都是字面值类型
		至少有一个constexpr构造函数
		析构函数是默认定义的

17、类的static成员变量
static成员变量都必须在类的外部初始化，如：double Account::interestRate = 5;
除非，该成员变量是const整型且为constexpr，这时可以在类内初始化
如：
class Account {
public:
	static double rate() { return interestRate; }
	static void rate(double);
private:
	static constexpr int period = 30;
	double daily_tbl[period];
};

class Account {
public:
	static double rate() { return interestRate; }
	static void rate(double);
private:
	static  int period = 30;#编译不过
	double daily_tbl[period];
};









18
19
20