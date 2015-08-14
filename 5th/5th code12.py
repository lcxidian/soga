1、静态内存、栈、堆
静态内存用于保存 局部static变量、static成员变量、全局变量（定义在任何函数之外的变量），#编译时创建
栈内存用于保存定义在函数体之内的非static变量，#运行时才创建
堆用于保存动态分配的对象，即在运行时才分配的对象
#注：静态内存中变量和栈内存中的变量都是编译器自动创建和销毁，而堆中的对象是程序员自己创建和销毁

2、智能指针
shared_ptr————多个指针指向同一个对象
unique_ptr————“独占”所指的对象
weak_ptr————弱引用，指向shared_ptr所管理的对象

3、shared_ptr和unique_ptr都支持的操作
	share_ptr<T> sp;
	如：# shared_ptr<int> p(new int(42)); 或 shared_ptr<int> p(make_shared<int>(42));
		// shared_ptr<int> p = new int(42); #错误
	unique_ptr<T> up;
	p
	*p 
	p->mem 
	p.get()
	swap(p,q)
	p.swap(q)
4、shared_ptr特有的操作
	make_shared<T>(args) #此函数在动态分配一个对象并初始化，然后返回一个shared_ptr类型的智能指针
	shared_ptr<T> p(q)#q为普通指针
	p = q #q为shared_ptr指针
	p.unique()
	p.use_count()
# make_shared类似于顺序容器中的emplace操作
# make_shared<T>(args)所传递的参数必须与类类型的某一构造函数所匹配
如：
shared_ptr<int> p3 = make_shared<int>(42);
shared_ptr<string> p4 = make_shared<string>(10, '9');
shared_ptr<int> p5 = make_shared<int>();
5、当给shared_ptr赋于一个新值时，shared_ptr的析构函数执行：引用计数器就减一(若引用计数器减一为0，则析构函数销毁原来所指的对象)，新的shared_ptr的引用计数器加一
   当shared_ptr被销毁时，shared_ptr的析构函数执行：shared_ptr的引用计数器就减一(若引用计数器减一为0，则析构函数销毁原来所指的对象)

#特别注意：shared_ptr类的析构函数执行：自动递减所指对象的引用计数器，若计数器为0，析构函数就销毁所指的对象(这过程中还会调用其对象的析构函数再释放其空间)
6、shared_ptr的拷贝和赋值都会让引用计数器加一
如：
shared_ptr<Foo> factory(T arg){
	return make_shared<Foo>(arg);
}
void use_factory(T arg)
{
shared_ptr<Foo> p = factory(arg);
// use p
}#离开作用域，自动执行shared_ptr的析构函数让其引用计数器减一

shared_ptr<Foo> use_factory(T arg)
{
	shared_ptr<Foo> p = factory(arg); # 引用计数器为 1
	return p; # 引用计数器为 2
}# 离开作用域，引用计数器为 1
7、使用动态内存的原则必须满足以下之一：
	不知道自己需要使用多少对象（对象个数不确定）
	不知道所需对象的类型
	多个对象之间需要共享数据

8、分配的资源与对象的生存期相互独立（之前所有分配的资源与对象的生存期是共存亡的）
如：两个对象共享底层的数据，当某个对象被销毁时，我们不能单方面地销毁底层的数据
class StrBlob {
public:
	typedef std::vector<std::string>::size_type size_type;
	StrBlob();
	StrBlob(std::initializer_list<std::string> il);
	size_type size() const { return data->size(); }
	bool empty() const { return data->empty(); }
	void push_back(const std::string &t) {data->push_back(t);}
	void pop_back();
	std::string& front();
	std::string& back();
private:
	std::shared_ptr<std::vector<std::string>> data;#对象b1和对象b2共享vector
	void check(size_type i, const std::string &msg) const;#每次对vector操作时，都要检查是否越界访问
}

StrBlob::StrBlob(): data(make_shared<vector<string>>()) { }
StrBlob::StrBlob(initializer_list<string> il):data(make_shared<vector<string>>(il)) { }

void StrBlob::check(size_type i, const string &msg) const{
	if (i >= data->size())
	throw out_of_range(msg);
}

string& StrBlob::front(){
	// if the vector is empty, check will throw
	check(0, "front on empty StrBlob");
	return data->front();
}

string& StrBlob::back(){
	check(0, "back on empty StrBlob");
	return data->back();
}
void StrBlob::pop_back(){
	check(0, "pop_back on empty StrBlob");
	data->pop_back();
}

StrBlob类使用默认的拷贝构造函数、赋值操作符、析构函数，当我们拷贝、赋值或销毁一个StrBlob对象时，它的shared_ptr也会跟着被拷贝、赋值或销毁

如： 
	拷贝一个shared_ptr会递增其引用计数器；
	将一个shared_ptr赋值给另一个shared_ptr会递减赋值操作符右侧shared_ptr的引用计数器。而递减赋值操作符左边shared_ptr的引用计数器
	当shared_ptr的引用计数器为0，则它所指向的对象会被销毁

9、直接管理内存new
动态分配的对象使用的是默认初始化的话：
	当动态分配的对象是内置类型时，默认初始化的值是未定义的
	当动态分配的对象是类类型时，默认初始化的值是调用其类的默认构造函数进行初始化
如：
string *ps = new string; #默认初始化，初始值为空字符串
int *pi = new int; #默认初始化，初始值为未定义

10、初始化方式
int *pi = new int(1024); #直接初始化
string *ps = new string(10, '9'); #构造函数初始化
vector<int> *pv = new vector<int>{0,1,2,3,4,5,6,7,8,9};#列表初始化
string *ps1 = new string;#默认初始化
string *ps = new string();#默认构造函数初始化
int *pi1 = new int; #默认初始化
int *pi2 = new int();#值初始化

11、new不能分配所要求的内存空间，会抛出一个bad_alloc类型的异常
int *p1 = new int; // 若不能分配空间，则throws std::bad_alloc
int *p2 = new (nothrow) int; // 若不能分配空间，则返回一个空指针

12、
int i, *pi1 = &i, *pi2 = nullptr;
double *pd = new double(33), *pd2 = pd;
delete i; // 错误
delete pi1; // 错误，不是动态分配的内存指针
delete pd; // ok
delete pd2; // 错误，重复删除已被删除的指针
delete pi2; // 正确，可以重复删除空指针
13、悬空指针(野指针)
悬空指针————当我们delete一个指针以后，虽然指针无效了，但很多时候指针仍然保留着原动态内存的地址，即指向一块曾经保存数对象但现在已经无效的内存的指针
#特别注意：delete指针已经，还要给指针赋nullptr
如： 
	int *p(new int(42)); 
	auto q = p; 
	delete p; 
	p = nullptr;
14、shared_ptr类的构造函数是explicit，因此无法将普通指针隐式转换为shared_ptr智能指针
如： 
shared_ptr<int> p1 = new int(1024); // error: 因为shared_ptr类的构造函数是explicit
改正：
shared_ptr<int> p2(new int(1024));

shared_ptr<int> clone(int p) {
	return new int(p); // error: implicit conversion to shared_ptr<int>
}
改正：
shared_ptr<int> clone(int p) {
	// ok: explicitly create a shared_ptr<int> from int*
	return shared_ptr<int>(new int(p));
}
15、定义和改变shared_ptr
定义：
shared_ptr<T> p(q) #q为普通指针
shared_ptr<T> p(u) #u为unique_ptr类型指针
shared_ptr<T> p(q,d) #q为普通指针
shared_ptr<T> p(q2,d) #q2为shared_ptr指针，且q2 的引用计数器加1

改变：
p.reset() # 让p置空
p.reset(q) #q为普通指针
p.reset(q,d) #q为普通指针

如：
p.reset(new int(1024));

如： 
if (!p.unique())
	p.reset(new string(*p)); 
*p += newVal; //
16、普通指针和智能指针不能混合使用
# make_shared函数在分配对象的同时将shared_pptr与之绑定，这样可以避免同一块内存绑定到多个独立的shared_ptr指针上的可能
因此，使用make_share，而避免使用new
如： 
void process(shared_ptr<int> ptr)
{
	// 使用ptr
} // 离开作用域，自动销毁临时ptr(调用ptr的析构函数，让引用计数器减1)
shared_ptr<int> p(new int(42)); // reference count is 1
process(p); // 发生了智能指针的拷贝，因此引用计数器为2
int i = *p; // 引用计数器为1

17、不要使用普通指针 去干 shared_ptr指针要做的事
int *x(new int(1024)); // dangerous: x is a plain pointer, not a smart pointer
process(x); #错误，因此shared_ptr类的构造函数是explicit的
process(shared_ptr<int>(x)); #千万不要这样做：使用虽然合法，但内存会被释放，因此后面的操作x无效
int j = *x; // 不能操作一个已经被释放的内存

18、不要使用get()去初始化另一个智能指针
shared_ptr<int> p(new int(42)); // reference count is 1
int *q = p.get(); // 把智能指针的原生指针赋给另一个普通指针，其智能指针的引用计数器不会加1
{ 
	// undefined: two independent shared_ptrs point to the same memory
	shared_ptr<int> h(q);
} h离开作用域，会释放h指向的内存空间
int foo = *p; #无法访问已经被释放的内存空间
19、智能指针的使用陷阱
不要使用相同的内置指针值去初始化或reset多个智能指针
不要做delete p.get()操作 
不要使用get()初始化或reset另一个智能指针
当智能指针管理资源的不是new分配的空间时，应该传递一个删除器
如： 
struct destination; 
struct connection;
connection connect(destination*); 
void disconnect(connection); 
void end_connection(connection *p) { disconnect(*p); }
void f(destination &d /* other parameters */)
{
	connection c = connect(&d);
	shared_ptr<connection> p(&c, end_connection);
	// use the connection
	// when f exits, even if by an exception, the connection will be properly closed
}
20、unique_ptr智能指针
由于unique_ptr独享一个对象，因此当unique_ptr被销毁时，它所指向的对象也被销毁
#注：unique_ptr不支持拷贝和赋值操作，要使用u.release()
如：
unique_ptr<string> p1(new string("Stegosaurus"));
unique_ptr<string> p2(p1); #错误
unique_ptr<string> p3;
p3 = p2; #错误
21、unique_ptr提供的操作
unique_ptr<T> u #使用默认的delete来释放它的指针
unique_ptr<T,D> u #使用类型D的可调用对象来释放它的指针
unique_ptr<T,D> u(d) #使用类型D的可调用对象d来释放它的指针

u = nullptr;
u.release() #放弃对对象的控制权，返回指针，并置空   内存并不会被释放
u.reset(); #释放所指的对象，并置空
u.reset(q); #q为普通指针
u.reset(nullptr);
如： 
unique_ptr<string> p1(new string("Stegosaurus"));
unique_ptr<string> p2(p1); #错误，不能拷贝
unique_ptr<string> p3;
p3 = p2;#错误，不能赋值
unique_ptr<string> p2(p1.release()); // release makes p1 null
unique_ptr<string> p3(new string("Trex"));
// transfers ownership from p3 to p2
p2.reset(p3.release()); #reset先会释放p2指向的资源，再接受p3

22、u.release()使用错误
p2.release(); #严重错误，直接发生内存泄露
改正：
p2.reset();
23、只有在参数传递或return时，unique_ptr才支持拷贝和赋值操作————特例
如： 
unique_ptr<int> clone(int p) {
	// ok: explicitly create a unique_ptr<int> from int*
	return unique_ptr<int>(new int(p));
}

如： 
unique_ptr<int> clone(int p) {
	unique_ptr<int> ret(new int (p));
	// . . .
	return ret;
}
23、向unique_ptr传递删除器
如： 
unique_ptr<objT, delT> p (new objT, fcn);

void f(destination &d /* other needed parameters */)
{
	connection c = connect(&d); // open the connection
	unique_ptr<connection, decltype(end_connection)*>  p(&c, end_connection); #特别支持
}
24、weak_ptr智能指针(必须由shared_ptr指针来初始化)
	weak_ptr<T> w;
	weak_ptr<T> w(sp);#sp是shared_ptr指针
	 w = p;#p可以是shared_ptr指针，也可以是weak_ptr指针
	 w.reset() #置空
	 w.use_count() #引用计数器的值
	 w.expired() #若引用计数器为0，则返回true
	 w.lock() #若引用计数器为0，则返回一个空shared_ptr，否则返回一个shared_ptr指针

特性： 
auto p = make_shared<int>(42);
weak_ptr<int> wp(p);
分析：p和w都指向相同的对象，但w的出现，并不会增加其引用计数器的值，wp指向的对象可能会被释放掉。为了防止访问wp指向的对象不存在，因为不能使用weak_ptr直接访问其对象，应当先调用lock()
如： 
if (shared_ptr<int> np = wp.lock()) { // true if np is not null
	// inside the if, np shares its object with p
}

使用weak_ptr来替换shared_ptr的作用：

// StrBlobPtr throws an exception on attempts to access a nonexistent element
class StrBlobPtr {
public:
	StrBlobPtr(): curr(0) { }
	StrBlobPtr(StrBlob &a, size_t sz = 0):
	wptr(a.data), curr(sz) { }
	std::string& deref() const;
	StrBlobPtr& incr(); // prefix version
private:
	// check returns a shared_ptr to the vector if the check succeeds
	std::shared_ptr<std::vector<std::string>>
	check(std::size_t, const std::string&) const;
	// store a weak_ptr, which means the underlying vector might be destroyed
	std::weak_ptr<std::vector<std::string>> wptr;
	std::size_t curr; // current position within the array
};

std::shared_ptr<std::vector<std::string>>
StrBlobPtr::check(std::size_t i, const std::string &msg) const
{
	auto ret = wptr.lock(); // is the vector still around?
	if (!ret)
		throw std::runtime_error("unbound StrBlobPtr");
	if (i >= ret->size())
		throw std::out_of_range(msg);
	return ret; // otherwise, return a shared_ptr to the vector
}

std::string& StrBlobPtr::deref() const
{
	auto p = check(curr, "dereference past end");
	return (*p)[curr]; // (*p) is the vector to which this object points
}

// prefix: return a reference to the incremented object
StrBlobPtr& StrBlobPtr::incr()
{
	check(curr, "increment past end of StrBlobPtr");
	++curr; // advance the current state
	return *this;
}

25、管理new分配的数组
unqiue_ptr<T[]> u;
unique_ptr<T[]> u(p);#p为普通指针
u(i);

如： 
unique_ptr<int[]> up(new int[10]);
up.release();

26、使用shared_ptr来管理new分配的数组

shared_ptr<int> sp(new int[10], [](int *p) { delete[] p; });
sp.reset(); //

27、动态方式创建容器：
#注：之前我们大多分配的都是在函数体内创建的局部容器，它具有自动析构的特性
using ptr = vector<int>*;
ptr p = new vector<int>{};
delete p;
p = nullptr;

38、这样并不会使引用计数器增加
    shared_ptr<vector<int>> p(new vector<int>{});
    #或 shared_ptr<vector<int>> p(new vector<int>());
    #或 shared_ptr<vector<string>> p(new vector<string>); #默认初始化
    cout<<p.use_count()<<endl;# 1

    p = func(p);
    cout<<p.use_count()<<endl;# 仍然是1
    return 0;
28、allocator的作用
new——把内存分配和对象构造组合在一起
delete——把对象析构和内存释放组合在一起
然后，有的时候我们并不需要内存分配和对象构造组合在一起，否则会造成不必要的浪费
如：
string *const p = new string[n]; // construct n empty strings
string s;
string *q = p; // q points to the first string
while (cin >> s && q != p + n)
	*q++ = s; // assign a new value to *q
const size_t size = q - p; // remember how many strings we read
// use the array
delete[] p; //

标准库中allocator类帮助我们将内存分配和对象构造分开，对象析构和内存释放分离开来，它分配的是原始的内存，未被构造的内存
类似于vector一样，allocator也是一个模板。
如： 
allocator<string> alloc; #allocator对象
auto const p = alloc.allocate(n);#分配了n个string的内存大小.

allocator操作：
	allocator<T> a;
	a.allocator(n); 	#内存分配————调用malloc  注意：分配的是n个T对象大小的空间
	a.deallocator(p,n);	#内存释放————调用delete
	a.construct(p,args);#对象构造————调用T的构造函数
	a.destroy(p)；		#对象析构————调用T的析构函数  注意：这里可能只析构了部分，但对为被析构的那部分调用会出现段错误
                                                                                            
#特别注意：allcator返回的内存，必须用construct构造对象以后才可以使用
如： 
allcator<int> a;
allcator<int>::iterator = a.allcate(10);
cout << *p << endl; #error: q points to unconstructed memory!

标准库为allcator类定义两个伴随算法，可以不调用construct就能使用未初始化内存创建对象
uninitialized_copy(iter1,iter2,iter) #[iter1,iter2] 拷贝到 iter
uninitialized_copy_n(iter1,n,iter)
uninitialized_fill(iter1,iter2,val) #在[iter1,iter2] 中一律填充 val
uninitialized_fill_n(iter1,n,val)

29、weak_ptr存在的必要——————用来解决shared_ptr可能发生的循环引用问题
	boost的shared_ptr如果在循环引用的时候会出现无法释放内存的情况，所谓循环引用就是
A智能指针类里存放B的智能指针，B的智能指针类里存放A，将a、b的值互相设置。增加引用计数，
在释放的时候由于计数问题，会导致在退出指针域的时候无法进行释放，解决该问题的方案是在
类成员中使用弱指针。
如： 
#include "stdafx.h"
#include <iostream>
#include <boost/shared_ptr.hpp>
#include <boost/weak_ptr.hpp>
using namespace std;
class ObjectB;
class ObjectA
{
public:
  ~ObjectA()
  {
    std::cout<<"dctor ~ObjectA"<<std::endl;
  }
  void setObjectB(boost::shared_ptr<ObjectB> b)
  {
    m_objB = b;
  }
private:
  boost::shared_ptr<ObjectB> m_objB;
};

class ObjectB
{
public:
  ~ObjectB()
  {
    cout<<"dctor ~ObjectB"<<endl;
  }

  void setObjectA(boost::shared_ptr<ObjectA> a)
  {
    m_objA = a;
  }
private:
  boost::shared_ptr<ObjectA> m_objA;
};

void test()
{
  boost::shared_ptr<ObjectA> a(new ObjectA);
  boost::shared_ptr<ObjectB> b(new ObjectB);
  a->setObjectB(b);
  b->setObjectA(a);
};

int _tmain(int argc, _TCHAR* argv[])
{
  test();
  printf("test ");
  getchar();
  return 0;
}

分析： 
			---------------------
			|					|
a----->new ObjectA<------|		|
					     |		|
b----->new ObjectB-------|		|
				^				|	
				|				|
				-----------------	
智能指针a，b在离开test作用域之后，各引用计数器减1：

			---------------------
			|					|
a      new ObjectA<------|		|
					     |		|
b      new ObjectB-------|		|
				^				|	
				|				|
				-----------------	
导致a，b各自的智能指针成员计数器仍不为0，引用计数器不为0，导致不能调用a，b的析构函数，从而无法释放象ObjectA,ObjectB空间，导致内存泄露

改正：
#include "stdafx.h"

#include <iostream>
#include <boost/shared_ptr.hpp>
#include <boost/weak_ptr.hpp>

using namespace std;

class ObjectB;

class ObjectA
{
public:
  ~ObjectA()
  {
    std::cout<<"dctor ~ObjectA"<<std::endl;
  }

  void setObjectB(boost::shared_ptr<ObjectB> b)
  {
    m_objB = b;
  }
private:
  boost::weak_ptr<ObjectB> m_objB;
};

class ObjectB
{
public:
  ~ObjectB()
  {
    cout<<"dctor ~ObjectB"<<endl;
  }

  void setObjectA(boost::shared_ptr<ObjectA> a)
  {
    m_objA = a;
  }
private:
  boost::weak_ptr<ObjectA> m_objA;
};

void test()
{
  boost::shared_ptr<ObjectA> a(new ObjectA);
  boost::shared_ptr<ObjectB> b(new ObjectB);

  a->setObjectB(b);
  b->setObjectA(a);
};

int _tmain(int argc, _TCHAR* argv[])
{
  test();
  printf("test ");
  getchar();
  return 0;
}
分析：       弱引用，引用计数器不加1
			---------------------
			|					|
a----->new ObjectA<------|		|
					     |		|
b----->new ObjectB-------|		|
				^				|	
				|				|
				-----------------	
				弱引用，引用计数器不加1

由于对象ObjectA,ObjectB各自的智能指针成员是weak_ptr，因此不会增加a，b的引用计数器，a，b离开test作用域后，a，b的引用计数器为0，则会调用a，b各自的析构函数，其析构函数就会调用的对象ObjectA,ObjectB的析构函数
从而，不会发生内存泄露问题。

30、
（p 404）实现一个StrBlob类：使得多个StrBlob对象能够共享一个vector<string>成员
分析：
	构造函数
	拷贝构造函数
	赋值拷贝构造函数（其他重载操作符）
	移动构造函数
	赋值移动构造函数
	析构函数

	数据成员:shared_ptr智能指针，指向一个动态分配的vector容器

	#（既然是管理多个对象可以共享一个vector，因此需要提供给用户有关vector的操作）
	函数成员：begin()
			  end()
			  front()
			  back()
			  push_back()
			  pop_back()
			  empty()
			  size()

			  check() ///检查是否在某些操作下是否会发生越界：越界就必须抛异常，而不是return出来

31、
（p 421）实现一个StrBlobPtr类：用其数据成员weak_ptr指针——————指向StrBlob中动态vector<string> 
								#如何才能让weak_ptr指向StrBlob类中vector<string>呢？？？ 靠得就是StrBlob中的shared_ptr给weak_ptr赋值
	构造函数
	拷贝构造函数
	赋值拷贝构造函数（其他重载操作符）
	移动构造函数
	赋值移动构造函数
	析构函数

	数据成员:weak_ptr智能指针
	函数成员：curr()
			  deref()
			  incr()
			  
			  check() ///检查是否weak_ptr是否指向空，若为空则抛出异常
			  		  ///检查是否在某些操作下是否会发生越界：越界就必须抛异常
			  		  ///以上都通过了，则返回shared_ptr类型指针，通过shared_ptr指针来操作，而不是直接使用weak_ptr操作
32、
33、
34、
35、

















