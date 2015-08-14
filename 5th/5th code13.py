0、一个对象可以显式或隐式地进行拷贝、移动、赋值、销毁，全部借助于“
		拷贝构造函数
		拷贝赋值操作符
		#移动构造函数
		#移动赋值操作符
		析构函数
其中拷贝构造函数和移动构造函数定义了————当用同类型的另一个对象初始化本对象时做什么
	拷贝赋值操作符和移动赋值操作符定义了————当用同类型的另一个对象赋予本对象时做什么

当一个类没有定义它们时，编译器会自动合成它们，这往往是很危险的
1、拷贝构造函数
拷贝函数的第一个参数必须是引用(否则会出现死循环拷贝)，大多往往还是const引用
由于拷贝构造函数就是为了初始化另一个对象，所有通常不能是explicit的

当没有定义它时，编译器通常会生成一个合成拷贝构造函数：编译器从给定的对象依次将每一个非static成员拷贝到正在创建的新对象中
	对某些类来说，合成拷贝函数可以用来阻止我们拷贝该类类型的对象
如：
#直接初始化：
string dots(10, '.'); 				// 调用相应的构造函数
string s(dots); 					// direct initialization
#拷贝初始化：
string s2 = dots; 					// 调用拷贝构造函数
string null_book = "9-999-99999-9"; // copy initialization
string nines = string(100, '9'); 	// copy initialization
	#注：拷贝初始化通常使用拷贝构造函数进行，但是如果有移动构造函数，则拷贝初始化有时会使用移动拷贝构造函数进行
拷贝初始化使用场景：
	对象创建
	非引用参数
	非引用返回值
	初始化列表
拷贝构造函数的参数类型为什么必须是引用呢？
分析：若拷贝构造函数的参数是非引用类型，则在调用时，？？？？？

在拷贝初始化时，不一定非要调用拷贝或移动构造函数，因为编译器可以进行优化：
	string null_book = "9-999-99999-9"; // copy initialization
	优化后：
	string null_book("9-999-99999-9"); // compiler omits the copy constructor
2、拷贝赋值操作符
拷贝赋值运算符通常返回一个指向其运算符对象的引用
如：
Sales_data&
Sales_data::operator=(const Sales_data &rhs)
{
	bookNo = rhs.bookNo; // calls the string::operator=
	units_sold = rhs.units_sold; // uses the built-in int assignment
	revenue = rhs.revenue; // uses the built-in double assignment
	return *this; // return a reference to this object
}

当没有定义它时，编译器通常会生成一个合成拷贝赋值运算符：编译器从给定的对象依次将每一个非static成员赋值到正在创建的新对象中(也包括数组类型的成员，逐个赋值数组元素)
	对某些类来说，合成拷贝赋值运算符函数可以用来禁止该类类型的对象的赋值
3、构造函数————先销毁对象的非static数据成员，再释放对象使用的资源
其成员销毁时完全依赖于成员的类型，销毁类类型成员需要执行成员自己的析构函数
								  销毁内置类型时，由于内置类型没有析构函数，所有什么也不做
析构函数自动调用：
		变量离开其作用域时
		一个对象被销毁，其成员也被销毁时
		容器被销毁，其容器中元素也会被销毁
		delete 动态分配的对象地址时
		临时对象,如：返回值是非引用类类型
如： 
{ // new scope
	// p and p2 point to dynamically allocated objects
	Sales_data *p = new Sales_data; // 默认初始化，内置指针
	auto p2 = make_shared<Sales_data>(); // 智能指针
	Sales_data item(*p); // 拷贝构造函数
	vector<Sales_data> vec; // 局部对象
	vec.push_back(*p2); // 拷贝构造函数
	delete p; // 析构函数
}// 离开作用域，p2，item，vec会自动调用析构函数

当没有定义它时，编译器通常会生成一个合成拷贝赋值运算符：
	某些类来说，合成拷贝赋值运算符函数可以用来阻止该类类型对象销毁

#特别注意：析构函数的函数体自身并不直接销毁数据成员，成员而是在析构函数的函数体之后隐含的析构阶段中被销毁
4、3——5法则
法则一：需要析构函数的时候，一定也同时需要拷贝构造函数和拷贝赋值运算符
法则二：需要拷贝构造函数或拷贝赋值运算符其中之一，一定也需要其中的另一个，即共存亡！

5、显式要求编译器生成合成版本用 =default
class Sales_data {
public:
	Sales_data() = default;#构造函数
	Sales_data(const Sales_data&) = default;#拷贝构造函数
	Sales_data& operator=(const Sales_data &);
	~Sales_data() = default;#析构函数
};
Sales_data& Sales_data::operator=(const Sales_data&) = default;#不希望合成的是内联的，则外部用default


6、如何阻止对象的拷贝或赋值
在某些类中，需要阻止对象的拷贝或赋值的发生：
	方法一：用 =delete
	方法二：通过将拷贝构造函数和拷贝赋值运算符声明为private，然后在定义。但这样无法阻止内部成员函数和friend函数调用。————改进————只声明private函数，但不再定义。这样仍有问题，无意间调用，在编译器链接时才报错
	方法三：继承一个空基类，而这个空基类的拷贝构造函数或拷贝赋值构造函数都是private，这样编译器在生成派生类合成版本时，发现无能为力，就放弃了
如： 
struct NoDtor {
	NoDtor() = default; 
	~NoDtor() = delete; #错误
};
NoDtor nd; # error: NoDtor destructor is deleted
NoDtor *p = new NoDtor(); # ok: but we can't delete p
delete p; # error: NoDtor destructor is deleted

#特别注意：通常析构函数不能是delete的
若类定义了删除的析构函数，编译器不让该类型创建对象，临时对象也不行。如果类中的某个类类型成员定义了自身的删除析构函数，编译器也不让该类创建对象和临时对象
因为如果该类的析构函数删除的，则该类的成员无法被销毁

编译器将合成版本定义为删除时的情况：
		若该类的某个成员的析构函数是删除的或不可访问的（如：private），则编译器合成的析构函数也是删除的 
		若该类的某个成员的拷贝构造函数是删除的或不可访问的，则编译器合成的拷贝构造函数也是删除的 
		若该类的某个成员的拷贝赋值运算符是删除的或不可访问的，则编译器合成的拷贝赋值运算符也是删除的
		若该类的某个成员的析构函数是删除的、不可访问的或该类有引用成员，而这个类又没有类内初始化器，或该类有一个const成员，而没有类内初始化器其未显式定义默认构造函数，则该类的合成构造函数是删除的

#附加：析构函数与复制构造函数或赋值操作符之间的一个重要区别是，即使我们编写了自己的析构函数，合成析构函数仍然运行。
如： 
	class Sales_item {
	public:
		~Sales_item() { }
	};
撤销 Sales_item 类型的对象时，将运行这个什么也不做的析构函数，它执行完毕后，将运行合成析构函数以撤销类的成员。合成析构函数调用 string 析
构函数来撤销 string 成员，string 析构函数释放了保存 isbn 的内存。units_sold 和 revenue 成员是内置类型，所以合成析构函数撤销它们不需要做
什么。这也就解释了为什么成员的销毁在析构函数执行结束后才进行的

7、	类的行为像一个值————意味着它有自己的状态，拷贝一个对象时，副本和源对象是全完独立的
	类的行为像一个指针————意味着共享状态，拷贝一个对象时，副本和源对象使用相同的底层数据，改变副本也会改变原对象

8、类的行为像一个值
如： 
class HasPtr {
public:
	HasPtr(const std::string &s = std::string()):
	ps(new std::string(s)), i(0) { }
	// each HasPtr has its own copy of the string to which ps points
	HasPtr(const HasPtr &p):
	ps(new std::string(*p.ps)), i(p.i) { }
	HasPtr& operator=(const HasPtr &);#特别注意其实现，体现了该类像一个值
	~HasPtr() { delete ps; }
private:
	std::string *ps;
	int i;
};

HasPtr& HasPtr::operator=(const HasPtr &rhs)
{
	auto newp = new string(*rhs.ps); // copy the underlying string
	delete ps; #释放其旧资源，否则发生资源泄漏
	ps = newp; // copy data from rhs into this object
	i = rhs.i;
	return *this; // return this object
}

分析：拷贝赋值运算符通常组合了析构函数和构造函数的特性：赋值操作会销毁左侧对象的旧资源
														赋值操作会从右侧对象拷贝数据
注意这些操作的顺序，否则不能保证异常安全：
如： 
// WRONG way to write an assignment operator!
HasPtr&  HasPtr::operator=(const HasPtr &rhs)
{
	delete ps; #万一ps和rhs.ps指向同一块资源怎么办？
	ps = new string(*(rhs.ps));
	i = rhs.i;
	return *this;
}
9、类的行为像一个指针
在定义拷贝构造函数或拷贝赋值运算符时，拷贝的是指针成员本身，而不是它指向的string，这样导致我们在定义析构函数的时候，不能单方面释放相关联的string，而是只有当最后一个指向string的对象被销毁时，它才可以释放string

实现类的行为像一个指针的方法有：
		方法一：借助share_ptr智能指针
		方法二：使用引用计数器来模拟share_ptr

方法二的实现：
class HasPtr {
public:
	HasPtr(const std::string &s = std::string()):
		ps(new std::string(s)), i(0), use(new std::size_t(1)) {}
	HasPtr(const HasPtr &p): 
		ps(p.ps), i(p.i), use(p.use) { ++*use; }
	HasPtr& operator=(const HasPtr&);
	~HasPtr();
private:
	std::string *ps;
	int i;
	std::size_t *use; #动态内存很好的解决了————如何共享引用计数器的问题
};

HasPtr::~HasPtr()
{
	if (--*use == 0) { // if the reference count goes to 0
		delete ps; // delete the string
		delete use; // and the counter
	}
}

HasPtr& HasPtr::operator=(const HasPtr &rhs)
{
	++*rhs.use; 
	if (--*use == 0) { 
			delete ps; 
			delete use; 
		}
	ps = rhs.ps; 
	i = rhs.i;
	use = rhs.use;
	return *this;
}
引用计数器的作用：
	除初始化对象之外，每个构造函数创建一个新的引用计数器（即申请动态内存）
	拷贝构造函数不分配新的引用计数器，只递增引用计数器
	析构函数递减引用计数器，当引用计数器为0时，才释放资源
	拷贝赋值构造函数递增右侧对象的引用计数器，递减左侧对象的引用计数器，若左侧的引用计数器为0时，则释放左侧对象的资源

10、编写我们自己的swap函数是有必要的：
注：如果一个类定义了自己的swap，那么算法将使用类 自己定义的那个swap，否则算法使用标准库的swap
如： 
交换两个HasPtr类对象：
HasPtr temp = v1; 
v1 = v2; 
v2 = temp;
分析：实际上内存分配是不必要的：改进
string *temp = v1.ps; 
v1.ps = v2.ps; 
v2.ps = temp;
因此我们有必要定义适合自己的swap函数：
class HasPtr {
	friend void swap(HasPtr&, HasPtr&);
	// other members as in § 13.2.1 (p. 511)
};
inline void swap(HasPtr &lhs, HasPtr &rhs) #自定义的swap
{
	using std::swap;
	swap(lhs.ps, rhs.ps); #一般情况下，编译器会调用类类型成员自定义的swap，但内置类型没有，所以调用成了std::swap
	swap(lhs.i, rhs.i); // swap the int members
}
一般情况下，自定义的swap函数内部调用的swap不是std::swap，但本例中由于lhs.ps和lhs.i是内置类型，内置类型没有特定版本的swap，所以编译器会去调用std::swap
如： 
void swap(Foo &lhs, Foo &rhs)
{
	std::swap(lhs.h, rhs.h);#虽然能够正常运行，但并不是调用HasPtr自定义的swap，性能上并没有得到提升
}
改进：
void swap(Foo &lhs, Foo &rhs)
{
	using std::swap;#此语句不能缺失，在706页解释using的作用：使某个名字在该作用域中可见
	swap(lhs.h, rhs.h); #这里调用的是HasPtr自定义的swap，而不是std::swap
}

swap在赋值运算符中价值：
HasPtr& HasPtr::operator=(HasPtr rhs)
{
	swap(*this, rhs); //调用的是自定义swap，其执行过程是其rhs.ps 和 rhs..i的值
	return *this; // 
}
分析：由于参数是非引用，是值传递，因此生成的rhs临时对象，在赋值运算符执行结束以后，
		临时对象rhs会自动被销毁：rhs的析构函数执行，会delete rhs现在指向的内存空间，本方法很好的借助了临时对象自动销毁的特性

11、设计类：message————folder
消息目录与电子邮件消息

	*每个消息都可以出现在多个目录中
	*每个消息只有一个副本
	*每个消息都保存了自己在哪些目录中，用set<Folder *>保存
	*每个目录都保存了存放了哪些消息，用set<Message *>保存

	*消息都至少在某一个目录中(先不考虑这样)
	*目录可以是空目录，无任何消息

：

#电子邮件消息
分析：	构造函数
		拷贝构造函数：拷贝一个Message对象时，原对象和副本将是不同的Message对象，但都出现在相同的Folder下
		拷贝赋值运算符：左侧的Message对象会被右侧Message对象的内容所代替，包括Folder集合
		*移动构造函数：
		*移动赋值运算符：
		析构函数：销毁一个Message对象时，必须从所有的Folder中删除指向该Message的指针

		数据成员：将消息添加到某一目录中
				  从某一目录中删除该消息
#消息目录
分析：	构造函数
		拷贝构造函数：
		拷贝赋值运算符
		移动构造函数
		移动赋值运算符
		析构函数

		数据成员：		  
		成员函数
优良设计：
class Folder;

class Message {
    friend void swap(Message &, Message &);
    friend void swap(Folder &, Folder &);
    friend class Folder;
public:
    explicit Message(const std::string &str = ""):contents(str) {}
    Message(const Message&);
    Message& operator=(const Message&);
    ~Message();
    void save(Folder&);
    void remove(Folder&);

    void print_debug();

private:
    std::string contents;
    std::set<Folder*> folders;

    void add_to_Folders(const Message&);
    void remove_from_Folders();

    void addFldr(Folder *f) { folders.insert(f); }
    void remFldr(Folder *f) { folders.erase(f); }
};

void swap(Message&, Message&);

class Folder {
    friend void swap(Message&, Message&);
    friend void swap(Folder &, Folder &);
    friend class Message;
public:
    Folder() = default;
    Folder(const Folder &);
    Folder& operator=(const Folder &);
    ~Folder();

    void print_debug();

private:
    std::set<Message*> msgs;

    void add_to_Message(const Folder&);
    void remove_to_Message();

    void addMsg(Message *m) { msgs.insert(m); }
    void remMsg(Message *m) { msgs.erase(m); }
};

void swap(Folder &, Folder &);
自己完成folder类的书写：





12、设计一个自己进行内存分配的类————StrVec（一个专门分配字符串的容器，类似于vector，但它只用来分配字符串）
• elements, which points to the first element in the allocated memory
• first_free, which points just after the last actual element
• cap, which points just past the end of the allocated memory
• alloc_n_copy will allocate space and copy a given range of elements.
• free will destroy the constructed elements and deallocate the space.
• chk_n_alloc will ensure that there is room to add at least one more element
	to the StrVec. If there isn’t room for another element, chk_n_alloc will call
	reallocate to get more space.
• reallocate will reallocate the StrVec when it runs out of space.
• The default constructor (implicitly) default initializes alloc and (explicitly)
	initializes the pointers to nullptr, indicating that there are no elements.
• The size member returns the number of elements actually in use, which is
	equal to first_free - elements.
• The capacity member returns the number of elements that the StrVec can
	hold, which is equal to cap - elements.
• The chk_n_alloc causes the StrVec to be reallocated when there is no room to
	add another element, which happens when cap == first_free.
• The begin and end members return pointers to the first (i.e., elements) and
	one past the last constructed element (i.e., first_free), respectively
class StrVec {
public:
	StrVec(): // the allocator member is default initialized
	elements(nullptr), first_free(nullptr), cap(nullptr) { }
	StrVec(const StrVec&); // copy constructor
	StrVec &operator=(const StrVec&); // copy assignment
	~StrVec(); // destructor
	void push_back(const std::string&); // copy the element
	size_t size() const { return first_free - elements; }
	size_t capacity() const { return cap - elements; }
	std::string *begin() const { return elements; }
	std::string *end() const { return first_free; }
	// ...
private:
	std::allocator<std::string> alloc; # 用来分配未初始化的内存空间
	void chk_n_alloc() { if (size() == capacity()) reallocate(); }
	std::pair<std::string*, std::string*> alloc_n_copy(const std::string*, const std::string*);
	void free(); #销毁元素并释放“内存”
	void reallocate(); #扩展“内存”
	std::string *elements; #指向数组的首元素
	std::string *first_free; #指向数组第一个空闲的元素
	std::string *cap; #指向数组的尾后位置
};
void StrVec::push_back(const string& s)
{
	chk_n_alloc(); // ensure that there is room for another element
	// construct a copy of s in the element to which first_free points
	alloc.construct(first_free++, s);
}
pair<string*, string*>	StrVec::alloc_n_copy(const string *b, const string *e)
{
	// allocate space to hold as many elements as are in the range
	auto data = alloc.allocate(e - b);
	// initialize and return a pair constructed from data and
	// the value returned by uninitialized_copy
	return {data, uninitialized_copy(b, e, data)};
}
void StrVec::free()
{
	// may not pass deallocate a 0 pointer; if elements is 0, there's no work to do
	if (elements) {
		// destroy the old elements in reverse order
		for (auto p = first_free; p != elements; /* empty */)
			alloc.destroy(--p);
		alloc.deallocate(elements, cap - elements);
	}
}

StrVec::StrVec(const StrVec &s)
{
	// call alloc_n_copy to allocate exactly as many elements as in s
	auto newdata = alloc_n_copy(s.begin(), s.end());
	elements = newdata.first;
	first_free = cap = newdata.second;
}
StrVec::~StrVec() { free(); }

StrVec &StrVec::operator=(const StrVec &rhs)
{
	// call alloc_n_copy to allocate exactly as many elements as in rhs
	auto data = alloc_n_copy(rhs.begin(), rhs.end());
	free();
	elements = data.first;
	first_free = cap = data.second;
	return *this;
}
分析：reallocate函数应该完成什么样的操作：分配一个内存更大的空间，再拷贝原空间内容到新内存空间，再释放原内存空间资源
注：拷贝一个string必须真的拷贝数据，因为通常情况下，拷贝string之后，string就用两个不同用户，每个用户管理都是自己string，而本次reallocate过程中，拷贝string之后，还是一个用户，且原string立即销毁
因此想办法能不能不拷贝string数据，因此拷贝这些string是多余的，只移动string数据，这样可以避免string在新内存空间的重新分配工作和原string的销毁工作
实现以上要求就需要调用string的移动构造函数，而std::move就是显式告诉编译器调用移动构造函数的标志

void StrVec::reallocate()
{
	auto newcapacity = size() ? 2 * size() : 1;
	auto newdata = alloc.allocate(newcapacity);
	auto dest = newdata; // points to the next free position in the new array
	auto elem = elements; // points to the next element in the old array
	for (size_t i = 0; i != size(); ++i)
		alloc.construct(dest++, std::move(*elem++));#告诉编译器调用string的移动构造函数，而不是拷贝构造函数
	free(); #移动完所有string之后，就释放旧的string空间
	elements = newdata;
	first_free = dest;
	cap = elements + newcapacity;
}
分析：string的移动构造函数内部是怎样完成工作的？
	移动构造函数必须保证————“移动源”后，源string是有效、可析构的状态
	虽然string的移动构造函数细节并没有公开，但我们可以想象每个string都是一个指向char数组的指针，string的移动构造函数是对其指针进行了拷贝，而不是先分配字符数组空间再拷贝

思考：	reallocate会不会浪费内存，因为那些源字符串的空间并没有被释放，只是释放了所有权而已
		由于是“移动”，因此会不会造成资源不连续？


13、对象移动————阐述对象移动的思想，并引进右值引用的概念
其目的是为了学习如何书写自己类的移动构造函数
新标准的一个最重要的特征就是可以移动而非拷贝对象，而适合移动对象的情况有有哪些：
		当对象拷贝后就立即被销毁了，这时改用移动对象数据
		IO类或unique_ptr类不能拷贝，只能通过移动来达到目的，因为这些类不用来被共享
		在旧的标准中，容器所包含的类必须可拷贝才行，新标准中容器包含的类可以是不可拷贝的类，只要它们可以被移动即可
什么是左值————左值是指表达式结束结束以后依然还存在的持久对象
什么是右值————右值是指表达式结束以后就不再存在的临时对象
如： 

其区分二者的方法：看能不能对表达式取地址，如果能，就是左值，否则是右值

左值引用————根据修饰符的不同，分为常量左值引用和非常量左值引用
	非常量左值引用只能绑定到非常量左值
	常量左值引用可以绑定到所有类型的值：非常量左值，常量左值，非常量右值，常量右值
右值引用————


14、书写自定义类的移动构造函数和移动赋值构造函数

15、下面发生了几次析构函数
bool fcn(const Sales_data *trans, Sales_data accum)
{
    Sales_data item1(*trans), item2(accum);
    return item1.isbn() != item2.isbn();
}
```
3 times. There are `accum`, `item1` and `item2`.
16、
HasPtr类：多个HasPtr对象共享同一个string, #使用自己定义的引用计数器去代替shared_ptr中的引用计数器功能
分析：
	构造函数
	拷贝构造函数
	赋值拷贝构造函数（其他重载操作符）
	移动构造函数
	赋值移动构造函数
	析构函数

	数据成员:string *str
			 size_t *use
			 int pos;

	成员函数：curr()
		


17、
18、
19、
20、
21、
22、
23、
24、
25、


















