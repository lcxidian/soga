0、	默认初始化：调用默认构造函数（对于类类型，默认初始化会调用构造函数，对于内置类型，默认初始化会出现预想不到的情况）
	直接初始化：调用对应的构造函数
	拷贝初始化：调用拷贝构造函数
#默认初始化
当动态分配的对象是内置类型时，默认初始化的值是未定义的
当动态分配的对象是类类型时，默认初始化的值是调用其类的默认构造函数进行初始化
如：
string *ps = new string; #默认初始化，初始值为空字符串
int *pi = new int; #默认初始化，初始值为未定义
1、面向对象编程的核心就是数据抽象、继承、动态绑定
	数据抽象————让接口和实现分离，使得动态链接的程序不需要重新编译
	继承———————定义相似的类，并对其相似关系进行建模
	动态绑定————一定程度上忽略了相似类型的差别，而以统一的方式使用它们的对象
2、继承
基类负责定义在层次关系中所有类共同拥有的成员，派生类定义各自特有的成员
如：
class Quote {
public:
    std::string isbn() const;
    virtual double net_price(std::size_t n) const;#virtual表明希望派生类各自定义自己的版本
}
class Bulk_quote : public Quote { // Bulk_quote inherits from Quote
public:
    double net_price(std::size_t) const override;#override显式表明它使用哪个成员函数改写基类的虚函数
};
分析：1）基类的成员函数分为2种，一种是基类希望派生类直接继承的，一种是基类希望派生类进行覆盖的
	2）如果基类把函数声明为虚函数，这在派生类中该函数也是虚函数，即使没有写virtual
	3）我们使用指针或引用调用虚函数时，该调用将被动态绑定，即在运行时决定使用哪个版本的函数：根据指针或引用所绑定的对象类型，决定调用哪个版本的虚函数
	4）如果调用的该成员函数是非虚函数，则其解析过程发生在编译时，而不是运行时，反之，如果调用的该成员函数是虚函数，则其解析过程发生在运行时
	5）派生类可以不覆盖它继承而来的虚函数，如果没有覆盖，则派生类使用的是基类的虚函数
	6）访问说明符的作用是控制派从基类继承而来的成员是否对派生类的用户可见
#派生类对象的数据成员在内存的结构：
class Quote {
public:
    Quote() = default;  // = default see § 7.1.4 (p. 264)
    Quote(const std::string &book, double sales_price):
                     bookNo(book), price(sales_price) { }
    std::string isbn() const { return bookNo; }
    virtual double net_price(std::size_t n) const
               { return n * price; }
    virtual ~Quote() = default; // dynamic binding for the destructor
private:
    std::string bookNo; // ISBN number of this item
protected:
    double price = 0.0; // normal, undiscounted price
};		

class Bulk_quote : public Quote { // Bulk_quote inherits from Quote
    Bulk_quote() = default;
    Bulk_quote(const std::string&, double, std::size_t, double);
 purchase discount policy
    double net_price(std::size_t) const override;
private:
    std::size_t min_qty = 0; // minimum purchase for the discount to apply
    double discount = 0.0;   // fractional discount to apply
};
分析：
		1）Bulk_quote对象的内存结构：
			（从基类继承而来的）	bookNo
								price
								-----
			（派生类自定义的）		min_qty
								discount
		2）可以看出不管是private还是public还是protected，都继承来了，只是private那部分无权访问而已
		3）从基类继承而来的成员，不能直接初始化，而是必须使用基类的构造函数才能对其初始化
		如：
			Bulk_quote(const std::string& book, double p,
					   std::size_t qty, double disc) :
					   Quote(book, p), min_qty(qty), discount(disc) { }
			};
		4）若派生类的构造函数没有调用基类构造函数去初始化基类那部分成员，则会对基类成员像数据成员一样进行默认初始化，#调用基类的默认构造函数还是基类成员的各自的默认构造函数
		如：
			Bulk_quote(const std::string& book, double p,
					   std::size_t qty, double disc) :
					   min_qty(qty), discount(disc) { }
			};
		5）可继承和可访问是两回事
		6）有时候我们希望其他类不要继承，则在类名后添加final关键字即可
		如：
			class NoDerived final { /*  */ };
			class Base { /*  */ };
			class Last final : Base { /*  */ }; 
			class Bad : NoDerived { /*  */ };   // error: NoDerived is final
			class Bad2 : Last { /*  */ };       // error: Last is final
3、动态绑定
double print_total(ostream &os,
                   const Quote &item, size_t n)
{
    double ret = item.net_price(n);
    os << "ISBN: " << item.isbn() // calls Quote::isbn
       << " # sold: " << n << " total due: " << ret << endl;
     return ret;
}
分析：net_price是虚函数，且被指针或引用调用，故会发生动态绑定：在编译器运行时才能决定调用哪个版本的net_price，有可能调用基类版本的net_price，也可能调用派生类版本的net_price
4、静态类型和动态类型
	我们可以使用一个派生类指针或引用赋给基类对象，但我们并不清楚该指针或引用所绑定对象的真实类型，有可能是派生类对象，也有可能是基类对象
分析：
	1）当使用存在继承关系的类型时，该变量或其他表达式的静态类型和动态类型很可能并不相同。其静态类型在编译的时候就决定了，而其动态类型在运行时才能确定
	如：
	double print_total(ostream &os, const Quote &item, size_t n){
		double ret = item.net_price(n);
		os << "ISBN: " << item.isbn() // calls Quote::isbn
		   << " # sold: " << n << " total due: " << ret << endl;
		 return ret;
	}
	item的静态类型是Quote&，而它的动态类型依据item绑定的实参所决定。只有在运行时才可知。
    2）如果表达式既不是指针也不是引用，则静态类型和动态类型始终相同
	3）之所以存在派生类向基类的类型转换是因为派生类对象都包含了一个基类部分，但不存在基类向派生类的隐身转换
	如：
		Bulk_quote bulk;
		Quote *itemP = &bulk;        // 正确
		Bulk_quote *bulkP = itemP;	 // 错误
	4）派生类向基类的自动类型转换只针对指针或引用的时候才有效，实际上我们确实希望将派生类对象转换成它的基类类型。但这种转换发生的过程与我们期望的有所差别：
	如：
	Bulk_quote bulk;   // object of derived type
	Quote item(bulk);  // 调用的是 Quote::Quote(const Quote&) constructor
	item = bulk;       // 调用的是 Quote::operator=(const Quote&)
	上述过程会忽略基类的那部分
	分析：我们初始化或赋值一个类类型的对象时，实际上是在调用该对象所属类的拷贝(移动)构造函数或拷贝(移动)赋值运算符；当派生类对象初始化一个基类对象时，是给基类的拷贝(移动)拷贝函数传递一个派生类对象，该构造函数只能处理基类自己的成员；当派生类对象赋值给一个基类对象时，是给基类的拷贝(移动)赋值运算符传递一个派生类对象，该赋值运算符只能处理基类自己的成员。
5、(不管是基类还是派生类的)基类的指针或引用调用函数时，我们并不知道该函数真正作用的对象是什么类型，它可能是一个基类的对象或派生类对象。
	若函数是虚函数，则运行时才决定到底执行哪个版本的函数
	如：
		Quote base("0-201-82470-1", 50);
		print_total(cout, base, 10);    #调用 Quote::net_price
		Bulk_quote derived("0-201-82470-1", 50, 5, .19);
		print_total(cout, derived, 10); #调用 Bulk_quote::net_price
	若函数不是虚函数，则在编译的时候就决定了。因为对象的静态类型和动态类型始终是一致的
注：再强调一遍：只有当指针或引用调用虚函数时，才会发生动态绑定！！！对象调用虚函数时，不会发生动态绑定
6、派生类覆盖基类的虚函数时，其形参和返回值必须和基类保持相同，除一种情况例外，即该虚函数的返回类型是基类的指针或引用
7、override关键字
struct B {
    virtual void f1(int) const;
    virtual void f2();
    void f3();
};
struct D1 : B {
    void f1(int) const override; // ok: f1 matches f1 in the base
    void f2(int)； #派生类并没有覆盖掉基类的虚函数，因此派生类有两个版本的f2函数，这就叫做重载。不是覆盖
    void f3() override;    # error: 只有虚函数可以被覆盖
    void f4() override;    // error: B doesn't have a function named f4
};
8、虚函数的默认实参是静态绑定的，而不是动态绑定，即派生类的指针或引用调用虚函数时，默认实参是基类的
如：
9、如何强迫执行特定版本的虚函数
如：
	double undiscounted = baseP->Quote::net_price(42);
10、抽象基类————存在纯虚函数的类
	1）抽象基类负责定义接口，而派生类覆盖该接口；
	2）不能使用抽象类直接创建一个实例对象；
	3）抽象类可以给出纯虚函数的定义，但必须在类外部定义，派生类是看不见这个函数的定义
	4）派生类的构造函数只能初始化直接基类，不能初始化间接基类
如： 
// derived classes will implement pricing strategies using these data
class Disc_quote : public Quote {
public:
    Disc_quote() = default;
    Disc_quote(const std::string& book, double price,
              std::size_t qty, double disc):
                 Quote(book, price),
                 quantity(qty), discount(disc) { }
	double net_price(std::size_t) const = 0;
protected:
    std::size_t quantity = 0; //  purchase size for the discount to apply
    double discount = 0.0;    //  fractional discount to apply
};

class Bulk_quote : public Disc_quote {
public:
    Bulk_quote() = default;
    Bulk_quote(const std::string& book, double price,
              std::size_t qty, double disc):
          Disc_quote(book, price, qty, disc) { }
    // overrides the base version to implement the bulk purchase discount policy
    double net_price(std::size_t) const override;
};
分析：Bulk_quote 的直接基类是 Disc_quote
				的间接基类是 Quote
11、protected关键字的作用
	————用来声明那些该基类希望与派生类分享但不想与其他公共访问使用的成员
	1）用户不能访问该基类受保护的成员
	2）派生类的成员或派生类的友元只能访问派生类对象中基类部分的受保护成员，而在派生类中基类对象中成员不具有特殊的访问权。

	如：
		class Base {
		protected:
			int prot_mem;     // protected member
		};
		class Sneaky : public Base  {
			friend void clobber(Sneaky&);  #正确，派生类的成员或友元才能访问基类受保护的成员
			friend void clobber(Base&);    #不合法，派生类中基类对象不能在派生类中访问Base::prot_mem
			int j;                          // j is private by default
		};
		使用：
		void clobber(Sneaky &s) { s.j = s.prot_mem = 0; }
		void clobber(Base &b) { b.prot_mem = 0; }#错误
12、友元关系不能传递，也不能继承
如：
class Base {
    friend class Pal; // Pal has no access to classes derived from Base
};
class Pal {
public:
    int f(Base b) { return b.prot_mem; } // ok: Pal is a friend of Base
    int f2(Sneaky s) { return s.j; } // error: Pal not friend of Sneaky
    int f3(Sneaky s) { return s.prot_mem; } // ok: Pal is a friend
};
class D2 : public Pal {
public:
   int mem(Base b)
       { return b.prot_mem; } #错误，友元关系不能继承
};
13、改变派生类继承而来的某个名字的访问级别：
class Base {
public:
    std::size_t size() const { return n; }
protected:
    std::size_t n;
};
class Derived : private Base {    //  note: private inheritance
public:
    using Base::size;
protected:
    using Base::n;
};
分析：原本私有继承而来的size和n在派生类在是private的，但可以通过using把size变成public的，把n变成protected的，类似与using namespace std;
14、每个类都有自己的作用域
	派生类的作用域嵌套在基类的作用域内(有点反常)：当一个名字在派生类作用域内无法解析时，编译器将在外层基类的作用域中寻找该名字的定义。
	一个对象、指针（其静态类型和动态类型可能不一致）、引用（其静态类型和动态类型可能不一致）的静态类型决定该对象的哪个成员可见。即静态类型决定了对象、指针或引用的其作用域
	如： 
	class Disc_quote : public Quote {
	public:
		std::pair<size_t, double> discount_policy() const
		    { return {quantity, discount}; }
	};
	class Bulk_quote : public Disc_quote {
	public:
		Bulk_quote() = default;
		Bulk_quote(const std::string& book, double price,
		          std::size_t qty, double disc):
		      Disc_quote(book, price, qty, disc) { }
		double net_price(std::size_t) const override;
	};
	Bulk_quote bulk;
	Bulk_quote *bulkP = &bulk; // 静态类型和动态类型都是Bulk_quote
	Quote *itemP = &bulk;      // 静态类型是Quote,动态类型是Bulk_quote
	bulkP->discount_policy();  // 正确，bulkP的静态类型是Bulk_quote，在Bulk_quote作用域中寻找discount_policy，找不到就在Disc_quote中找discount_policy，找到了
	itemP->discount_policy();  // 错误，itemP的静态类型是Quote作用域中找，找不到了

#名字在作用域中冲突
struct Base {
    Base(): mem(0) { }
protected:
    int mem;
};
struct Derived : Base {
    Derived(int i): mem(i) { } //用i初始化派生类的mem，基类的mem采用默认初始化
    int get_mem() { return mem; }  // returns Derived::mem
protected:
    int mem;   #隐藏了基类的men
};
#很重要：名字查找优先于类型检查
	————即先名字匹配，匹配到了再做类型检查，即便类型检查失败，也不在往后进行名字检查了

15、明白函数调用的解析过程：p->men()或p.men()
		1）先确定p的静态类型
		2）在其静态类型对应的类中查找men，若找不到，则向基类查找，直到到达继承链的顶层，如果还是找不到，编译器保错；若找到，则进行类型检查，以确定本次调用是否合法
		3）若合法，编译器再根据调用的是否是虚函数而产生不同版本的代码：
				men是虚函数且被指针或引用调用的，则编译器在运行时决定到底执行哪个版本的men函数
				men不是虚函数，或men是虚函数，但通过对象调用，则编译器产生一个常规men函数调用
如：
	struct Base {
		int memfcn();
	};
	struct Derived : Base {
		int memfcn(int);  #重载，隐藏了基类的menfcn()
	};
	Derived d; 
	Base b;
	b.memfcn();       //  calls Base::memfcn
	d.memfcn(10);     //  calls Derived::memfcn
	d.memfcn();       //  错误，（基类的menfcn被隐藏了）名字查找到了，类型检查时失败，但不会再往后继续查找
	d.Base::memfcn(); //  ok: calls Base::memfcn
又如：
	class Base {
	public:
		virtual int fcn(); //虚函数
	};
	class D1 : public Base {
	public:
		int fcn(int);      //重载，隐藏了Base的fcn(int)，
		virtual void f2(); // 虚函数
	};
	class D2 : public D1 {
	public:
		int fcn(int); // 重载，隐藏了D1的fcn(int)
		int fcn();    // 覆盖，隐藏了Base的fcn()
		void f2();    // 覆盖，隐藏了D1的f2()
	};
	#注：不管是重载还是隐藏，都会发生隐藏
	Base bobj;  
	D1 d1obj; 
	D2 d2obj;
	Base *bp1 = &bobj, *bp2 = &d1obj, *bp3 = &d2obj;
	bp1->fcn(); 
	#分析：bp1的静态类型是Base，在Base的作用域中查找fcn：找到了，类型检查：成功，发现又是虚函数，则调用版本随动态绑定的对象类型而定：动态类型是Base————>则调用Bse的fcn
	bp2->fcn(); 
	#分析：bp2的静态类型是Base，在Base的作用域中查找fcn：找到了，类型检查：成功，发现又是虚函数，则调用版本随动态绑定的对象类型而定：动态类型是D1,————>则调用D1的fcn,恰好D1的fcn就是从Base直接继承而来的：Base::fcn
	bp3->fcn(); 
	#分析：bp3的静态类型是Base，在Base的作用域中查找fcn：找到了，类型检查：成功，发现又是虚函数，则调用版本随动态绑定的对象类型而定：动态类型是D2,————>则调用D2的fcn
	D1 *d1p = &d1obj; 
	D2 *d2p = &d2obj;
	bp2->f2(); 
	#分析：bp3的静态类型是Base，在Base的作用域中查找fcn：找不到————>编译器报错
	d1p->f2(); 
	#分析：d1p的静态类型是D1，在D1的作用域中查找fcn：找到了，类型检查：成功，发现又是虚函数，则调用版本随动态绑定的对象类型而定：动态类型是D1，—————>则调用D1的f2
	d2p->f2();
	#分析：d2p的静态类型是D2，在D2的作用域中查找fcn：找到了，类型检查：成功，发现又是虚函数，则调用版本随动态绑定的对象类型而定：动态类型是D2，—————>则调用D2的f2
	Base *p1 = &d2obj; D1 *p2 = &d2obj; D2 *p3 =  &d2obj;
	p1->fcn(42); 
分析：p1的静态类型是Base，在Base的作用域中查找fcn:找不到————>编译器报错
	p2->fcn(42);  
分析：p2的静态类型是D1，在D1的作用域中查找fcn:找到了，不是虚函数，则调用D1的fcn(int)
	p3->fcn(42);  
分析：p3的静态类型是D2，在D1的作用域中查找fcn:找到了，不是虚函数，则调用D2的fcn(int)
16、派生类的重载或覆盖总会隐藏基类全部的名字，如何实现只隐藏基类的部分：
	解决办法：为重载的成员提供一条using声明语句。这样我们就不会覆盖基类中的每一个重载版本了
17、基类的虚析构函数————对继承关系中的基类来说，其析构函数必须是虚函数
如：
class Quote {
public:
    virtual ~Quote() = default; // dynamic binding for the destructor
};
Quote *itemP = new Quote;   //  静态类型和动态类型一致
delete itemP;               //  destructor for Quote called
itemP = new Bulk_quote;     //  静态类型和动态类型不一致
delete itemP; 
分析：当我们delete一个动态分配的对象的指针时，指针的静态类型和动态类型可能不一致，如：当delete一个Quote类型的指针，而该指针可能动态绑定并不是Quote，而是派生类Bulk_quote类型的指针，这时要保证编译器调用的是派生类的析构函数，而不是基类的析构函数，若调用的基类的析构函数就会发生资源泄露。————虚函数的功劳

#如果一个类需要析构函数，那么同样需要拷贝和赋值操作，但继承关系中的基类并不遵循这一条。
18、合成拷贝控制
派生类合成的构造函数、赋值运算符、析构函数不但对类本身的成员进行初始化、赋值、销毁操作，还会对基类部分进行初始化、赋值、销毁操作，如：
派生类合成构造函数：
	Bulk_quote合成的默认构造函数会调用Disc_Quote的默认构造函数，后者又会调用
19、如何书写派生类的构造函数、赋值运算符、析构函数
	1）派生类的构造函数————不但要初始化派生类自己的成员，还要负责初始化派生类对象的基类部分

	2）派生类的拷贝和移动构造函数————不但要拷贝或移动派生类自己的成员，还要负责拷贝或移动派生类对象的基类部分
如：
	class Base { /* ...    */ } ;
	class D: public Base {
	public:
		D(const D& d): Base(d) { /* ...  */ } #派生类的拷贝构造函数
		D(D&& d): Base(std::move(d)) { /* ...  */ } #派生类的移动构造函数
	};
	分析：Base(d)会匹配基类Base的拷贝构造函数，从而将d的基类部分拷贝到要创建的对象中
	若派生类的拷贝构造函数没有负责拷贝基类部分，则很可能这时拷贝构造函数是不正确的：
如：
	D(const D& d): { /* ...  */ } #派生类的拷贝构造函数
	分析：基类部分会被默认初始化，而非从d中拷贝而来，这样会导致：派生类对象的Base成员被赋值了默认值，而派生类对象本身类的成员的值是从d中拷贝而来的
	3）派生类的赋值运算符————不但要对派生类自己的成员进行赋值，还要负责对初始化派生类对象的基类部分进行赋值
如：
D &D::operator=(const D &rhs)
{
    Base::operator=(rhs); // assigns the base part
	....
    return *this;
}
	4）派生类的析构函数————与前面的不同，只负责销毁派生类自己分配的资源。但派生类对象的基类部分会被自己销毁(隐式调用基类的析构函数)
class D: public Base {
public:
    // Base::~Base 会被自动调用执行
    ~D() { /* do what it takes to clean up derived members   */ }
};
20、新标准中，派生类可以继承基类的构造函数了
如：
class Bulk_quote : public Disc_quote {
public:
    using Disc_quote::Disc_quote; // 这样就继承了基类的所有的构造函数，但它的默认实参并不会被继承
    double net_price(std::size_t) const;
};
分析：using的用途有两个，这里用到的是它的第二个用途：
	1）用途一：令某个名字在当前作用域可见(前面用到都是)
	2）用途二：令编译器产生代码：对于基类的每个构造函数，编译器都将生成一个与之对应的派生类的构造函数。
	如：
	基类有这个构造函数：
	Disc_quote(book, price, qty, disc) { }
	则派生类就会生成与之对应的构造函数：
	Bulk_quote(const std::string& book, double price,
		      std::size_t qty, double disc):
		  Disc_quote(book, price, qty, disc) { }



