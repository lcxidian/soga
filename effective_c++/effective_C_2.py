/////////////////////////////////////////////////////////
// 11、在赋值操作符中避免出现“自我赋值”的怪癖          //
/////////////////////////////////////////////////////////

a：自我赋值现象
如：
class Widget { ... };
Widget w;
...
w = w;                                   // assignment to self
再如：
a[i] = a[j];//其实i == j  
*px = *py;  //其实px和py指向同一对象  

b：
class Bitmap { ... };
class Widget {
  ...
private:
  Bitmap *pb;                                     // ptr to a heap-allocated object
};
Widget&   Widget::operator=(const Widget& rhs)              // unsafe impl. of operator=
{
  delete pb;                                      // stop using current bitmap
  pb = new Bitmap(*rhs.pb);                       // start using a copy of rhs's bitmap
  return *this;                                   // see Item 10
}

//有可能rhs.pb和pb指向同一对象时，pb将会指向一个已被删除的对象

解决：
Widget& Widget::operator=(const Widget& rhs)
{
  if (this == &rhs) return *this;   // identity test: if a self-assignment,
  delete pb;
  pb = new Bitmap(*rhs.pb);#但不具备异常安全性：new Bitmap()可能会发生异常
  return *this;
}

彻底解决：在复制pb所指东西之前别删除pb
Widget& Widget::operator=(const Widget& rhs)
{
  Bitmap *pOrig = pb;               // remember original pb
  pb = new Bitmap(*rhs.pb);         // make pb point to a copy of *pb
  delete pOrig;                     // delete the original pb
  return *this;
}
从效率上讲，估计“自我赋值”的发生的频率有多高？因为这种方法降低效率

c：
#一个手工排列语句的代替方案：copy and swap技术
class Widget {
  ...
  void swap(Widget& rhs);   // exchange *this's and rhs's data;
  ...                       // see Item 29 for details
};

Widget& Widget::operator=(const Widget& rhs)
{
  Widget temp(rhs);             // make a copy of rhs's data
  swap(temp);                   // swap *this's data with the copy's
  return *this;
}
///////////////////////////////////////////////////////////
// 12、拷贝对象时勿忘每一成分（这个里还不是指小心浅拷贝）//
///////////////////////////////////////////////////////////

a:
如：
void logCall(const std::string& funcName);          // make a log entry
class Customer {
public:
  ...
  Customer(const Customer& rhs);
  Customer& operator=(const Customer& rhs);
  ...
private:
  std::string name;
};

Customer::Customer(const Customer& rhs): name(rhs.name)                                 // copy rhs's data
{
  logCall("Customer copy constructor");
}
Customer& Customer::operator=(const Customer& rhs)
{
  logCall("Customer copy assignment operator");
  name = rhs.name;                               // copy rhs's data
  return *this;                                  // see Item 10
}
#如果你为类增加一个成员变量时，别忘了同时修改类的拷贝构造函数和赋值操作符
class Date { ... };       // for dates in time
class Customer {
public:
  ...                     // as before
private:
  std::string name;
  Date lastTransaction;#增加成员变量时
};

b:
若忘记了，编译器不大可能会提醒你，一旦发生继承时，会产生危机：
如：
class PriorityCustomer: public Customer {                  // a derived class
public:
   ...
   PriorityCustomer(const PriorityCustomer& rhs);
   PriorityCustomer& operator=(const PriorityCustomer& rhs);
   ...
private:
   int priority;
};

自己书写拷贝构造函数和赋值操作符：#并没有把新添加的lastTransaction修改进去
PriorityCustomer::PriorityCustomer(const PriorityCustomer& rhs): priority(rhs.priority)
{
  logCall("PriorityCustomer copy constructor");
}
PriorityCustomer&   PriorityCustomer::operator=(const PriorityCustomer& rhs)
{
  logCall("PriorityCustomer copy assignment operator");
  priority = rhs.priority;
  return *this;
}
由于派生类中拷贝构造函数和赋值操作符中并没有对PriorityCustomer对象的基类部分Customer初始化，
这时对调用Customer默认构造函数。但默认构造函数并不存在，因此发生编译错误（？？？）

解决：
PriorityCustomer::PriorityCustomer(const PriorityCustomer& rhs): Customer(rhs), priority(rhs.priority)#显式调用基类Customer构造函数
{
  logCall("PriorityCustomer copy constructor");
}
PriorityCustomer& PriorityCustomer::operator=(const PriorityCustomer& rhs)
{
  logCall("PriorityCustomer copy assignment operator");
  Customer::operator=(rhs); #显式调用基类Customer的赋值操作符
  priority = rhs.priority;
  return *this;
}

///////////////////////////////////////////////////  
// 13、使用资源管理类来管理资源，可避免内存泄露  //
///////////////////////////////////////////////////

a:
class Investment { ... };   
Investment* createInvestment();  
void f()
{
  Investment *pInv = createInvestment();         // call factory function
  ...                                            #发生意想不到的情况，怎么办
  delete pInv;                                   // 资源泄露可能泄露
}

问题：
一、万一在...中过早的return，怎么办
二、万一在...中发生异常，怎么办
三、万一有人忘记delete，怎么办

为了确保资源总会被释放，我们将资源放进对象，当控制流离开时，该资源的析构函数自动释放那些资源，其利用的就是析构函数自动被调用的机制
解决一：智能指针auto_ptr
auto_ptr是一个类指针对象，其析构函数自动对其所指Investment对象调用delete，从而delete引发Investment对象的析构函数指向

void f()
{
  std::auto_ptr<Investment> pInv(createInvestment());  // call factory
  ...                                                  // use pInv as
}   

b:
auto_ptr有一个不寻常的特性：通过其拷贝构造函数和赋值操作符复制它们时，自身会变成NULL
如:
std::auto_ptr<Investment> pInv1(createInvestment());              // object returned from
std::auto_ptr<Investment> pInv2(pInv1);   // pInv1 为NULL
pInv1 = pInv2;                            // pInv2 为NULL

#因而auto_ptr并非管理动态分配资源的神兵利器，STL中禁用auto_ptr

c：auto_ptr的替代方案：shared_ptr(引用计数型智慧指针)
注：无人指向资源时，才自动删除该资源

void f()
{
  ...
  std::tr1::shared_ptr<Investment>  pInv1(createInvestment());              // object returned from
  std::tr1::shared_ptr<Investment>  pInv2(pInv1);                           // point to the object
  pInv1 = pInv2;                            // pInv1 和 pInv2都不为NULL
  ...
}   

#但auto_ptr和shared_ptr两者的析构函数内部都是做delete，而不是delete []
#因此对象数组并不适用，否则发生内存泄露
如：
std::auto_ptr<std::string> aps(new std::string[10]); // 内存泄露
std::tr1::shared_ptr<int>  spi(new int[1024]);    //内存泄露

#为了更好的解决数组问题，出现了boost::scopes_array和voost::shared_array_classes

d：
切记不能给智能指针返回一个“未加工指针”,即std::tr1::shared_ptr<Investment>  pInv1(未加工的指针)是错误的

//////////////////////////////////////////
// 14、在资源管理类中 小心coping行为    //
//////////////////////////////////////////

a：
并非所有的资源都是heap_based(堆资源)的，因此auto_ptr和shared_ptr不是适合所有资源，
这时我们需要建立自己的资源管理类，资源在构造期间获得，在析构期间释放

void lock(Mutex *pm);               // lock mutex pointed to by pm
void unlock(Mutex *pm);             // unlock the mutex

class Lock {
public:
  explicit Lock(Mutex *pm): mutexPtr(pm)  { lock(mutexPtr); }                          // acquire resource
  ~Lock() { unlock(mutexPtr); }                // release resource
private:
  Mutex *mutexPtr;
};


Mutex m;                    // define the mutex you need to use
...
{                           // create block to define critical section
 Lock ml(&m);               // lock the mutex
...                         // perform critical section operations
}                           // automatically unlock mutex at end
Lock ml1(&m);                      // lock m
Lock ml2(ml1); #我们的目标不是再次加锁，即不应许两个锁用在同一个资源上  
#这种情况下，你可有两种选择：

选择一：
  禁止复制，即不应许两个锁用在同一个资源上
  class Lock: private Uncopyable {            // prohibit copying — see
  public:                                     // Item 6
   ...                                        // as before
  };
选择二：
  可以允许多个锁用在同一资源上，即这时需要借用引用计数法shared_ptr，但shared_ptr的缺省行为是
  当引用次数为0时，删除释放其其智能指针指向的资源，而我们想要的当引用计数为0时，解锁

class Lock {
public:
  explicit Lock(Mutex *pm): mutexPtr(pm, unlock)#删除器的用途就在此体现
  {                              // as the deleter
    lock(mutexPtr.get());   // "get"获得原始指针
  }
private:
  std::tr1::shared_ptr<Mutex> mutexPtr;    // use shared_ptr
};                                         // instead of raw pointer
注：这时不再需要析构函数。

b：
在建立自己的资源管理器时，可能需要复制底部资源 或者 转移底部资源的拥有权
  复制底部资源：
    需要注意的时，别忘记深拷贝行为
  转移底部资源的拥有权：
    这时需要auto_ptr，而不是shared_ptr

///////////////////////////////////////////////////////
// 15、如何在资源管理中提供对原始资源的访问          //
///////////////////////////////////////////////////////

a：
很多API直接涉及资源，因此资源管理器也需要提供可以访问原始资源的指针
如：
std::tr1::shared_ptr<Investment> pInv(createInvestment());  // from Item 13
int daysHeld(const Investment *pi);        // return number of days
int days = daysHeld(pInv);// 编译不过，API需要指向原始资源的指针，而不是智能指针
#因此自定义的资源管理器需要提供访问原始指针的容器，其有两种做法：显示转换和隐式转换

b：	
#显式转换
默认的shared_ptr和auto_ptr也提供了get()成员函数（即显示转换），用来返回原始指针
int days = daysHeld(pInv.get());            // fine, passes the raw pointer
#隐式转换
同时也提供了隐式转换：shared_ptr和auto_ptr重载了operator->和operator*,它们隐私转换至底部原始指针
class Investment {                         // root class for a hierarchy
public:                                    // of investment types
  bool isTaxFree() const;
  ...
};
Investment* createInvestment();                    // factory function
std::tr1::shared_ptr<Investment>  pi1(createInvestment());                         // manage a resource
bool taxable1 = !(pi1->isTaxFree()); // 隐私转换至底部资源，否则无法直接访问isTaxFree()
...
std::auto_ptr<Investment> pi2(createInvestment()); // have auto_ptr
bool taxable2 = !((*pi2).isTaxFree());             // access resource
...

c:有点疑惑
例：将Font转换成FontHandle对象会是一种很频繁的需求：
#显示转换：提供get接口
FontHandle getFont();               // from C API—params omitted
void releaseFont(FontHandle fh);    // from the same C API

class Font {                           // RAII class
public:
  explicit Font(FontHandle fh): f(fh){} #构造函数
  ~Font() { releaseFont(f); }           #析构函数
  FontHandle get() const { return f; }
private:
  FontHandle f;                        // 指针类型
};

void changeFontSize(FontHandle f, int newSize);     // from the C API
Font f(getFont());#定义一个f对象
int newFontSize;
...
changeFontSize(f.get(), newFontSize);               // explicitly convert

#隐私转换：
class Font {
public:
  ...
  operator FontHandle() const { return f; }        // implicit conversion function
  ...
};

///////////////////////////////////////////////////////
// 16、成对使用new和delete时要采用相同形式           //
///////////////////////////////////////////////////////

string *stringptr1 = new string;
delete stringptr1;// 删除一个对象

string *stringptr2 = new string[100];
delete [] stringptr2;// 删除对象数组
#即如果你调用new时用了[]，调用delete时也要用[]。如果调用new时没有用[]，那调用delete时也不要用[]。
易错：
typedef string addresslines[4];	//一个人的地址，共4行，每行一个string
string *pal = new addresslines;	//

delete pal;// 错误!
delete [] pal;// 正确
（为了避免混乱，最好杜绝对数组类型用typedefs。）
///////////////////////////////////////////////////////////////////////
// 17、用单独一条语句将new对象指针赋值给智能指针，否则有可能内存泄露 //
///////////////////////////////////////////////////////////////////////

如：
int priority();
void processWidget(std::tr1::shared_ptr<Widget> pw, int priority);

processWidget(new Widget, priority());//编译不过，需要智能指针，而不是原始指针
processWidget(std::tr1::shared_ptr<Widget>(new Widget), priority());//编译通过，但有可能发生内存泄露

分析：执行顺序可能以下两种：
#std::tr1::shared_ptr<Widget>(new Widget)和priority()，不确定谁先执行：
第一种：
Call priority.//发生异常，但不会内存泄露
Execute "new Widget".
Call the tr1::shared_ptr constructor.

Execute "new Widget".
Call priority.//发生异常，有内存泄露，new出来的新对象并没有成功交给智能指针
Call the tr1::shared_ptr constructor.
解决：
std::tr1::shared_ptr<Widget> pw(new Widget);  // 马上赋给智能指针
processWidget(pw, priority());   

///////////////////////////////////////////////////////
// 18、我们设计类的接口应该容易正确被使用，即兼容性强//
///////////////////////////////////////////////////////

设计一个类的接口之前，必须考虑到用户可能会出什么样的错误使用
a：
设计一个接口：
class Date {
public:
  Date(int month, int day, int year);
  ...
};
Date d(30, 3, 1995);   //顺序错误
Date d(2, 20, 1995); //值范围超出

重新设计类的接口：
struct Day {            struct Month {                struct Year {
  explicit Day(int d)     explicit Month(int m)         explicit Year(int y)
  :val(d) {}              :val(m) {}                    :val(y){}
  int val;                int val;                      int val;
};                      };                            };
class Date {
public:
 Date(const Month& m, const Day& d, const Year& y);
 ...
};
Date d(30, 3, 1995);                      // error! wrong types
Date d(Day(30), Month(3), Year(1995));    // error! wrong types
Date d(Month(3), Day(30), Year(1995));    // okay, types are correct
再对一些特殊值做限定：
class Month {
public:
  static Month Jan() { return Month(1); }   // functions returning all valid
  static Month Feb() { return Month(2); }   // Month values; see below for
  ...                                       // why these are functions, not
  static Month Dec() { return Month(12); }  // objects
  ...                                       // other member functions
private:
  explicit Month(int m);                    // prevent creation of new
  ...                                       // month-specific data
};
Date d(Month::Mar(), Day(30), Year(1995));

b：
限定类型内什么事可做，什么不可做
如：以const修饰operator*的返回类型，可阻止用户修改其值

c:
尽量限制用户使用的type和类中type一致

Investment* createInvestment();  
改进：
std::tr1::shared_ptr<Investment> createInvestment();//可防止用户使用时出现内存泄露

d:
在类中声明智能指针时，就指定其删除器具体做什么，而不要交给用户自己去做，除非有需要才那么做

std::tr1::shared_ptr<Investment>  pInv(0, getRidOfInvestment);  //编译不过
改进：
std::tr1::shared_ptr<Investment> pInv(
									static_cast<Investment*>(0), 
									getRidOfInvestment
									);          
因此，实际使用时：
std::tr1::shared_ptr<Investment> createInvestment()
{
  std::tr1::shared_ptr<Investment> retVal(
  									static_cast<Investment*>(0),
                                    getRidOfInvestment
                                    );
  retVal = ... ;                                            
  return retVal;
}
分析：为什么要先把0赋给智能指针呢？即有时我们并不能在定义的时候就能确定其值，所以先用0去初始化，当然直接用值初始化去初始化效率更高，如下：
std::tr1::shared_ptr<Investment> createInvestment()
{
  return std::tr1::shared_ptr<Investment>(new Stock);
}
///////////////////////////////////////////////////////
// 19、把class设计的想内置类型type一样优雅           //
///////////////////////////////////////////////////////

应该带着和“语言设计者当初设计语言内置类型时”的严谨来思考如何设计自己的类
你应该注意一下几个问题：
	0、真的有必要定义这个类吗
	1、你的类如何被创建和销毁
	2、应该明白对象初始化和对象的赋值有什么差别
	3、你的类的对象如果被pass-by-value,意味着什么
	4、类的成员变量的合法值是什么
	5、你的数据成员需要从别的类继承而来吗
	6、类的成员变量需要什么样的类型转换吗
	7、需要重载哪些操作符
	8、什么样的标准函数应该驳回
	9、谁会调用类的成员变量
	10、什么是类的未声明接口
  
////////////////////////////////////////////////////////////////
// 20、能用pass-by-value的地方用pass-by-reference-to-const替换//
////////////////////////////////////////////////////////////////

a：
分析pass-by-reference-to-const与pass-by-value在效率上的差别
如：
class Person {
public:
  Person();                          // parameters omitted for simplicity
  virtual ~Person();                 // see Item 7 for why this is virtual
  ...
private:
  std::string name;
  std::string address;
};
class Student: public Person {
public:
  Student();                         // parameters again omitted
  ~Student();
  ...
private:
  std::string schoolName;
  std::string schoolAddress;
};

bool validateStudent(Student s);           // function taking a Student
Student plato;                             // Plato studied under Socrates
	
	pass-by-value方式：6次拷贝构造函数+6次析构函数
bool platoIsOK = validateStudent(plato); 
	分析：先调用6次拷贝构造函数，当validateStudent返回时s会被销毁（局部变量），因此再调用6次析构函数
	改进：
	pass-by-reference-to-const方式：0拷贝0析构
bool validateStudent(const Student& s);
	分析：由原来的bool validateStudent(Student s); 可知不希望用户改变其s的内容，因此改进时写成conse引用，整个过程没有任何拷贝构造函数和析构函数被调用，因为没有任何新对象被创造
b：
by-reference方式可以避免对象切割问题
如：
class Window {
public:
  ...
  std::string name() const;           // return name of window
  virtual void display() const;       // draw window and contents
};
class WindowWithScrollBars: public Window {
public:
  ...
  virtual void display() const;
};
void printNameAndDisplay(Window w)         // incorrect! parameter
{                                          // may be sliced!
  std::cout << w.name();
  w.display();
}
WindowWithScrollBars wwsb;
printNameAndDisplay(wwsb); #本应该传递基类对象，但不小心传递成了派生类对象，这时passed-by-value方式导致派生类的数据成员 “拷贝” 给基类的数据成员，导致其数据成员display版本错误
分析：当把派生类对象视为一个基类对象传递至实参时，基类的拷贝构造函数会被调用，导致“此对象的行为像个派生类对象的那些特征性质全被切割掉了”
		因此，必然调用的是基类的display()，而不是我们想要派生类的display()

解决办法：
void printNameAndDisplay(const Window& w)   // fine, parameter won't
{                                           // be sliced
  std::cout << w.name();
  w.display();
}
WindowWithScrollBars wwsb;
printNameAndDisplay(wwsb);#此时不小心的错误类型参数传递，并不会造成其数据成员display版本错误
分析：这时传进来的窗口是什么类型，就调用什么类型的display()

c:
能用pass-by-value的地方必然可以用pass-by-reference-to-const替换，
但不一定能用pass-by-reference替换

d：
#引用的实质是用指针实现出来的，因此pass-by-reference意味着传递的是指针，
#但如果对象是内置类型的话，pass-by-value比pass-by-reference效率要高很多当是内置类型时，则尽量选用pass-by-value
