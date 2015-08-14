////////////////////////////////////////////////////////////
// 21、当函数必须返回对象时，不要返回其引用reference      //
////////////////////////////////////////////////////////////


a:不要返回局部对象的引用
pass-by-reference-to-const不一定处处比pass-by-value好，返回值时大多必须用pass-by-value
如：
易错：
class Rational {
public:
  Rational(int numerator = 0,int denominator = 1):n(numerator),d(denominator){}
private:
  int n, d;                                 // numerator and denominator
friend
   const Rational&  operator*(const Rational& lhs, const Rational& rhs)
   {
   		int n = lhs.n*rhs.n;
   		int d = lhs.d*rhs.d;
   		Rational r4 = Rational(n,d);
   		return r4; #错误，Rational(n,d)是一个局部变量。因为在函数退出之前就已经被销毁了
   }
public:
    void print(){
        cout<<n<<"  "<<d<<endl;
    }
    ~Rational(){
        n = 0;
        d = 0;
    }
};
int main(){
    Rational r1(1,4);
    Rational r2(1,4);
    Rational r3 = r1*r2;
    r3.print();
    return 0;
}

或者：
   const Rational&  operator*(const Rational& lhs, const Rational& rhs)
   {
   		int n = lhs.n*rhs.n;
   		int d = lhs.d*rhs.d;
   		return Rational(n,d);#错误，Rational(n,d)是一个局部变量。因为在函数退出之前就已经被销毁了
   }

#改进一：考虑在heap内构造一个对象
const Rational& operator*(const Rational& lhs,const Rational& rhs) 
{
  Rational *result = new Rational(lhs.n * rhs.n, lhs.d * rhs.d);
  return *result;
}#很可能调用者会忘记释放动态空间
例如：以下情况必然会发生泄露资源
Rational w, x, y, z;
w = x * y * z;  

#改进二：static对象（利用static具有自动析构的特性）
const Rational& operator*(const Rational& lhs, const Rational& rhs)    // bad code!
{
  static Rational result;             // static object to which a
  result = ... ;                      // multiply lhs by rhs and put the
  return result;
}//很可能造成线程不安全

bool operator==(const Rational& lhs,const Rational& rhs); 
Rational a, b, c, d;
...
if ((a * b) == (c * d))  {
    do whatever's appropriate when the products are equal;
} else    {
   do whatever's appropriate when they're not;
}
调用时：
if (operator==(operator*(a, b), operator*(c, d))) #会导致static Rational对象被赋值两次


#改进三：还是“坚持”原来的passed-by-value，因此此时passed-by-reference替代不了
const Rational  operator*(const Rational& lhs, const Rational& rhs)
{
		int n = lhs.n*rhs.n;
		int d = lhs.d*rhs.d;
		return Rational(n,d);//调用拷贝构造函数，operator*函数结束时会自动调用析构函数释放局部变量
}
////////////////////////////////////////////////////////////
// 22、成员变量大多都应声明为private                      //
////////////////////////////////////////////////////////////

排除法：首先分析为什么不是public，其次分析为什么不是protected，最后得出结论:应该是private
#a:使用函数可以让你对private成员变量的处理有更精确的控制
如：
class AccessLevels {
public:
  ...
  int getReadOnly() const        { return readOnly; }
  void setReadWrite(int value)   { readWrite = value; }
  int getReadWrite() const       { return readWrite; }
  void setWriteOnly(int value)   { writeOnly = value; }
private:
  int noAccess;                         // no access to this int
  int readOnly;                         // read-only access to this int
  int readWrite;                        // read-write access to this int
  int writeOnly;                        // write-only access to this int
};
#b:private成员变量具有封装的特性————通过函数访问成员变量，日后可改以某个计算替换这个成员变量，而class客户一点也不知道class的内部实现已经发生了变化，封装的意义就在此体现。
如：
class SpeedDataCollection {
  ...
public:
  void addValue(int speed);          // add a new data value
  double averageSoFar() const;       // return average speed
  ...
};
分析：每增加一个value，就重新计算一个平均值，计算平均值的方有两种：
  一种是在内存比较吃紧时，则考虑每次把所有的元素计算一遍，再算平均值
  一种是频繁需要使用到平均值时，且内存足够，则考虑随时维持一个当下平均值，增量计算平均值
然而，这两种方式的相互变换，class客户并不知情。

////////////////////////////////////////////////////////////
// 23、宁以non-member、non-friend替换member函数           //
////////////////////////////////////////////////////////////
#封装——————某些东西被封装，它就不再可见，愈多东西被封装，愈少人可以看到它，愈少人可以看到它，我们就有愈大的弹性去变化它，我们的改变仅仅只会影响能够看到改变的那些人事物。
#            同理：愈多函数可访问它，它的封装性就愈低。
class WebBrowser {
public:
  ...
  void clearCache();
  void clearHistory();
  void removeCookies();
  void clearEverything()#事实上，clearEvery带来的封装性比non-member函数clearCache要低
  {
  	  clearCache();#成员函数
  	  clearHistory();#成员函数
  	  removeCookies();#成员函数
	}
  ...
};

void clearBrowser(WebBrowser& wb)//non-member函数更好
{
  wb.clearCache();
  wb.clearHistory();
  wb.removeCookies();
}
注：能够访问private成员变量的函数只用class的member函数和friend函数。
如果在一个member函数和一个non-member,non-friend函数之间选择，且（前提）两者都能提供相同机能，那导致较大封装性的是后者，因为后者不会增加“能够访问private成员”的函数数量
//////////////////////////////////////////////////////////////////////
// 24、若函数的参数类型都需要类型转换，则采用non-member函数形似定义 //
//////////////////////////////////////////////////////////////////////

注：class内部的类型转换不定性很大，大大增加了出错的概率，因而令class支持隐式类型转换是个很糟糕的主意。
如：
class Rational {
public:

  Rational(int numerator = 0, int denominator = 1);     // allows implicit int-to-Rational
  int numerator() const;             // accessors for numerator and
  int denominator() const;           // denominator — see Item 22
  const Rational operator*(const Rational& rhs) const;
private:
  ...
};

Rational oneEighth(1, 8);#对象一
Rational oneHalf(1, 2);#对象二
Rational result = oneHalf * oneEighth;  
result = result * oneEighth;   

例1：
result = oneHalf * 2;   //即result = oneHalf.operator*(2);  #编译成功  
#分析：2——>调用构造函数，生成一个临时对象（隐式转换）
		const Rational temp(2);              // create a temporary
		result = oneHalf * temp;
例2：
result = 2 * oneHalf;   //即result = 2.operator*(oneHalf);  #编译失败
#分析：只有在参数被列于参数列中，才会有隐式转换

解决：把member函数变成non-member函数
class Rational {
  ...                                             // contains no operator*
};

const Rational operator*(const Rational& lhs,const Rational& rhs)     // function
{
  return Rational(lhs.numerator() * rhs.numerator(),lhs.denominator() * rhs.denominator());
}
Rational oneFourth(1, 4);
Rational result;

result = oneFourth * 2;                           // fine
result = 2 * oneFourth;

//////////////////////////////////////
// 25、写一个不抛出异常的swap函数   //
//////////////////////////////////////
		
#传统的swap:
namespace std{
  template<typename T>          // typical implementation of std::swap;
  void swap(T& a, T& b)         // swaps a's and b's values
  {
    T temp(a);
    a = b;
    b = temp;
  }
}

#swap缺省行为有时候效率却十分低下，如：置换Widget对象值，本质上只是置换其pImpl指针而已
class WidgetImpl {                         
public:                                     
  ...
private:
  int a, b, c;                              
  std::vector<double> v;                   
  ...
};

class Widget {                            
public:
  Widget(const Widget& rhs);
  Widget& operator=(const Widget& rhs)      
  {                                       
   ...                                    
   *pImpl = *(rhs.pImpl);                   
   ...                              
  }
  ...
private:
  WidgetImpl *pImpl; #上面                      
};  

问题一：调用swap缺省行为导致效率低下，用户只是想交换对象的指针而已
#解决：写一个全特化版本的swap(在内部调用swap缺省行为),专门针对交换Widget对象是时候。
namespace std {
  template<>  void swap<Widget>(Widget& a, Widget& b)    #全特化版本
  {
    swap(a.pImpl, b.pImpl);  #但编译不过，因为是数据成员pIml是private的
  }                                 
}

改正：
这个swap是专门为这个widget类而设计的
namespace std {
  template<>  void swap<Widget>(Widget& a,Widget& b)  #<widget>表示这一特化版本是针对T是widgetde的时候而设计的
  {
    a.swap(b);                     // to swap Widgets, call their
  }                                // swap member function
}

class Widget {                     
public:                            
  ...
  void swap(Widget& other){//member函数
    using std::swap;  #此语句的作用是如果没有专属的swap，则调用std中的swap             
    swap(pImpl, other.pImpl); #调用缺省的swap   
  }  
  ...
};
应用：
Widget w1；
Widget w2；
swap(w1,w2); #自动调用全特化版本的swap函数

问题二：如果widgetImpl是模板类，而不是类，还会适合吗？
template<typename T>
class WidgetImpl { ... };

template<typename T>
class Widget { ... };

namespace std {
  template<typename T>
  void swap<Widget<T乱流> >(Widget<T>& a, Widget<T>& b)  #编译不过，在特化std:swap时会遇上乱流。
  { a.swap(b); }
}
#解决办法：
namespace std {
  template<typename T> #编译不过
  void swap(Widget<T>& a,         
            Widget<T>& b)         
  { a.swap(b); }                  
}
分析：虽然添加了一个重载swap版本，但std是个特殊的命名空间，客户可以全特化std的templates，但不可以随意添加新的templates。
#改正：声明一个非std命名空间的non-member swap，让它调用member swap，即换个命名空间即可。
namespace WidgetStuff {
  ...                                    
  template<typename T>                  
  class Widget { ... };                   
  ...
  template<typename T>                   #non-member swap
  void swap(Widget<T>& a, Widget<T>& b)                                         
  {
    a.swap(b);
  }
}

#补充：using std::swap;的作用
#注：有std的那个一般化版本的swap，可能有或没有专属版本的swap，如何让编译器知道最好调用合适专属的swap，若没有专属版本的swap，才调用一般版本的swap，using std::swap语句正是起此作用。
template<typename T>
void doSomething(T& obj1, T& obj2)
{
  using std::swap;           // make std::swap available in this function
  ...
  swap(obj1, obj2);          // call the best swap for objects of type T
  ...
}

/////////////////////////////////////////////////////
// 26、尽量在变量使用的时候再去定义                //
/////////////////////////////////////////////////////

a：
方式一：
std::string encryptPassword(const std::string& password)
{
  using namespace std;
  string encrypted;
  if (password.length() < MinimumPasswordLength) {
      throw logic_error("Password is too short");
  }
  ...                        // do whatever is necessary to place an
  return encrypted;
}
#分析：对象encrypted并非完全被使用，在异常发生时，encrypted白白付出了构造成本和析构成本
方式二：
void encrypt(std::string& s);   
std::string encryptPassword(const std::string& password)
{
  using namespace std;
  if (password.length() < MinimumPasswordLength) {
     throw logic_error("Password is too short");
  }

 std::string encrypted;                // default-construct encrypted
  encrypted = password;                 // assign to encrypted
  encrypt(encrypted);
  return encrypted;
}
#分析：白白付出了default构造函数
方式三：
void encrypt(std::string& s);   
std::string encryptPassword(const std::string& password)
{
  ...                                     // check length 
  std::string encrypted(password);        // define and initialize
  encrypt(encrypted);
  return encrypted;
}

b：
但如果是循环怎么办？
如：
Widget w;
for (int i = 0; i < n; ++i){         
  w = some value dependent on i;     
  ...                                
}                                   
分析：一次构造函数+一次析构函数+n次赋值操作
for (int i = 0; i < n; ++i) {
  Widget w(some value dependent on i);
  ...
 }
分析:n次构造函数+n次析构函数，因此前者效率高一些

/////////////////////////////////////////
// 27、尽量少做类似转换：你不知道的事  //
/////////////////////////////////////////

a:
类型转换：	
      (T) expression 
			T(expression) 
			const_cast<T>(expression)//常量属性消失
			dynamic_cast<T>(expression)//安全向下转型：决定某对象是否归属继承体系中的某个类型（运行成本比较高）
			reinterpret_cast<T>(expression)//低级转型（不常用），如：int *转换成 int
			static_cast<T>(expression)//强制隐私转换（non-const->const, void*指针->type指针，pointer-to-base->pointer-to-derived）
static_cast：
	void doSomeWork(const Widget& w);
	doSomeWork(Widget(15));                    // create Widget from int
	doSomeWork(static_cast<Widget>(15));//隐式转换
b：
#误区：很多程序员以为类型转换其实没做什么
例一：
int x, y;
...
double d = static_cast<double>(x)/y;           // divide x by y, but use
分析：其实int的底层表示不同于double的底层表述，再例如：
例二：
class Base { ... };
class Derived: public Base { ... };
Derived d;
Base *pb = &d; 
分析：由于这两个指针值并不相同，在运行期间有个叫偏移量的东西作用在Derived*指针之上
#单一对象d可能拥有一个以上的地址：以Base*指向d的地址+以Derived*指向d的地址，即这就是多重继承的本质。
验证结果并不是这样，可能跟编译器有关。
c:
注：SpecialWindow s;
    Window *w = &s;
    w->onResize();//会调用派生类的onResize
问题：如何让派生类中成员函数去调用基类的成员函数？
class Window {                         
public:
  virtual void onResize() { ... }       
  ...
};

class SpecialWindow: public Window {     
public:
  virtual void onResize() {                   
    static_cast<Window>(*this).onResize();    #会创建*this对象的基类的副本
    ...                                   
  }                                          
  ...
};
目的是希望派生类能调用基类的onResize成员函数，事实上上面的代码并不是我们想那样，
因此static_cast<Window>(*this)会创建*this对象的基类的副本，而不是引用，若onResize函数中会修改
成员变量，那修改的基类的副本的成员变量，因此并没有达到修改原始基类对象的内容
解决：
class SpecialWindow: public Window {
public:
  virtual void onResize() {
    Window::onResize();                    // call Window::onResize
    ...                                    // on *this
  }
  ...
};

d:
研究dynamic_cast
#问题：如何让基类指针去调用派生类的成员函数？
class Base { ... };
class Derived: public Base { ... };
Base *pb = Base();
通常有两种一般性的做法：
#注：借助dynamic_cast        (尽量不要使用：运行成本高)
class Window { ... };
class SpecialWindow: public Window {
public:
  void blink();
  ...
};
typedef  std::vector<std::tr1::shared_ptr<Window> > VPW;  // on tr1::shared_ptr
VPW winPtrs; #申请一个存放基类指针的容器
...
for (VPW::iterator iter = winPtrs.begin(); iter != winPtrs.end(); ++iter) {
  if (SpecialWindow *psw = dynamic_cast<SpecialWindow*>(iter->get())) #dynamic_cast应用：向下转型
      psw->blink();
}

#方法一：使用容器并在其中事先存储直接指向derived class对象的指针(很笨重的方法)
typedef std::vector<std::tr1::shared_ptr<SpecialWindow> > VPSW;
VPSW winPtrs;  #申请一个存放派生类指针的容器
...
for (VPSW::iterator iter = winPtrs.begin(); iter != winPtrs.end(); ++iter)
  (*iter)->blink();

#方法二：定义基类的接口去处理“所有可能之各种派生类”
class Window {
public:
  virtual void blink() {}                       # 必须定义为空函数
  ...                                           #see Item 34 for why
}; 
class SpecialWindow: public Window {
public:
  virtual void blink() { ... };                 // 多态
  ...                                           // does something
};

typedef std::vector<std::tr1::shared_ptr<Window> > VPW;
VPW winPtrs;   #申请一个存放基类指针的容器 
...              
for (VPW::iterator iter = winPtrs.begin(); iter != winPtrs.end(); ++iter)
  (*iter)->blink();                             // 会执行派生类的blink吗？？？  #答案是不会执行派生类的blink，为什么？？？

#方法三：但尽量不要这么做，维护成本很高
class Window { ... };
...                                     // derived classes are defined here
typedef std::vector<std::tr1::shared_ptr<Window> > VPW;
VPW winPtrs;   #申请一个存放基类指针的容器
...
for (VPW::iterator iter = winPtrs.begin(); iter != winPtrs.end(); ++iter)
{
  if (SpecialWindow1 *psw1 =
       dynamic_cast<SpecialWindow1*>(iter->get())) { ... } #将基类指针进行 “向下安全转型” 到派生类指针
  else if (SpecialWindow2 *psw2 =
            dynamic_cast<SpecialWindow2*>(iter->get())) { ... }
  else if (SpecialWindow3 *psw3 =
            dynamic_cast<SpecialWindow3*>(iter->get())) { ... }
  ...
}

注：尽量不要在定义类的时候使用转型

///////////////////////////////////////////////////////////////////
// 28、不要返回handles(reference、指针、迭代器)指向对象内部成分  //
///////////////////////////////////////////////////////////////////

#安全性太差
如：
class Point {                      // class for representing points
public:
  Point(int x, int y);
  ...
  void setX(int newVal);
  void setY(int newVal);
  ...
};

struct RectData {                    // Point data for a Rectangle
  Point ulhc;                        // ulhc = " upper left-hand corner"
  Point lrhc;                        // lrhc = " lower right-hand corner"
};

class Rectangle {
  ...
private:
  std::tr1::shared_ptr<RectData> pData;          // see Item 13 for info on
};
class Rectangle {
public:
  ...
  Point& upperLeft() const { return pData->ulhc; }
  Point& lowerRight() const { return pData->lrhc; }
  ...
};

分析：编译虽然能通过，但有两点错误
#错误一：upperLeft()和lowerRight()返回了其引用，而我们的目的只是想返回值而已，但不是让其有被修改的风险
#错误二：虽然指针pData是private的，但指针指向的struct数据成员仍是public，因为lowerRight()和upperLeft()传回了其引用，则有被修改的风险

////////////////////////////////////
// 29、为“异常安全”而努力是值得的 //
////////////////////////////////////

a：
class PrettyMenu {
public:
  ...
  void changeBackground(std::istream& imgSrc);           // change background
  ...                                                    // image
private:
  Mutex mutex;                    // mutex for this object 
  Image *bgImage;                 // current background image
  int imageChanges;               // # of times image has been changed
};

void PrettyMenu::changeBackground(std::istream& imgSrc)
{
  lock(&mutex);                      // acquire mutex (as in Item 14)
  delete bgImage;                    // get rid of old background
  ++imageChanges;                    // update image change count
  bgImage = new Image(imgSrc);       // install new background
  unlock(&mutex);                    // release mutex
}
分析：当new Image(imgSrc)发生异常时，可能会出现：
	资源泄露：没有解锁
	数据败坏：原背景已删除， ++imageChanges，但新背景安装失败
b：
先解决资源泄露：借助智能指针（删除器）
void PrettyMenu::changeBackground(std::istream& imgSrc)
{
  Lock ml(&mutex);                
  delete bgImage;
  ++imageChanges;
  bgImage = new Image(imgSrc);
}
c：
异常安全的函数应该提供三个保证之一：
	基本承诺：如果异常抛出，程序内部应该仍保持有效状态，如：new Image(imgSrc)异常发生，继续拥有原背景，或者缺省背景
	强烈承诺：如果异常发生，程序的状态不改变。即异常发生时，程序<恢复>到原来的状态：原背景。
	不再抛出异常：承诺不再抛出其他意想不到的异常。
异常安全的函数必须提供上述三种保证之一。如果做不到，它就不具备异常安全性。

d：
解决数据败坏：
class PrettyMenu {
  ...
  std::tr1::shared_ptr<Image> bgImage;
  ...
};
void PrettyMenu::changeBackground(std::istream& imgSrc)
{
  Lock ml(&mutex);
  bgImage.reset(new Image(imgSrc));  #实现了基本保证，但还不能做到强烈保证
  ++imageChanges;
}
分析：智能指针bgImage.reset能做到只有在参数（new Image(imgSrc)）被成功生成之后才会执行，因此似乎可以保证若异常发生，能恢复到原来的状态。
		但如果Image构造函数在执行时发生了异常，可能导致输入流的读取记号被移动，从而对程序其余部分造成了一种可见的状态改变。由此看来还并不能做到强烈承诺

这时提出了copt and swap技术！
原理：对要修改的对象复制一份副本，在副本上做修改，若修改过程中发生异常，原对象保持不变；若修改没有异常，则原对象和副本做swap即可。
struct PMImpl {                              
  std::tr1::shared_ptr<Image> bgImage;        
  int imageChanges;                          
};
class PrettyMenu {
  ...
private:
  Mutex mutex;
  std::tr1::shared_ptr<PMImpl> pImpl;
};

void PrettyMenu::changeBackground(std::istream& imgSrc)
{
  using std::swap;                            // see Item 25
  Lock ml(&mutex);                            // acquire the mutex
  std::tr1::shared_ptr<PMImpl>  pNew(new PMImpl(*pImpl));
  pNew->bgImage.reset(new Image(imgSrc));     // modify the copy
  ++pNew->imageChanges;
  swap(pImpl, pNew);                          // swap the new
}                                             // release the mutex

现在看来已经做到了强烈承诺，但如果稍微添加几行代码，强烈承诺又失效了
void PrettyMenu::changeBackground(std::istream& imgSrc)
{
  using std::swap;                            // see Item 25
  Lock ml(&mutex);                            // acquire the mutex
  std::tr1::shared_ptr<PMImpl>  pNew(new PMImpl(*pImpl));
  pNew->bgImage.reset(new Image(imgSrc));     // modify the copy
  ++pNew->imageChanges;
  f1();
  f2();
  swap(pImpl, pNew);                          // swap the new
}   
分析：如果f1或者f2的异常安全性比“强烈保证低”，则就很难保证整体的强烈保证了

总结：当强烈保证不切实际时，你就必须提供基本保证，对很多函数而言，“异常安全之基本保证”是一定要做到的！

////////////////////
// 30、透析inline //
////////////////////

a：
inline的优缺点：
	免除了函数的调用成本，但目标代码体积增大了，从而可能导致缺页率增高
	如果inline函数的本体很小，编译器对函数本体产生的码可能比对函数调用产生的码更小
	#编译器有权对inline函数进行相关优化
	#inline只是对编译器提出申请，不是强制命令，编译器可加以忽略：大部分编译器拒绝太过复杂的函数inlining，如：递归函数，带有for的函数
	模板函数不一定就要inline化：需要template具现出来的函数才inline，不需要template具现出来的函数不inline，
	#virtual意味着“等待，直到运行时才确定调用哪一个函数”；inline意味着“执行前，先将调用动作替换成被调用函数的本体”，因此#virtual不应该写成inline
	inline可以显示提出，也可以隐式提出
	inline过程在编译期间进行
	#编译器不会对“通过函数指针而进行的函数调用”而inline
如：
inline void f() {...}      // assume compilers are willing to inline calls to f
void (*pf)() = f;          // pf points to f
...
f();                      // inline
pf();                    #不能inline

#将构造函数和析构函数inline是一个糟糕的做法，导致代码体积膨胀很大
如：
class Base {
public:
 ...
private:
   std::string bm1, bm2;               // base members 1 and 2
};
class Derived: public Base {
public:
  Derived() {}                         #隐式inline
  ...
private:
  std::string dm1, dm2, dm3;           // derived members 1–3
};
	编译器会生成：
Derived::Derived()                       // conceptual implementation of
{                                        // "empty" Derived ctor
 Base::Base();                           // initialize Base part
 try { dm1.std::string::string(); }      // try to construct dm1
 catch (...) {                           // if it throws,
   Base::~Base();                        // destroy base class part and
   throw;                                // propagate the exception
 }
 try { dm2.std::string::string(); }      // try to construct dm2
 catch(...) {                            // if it throws,
   dm1.std::string::~string();           // destroy dm1,
   Base::~Base();                        // destroy base class part, and
   throw;                                // propagate the exception
 }
 try { dm3.std::string::string(); }      // construct dm3
 catch(...) {                            // if it throws,
   dm2.std::string::~string();           // destroy dm2,
   dm1.std::string::~string();           // destroy dm1,
   Base::~Base();                        // destroy base class part, and
   throw;                                // propagate the exception
 }
}
由此看来，inline造成了程序体积比我们想象的大得多，因而程序设计者必须评估“将函数声明成inline”的冲击：inline函数无法随着程序库升级而升级，必须重新编译。
即：如果f是程序库的一个inline函数，客户将f函数本体编进其程序中，一旦程序设计者修改了f，所用的f的客户端程序都必须重新编译。
	
总结：由此看来，不大可能会修改的函数才适合被考虑声明为inline