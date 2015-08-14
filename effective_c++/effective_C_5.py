//////////////////////////////////////
// 41、了解隐式接口和编译期多态     //
//////////////////////////////////////

#注：面向对象是以显式接口和运行期多态解决问题；而template是以隐式接口和编译期多态解决问题
a：
class Widget {
public:
  Widget();
  virtual ~Widget();
  virtual std::size_t size() const;
  virtual void normalize();
  void swap(Widget& other);                 // see Item 25
  ...
};
显式接口：
void doProcessing(Widget& w)
{
  if (w.size() > 10 && w != someNastyWidget) {
      Widget temp(w);
      temp.normalize();
      temp.swap(w);
  }
}

隐式接口：
template<typename T>
void doProcessing(T& w)
{
  if (w.size() > 10 && w != someNastyWidget) {
     T temp(w);
     temp.normalize();
     temp.swap(w);
  }
}
以不同的template参数具现化function template会导致调用不同的函数————编译期多态

//////////////////////////////////////
// 42、了解typename的双重意义       //
//////////////////////////////////////

a：
template<class T> class Widget;                 // uses "class"
template<typename T> class Widget;              // uses "typename"
注：当声明template类型参数时，class和typename的意义完全相同，只是typename暗示了参数类型不一定是class而已

b：
C++并非总把class和typename看做等价关系，有时候只能只用typename
如：设计一个函数只打印其第二个元素的值
template<typename C>                            // print 2nd element in
void print2nd(const C& container)               // container;
{                                               // this is not valid C++!
  if (container.size() >= 2) {
     C::const_iterator iter(container.begin()); // get iterator to 1st element
     ++iter;                                    // move iter to 2nd element
     int value = *iter;                         // copy that element to an int
     std::cout << value;                        // print the int
  }
}
template内出现的名称如果想依于某个template参数，则称之为从属名称，如：C
如果从属名称在class内呈嵌套状，则称之为嵌套从属名称，如：C::const_iterator
template<typename C>
void print2nd(const C& container)
{
  C::const_iterator * x;
  ...
}
分析：目的是声明一个C::const_iterator类型指针变量x，但编译器不知道，编译器可能以为类型C下有一个叫const_iterator的static变量，
		导致编译器错误的当做变量与x的乘积。
C++在解析这一歧义时的规则是：如果解析器在template中遇到嵌套从属名称，它缺省认为这不是一个类型，而是变量，因此我们需要显式告诉编译器
即在嵌套从属名称前加typename关键字：
如：
template<typename C>                           // this is valid C++
void print2nd(const C& container)
{
  if (container.size() >= 2) {
    typename C::const_iterator iter(container.begin());
    ...
  }
}
再如：
template<typename C>                   // typename allowed (as is "class")
void f(
	const C& container,             // typename not allowed
    typename C::iterator iter
      ); 

c：
“typename必须作为嵌套从属名称的前缀词”，这样规则有个情况例外：typename不可出现在基类列表内的嵌套从属类型名称之前
如：
template<typename T>
class Derived: public Base<T>::Nested { // base class list: typename not
public:                                 // allowed
  explicit Derived(int x)
  : Base<T>::Nested(x)                 # 不能加typename
  {                                     // init. list: typename not allowed
    typename Base<T>::Nested temp;      // use of nested dependent type
    ...                                 // name not in a base class list or
  }                                     // as a base class identifier in a
  ...                                   // mem. init. list: typename required
};

d：
typename的应用：举例
如：
template<typename IterT>
void workWithIterator(IterT iter)
{
  typename std::iterator_traits<IterT>::value_type temp(*iter);
  ...
}
再如：
template<typename IterT>
void workWithIterator(IterT iter)
{
  typedef typename std::iterator_traits<IterT>::value_type value_type;
  value_type temp(*iter);
  ...
}

//////////////////////////////////////
// 43、学会处理模板化基类中名称     //
//////////////////////////////////////

#由模板类延伸到模板化基类
a:
假如如下：
class CompanyA {
public:
  ...
  void sendCleartext(const std::string& msg);
  void sendEncrypted(const std::string& msg);
  ...
};

class CompanyB {
public:
  ...
  void sendCleartext(const std::string& msg);
  void sendEncrypted(const std::string& msg);
  ...
};
...                                     // classes for other companies
class MsgInfo { ... };                  // class for holding information

template<typename Company>
class MsgSender {                #模板化类
public:
  ...                                   // ctors, dtor, etc.
  void sendClear(const MsgInfo& info)
  {
    std::string msg;
    create msg from info;//先产生信息
    Company c;
    c.sendCleartext(msg);#表示Company类中有这个sendSecret API才行
  }
  void sendSecret(const MsgInfo& info)   // similar to sendClear, except
  { ... }                                // calls c.sendEncrypted
};

要求：在我们每次发送信息之前之后，把状态写入日志log中：
template<typename Company>
class LoggingMsgSender: public MsgSender<Company> { #继承这个模板化类
public:
  ...                                    // ctors, dtor, etc.
  void sendClearMsg(const MsgInfo& info)
  {
    write "before sending" info to the log;
    sendClear(info);                    
   # 编译不过。原因：找不到sendClear函数，编译器不确定MsgSender<Company>中有sendClear
    write "after sending" info to the log;
  }
  ...
};
#分析：在编译LoggingMsgSender类的时候，编译器并不知道LoggingMsgSender继承了一个什么样的类，
#   	MsgSender<Company>中Company具体是哪个类，无法具现化。因此更无法知道sendClear

b：
#解决上述问题：如何让问题具体化？
class CompanyZ {                             // 这个template 参数中并没有sendCleartext，如果MsgSender拿去做模板参数时，成员函数sendClear是无效的
public:                                      // sendCleartext function
  ...
  #没有 sendCleartext函数
  void sendEncrypted(const std::string& msg);
  ...
};
template<typename Company>
class MsgSender {               
public:
  ...                                   // ctors, dtor, etc.
  void sendClear(const MsgInfo& info)
  {
    std::string msg;
    create msg from info;//先产生信息
    Company c;
    c.sendCleartext(msg);             # 编译不过：CompanyZ中没有sendCleartext，因此CompanyZ类并不适合一般性的模板化类MsgSender<Company>
  }
  void sendSecret(const MsgInfo& info)   // similar to sendClear, except
  { ... }                                // calls c.sendEncrypted
};
#由于CompanyZ类并不适合一般性的模板化类MsgSender<Company>，因为CompanyZ只有一个sendEncrypted，没有sendCleartext，为了让其合适模板化类MsgSender<Company>，
#从而产生一个MsgSender特化版：
template<>                                 // 特化版MsgSender
class MsgSender<CompanyZ> {             
public:                             
  ...                                    
  void sendSecret(const MsgInfo& info)
  { ... }
};

什么是模板全特化————模板化类对类型CompanyZ特化了，而且特化是全面性的，即一旦CompanyZ被确定，就不再有其他template参数可以选择了
对CompanyZ进行全特化的意义：
template<typename Company>
class LoggingMsgSender: public MsgSender<Company> {
public:
  ...
  void sendClearMsg(const MsgInfo& info)
  {
    write "before sending" info to the log;
    sendClear(info); # if Company == CompanyZ,这个template 参数中并没有sendCleartext，如果MsgSender拿去做模板参数时，编译器就找不到有效的sendClear
    write "after sending" info to the log;
  }
  ...
};

分析：如果Company是CompanyZ时，因此C++拒绝编译通过，即当我们从面向对象继承跨进template C++继承不再像以前那样畅通无阻了

#解决——————如何让class MsgSender即适合一般性的template Company,又适合特化的CompanyZ
            想办法让c++在 “进入” templated base class“观察”
方法一：
template<typename Company>
class LoggingMsgSender: public MsgSender<Company> {
public:
  ...
  void sendClearMsg(const MsgInfo& info)
  {
    write "before sending" info to the log;
    this->sendClear(info);                // okay, assumes that
    write "after sending" info to the log;
  }
  ...
};

方法二：
template<typename Company>
class LoggingMsgSender: public MsgSender<Company> {
public:
  using MsgSender<Company>::sendClear;   // tell compilers to assume
  ...                                    // that sendClear is in the
  void sendClearMsg(const MsgInfo& info)
  {
    ...
    sendClear(info);                   // okay, assumes that
    ...                                // sendClear will be inherited
  }
  ...
};

方法三：
template<typename Company>
class LoggingMsgSender: public MsgSender<Company> {
public:
  ...
  void sendClearMsg(const MsgInfo& info)
  {
    ...
    MsgSender<Company>::sendClear(info);      // okay, assumes that
    ...                                       // sendClear will be
  }                                           //inherited
  ...
};
////////////////////////////////////////////////////
// 44、将与参数无关的代码从模板化类中分析处理     //
////////////////////////////////////////////////////

如：
template代码中，重复是隐晦的，必须仔细去发觉当template被具现化时，可能发生的重复操作，这样重复的操作与template参数无关
如：
template<typename T,           // template for n x n matrices of
         std::size_t n>        // objects of type T; see below for info
class SquareMatrix {           // on the size_t parameter
public:
  ...
  void invert();              // invert the matrix in place
};
SquareMatrix<double, 5> sm1;
...
sm1.invert();                  // call SquareMatrix<double, 5>::invert

SquareMatrix<double, 10> sm2;
...
sm2.invert();                  // call SquareMatrix<double, 10>::invert

观察：重复代码invert()操作
解决：将重复的操作从模板化类中分离处理
template<typename T>                   // size-independent base class for
class SquareMatrixBase {               // square matrices
protected:
  ...
  void invert(std::size_t matrixSize); // invert matrix of the given size
  ...
};

template<typename T, std::size_t n>
class SquareMatrix: private SquareMatrixBase<T> {
private:
  using SquareMatrixBase<T>::invert;   // avoid hiding base version of
public:
  ...
  void invert() { this->invert(n); }   // make inline call to base class
};     
注：private继承表明：base class只是为了帮助derived classes实现，不是is-a的关系

b：
新问题：如何把派生类的矩阵计算数据传给基类的invert
解决:
方法一:
template<typename T>
class SquareMatrixBase {
protected:
  SquareMatrixBase(std::size_t n, T *pMem)     // store matrix size and a
  : size(n), pData(pMem) {}                    // ptr to matrix values
  void setDataPtr(T *ptr) { pData = ptr; }     // reassign pData
  ...
private:
  std::size_t size;                            // size of matrix
  T *pData;                                    // pointer to matrix values
};

方法二：
template<typename T, std::size_t n>
class SquareMatrix: private SquareMatrixBase<T> {
public:
  SquareMatrix()                             // send matrix size and
  : SquareMatrixBase<T>(n, data) {}          // data ptr to base class
  ...
private:
  T data[n*n];
};
//////////////////////////////////////////////
// 45、让成员函数模板接受所有的兼容类型     //
//////////////////////////////////////////////

a:
真实的指针支持隐式转换：
class Top { ... };
class Middle: public Top { ... };
class Bottom: public Middle { ... };
Top *pt1 = new Middle;                   // convert Middle* Top*
Top *pt2 = new Bottom;                   // convert Bottom* Top*
const Top *pct2 = pt1;                   // convert Top*  const Top*

b：
自定义的智能指针如何支持隐式转换：
template<typename T>
class SmartPtr {//自定义的智能指针
public:                             // smart pointers are typically
  explicit SmartPtr(T *realPtr);    // initialized by built-in pointers
  ...
};
SmartPtr<Top> pt1 = martPtr<Middle>(new Middle);     //  编译不过
SmartPtr<Top> pt2 = SmartPtr<Bottom>(new Bottom);     //  编译不过
SmartPtr<const Top> pct2 = pt1;     // convert SmartPtr<Top> 

分析：同一个template的不同具现体之间不存在与生俱来的固有关系，即便是继承也没有
		即martPtr<Middle>(new Middle)和SmartPtr<Bottom>(new Bottom)没有什么关系，即便他们有相同的基类
c：
为了让自定义的智能指针支持隐式转换，就必须显式定义出来：如何编写智能指针的构造函数？
由于智能指针是模板化类，所以无法编写具体的构造函数，因此需要编写一个构造模板：
template<typename T>
class SmartPtr {
public:
  template<typename U>                       // 
  SmartPtr(const SmartPtr<U>& other);        // 泛化拷贝构造函数：SmartPtr<U>智能指针 转换成一个SmartPtr<T>的智能指针
  ...                                        
};

我们希望SmartPtr<Bottom>转换成一个SmartPtr<Top>，而不希望SmartPtr<Top>转换成一个SmartPtr<Bottom>，否则继承是矛盾的
d：
通过学习auto_ptr和shared_ptr都提供一个get()成员函数来返回智能指针的原始指针的副本，我们的自定义也需要这样做，才能完成
SmartPtr<Bottom>————》原始指针——————》SmartPtr<Top>
template<typename T>
class SmartPtr {
public:
  template<typename U>
  SmartPtr(const SmartPtr<U>& other)         // initialize this held ptr
  : heldPtr(other.get()) { ... }             // with other's held ptr
  T* get() const { return heldPtr; }
  ...
private:                                     // built-in pointer held
  T *heldPtr;                                // by the SmartPtr
};

e:
成员函数模板(template<typename U>SmartPtr(const SmartPtr<U>& other))作用不限于构造函数，还能支持隐式转换的赋值操作
template<class T> class shared_ptr {
public:
  template<class Y>                                     // construct from
    explicit shared_ptr(Y * p);                         // any compatible
  template<class Y>                                     // built-in pointer,
    shared_ptr(shared_ptr<Y> const& r);                 // shared_ptr,
  template<class Y>                                     // weak_ptr, or
    explicit shared_ptr(weak_ptr<Y> const& r);          // auto_ptr
  template<class Y>
    explicit shared_ptr(auto_ptr<Y>& r);
  template<class Y>                                     // assign from
    shared_ptr& operator=(shared_ptr<Y> const& r);      // any compatible
  template<class Y>                                     // shared_ptr or
    shared_ptr& operator=(auto_ptr<Y>& r);              // auto_ptr
  ...
};

///////////////////////////////////////////////////////////////////////////////////////////
// 46、将需要类型转换时请定义为非成员函数模板，而不要定义为成员函数模板,即普通的模板函数 //
///////////////////////////////////////////////////////////////////////////////////////////

a:
template<typename T>
class Rational {
public:
  Rational(const T& numerator = 0,     // see Item 20 for why params
           const T& denominator = 1);  // are now passed by reference
  const T numerator() const;           // see Item 28 for why return
  const T denominator() const;         // values are still passed by value,
  ...                                  // Item 3 for why they're const
};

template<typename T>
const Rational<T> operator*(const Rational<T>& lhs,
                            const Rational<T>& rhs)
{ ... }
Rational<int> oneHalf(1, 2);          // this example is from Item 24,
Rational<int> result = oneHalf * 2;   // 错误，编译器不能把int 2 隐式转换成  Rational<int>
分析：模板化的Rational内的某些东西似乎和其non-template的Rational不同：
	我们希望编译器使用Rational<int>的构造函数可以将int 2转换成Rational<int,但事实上在template实参推导不会将隐式转换纳入考虑
解决：
在template class内将 operator*声明为一个friend函数。使得编译器能够在template<T>具现时得知T是什么
即：
template<typename T>
class Rational {
public:
  ...
friend
   const Rational<T> operator*(const Rational<T>& lhs,
                               const Rational<T>& rhs);
  // 这时编译器知道我们要调用哪一个函数了
  ...
};

Rational<int> oneHalf(1, 2);          // this example is from Item 24,
Rational<int> result = oneHalf * 2;   //编译通过，但连接器报错

但 friend operator*并没有实现定义，因此连接器报错，简单的做法是把实现写入类中(注，这是非成员函数)
template<typename T>

class Rational {
public:
  ...
friend const Rational operator*(const Rational& lhs, const Rational& rhs)
{
  return Rational(lhs.numerator() * rhs.numerator(),       // same impl
                  lhs.denominator() * rhs.denominator());  // as in
}                                                          // Item 24
};

/////////////////////////////////////////
// 47、使用traits calsses表示类型信息  //
/////////////////////////////////////////

a:
traits技术————在编译期间取得某些类型信息，它是一种技术，也是c++的协议。
	它要求对内置的类型和用户自定义的类型的表现都一样好。如：下面例子收到的实参是一个指针和int，advance也一样能运行好。
如：
template<typename IterT, typename DistT>
void advance(IterT& iter, DistT d)
{
  if (iter is a random access iterator) {
     iter += d;                                      // use iterator arithmetic
  }                                                  // for random access iters
  else {
    if (d >= 0) { while (d--) ++iter; }              // use iterative calls to
    else { while (d++) --iter; }                     // ++ or -- for other
  }                                                  // iterator categories
}
分析：traits能够做到像class（class可以嵌套类型信息）一样，接受内置类型，但内置类型无法办到内嵌类型信息。
	因此类型的traits信息（即类型信息）必须位于类型自身之外。标准技术是把它放到一个template或多个特化版本template中，
	这样的template在程序中就可表示若干个类型信息。其中针对迭代器的被命名为iterator_traits
template <class Iterator>
struct iterator_traits {
  typedef typename Iterator::iterator_category iterator_category;
  typedef typename Iterator::value_type        value_type;
  typedef typename Iterator::difference_type   difference_type;
  typedef typename Iterator::pointer           pointer;
  typedef typename Iterator::reference         reference;
};

template <class T>	//特化版（支持内置类型和指针）
struct iterator_traits<T*> {
  typedef random_access_iterator_tag iterator_category;
  typedef T                          value_type;
  typedef ptrdiff_t                  difference_type;
  typedef T*                         pointer;
  typedef T&                         reference;
};

template <class T> //特化版（支持内置类型和指针）
struct iterator_traits<const T*> {
  typedef random_access_iterator_tag iterator_category;
  typedef T                          value_type;
  typedef ptrdiff_t                  difference_type;
  typedef const T*                   pointer;
  typedef const T&                   reference;
};
b:
如何利用traits获取类型信息，也包括内置类型或指针在内
例1：
template < ... >                    // template params elided
class deque {
public:
  class iterator {
  public:
    typedef random_access_iterator_tag iterator_category;
    ...
  }:
  ...
};

template < ... >
class list {
public:
  class iterator {
  public:
    typedef bidirectional_iterator_tag iterator_category;
    ...
  }:
  ...
};

获取类型信息:
template<typename IterT>
struct iterator_traits {
  typedef typename IterT::iterator_category iterator_category;
  ...
};

template<typename IterT, typename DistT>
void advance(IterT& iter, DistT d)
{
  if (typeid(typename std::iterator_traits<IterT>::iterator_category) ==
     typeid(std::random_access_iterator_tag))//编译不过：原因：见条款48
  ...
}
新问题：IterT类型在编译时确定，但if判断是在运行时才执行，如何做到在编译时进行类型判断：
解决：重载————重载某个函数时，你必须详细叙述各个重载件的参数类型。编译器通过实参来选择最合适的重载函数，这过程发生在编译期间：
template<typename IterT, typename DistT>              // use this impl for
void doAdvance(IterT& iter, DistT d,                  // random access
               std::random_access_iterator_tag)       // iterators
{
  iter += d;
}
template<typename IterT, typename DistT>              // use this impl for
void doAdvance(IterT& iter, DistT d,                  // bidirectional
               std::bidirectional_iterator_tag)       // iterators
{
  if (d >= 0) { while (d--) ++iter; }
  else { while (d++) --iter;         }
}
template<typename IterT, typename DistT>              // use this impl for
void doAdvance(IterT& iter, DistT d,                  // input iterators
               std::input_iterator_tag)
{
  if (d < 0 ) {
     throw std::out_of_range("Negative distance");    // see below
  }
  while (d--) ++iter;
}
有了这些重载版本，advance需要做的就是调用它们，并额外传递一个对象，对象必须带有适当的迭代器分类：
template<typename IterT, typename DistT>
void advance(IterT& iter, DistT d)
{
  doAdvance(                                              // call the version
    iter, d,                                              // of doAdvance
    typename                                              // that is
      std::iterator_traits<IterT>::iterator_category()    // appropriate for
  );                                                      // iter's iterator
}   
//////////////////////////////////////
// 48、认识template元编程           //
//////////////////////////////////////

a：
template元编程—————编写template-based C++程序并执行于编译期间的过程。
template<typename IterT, typename DistT>
void advance(IterT& iter, DistT d)
{
  if (typeid(typename std::iterator_traits<IterT>::iterator_category) ==
      typeid(std::random_access_iterator_tag)) {
     iter += d;                                     // use iterator arithmetic
  }                                                 // for random access iters
  else {
    if (d >= 0) { while (d--) ++iter; }             // use iterative calls to
    else { while (d++) --iter; }                    // ++ or -- for other
  }                                                 // iterator categories
}
调用时：
std::list<int>::iterator iter;
...
advance(iter, 10);      //编译不过

其过程如：
void advance(std::list<int>::iterator& iter, int d)
{
  if (typeid(std::iterator_traits<std::list<int>::iterator>::iterator_category) ==
      typeid(std::random_access_iterator_tag)) {
    iter += d;                                       
     // 错误：只有random access迭代器才支持+=，编译器必须确保所有的源码都必须有效，纵使不会执行的代码也应该有效。
     // 由于if判断在运行期，而在编译期编译iter += d时并不能通过。即当iter不是random access迭代器时，iter += d代码无效

  }
  else {
    if (d >= 0) { while (d--) ++iter; }
    else { while (d++) --iter; }
  }
}

理解template元编程的目的————在编译期，而不再运行期

//////////////////////////////////////
// 49、new-handle的作用和使用       //
//////////////////////////////////////
a：
当operator new无法满足某一内存分配需求时，它会抛出异常。但在抛出异常前，会调用一个客户指定的错误处理函数new-handle
为了指定这个“new-handle”，客户必须调用set-new-handle设置new-handle。
如：
namespace std {
  typedef void (*new_handler)();
  new_handler set_new_handler(new_handler p) throw();
  // 获取一个new-handler，并返回一个new-handler（指向set_new-handler被调用前正在使用的那个new-handler），该函数尾部的throw是为了该函数不抛出任何异常
}
注：当operator new无法满足内存申请时，它会不断调用new-handler函数，知道找到足够内存。
b：
设计一个良好的new-handler时，必须做到：
	让更多的内存可被使用
	安装另一个new-handler：当当前这个new-handler无法取得更多可用内存时，可安装另外那一个new-handler
	卸载另一个new-handler：将NULL传给set_new_handler，一旦没有安装任何new-handler，operator new会在内存分配失败时，抛出异常
	抛出bad_alloc异常：这样的异常不会被operator new捕捉，会被传入内存索求处
	没有返回值：直接调用abort或exit
c：
c++不支持class专属之new-handlers，其实也不需要，不过我们可以实现

//////////////////////////////////////
// 50、new的合理替换时机            //
//////////////////////////////////////

编译器已经提供了operator new和operator delete，为什么我们还有定义自己的operator new和operator deleter呢？
理由：	用来检测运行上的错误
		为了收集动态分配内存之使用统计信息
		为了增加分配和归还的速度
		为了降低缺省内存管理器带来的空间额外开销
		为了弥补缺省分配器中的非最佳齐位
		为了将相关对象集中
		为了获得非传统的行为

//////////////////////////////////////
// 51、编写时需固定常规             //
//////////////////////////////////////

//////////////////////////////////////
// 52、new 与 delete应成对出现      //
//////////////////////////////////////

string *stringptr1 = new string;
delete stringptr1;// 删除一个对象

string *stringptr2 = new string[100];
delete [] stringptr2;// 删除对象数组
即如果你调用new时用了[]，调用delete时也要用[]。如果调用new时没有用[]，那调用delete时也不要用[]。
易错：
typedef string addresslines[4];	//一个人的地址，共4行，每行一个string
string *pal = new addresslines;	//

delete pal;// 错误!
delete [] pal;// 正确
（为了避免混乱，最好杜绝对数组类型用typedefs。）

//////////////////////////////////////
// 53、不要轻视编译器告警           //
//////////////////////////////////////

//////////////////////////////////////
// 54、熟悉TR1                      //
//////////////////////////////////////

TR1：STL、Iostream、异常类、智能指针、tr1::function、tr1::bind、tr1::hash tables、regex、tuples、
	tr1::array、tr1::mem_fn、随机数、types traits、trl::result_of、、、
  
//////////////////////////////////////
// 55、熟悉boost                    //
//////////////////////////////////////

