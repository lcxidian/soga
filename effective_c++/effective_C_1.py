2015-4-27
"学习 effective c++"
注：c++中先有声明，后有定义
///////////////////////////////////////////
//0、导读                                //
///////////////////////////////////////////
#补充1：明白std::size_t和size_t的本质意义：std::size_t是c++范畴内的，size_t有可能是c++范畴内的，也有可能是c范畴内的
#补充2：size_t是unsignde 类型的
#补充3：default构造函数——要不没有参数，要不每个参数都有缺省值
#补充4：拷贝构造函数的过程是其内部成员的passed by value，而不是引用传递
#补充5：C++中没有像java或.net中的提供的interface关键字，而是用类来实现一个interface接口
#补充6：TR1——是一份规范，描述了c++标准库的许多新技能,其中大多TR1新技能都是以Boost为基础的
a:
分清声明和定义
	对象声明：extern int x;#没有“形式”的，需要extern
	函数声明：size_t numDigits(int Number);#有形式的，省略extern
	类声明：class Widget;
	模板声明：template<typename T>class GraphNode;

	对象定义：int x;
	函数定义：size_t numDigits(int Number){...}
	类定义：class Widget{...}
	模板定义：template<typename T>class GraphNode {...}

#注：c++中先有声明还是先定义？？？  因情况而定
#	解决：类中成员变量中————是先声明，在定义(在构造函数中进行分配空间并初始化的操作即“定义”)
#		  类————在头文件中定义，在源码文件中声明。
b:
构造函数中explicit关键字的作用：阻止构造函数所属的类被用来隐式类型转换，但仍可以被用来进行显式类型转换
	如：class B{
		public:
				explicit B(int x=0,bool b=true);
		private:
				int x;
				bool b;
	}
	void something(B object)
	 B obj(28);
	 something(obj);
	 something(28);//错误，不接受隐式转换，something应该接受一个B对象，而不是Int
	 something(B(28))
#注：explicit构造函数比non-explicit构造函数更受欢迎，除非你要一个更好的理由让构造函数被用于隐式转换，否则都通通声明为explicit构造函数
c:
拷贝构造函数的作用：用来以同型对象初始化自我对象
赋值操作符的作用：用来从另一个同型对象中拷贝其值到自我对象
如何区分：一个新对象被定义时，一定有构造函数被调用，不可能调用赋值操作
		  若没有新对象被定义时，就不会用构造函数，而是用赋值操作符

class Widget {
public:
  Widget();                                 // default constructor
  Widget(const Widget& rhs);                // copy constructor
  Widget& operator=(const Widget& rhs);     // copy assignment operator
  ...
};
Widget w1;                                  // invoke default constructor
Widget w2(w1);                              // invoke copy constructor
Widget w3 = w2;                           // invoke copy constructor!
w1 = w2;                                    // invoke copy

#注：拷贝构造函数的用途：同类型对象显示或隐式初始化另一个对象
#						复制一个对象，作实参传递给另一个函数
#						从函数返回值时，复制一个对象
#						初始化顺序容器
#						根据元素初始化列表初始化数组元素
d:
从内置类型而言，pass-by-value比pass-by-reference要好
从自定义类型而言，pass-by-reference-to-const 比 pass-by-value效率要高很多
#注：在STL中，为了适应所有情况，通常是pass-by-value

///////////////////////////////////////////
//1、视C++为一个语言联邦：同时支持       //
///////////////////////////////////////////
	过程形式: 没有模板，没有异常，没有重载
	面向对象形式: 有封装，继承，多态，虚函数
	函数形式:
	泛型形式: 即模板元编程
	元编程形式: 
把c++视为一个由相关语言组成的联邦，而不是单一语言。即由四个部分组成：C、Object-Oriented C++、Template C++（泛型编程）、STL（容器）

///////////////////////////////////////////
//2、尽量用const和inline而不用#define    //
///////////////////////////////////////////
a：
问题：#define ASPECT_RATIO 1.653

编译器会永远也看不到ASPECT_RATIO这个符号名，因为在源码进入编译器之前，它会被预处理程序
去掉，于是ASPECT_RATIO不会加入到符号列表中。如果涉及到这个常量的代码在编译时报错，就会
很令人费解，因为报错信息指的是1.653，而不是ASPECT_RATIO。
改进：const double ASPECT_RATIO = 1.653;

注：常量定义一般是放在头文件中
	除了指针所指的类型要定义成const外，重要的是指针也经常要定义成const。
	如：const char * const authorName = "Scott Meyers";
b:
为了确保常量只有一份的：
头文件中：
class GamePlayer {
private:
  static const int NumTurns = 5;      // 是声明，不是定义，但如果是static成员变量，则可以把初值写在其后。
  int scores[NumTurns];               // use of constant
  ...
};
#注：定义一个类时，其数据成员是声明而不是定义，因为定义意味着分配空间，而数据成员的分配空间是在执行类的构造函数中进行
通常C++要求对你所使用的任何成员变量都提供一个定义式，但如果该成员变量是static const成员变量且为整型，
则作特殊对待：只要不取它们的地址，可以只在类中声明，而不需要定义式

#如果你的编译器可能非要看到其定义式，且把定义式放在实现文件，而不是头文件，则必须加上，而不再省略：
#	实现文件中：const int GamePlayer::NumTurns; //因为在类中声明时已获初值，则定义式中不再设初值

比较旧的编译器是这样子声明和定义的：
定义文件：
class CostEstimate {
private:
  static const double FudgeFactor;       // 声明
  ...                                    // constant; goes in header file
};
头文件：
const double CostEstimate::FudgeFactor = 1.35;      // 定义

c:
如果你不想让指针或引用提取你成员常量的地址，enum可以帮你实现：
	提取一个const的地址是合法的
	提取一个enum的地址是不合法的
	提取一个#define的地址是不合法的
class GamePlayer {
private:
  enum { NumTurns = 5 };        // "the enum hack" — makes
  int scores[NumTurns];         // fine
  ...
};


d:
问题：#define max(a,b) ((a) > (b) ? (a) : (b))
	
(注：define一个表达式时，一定要加(),其很多情况下，表达式中元素也要加())
int a = 5, b = 0;
max(++a, b);// a 的值增加了2次   7
max(++a, b+10); // a 的值只增加了1次   10

改进：inline int max(int a, int b) { return a > b ? a : b; }

引申：	const 用来解决define 一个常量
		inline 用来解决define 一个表达式

///////////////////////////////////////////
//3、尽量使用const                       //
///////////////////////////////////////////
a:
const用法
	char greeting[] = "Hello";
	char *p = greeting;               
	const char *p = greeting;                                    
	char * const p = greeting;          
	const char * const p = greeting;      

b:
iterator和const_iterator的使用场合：
	迭代器可以指向不同的东西，且所指的东西是可以改变的，则用iterator
	迭代器只能指向一个东西，但指向的内容是可以改变的，则用const iterator
	迭代器可以指向不同的东西，但所指的东西不可被改动，则需要const_iterator

std::vector<int> vec;
const std::vector<int>::iterator iter = vec.begin();
*iter = 10;                                 // OK, changes what iter points to
++iter; 错误                                   // error! iter is const

std::vector<int>::const_iterator cIter = vec.begin();
*cIter = 10; 错误                              // error! *cIter is const
++cIter;                                  // fine, changes cIter

c:
函数返回常量值，往往可以降低因用户错误而造成的意外，而又不至于放弃安全性和高效性
class Rational { ... };
const Rational operator*(const Rational& lhs, const Rational& rhs);

Rational a, b, c;
...
(a * b) = c;                           // 编译就提示报错

d:
const成员函数的意义：
	其一：容易区分哪个函数可以改动对象的内容，哪个函数不可以
	其二：使用“操作const对象”（mutable）成为可能
#注：当我们操作“const对象”时，该对象所属的类中必需有相对应的const成员函数才行。所有有时const成员函数必不可少
如1：
头文件:
class TextBlock{
public:
    TextBlock(string str):text(str){}
    const char& operator[](size_t pos) {#不是const成员函数
        return text[pos];
    }
private:
    string text;
};
定义文件：
#include"testall.h"
int main()
{
    const TextBlock tb("hello");
    # cout<<tb[1]<<endl;
    return 0;
}
执行结果：可以成功定义

如2：
头文件:
class TextBlock{
public:
    TextBlock(string str):text(str){}
    const char& operator[](size_t pos) {#不是const成员函数
        return text[pos];
    }
private:
    string text;
};
定义文件：
#include"testall.h"
int main()
{
    const TextBlock tb("hello");
    cout<<tb[1]<<endl;#编译不过，因为操作const对象时，编译器找不到其相对应的const成员函数
    return 0;
}
执行结果：编译不过
如3：
头文件:
class TextBlock{
public:
    TextBlock(string str):text(str){}
    const char& operator[](size_t pos) const {#const成员函数
        return text[pos];
    }
private:
    string text;
};
定义文件：
#include"testall.h"
int main()
{
    const TextBlock tb("hello");
    cout<<tb[1]<<endl;
    return 0;
}
执行结果：成功

e：
const成员函数用法，和易错点：
	class TextBlock {
	public:
	  const char& operator[](std::size_t position) const 
	  { return text[position]; }                     

	  char& operator[](std::size_t position)          
	  { return text[position]; }                 
	private:
	   std::string text;
	};

	TextBlock tb("Hello");
	std::cout << tb[0]; //调用普通的operator[]      
	tb[0] = 'x';//跟普通operator[]的返回值类型有关

	const TextBlock ctb("World");
	std::cout << ctb[0]; //调用相对应的const成员函数operator[]  
	ctb[0] = 'x';//错误,跟const成员函数operator[]的返回值类型有关
易错：
第一点：char operator[](std::size_t position)//编译可以通过，但并没有达到我们的目的          
	  { return text[position]; }   

第二点：class TextBlock {
	public:
	  const char& operator[](std::size_t position) const 
	  { return text[position]; }                     

	  char& operator[](std::size_t position)          
	  { return text[position]; }                 
	private:
	   const std::string text; #const常量
	};   

	TextBlock tb("World");
	std::cout << tb[0]; //调用普通operator[] ，而不是调用const成员函数operator[]
	tb[0] = 'x';//错误，string是一个const常量

f:
分清const类对象（const ctb）和const成员数据（const text）
const成员函数的定义有两种门派：
第一种说法：
成员函数内部在不改变成员变量的时才叫const成员函数，但许多成员函数可以达到不改变成员变量的目的，但仍不能叫const成员函数
如：
class CTextBlock {
public:
  char& operator[](std::size_t position) const  //错误
  { return pText[position]; }                  
private:
  char *pText;
};
以上成员函数虽然没有改变成员变量，但仍不适合写成const成员函数，因为：
const CTextBlock cctb("Hello");  
char *pc = &cctb[0];                  
*pc = 'J'; //如果上面写成const成员函数，此语句编译是错误的，但实际上编译没有问题 
易错：
class CTextBlock {
public:
    CTextBlock(string ss){
        pText = (char *)(new string(ss));
    }
  char& operator[](std::size_t position) //编译通不过
  {     cout<<"hh"<<endl;
      return pText[position]; }
private:
  char *pText;
};
int main(){
    const CTextBlock cctb("Hello");
    char *pc = &cctb[0];//找不到const []操作符成员函数
    *pc = 'J';
    return 0;
}
正确：
class CTextBlock {
public:
    CTextBlock(string ss){
        pText = (char *)(new string(ss));
    }
  char& operator[](std::size_t position) const//这样才可以通过，但这里写成const并不合适
  {     cout<<"hh"<<endl;
      return pText[position]; }
private:
  char *pText;
};
int main(){
    const CTextBlock cctb("Hello");
    char *pc = &cctb[0];
    *pc = 'J';
    return 0;
}

因而产生了第二种说法：
一个const成员函数可以修改它所处理对象内的某些bits，但必须在用户察觉不到情况下才行
class CTextBlock {
public:
  std::size_t length() const;
private:
  char *pText;
  std::size_t textLength;           
  bool lengthIsValid;              
};
std::size_t CTextBlock::length() const
{
  if (!lengthIsValid) {
    textLength = std::strlen(pText);  // error!这个确实需要改变该成员变量的值，但用户察觉不打，所以写为const成员函数，但编译器通不过
    lengthIsValid = true;            
  }                                  
  return textLength;
}

解决：为了符合第二种说法，出现了mutable关键字
class CTextBlock {
public:
  std::size_t length() const;
private:
  char *pText;
  mutable std::size_t textLength;           
  mutable bool lengthIsValid;              
};
std::size_t CTextBlock::length() const
{
  if (!lengthIsValid) {
    textLength = std::strlen(pText); //编译器可以通过了
    lengthIsValid = true;            
  }                                  
  return textLength;
}

g:
问题：如何避免const和non-const成员函数中的重复代码：重构
如：
class TextBlock {
public:
  const char& operator[](std::size_t position) const
  {
    ...                                 // do bounds checking
    ...                                 // log access data
    ...                                 // verify data integrity
    return text[position];
  }
  char& operator[](std::size_t position)
  {
    ...                                 // do bounds checking
    ...                                 // log access data
    ...                                 // verify data integrity
    return text[position];
  }
private:
   std::string text;
};
解决：实现operator[]的机能一次并使用它两次，即其中一个调用另一个
class TextBlock {
public:
  const char& operator[](std::size_t position) const     // same as before
  {
    ...
    ...
    ...
    return text[position];
  }
  char& operator[](std::size_t position)         // now just calls const op[]
  {
    return const_cast<char&>(static_cast<const TextBlock&>(*this)[position]);//为了避免[]会递归调用自己，所以使用static_cast<const TextBlock&>
  }
  分析：static_cast<const TextBlock&>导致调用const char& operator[](std::size_t position) const，这时返回的是一个const char&，
  		const_cast<char&>导致消除const
};
注：
const_cast<T>(expression)————将对象的常量性消除，即const转non-const

static_cast<T>(expression)————强迫隐式转换，如：non-const转const，int转double，pointer-to-base转pointer-to-derived，反向转换也行
/////////////////////////////////////////
// 4、确定对象在使用前已经被初始化了   //
/////////////////////////////////////////
a:
#即永远确保每一个构造函数都将对象的每一成员变量初始化，除static类变量、const static、引用
因此立下一个规定————规定总是在初值列中列出所有成员变量，以免还得记住哪些成员变量可以无需初值
b:
别混淆了赋值和初始化。初始化操作的构造函数比赋值操作构造函数的效率要高很多
一、赋值：3步完成————调用其default构造函数，设初值，调用其赋值操作符
ABEntry::ABEntry(const std::string& name, const std::string& address,
                 const std::list<PhoneNumber>& phones)
{
  theName = name;                       // these are all assignments,
  theAddress = address;                 // not initializations
  thePhones = phones
  numTimesConsulted = 0;
}
分析：先调用default构造函数为 theName、theAddress、thePhones设初值，然后再用实参对它们各自赋值操作（调用各自的赋值操作符）

二、初始化：1步完成————调用其拷贝构造函数
注：对象的成员变量初始化动作发生在进入构造函数体之前就进行了
ABEntry::ABEntry(const std::string& name, const std::string& address,
                 const std::list<PhoneNumber>& phones)
: theName(name),//各自调用各自的构造函数
  theAddress(address),                  // these are now all initializations
  thePhones(phones),
  numTimesConsulted(0) #由于numTimesConsulted是内置类型，如果成员初始列遗漏了它，它就没有初始值，可能发生意想不到的情况
{}   
分析：各自调用自己的copy构造函数，而实参就是name,address,phones，因此该操作效率要高很多

#注：一定要为内置型进行手工初始化，因为c++不保证它们会被初始化

#c：有的成员变量必须放在初始列表中初始化，而不能被赋值初始化：const，reference

d:
成员初始化次序
  先初始化基类的成员变量，在初始化派生类的成员变量，而类的内部是按照成员变量声明的次序被初始化
f:
static对象
  其寿命从被构造出来到成员结束。它的析构函数会再main结束时自动调用，因此在我们的类的析构函数不涉及static成员变量的析构
e:
#static对象包括global对象、namespace作用域内对象，在class内、函数内、file作用域内被声明为static的对象。
#而函数内的static对象叫local-static，其他static对象叫non-local static

问题：一个源文件的的non-static对象在初始化的时候，调用了第二个文件的non-static对象，
    但该non-static对象还未初始化
class FileSystem {                    // from your library
public:
  ...
  std::size_t numDisks() const;       // one of many member functions
  ...
};
extern FileSystem tfs;   //声明(global对象)，即non local static对象

class Directory {                       // created by library client
public:
   Directory( params );
  ...
};

Directory::Directory( params )
{
  ...
  std::size_t disks = tfs.numDisks();   // 在使用tfs对象时，可能该对象还未被初始化
  ...
}
解决：将non-local static对象变成local static对象
class FileSystem { ... };           // as before

FileSystem& tfs()#专属函数                   // this replaces the tfs object; it could be
{                                   // static in the FileSystem class
  static FileSystem fs;             // 定义并初始化fs变量: define and initialize a local static object
  return fs;                        // return a reference to it
}

class Directory { ... };            // as before

Directory::Directory( params )      // as before, except references to tfs are
{                                   // now to tfs()
  ...
  std::size_t disks = tfs().numDisks();
  ...
}

Directory& tempDir()                // this replaces the tempDir object; it
{                                   // could be static in the Directory class
  static Directory td;              // define/initialize local static object
  return td;                        // return reference to it
}

#因此：为了避免“跨编译单元初始化次序”问题，把non-local static变成local static

/////////////////////////////////////////////////////////////////
// 5、编译器默认声明了哪些函数，又何时生成了该函数的定义式     //
/////////////////////////////////////////////////////////////////

a:
一个空类时，编译器会自动声明构造函数，拷贝构造函数，赋值操作符，析构函数，且都是public inline
#注：只是声明，不是定义
b:
只有在这些函数被用到的时候，才会被编译器真正创建出来
Empty e1;                               // 编译器创建默认构造函数和析构函数
Empty e2(e1);                           // 编译器创建拷贝构造函数
e2 = e1;                //编译器创建赋值操作符（先调用默认构造函数设初值，再调用赋值操作符）
注：编译器产生的是一个non-virtual析构函数，除非这个类的基类的析构函数是virtual，这时编译器产生的是一个virtual析构函数
编译器生成的拷贝构造函数和赋值操作符只是单纯的把源对象的每一个non-static成员变量拷贝或赋值到目标对象而已。
c:
  template<typename T>
  class NamedObject {
  public:
    NamedObject(const char *name, const T& value);
    NamedObject(const std::string& name, const T& value);
  private:
    std::string nameValue;
    T objectValue;
  };

  NamedObject<int> no1("Smallest Prime Number", 2);//它会调用哪一个构造函数？？#需要最匹配的那个构造函数
  NamedObject<int> no2(no1); 调用拷贝构造函数，即便没有，编译器会自动生成
  //编译器生成的拷贝构造函数，no2.nameValue会以“拷贝no1.objectValue内的每一个bits”来完成初始化。
  //这时由于第一个参数是string，因此会调用string的拷贝构造函数
d：
问题：有时候编译器无法为我们自动某些函数，则拒绝生成该函数
如：
template<class T>

class NamedObject {
public:
  NamedObject(std::string& name, const T& value);
private:
  std::string& nameValue;           // this is now a reference
  const T objectValue;              // this is now const
};
Now consider what should happen here:
std::string newDog("Persephone");
std::string oldDog("Satch");

NamedObject<int> p(newDog, 2);               // when I originally wrote this, our
NamedObject<int> s(oldDog, 36);              // the family dog Satch (from my
p = s; //此时编译器自动为我们生成赋值操作符时，发现根本做不到const常用被赋值的情况，因此拒绝生成该赋值操作符
////////////////////////////////////////////////////////
// 6、不想使用编译器自动生成的函数，应该明确拒绝才是  //
////////////////////////////////////////////////////////
HomeForSale h1;
HomeForSale h2;
HomeForSale h3(h1);               // 阻止
h1 = h2;                          // 阻止
方法一：
把拷贝构造函数和赋值操作符定义为私有的，但成员函数和friend函数仍可以访问
方法二：
只声明不定义，但用户不小心用到的话，连接器发出抱怨
class HomeForSale {
public:
  ...
private:
  ...
  HomeForSale(const HomeForSale&);            // 只声明，不定义
  HomeForSale& operator=(const HomeForSale&);
};

方法三：
专门用一个基类去声明拷贝构造函数和赋值操作符，这样派生类就不用再声明拷贝构造函数和赋值操作符
class Uncopyable {
protected:                                   // allow construction
  Uncopyable() {}                            // and destruction of
  ~Uncopyable() {}                           // derived objects...
private:
  Uncopyable(const Uncopyable&);             // ...but prevent copying
  Uncopyable& operator=(const Uncopyable&);
};

class HomeForSale: private Uncopyable {     // class no longer
  ...                                       // declares copy ctor or
}; 
分析：这时编译器会自动生成派生类的拷贝构造函数和赋值操作符，但生成的时候，
发现基类的拷贝构造函数和赋值操作符是private，根本无法调用，因为拒绝创建拷贝构造函数和赋值操作符

注：派生类会自动调用基类的构造函数，拷贝构造函数和赋值操作符。

////////////////////////////////////////////////////////
// 7、多态基类的析构函数应该为virtual                 //
////////////////////////////////////////////////////////
a：
#注：类的析构不是虚析构函数时，不能用来被继承，否则派生类继承之后，在delete基类型指向派生类对象的指针时，没有调用派生类的析构函数，因为发生内存泄露
注意：仅限于delete 基类指针且指向派生类对象时，基类不是virtual析构函数才会发生内存泄露
如1.1：
class base{
public:
    base()
    {
        cout<<"base"<<endl;;
    }
    ~base()
    {
        cout<<"~base"<<endl;
    }
};
class derived:public base{
public:
    derived()
    {
        cout<<"derived"<<endl;
    }
    ~derived()
    {
        cout<<"~derived"<<endl;
    }
};
int main()
{
    derived d;#不会发生内存泄露
    return 0;
}
输出：  base
    derived
    ~derived
    ~base
如1.2：
class base{
public:
    base()
    {
        cout<<"base"<<endl;;
    }
    ~base()
    {
        cout<<"~base"<<endl;
    }
};
class derived:public base{
public:
    derived()
    {
        cout<<"derived"<<endl;
    }
    ~derived()
    {
        cout<<"~derived"<<endl;
    }
};
int main()
{
    derived *bb;
    bb = new derived();#不会发生内存泄露
    delete bb;
    return 0;
}
输出：  base
    derived
    ~derived
    ~base
如2：
class base{
public:
    base()
    {
        cout<<"base"<<endl;;
    }
    ~base()
    {
        cout<<"~base"<<endl;
    }
};
class derived:public base{
public:
    derived()
    {
        cout<<"derived"<<endl;
    }
    ~derived()
    {
        cout<<"~derived"<<endl;
    }
};
int main()
{
    base *bb;
    bb = new derived();#发生内存泄露
    delete bb;
    return 0;
}
输出： base
    derived
    ~base
如3：
virtual析构函数的基本被继承：
class base{
public:
    base()
    {
        cout<<"base"<<endl;;
    }
   virtual ~base()
    {
        cout<<"~base"<<endl;
    }
};
class derived:public base{
public:
    derived()
    {
        cout<<"derived"<<endl;
    }
    ~derived()
    {
        cout<<"~derived"<<endl;
    }
};
int main()
{
    base *bb;
    bb = new derived();#不会发生内存泄露
    delete bb;
    return 0;
}
输出：  base
    derived
    ~derived
    ~base
b:
问题：当多态基类的析构函数是non-virtual时
class TimeKeeper {
public:
  TimeKeeper();
  ~TimeKeeper();
  ...
};
class AtomicClock: public TimeKeeper { ... };
class WaterClock: public TimeKeeper { ... };
class WristWatch: public TimeKeeper { ... };

TimeKeeper* getTimeKeeper(); 
TimeKeeper *ptk = getTimeKeeper(); #基类指针
delete ptk;  //只调用了基类的析构函数，正常

AtomicClock* getTimeKeeper();  
TimeKeeper *ptk = getTimeKeeper();#派生类指针赋给基类指针
delete ptk;  //只调用了基类的析构函数，没有调用派生类的析构函数，会发生内存泄露

解决：
class TimeKeeper {
public:
  TimeKeeper();
  virtual ~TimeKeeper();
  ...
};

AtomicClock* getTimeKeeper();  
TimeKeeper *ptk = getTimeKeeper();
delete ptk; //此时会调用派生类的析构函数和基类的析构函数

c:
如果class不含virtual函数，通常它不意图被用做一个基类，否则会发生基类下的内存泄露

d:不要把non-virtual的类当做基类去继承
class SpecialString: public std::string {   // bad idea! std::string has a
  ...                                       // non-virtual destructor
};
SpecialString *pss =   new SpecialString("Impending Doom");
std::string *ps;
ps = pss;                               // SpecialString* std::string*
delete ps;                              // 只会调用基类string的析构函数，派生类的析构函数不会被调用，资源泄露

#e:
当对象调用某一virtual函数，实际被调用的函数取决于该对象的vptr(虚函数表指针)所指的那个vtbl(虚函数表)————编译器在其中寻找适当的函数指针

f:
分清抽象类（为了继承，不能直接实例化）和接口类（为了多态，类继承接口）
抽象类：至少带一个pure virtual成员函数，但不能全是（1<= X < n）
接口类：全是virtual成员函数

g：当定义一个抽象类，但手里没有pure virtual函数，这时把析构函数定义为pure virtual析构函数即可
如：
class AWOV {                            // AWOV = "Abstract w/o Virtuals"
public:
  virtual ~AWOV() = 0;                  // declare pure virtual destructor
};
AWOV::~AWOV() {}  //必须存在，否则连接器会抱怨

h:
析构函数的调用顺序：先调用派生类的析构函数，再调用基类的析构函数
#注：心得：只有当class内含知识一个virtual函数时，才将析构函数声明为virtual析构函数
/////////////////////////////////////////
// 8、析构函数中应该有异常处理部分     //
/////////////////////////////////////////

在执行析构函数时抛出异常，怎么办？可能会造成内存泄露
如：
class DBConnection {
public:
  ...
  static DBConnection create();        // function to return
  void close();                        // close connection; throw an
};   
                                  // exception if closing fails
class DBConn {                          // class to manage DBConnection
public:                                 // objects
  ...
  ~DBConn()    #有可能发生异常，导致资源泄露         // make sure database connections
  {                                     // are always closed
   db.close();
   }
private:
  DBConnection db;

};

{
  ....
  DBConn dbc(DBConnection::create());  //在该局部对象结束时，会自动调用其析构函数，而析构函数中抛出一个异常怎么办
  ....
}

解决方案一：只要抛出异常就结束程序
DBConn::~DBConn()
{
 try { db.close(); }
 catch (...) {
   make log entry that the call to close failed;
   std::abort();//异常结束程序
 }
}

解决方案二：吞下异常，它压制了“某些动作失败”的重要信息

DBConn::~DBConn()
{
 try { db.close(); }
 catch (...) {
      make log entry that the call to close failed;
 }
}

上述两种方案都不能保证程序还可以继续可靠执行，即使在遇到一个异常之后

因此：需要重新设计接口，使其用户有机会对可能出现的问题作出反应
class DBConn {
public:
  ...
  void close(){      #DBConn自己提供一个close函数，使其客户有机会对可能出现的问题作出反应
    db.close();
    closed = true;
  }

  ~DBConn(){
   if (!closed) {
   try {                                            // close the connection
     db.close();                                    // if the client didn't
   }
   catch (...) {                                    // if closing fails,
     make log entry that call to close failed;   // note that and
     ...                                             // terminate or swallow
   }
  }
private:
  DBConnection db;
  bool closed;
};

分析：把调用close的责任从DBConn析构函数上转移到了DBConn用户手上，由用户自己调用close，给他们一个处理错误的机会，当然他们可以忽略这个机会，然后再由DBConn析构函数决定在在异常发生时，到底是吞下这个异常还是结束程序

////////////////////////////////////////////////////////////////////////////////////////
// 9、在构造和析构函数内部中绝不能使用virtual成员函数（不管是virtual还是pure virtual）//
////////////////////////////////////////////////////////////////////////////////////////

a：
如：
class Transaction #抽象类
{                               // base class for all
public:                                           // transactions
  Transaction();
  virtual void logTransaction() const = 0;       // make type-dependent
  ...
};
Transaction::Transaction()                        // implementation of
{                                                 // base class ctor
  ...
  logTransaction(); #调用其pure-virtual虚函数
}                                                 // transaction

class BuyTransaction: public Transaction { #不是接口类，去查看接口类的定义       // derived class
public:
  virtual void logTransaction() const;          // how to log trans-
                                            // actions of this type
  ...
};

BuyTransaction b;

分析：进入BuyTransaction构造函数被调用，进入Transaction构造函数，
    这时调用Transaction的LogTransaction，而不是BuyTransaction的LogTransaction。
    而LogTransaction是pure virtual，在导致程序还是无法链接
理由是：假如此期间调用的virtual函数下降至派生类阶层，要知道派生类的函数几乎会使用到
    派生类的数据成员，而这时派生类的构造函数还未执行完成，则派生类的数据成员尚未初始化

#注：相同的道理也适用析构函数。

b：要确定构造和析构函数中有没有调用virtual函数并不容易
如1：当logTransaction是pure virtual函数时，大多执行系统会终止程序
class Transaction {
public:
  Transaction()
  { 
    init(); #这种情况下，是比较难发现其中是不是有virtual函数被调用
  }
                                        // call to non-virtual...
  virtual void logTransaction() const = 0; #抽象类
  ...
private:
  void init()
  {
    ...
    logTransaction();#pure virtual函数调用，导致系统终止运行                              // ...that calls a virtual!
  }
};

如2：当logTransaction是virtual，程序会高兴的执行，但调用错误版本的logTransaction（基类的logTransaction）
class Transaction {
public:
  Transaction()
  { 
    init(); #这种情况下，是比较难发现其中是不是有virtual函数被调用
  }
                                        // call to non-virtual...
  virtual void logTransaction() const;
  ...
private:
  void init()
  {
    ...
    logTransaction();#调用错误版本的logTransaction（基类的logTransaction）                              // ...that calls a virtual!
  }
};


c：解决上述问题
想要让派生类执行正确版本的logTransaction，要把logTransaction写成non-virtual，然后要求derived class构造函数传递必要信息给Transaction构造函数
这样就可以让那个构造函数调用想要版本的logTransaction
如：
class Transaction {
public:
  explicit Transaction(const std::string& logInfo);
  void logTransaction(const std::string& logInfo) const;   // now a non-
  ...
};
Transaction::Transaction(const std::string& logInfo)
{
  ...
  logTransaction(logInfo);                                // now a non-
}                                                         // virtual call

class BuyTransaction: public Transaction {
public:
 BuyTransaction( parameters ): Transaction(createLogString( parameters ))             // pass log info
  { ... }                                                 // to base class
   ...                                                    // constructor
private:
  static std::string createLogString( parameters );
};

BuyTransaction b;
总结：当你无法使用virtual函数从基类中向下调用，在构造期间，可以由派生类将必要的构造信息向上传递至基类构造函数，从而弥补缺陷
/////////////////////////////////////////////////////////
// 10、赋值操作符应该返回一个refernce to *this,包括+=  //
/////////////////////////////////////////////////////////

如：
class Widget {
public:
  ...
Widget& operator=(const Widget& rhs)   // return type is a reference to
{                                      // the current class
  ...
  return *this;                        // return the left-hand object
  }

Widget& operator+=(const Widget& rhs   // the convention applies to
  {                                     // +=, -=, *=, etc.
   ...
   return *this;
  }
  ...
};
