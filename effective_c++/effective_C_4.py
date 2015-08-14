/////////////////////////////////////
// 31、降低文件之间的编译依赖      // 
/////////////////////////////////////

a:
#问题：假如你对某个class文件做了修改，修改的不是class接口，而是实现，而且只修改private成分，这时这个工程都需要被重新编译和连接
分析：其根本原因是没有把接口从现实中分离出去。
如：
class Person {
public:
  Person(const std::string& name, const Date& birthday, const Address& addr);
  std::string name() const;
  std::string birthDate() const;
  std::string address() const;
  ...
private:
      std::string theName;        # 实现细目
      Date theBirthDate;          # 实现细目
      Address theAddress;         # 实现细目
};
class Person无法编译————因为没有class string，Date和Address的定义式。这样的定义式通常用#include""提供
改进一：
#include<string>
#include"Date.h"
#include"Address.h"
class Person {
public:
  Person(const std::string& name, const Date& birthday, const Address& addr);
  std::string name() const;
  std::string birthDate() const;
  std::string address() const;
  ...
private:
      std::string theName;        # 实现细目
      Date theBirthDate;          # 实现细目
      Address theAddress;         # 实现细目
};
#分析：这样形式存在一种编译依赖关系：如果头文件中有任何改变，或头文件所依赖的其他内部头文件有任何改变，导致每一个include Person的文件都得重新编译

改进二：将三个实现细目从class Person中分离
namespace std {
     class string;             // 前置声明
}                             
class Date;                    // 前置声明
class Address;                 // 前置声明
class Person {
public:
      Person(const std::string& name, const Date& birthday, onst Address& addr);
      std::string name() const;
      std::string birthDate() const;
      std::string address() const;
    ...
};
分析：以上存在几个错误：
	错误一：string不是类，它是typedef basic_string<char> string；
	错误二：前置声明每一个变量，都必须知道其变量的大小才行，编译器如何知道其变量p的大小————通过询问这个类Person的定义式，但如果这个类Person的定义式并没有列出，怎么办？
			如：
				int main()
				{
				 int x;                // define an int
				 Person p( params );   // define a Person
				   ...
				}
			对java来说，这不是问题，编译器每次都分配一个足够空间给一个指针使用。因此java中把以上代码视同为如下形式：尽管java中没有指针（这里只是想说明java把没有列出定义式的类时，分配一个足够大小的空间给一个指针）
				int main()
				{
				  int x;               // define an int
				  Person *p;           // define a pointer to a Person
				  ...
				}
			借助java这种思想，c++也可以将对象实现细目隐藏在一个指针背后，这样一来从而降低了文件直接编译的依赖性
				#include <string>                      // standard library components
				#include <memory>                      // for tr1::shared_ptr; see below
				class PersonImpl;                      // 前置声明一个PersonImpl指针类，而不再是Person
				class Date;                            // forward decls of classes used in
				class Address;                         // Person interface
				class Person {
				public:
				 Person(const std::string& name, const Date& birthday, const Address& addr);
				 std::string name() const;
				 std::string birthDate() const;
				 std::string address() const;
				 ...
				private:                                   // ptr to implementation;
				  std::tr1::shared_ptr<PersonImpl> pImpl;  # 指针变量，这样编译器就不需要知道Person类定义式了，从而降低了依赖性
				};                                         // std::tr1::shared_ptr
				#这样的设计，那些calss的任何实现修改都不要重新编译Person客户端了，真正实现了“接口与实现的分离”
注：分离的关键是将“定义的依赖性” 替换成 “声明的依赖性”。
b：
接口设计策略：
	一、如果对象指针或对象引用可以完成任务，就不要用对象本身来完成。
	二、尽量以class声明代替class定义式，这样才能降低其依赖性。
	三、为声明式和定义式提供不同的头文件。
	这样一来，用#include 声明式 替代 以手工方式前置声明Date
	class Date;                      修改成     #include"datafwd.h"   
	Date today();								Date today();
	void clearAppointments(Date d);             void clearAppointments(Date d);

c:
#注：像Person这样的使用piml idiom的类叫做 Handle class
应用：

Person声明式：
#include <string>                      // standard library components
#include <memory>                      // for tr1::shared_ptr; see below
class PersonImpl;                      // 前置声明一个PersonImpl指针类，而不再是Person
class Date;                            // forward decls of classes used in
class Address;                         // Person interface
class Person {
public:
 Person(const std::string& name, const Date& birthday, const Address& addr);
 std::string name() const;
 std::string birthDate() const;
 std::string address() const;
 ...
private:                                   // ptr to implementation;
  std::tr1::shared_ptr<PersonImpl> pImpl;  # 指针变量，这样编译器就不需要知道Person类定义式了，从而降低了依赖性
}; 

Person定义式：
#include "Person.h"       // we're implementing the Person class,
#include "PersonImpl.h"      // we must also #include PersonImpl's class
Person::Person(const std::string& name, const Date& birthday, const Address& addr): pImpl(new PersonImpl(name, birthday, addr)){}
std::string Person::name() const
{
  return pImpl->name();
}

d：
还有一种制作Handle class的方法：即定义个接口类interface classes，即抽象类
class Person {
public:
  virtual ~Person();
  virtual std::string name() const = 0;
  virtual std::string birthDate() const = 0;
  virtual std::string address() const = 0;
  static std::tr1::shared_ptr<Person>  create(const std::string& name,      // Person initialized with the
          									  const Date& birthday,         // given params; see Item 18 for
          									  const Address& addr);         // why a tr1::shared_ptr is returned
  ...
};

class RealPerson: public Person {
public:
  RealPerson(const std::string& name, const Date& birthday,
             const Address& addr)
  : theName(name), theBirthDate(birthday), theAddress(addr)
  {}
  virtual ~RealPerson() {}
  std::string name() const;        // implementations of these 
  std::string birthDate() const;   // functions are not shown, but
  std::string address() const;     // they are easy to imagin
private:
  std::string theName;
  Date theBirthDate;
  Address theAddress;
};
std::tr1::shared_ptr<Person> Person::create(const std::string& name,
                                            const Date& birthday,
                                            const Address& addr)
{
  return std::tr1::shared_ptr<Person>(new RealPerson(name, birthday,addr));
}

e：
#Handle class 和 interface class都能解除接口和实现之间的耦合关系。

////////////////////////////////////////
// 32、理解public继承是一种is a的关系 // 
////////////////////////////////////////

注：public继承————class D继承自class B，则每一个D的对象同时也是一个类型B的对象，反之不成立。

a：
class Person {...};
class Student: public Person {...};

void eat(const Person& p);            // anyone can eat
void study(const Student& s);         // only students study
Person p;                             // p is a Person
Student s;                            // s is a Student
eat(p);                               // fine, p is a Person
eat(s);                               // fine, s is a Student,
study(s);                             // fine
study(p);                             #错误

b：
public继承 == is a ，并不是那么容易去理解
第一种写法：
	class Bird {
	public:
	  virtual void fly();                  // birds can fly
	  ...
	};

	class Penguin:public Bird {            // penguins are birds
	  ...
	};//遇上的乱流情况，因为实际上企鹅不会fly，#因此要灵活理解 is a关系
第二种写法：
	class Bird {
	  ...                                       // 没有fly
	};

	class FlyingBird: public Bird {
	public:
	  virtual void fly();
	  ...
	};
这反映了世界上并不存在一个“适用于所有软件”的完美设计，所谓最佳设计取决于系统希望做什么事，包括现在与未来。
第三种写法：
	class Bird {
	public:
	  virtual void fly();                  // birds can fly
	  ...
	};
	void error(const std::string& msg);       // defined elsewhere
	class Penguin: public Bird {
	public:
	  virtual void fly() { error("Attempt to make a penguin fly!");}//fly提示错误的
	  ...
	};
第四种写法：
	class Bird {
	  ...                                # no fly function is declared
	};
	class Penguin: public Bird {
	  ...                                # no fly function is declared
	};
	Penguin p;
	p.fly();   //编译不过

#分析：第四种做法要优于第三种做法：好的接口可以防止无效的代码通过编译。应该在编译期间拒绝企鹅飞行，而不是在运行期间才能侦测出来

c：
继续理解public继承是is a的关系
#矩形类
class Rectangle {
public:
  virtual void setHeight(int newHeight);
  virtual void setWidth(int newWidth);
  virtual int height() const;             
  virtual int width() const;
  ...
};

void makeBigger(Rectangle& r)   #理论上，基类参数，也可以用派生类替代，但事实上并不对           
{
  int oldHeight = r.height();
  r.setWidth(r.width() + 10);               // 增加宽的长度
  assert(r.height() == oldHeight);          // 始终为 true
}                                           // height is unchanged
#正方形类
class Square: public Rectangle {...};
Square s;
...
assert(s.width() == s.height());           // this must be true for all squares
makeBigger(s);                             // s可以接派生类对象，但该接口在派生类调用时逻辑上并不正确
assert(s.width() == s.height());        //对所有的正方形应该为真才是，事实上为假   

分析：某些可以施行于矩阵身上的事情，并不一定能施行在正方形身上，但public继承主张能够施行于基类身上的，也可以施行在派生类身上，
		在矩形和正方形上可以看出public继承塑造它们之间的关系并不正确。由此看来public继承并那么简单
#注：代码编译通过，并不表示可以正确运作。
/////////////////////////////////////
//  // 
/////////////////////////////////////
33、避免不要覆盖继承而来的名称
a：
class Base {
private:
  int x;
public:
  virtual void mf1() = 0;  # pure virtual
  virtual void mf2();      # virtual
  void mf3();              # non-virtual
  ...
};

class Derived: public Base {
public:
  virtual void mf1(); #重写
  void mf4();
  ...
};

void Derived::mf4()
{
  ...
  mf2();
  ...
}
分析：Derived::mf4()的调用过程：local作用域————>外围作用域：Derived————>外围作用域：Base（若没找到）————>base的namespace作用域————>global作用域

b:
class Base {
private:
  int x;
public:
  virtual void mf1() = 0;
  virtual void mf1(int);  #重载一个新函数
  virtual void mf2();
  void mf3();          
  void mf3(double);      #重载一个新函数
  ...
};

class Derived: public Base {
public:
  virtual void mf1(); #重写基类的成员函数（多态）
  void mf3();         #覆盖基类的成员函数
  void mf4();        
  ...
};
##由名称遮掩规则（无论是pure virtual还是virtual还是non-virtual，也不管参数类型是否相同），基类所有名为mf1和mf3都被派生类的mf1和mf3掩盖了，因此：
Derived d;
int x;
...
d.mf1();                   # fine, calls Derived::mf1
d.mf1(x);                  #错误，易错
d.mf2();                   # fine, calls Base::mf2
d.mf3();                   # 派生类的mf3
d.mf3(x);                  # 错误

c：
class Base {
private:
  int x;
public:
  virtual void mf1() = 0;
  virtual void mf1(int);
  virtual void mf2();
  void mf3();
  void mf3(double);
  ...
};

class Derived: public Base {
public:
  using Base::mf1;       # 让基类所有名为mf1的在派生类作用域内可见
  using Base::mf3;       # 让基类所有名为mf3的在派生类作用域内可见
  virtual void mf1();
  void mf3();
  void mf4();
  ...
};
Derived d;
int x;
...
d.mf1();                 // 派生类的mf1
d.mf1(x);                # 基类的mf1
d.mf2();                 // still fine, still calls Base::mf2
d.mf3();                 // 派生类的mf3
d.mf3(x);                # 基类的mf3

d：
有时候你并不想继承基类的所有函数，采用private继承
假如你只想继承那个无参数版本的mf1，这时using做不到了，因为using base::mf1让基类的所有名为mf1的函数在派生类下都可见
解决：写一个转交函数即可做到
class Base {
public:
  virtual void mf1() = 0; #基类是可以给出pure virtual函数的定义的，但派生类永远只能继承其接口，不能继承其实现
  virtual void mf1(int); #不想被派生类继承
  ...                                    // as before
};
class Derived: private Base {
public:
  virtual void mf1()                   // forwarding function; implicitly
  { Base::mf1(); }                     // 这时就可调用那个无参的mf1，继承的目的就是为了调用
  ...
};
...
Derived d;
int x;
d.mf1();                               // fine, calls Derived::mf1
d.mf1(x);         # error

////////////////////////////////////////
// 34、区分函数接口继承和函数实现继承 // 
////////////////////////////////////////

a：
有时候你只想继承函数的接口（即声明）    # pure virtual
有时候你想继承函数的接口和函数的实现（即定义），但有准备去覆盖继承过来的函数实现      #virtual
有时候你想继承函数的接口和函数的实现（即定义），但不允许覆盖函数的实现                #non-virtual

b：
class Shape {
public:
  virtual void draw() const = 0;              //pure virtual  #抽象类
  virtual void error(const std::string& msg); //virtual
  int objectID() const;                       //non-virtual
  ...
};
class Rectangle: public Shape { ... };
class Ellipse: public Shape { ... };
分析：  有pure virtual，则一定是抽象类
		成员函数的接口都会被继承（无论是pure virtual还是virtual还是non-virtual）
		pure virtual函数必须被继承的派生类重新声明
		基类中声明一个pure virtual函数，通常希望派生类只继承它的接口（可以在抽象类中给出pure virtual的实现）
如：
Shape *ps = new Shape;              // 错误，抽象类不能被实例化
Shape *ps1 = new Rectangle;         // fine
ps1->draw();                     // 派生类Rectangle的draw
Shape *ps2 = new Ellipse;           // fine
ps2->draw();                     // 派生类Ellipse的draw
ps1->Shape::draw();                 // calls Shape::draw
ps2->Shape::draw();                 // calls Shape::draw
		virtual函数是希望派生类继承它的接口和缺省实现

b：
# 但有时候派生类即继承virtual函数的接口和缺省实现，可能会造成不必要的麻烦：因此只想继承基类函数的声明而已
class Airport { ... };                     // represents airports
class Airplane {
public:
  virtual void fly(const Airport& destination);
  ...
};

void Airplane::fly(const Airport& destination)
{
  //飞往缺省的地点
}
class ModelA: public Airplane { ... };
class ModelB: public Airplane { ... };
class ModelC: public Airplane {
  ...                                   // 这里忘记覆写继承而来的实现了
};
Airport PDX(...);                       // PDX is the airport near my home
Airplane *pa = new ModelC;
...
pa->fly(PDX); //导致飞往基类缺省的地点，而我们的目标并非如此。出现这种情况，编译器应该报错才是我们想要的
#解决:重新命名缺省fly，即切断virtual函数接口和其缺省实现 的关联
class Airplane {
public:
  virtual void fly(const Airport& destination) = 0;　#pure virtual
  ...
protected:
  void defaultFly(const Airport& destination);
};
void Airplane::defaultFly(const Airport& destination)
{
  飞往缺省的地点
}

class ModelA: public Airplane {
public:
  virtual void fly(const Airport& destination)
  { defaultFly(destination); }
  ...
};
class ModelB: public Airplane {
public:
  virtual void fly(const Airport& destination)
  { defaultFly(destination); }
  ...
};
class ModelC: public Airplane {
public:
  virtual void fly(const Airport& destination); #如果忘记重写fly，会起到 编译器会提示报错 的作用
  ...
};
void ModelC::fly(const Airport& destination)
{
  code for flying a ModelC airplane to the given destination
}
这时就不再会出现ModelC忘记覆写fly，而编译器不会报错的情况了

c：
有些人返回以不同的函数名来提供接口和缺省实现，因为会引起命名空间污染问题，#即把fly和defualt合成一个fly，防止命名空间污染
#解决：利用pure virtual函数必须在派生类中重新声明，但它们也可以在基类有一份自己的实现
如：
class Airplane {
public:
  virtual void fly(const Airport& destination) = 0;
  ...
};
void Airplane::fly(const Airport& destination)     # 在基类是可以给pure virtual一份自己的实现，但派生类是继承不来这份实现的，它只能继承函数的接口而已
{                                                
  default code for flying an airplane to
  the given destination
}
class ModelA: public Airplane {
public:
  virtual void fly(const Airport& destination)
  { Airplane::fly(destination); }
  ...
};

class ModelB: public Airplane {
public:
  virtual void fly(const Airport& destination)
  { Airplane::fly(destination); }
  ...
};
class ModelC: public Airplane {
public:
  virtual void fly(const Airport& destination);
  ...
};
void ModelC::fly(const Airport& destination)
{
  code for flying a ModelC airplane to the given destination
}

e：
#non-virtual函数的目的就是为了让派生类继承它的接口和一份强制实现
///////////////////////////////////////
// 35、考虑virtual函数以外的其他选择 // 
///////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////////////////////////
// 36、绝不重新定义继承而来的non-virtual函数（不是不可以，而是最好不要）即不要覆盖基类的同名函数 // 
///////////////////////////////////////////////////////////////////////////////////////////////////

a：
class B {
public:
  void mf();
  ...
};
class D: public B { ... };
D x;                              // x is an object of type D
B *pB = &x;                       // get pointer to x
pB->mf();                         // call mf through pointer
D *pD = &x;                       // get pointer to x
pD->mf();                         // call mf through pointer
以上两个指针都会调用基类的mf函数

b:
学习对象的静态类型和对象的动态类型：
	1、对象的静态类型：对象在声明时采用的类型。是在编译期确定的。
	2、对象的动态类型：目前所指对象的类型。是在运行期决定的。
	3、静态绑定：绑定的是对象的静态类型，某特性（比如函数）依赖于对象的静态类型，发生在编译期。
	4、动态绑定：绑定的是对象的动态类型，某特性（比如函数）依赖于对象的动态类型，发生在运行期。
如：	
	class B {}
	class C : public B {}
	class D : public B {}
	D* pD = new D();//pD的静态类型是它声明的类型D*，动态类型也是D*
	B* pB = pD;//pB的静态类型是它声明的类型B*，动态类型是pB所指向的对象pD的类型D*
	C* pC = new C();
	pB = pC;//pB的动态类型是可以更改的，现在它的动态类型是C*

c：
若mf是non-virtual，但派生类覆写了mf
#注：non-virtual函数都是静态绑定！ virtual函数都是动态绑定
class B {
public:
  void mf();
  ...
};
class D: public B {
public:
  void mf();                      // hides B::mf; see Item33
  ...
};
D x;                             
B *pB = &x; //pB的静态类型是B，动态类型是D     
D *pD = &x; //pD的静态类型是D，动态类型是D  
pB->mf();   // non-virtual函数是静态类型，因此调用的B::mf()
pD->mf();   // non-virtual函数是静态类型，因此调用的D::mf()

d：
若mf是virtual，但派生类覆写了mf
class B {
public:
  virtual void mf();
  ...
};
class D: public B {
public:
  void mf();                      // hides B::mf; see Item33
  ...
};
D x;                             
B *pB = &x; //pB的静态类型是B，动态类型是D     
D *pD = &x; //pD的静态类型是D，动态类型是D  
pB->mf();   // virtual函数是动态类型，因此调用的D::mf()
pD->mf();   // virtual函数是动态类型，因此调用的D::mf()

37、绝不重新定义继承而来的缺省参数值
#因为，virtual函数是动态绑定，但缺省参数值却是静态绑定
a：
如：
class Shape {
public:
  enum ShapeColor { Red, Green, Blue };
  virtual void draw(ShapeColor color = Red) const = 0;
  ...
};
class Rectangle: public Shape {
public:
  virtual void draw(ShapeColor color = Green) const; #重新定义了 继承而来的缺省参数值
  ...
};

class Circle: public Shape {
public:
  virtual void draw(ShapeColor color) const; #重新定义了 继承而来的缺省参数值
  ...
};
Shape *ps;                       // static type = Shape*
Shape *pc = new Circle;          // static type = Shape*
Shape *pr = new Rectangle;       // static type = Shape*
ps = pc;                       
ps = pr;                       
pc->draw(Shape::Red);           // virtual函数的动态绑定：派生类Circle的draw(Shape::Red)
pr->draw(Shape::Red);           // virtual函数的动态绑定：派生类Rectangle的draw
pr->draw();                     # virtual函数的动态绑定，其缺省值参数的静态绑定：派生类Rectangle的draw(Shape::Red)

#分析：virtual函数的动态绑定，其缺省值参数的静态绑定，这样的目的是为了运行期效率

b：
非常糟糕的写法：
class Shape {
public:
  enum ShapeColor { Red, Green, Blue };
  virtual void draw(ShapeColor color = Red) const = 0;
  ...
};
class Rectangle: public Shape {
public:
  virtual void draw(ShapeColor color = Red) const;
  ...
};
分析：代码重复，导致：如果Shape内的缺省值改变，派生类的缺省值也应该改变，否则出现重复定义一个继承而来的缺省值参数值，而我们的标题正是不提倡这么去做

解决：
class Shape {
public:
  enum ShapeColor { Red, Green, Blue };
  void draw(ShapeColor color = Red) const           // now non-virtual
  {
    doDraw(color);                                  // calls a virtual
  }
  ...
private:
  virtual void doDraw(ShapeColor color) const = 0;  // the actual work is
};    
                                              // done in this func
class Rectangle: public Shape {
public:
  ...
private:
  virtual void doDraw(ShapeColor color) const;       // note lack of a
  ...                                                // default param val.
};

执行结果：
/////////////////////////////////////
// 38、理解has a的关系             // 
/////////////////////////////////////

a：
如：复合是类型之间的一种关系。复合又叫分层，聚合，内嵌，内含...
class Address { ... };             // where someone lives
class PhoneNumber { ... };
class Person {
	public:
	  ...
	private:
	  std::string name;               // composed object
	  Address address;                # 聚合
	  PhoneNumber voiceNumber;        # 聚合
	  PhoneNumber faxNumber;          # 聚合
};

b：
借助list容器去实现一个自己的set容器：
初步做法：采用public继承
template<typename T>           // the wrong way to use list for Set
class Set: public std::list<T> { ... };
分析：由is a的关系可知，如果D继承自B，则对B为真的每一件事，对D也为真。推理list可以有重复的元素，则Set应该也可以有重复的元素，而事实上Set并不能为重复的元素
	因此，Set和list之间并非is-a关系，所用不应用public继承

template<class T>                   // the right way to use list for Set
class Set {
public:
  bool member(const T& item) const;
  void insert(const T& item);
  void remove(const T& item);
  std::size_t size() const;
private:
  std::list<T> rep;                 // representation for Set data
};

template<typename T>
bool Set<T>::member(const T& item) const
{
  return std::find(rep.begin(), rep.end(), item) != rep.end();
}
template<typename T>
void Set<T>::insert(const T& item)
{
  if (!member(item)) rep.push_back(item);
}
template<typename T>
void Set<T>::remove(const T& item)
{
  typename std::list<T>::iterator it = std::find(rep.begin(), rep.end(), item);         // "typename" here
  if (it != rep.end()) rep.erase(it);
}
template<typename T>
std::size_t Set<T>::size() const
{
  return rep.size();
}

总结：由此深刻理解了is-a关系

/////////////////////////////////////
// 39、明智而谨慎使用private继承   // 
/////////////////////////////////////

a：
注：private继承不会将一个派生类对象转换为一个基类对象
如：
class Person { ... };
class Student: private Person { ... };     // inheritance is now private
void eat(const Person& p);                 // anyone can eat
void study(const Student& s);              // only students study
Person p;                                  // p is a Person
Student s;                                 // s is a Student
eat(p);                                    // fine, p is a Person
eat(s);                                    # 因此错误

b：
# private继承意味着只继承实现部分，不继承接口部分。
# 即private继承在软件设计层面上没有意义，而只在软件实现层面有意义。
使用原则：尽可能使用复合，必要时才使用private继承。主要当protected成员或virtual函数牵连进来时，才考虑用private继承

class Timer {
public:
  explicit Timer(int tickFrequency);
   virtual void onTick() const;          // automatically called for each tick
  ...
};
为了让Widget重新定义Timer内的virtual函数，widget就必须继承Timer，<而且>不能让用户直接调用从基类继承而来的virtual函数
#假如采用public继承，但Widget和Timer并不是is-a关系。  即只有辨别是is a的关系采用public继承，否则用private继承或复合方式
因此采用private继承或复合做法：

private继承：
class Widget: private Timer {
private:
  virtual void onTick() const;        # 重写onTick
  ...
};

复合：
class Widget {
private:
  class WidgetTimer: public Timer {
  public:
    virtual void onTick() const;
    ...
  };
   WidgetTimer timer;
  ...
};
总结：private继承和复合都可以满足我们要求，但复合可能更好，因为复合不仅可以拥有Timer所有成员，还可以可以阻止自己重新定义onTick函数

/////////////////////////////////////
// 40、明智而谨慎使用多重继承      // 
/////////////////////////////////////

#注：多重继承和多继承不是一回事！
#    多重继承是指继承一个以上的基类，叫多重继承
#	 多继承是指基类，基类的基类，派生类之间的关系。
a：
class BorrowableItem {             // something a library lets you borrow
public:
  void checkOut();                 // check the item out from the library
  ...
};
class ElectronicGadget {
private:
  bool checkOut() const;           // perform self-test, return whether
  ...                              // test succeeds
};
class MP3Player: public BorrowableItem, public ElectronicGadget
	{ ... };                           // class definition is unimportant
MP3Player mp;
mp.checkOut();                     // 到底调用哪一个基类的checkout函数？

C++解析重载函数调用的规则：在看是否有个函数可取用之前，先确定这个函数对此调用是不是最佳匹配,在找到最佳匹配之后再检查该函数是否有可取性。
#分析：本例中两个checkout函数都有相同的匹配程度，即然没有最佳匹配时，需要明确指出到底调用哪一个函数
		mp.BorrowableItem::checkOut();//有可取性
		ElectronicGadget::checkOut()；//无可取性，因为是基类的private成员

b：
class File { ... };
class InputFile: public File { ... };
class OutputFile: public File { ... };
class IOFile: public InputFile,
              public OutputFile
{ ... };
#IOFile到底走哪一条路径去继承File类的所有成员？
（缺省情况）第一种做法是：IOFile从其每一个基类都继承一份File成员变量 #普通多继承
			第二种做法是：IOFile从继承一份File成员变量：#virtual多继承

C++中，两种做法都支持，但缺省做法是第一种，如果第一种做法不是你想要的，就这样做：virtual base class
#virtual多继承 （菱形结构）
class File { ... };
class InputFile: virtual public File { ... };
class OutputFile: virtual public File { ... };
class IOFile: public InputFile,
              public OutputFile
{ ... };

#分析：使用virtual继承的那些类往往比普通继承而来的派生类体积大一些，访问派生类的成员速度也慢一些，这就是virtual继承要付出的代价
c：
未完待续