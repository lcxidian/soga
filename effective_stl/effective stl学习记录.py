2015-4-27
"学习effective STL"
目的：
0、导读
容器分类：
	标准序列容器：vector、string、deque、list
	非标准序列容器：slist、rope
	标准关联容器：set、multiset、map、multimap(红黑树实现)
	非标准关联容器：hash_set、hash_multiset、hash_map、hash_multimap（hash实现）

迭代器分类：
	输入迭代器是每个迭代位置只能被读一次的只读迭代器.
	输出迭代器是每个迭代位置只能被写一次的只写迭代器.
	前向迭代器有输入和输出迭代器的能力，但是它们可以反复读或写一个位置.
	双向迭代器就像前向迭代器，除了它们的后退可以像前进一样容易.
	随机访问迭代器可以做双向迭代器做的一切事情,但有有一步向前或向后跳的能力。

函数对象：
	重载了函数调用操作符（即，operator()）的任何类叫做仿函数类。从这样的类建立的对象称
	为函数对象

时间复杂度：
	通常，常数时间操作运行得比要求对数时间的快，而对数时间操作运行得比线性的快。

tyename和class
	其一：typename能更清楚地表示我通常想要说的：T可以是任何类型；不必是一个类。
	其二：为了避免潜在的解析含糊，你被要求在依赖形式类型参数的类型名字之前使用typename
		  。这样的类型被称为依赖类型。
		如：typename C::const_iterator begin(container, begin());

1、仔细选择你的容器
	标准序列容器：vector, string(不是class), deque, list
	非标准序列容器：slist, rope
	标准关联容器：set, multiset, map, multimap
	非标准关联容器：hash_set, hash_multiset, hash_map, hash_multimap
	几种标准非STL容器：数组、bitset、valarray、stack、queue和priority_queue。


·你需要“可以在容器的任意位置插入一个新元素”的能力吗？如果是，你需要序列容器
.你关心元素在容器中的顺序吗？如果不，散列容器就是可行的选择。
.必须使用标准C++中的容器吗？如果是，就可以除去散列容器、slist和rope。
.如果必须是随机访问迭代器，在技术上你就只能限于vector、deque和string，但也可能会考虑rope（
.当插入或者删除数据时，是否非常在意容器内现有元素的移动？如果是，你就必须放弃连续内存容器
.查找速度很重要吗？如果是，你就应该看看散列容器或关联容器.
.你需要插入和删除的事务性语义吗？也就是说，你需要有可靠地回退插入和删除的能力吗？如果是，
你就需要使用基于节点的容器。
.你要把迭代器、指针和引用的失效次数减到最少吗？如果是，你就应该使用基于节点的容器

2、根本不可能做到容器也泛化
a：
stl是建立在泛化的基础之上：
	数组泛化为容器，参数化了所包含的对象的类型。
	函数泛化为算法，参数化了所用的迭代器的类型。
	指针泛化为迭代器，参数化了所指向的对象的类型。

标准的内存相邻容器都提供随机访问迭代器	
标准的基于节点的容器都提供双向迭代器

b:
很多程序员试图试图在他们的软件中泛化容器的不同，而不是针对容器的特殊性编程，以至于他们可以用，可以说，现在是一个vector，但
以后仍然可以用比如deque或者list等东西来代替——都可以在不用改变代码的情况下来使用
因为不是所有的容器都支持某一个操作

c:
当你需要使用一个不同的容器类型。你现在知道当你改变容器类型的时候，不光要修正编译器诊断出来的问题，而且要检查所有使用容器的代
码，根据新容器的性能特征和迭代器，指针和引用的失效规则来看看那些需要修改

解决：可以用这个常用的方法让改变得以简化：使用封装，封装，再封装。其中一种最简单的方法是通过自由地对容器和迭代器类型使用typedef。
写法一：
class Widget {...};
vector<Widget> 			vw;
Widget 					bestWidget;
... 								// 给bestWidget一个值
vector<Widget>::iterator i = find(vw.begin(), vw.end(), bestWidget);

写法二：
class Widget { ... };
typedef vector<Widget> 				WidgetContainer;
typedef WidgetContainer::iterator 	WCIterator;
WidgetContainer 					cw;
Widget 								bestWidget;
...
WCIterator i = find(cw.begin(), cw.end(), bestWidget);

写法三：
class Widget { ... };
template<typename T> // 关于为什么这里需要一个template
SpecialAllocator { ... }; // 请参见条款10
typedef vector<Widget, SpecialAllocator<Widget> > 		WidgetContainer;
typedef WidgetContainer::iterator 						WCIterator;
WidgetContainer 										cw; // 仍然能用
Widget 													bestWidget;
...
WCIterator i = find(cw.begin(), cw.end(), bestWidget); // 仍然能用

d:
typedef并不能阻止用户使用（或依赖）任何他们不应该用的（或依赖的）。因此如果你不想暴露出用户对
你所决定使用的容器的类型，你需要更大的火力，那就是class。
class CustomerList {
private:
	typedef list<Customer> 				CustomerContainer;
	typedef CustomerContainer::iterator CCIterator;
	CustomerContainer 					customers;
public: // 通过这个接口
... // 限制list特殊信息的可见性
};

3、不要创建对象的容器，应该创建对象指针的容器
a:
当你从容器中获取一个对象时，你所得到的对象不是容器里的那个对象。而是对象的副本
当你向容器中添加一个对象（比如通过insert或push_back等），进入容器的是你指定的对象的拷贝。
这就是STL的方式。

b：
你可能会对所有这些拷贝是怎么完成的感兴趣？
解决：这很简单，一个对象通过使用它的拷贝成员函数来拷贝，特别是它的拷贝构造函数和它的拷贝赋值操作符
如：
class Widget {
public:
	...
	Widget(const Widget&); // 拷贝构造函数
	Widget& operator=(const Widget&); // 拷贝赋值操作符
	...
};
如果你自己没有声明这些函数，你的编译器始终会为你声明它们。（编译器生成的是const引用类型吗？？？）

c:
问题一：如果你用一个拷贝过程很昂贵对象填充一个容器，那么一个简单的操作——把对象放进容器也会被证明为是一个性能瓶颈.
问题二：以基类对象建立一个容器，而你试图插入派生类对象，那么当对象（通过基类的拷贝构造函数）拷入容器的时候对象的派生部分会被删除
如：
vector<Widget> 			vw;
class SpecialWidget:public Widget {...};
SpecialWidget 			sw;
vw.push_back(sw); // sw被当作基类对象拷

d:
一个使拷贝更高效、正确而且对分割问题免疫的简单的方式是建立指针的容器而不是对象的容器。
不幸的是，指针的容器有它们自己STL相关的头疼问题。

解决：
你想避免这些头疼并且仍要避开效率、正确性和分割问题，你可能会发现智能指针的容器是一个吸引人的选择。


4、用empty来代替检查size()是否为0
a:
事实上empty的典型实现是一个返回size是否返回0的内联函数。理由很简单：对于所有的标准容器，empty是一个常数时间的操作，但对于一
些list实现，size花费线性时间。

b:解释为什么list中size()可能是线性时间，而不是常数时间
list<int> list1;
list<int> list2;
...
list1.splice( 
	list1.end(), 
	list2, 
	find(list2.begin(), list2.end(), 5), 
	find(list2.rbegin(), list2.rend(), 10).base() 
			);
//把list2中从第一次出现5到最后一次出现10的所有节点移到list1的结尾。

设计方式一：
如果size是一个常数时间操作，当操作时每个list成员函数必须更新list的大小。也包括了splice。
让区间版本的splice更新它所更改的list大小的唯一的方法是算出接合进来的元素的个数，但那么做
就会使splice不可能有你所希望的常数时间的性能。

设计方式二：
如果你去掉了splice的区间形式要更新它所修改的list的大小的需求，splice就可以是常数时间，但size就变成线性时间的操作。

选择：
不同的list实现用不同的方式解决这个矛盾，依赖于他们的作者选择的是让size或splice的区间形式达到最高效率。

c：
不管发生了什么，如果你用empty来代替检查是否size() == 0，你都不会出错


5、能使用区间成员函数尽量使用区间成员函数，而不使用单成员函数
a:
如：区间赋值
方式一：
vector<Widget> v1, v2; // 假设v1和v2是Widget的vector
v1.clear();
for (vector<Widget>::const_iterator ci = v2.begin() + v2.size() / 2;ci != v2.end();++ci)
	v1.push_back(*ci);
分析：
有时候assign可以做的，但operator=做不了。
单元素成员函数比完成同样目的的区间成员函数需要更多地内存分配，更频繁地拷贝对象，而且/或者造成多余操作。


方式二：
v1.clear();
copy(v2.begin() + v2.size() / 2, v2.end(), back_inserter(v1));//实际上：在copy中存在一个循环
分析：
由于在copy中存在一个循环，故效率损失仍在，但比方式一要高
学习函数适配器：inserter，back_inserter或front_inserter

方式三：
v1.clear();
v1.insert(v1.end(), v2.begin() + v2.size() / 2, v2.end());

方式四：
v1.assign(v2.begin() + v2.size() / 2, v2.end());
分析：
● 一般来说使用区间成员函数可以输入更少的代码。
● 区间成员函数会导致代码更清晰更直接了当。效率高

b:
分析为什么区间成员函数比单成员函数效率高很多
单成员函数：
vector<int>::iterator insertLoc(v.begin());
for (int i = 0; i < numValues; ++i) {
	insertLoc = v.insert(insertLoc, data[i]);
	++insertLoc;
}

区间成员函数：
int data[numValues]; // 假设numValues在
vector<int> v;
...
v.insert(v.begin(), data, data + numValues); // 把data中的int

原因一：
把numValues个元素插入v，每次一个，自然会花费你numValues次调用insert。使用
insert的区间形式，你只要花费一次调用，节省了numValues-1次调用

原因二：
每次insert调用时每个只能向上移动一个位置，所以每个元素一共会被移动numValues
次。如果v在插入前有n个元素，则一共会发生n*numValues次移动。每次移动可能会归结
为一次memmove调用，但如果v容纳了用户自定义类型比如Widget，每次移动会导致调用那个类型的赋值操作符或者拷
贝构造函数。区间insert函数直接把现有元素移动到它们最后的位置，也就是，开销是每个元素一次移动。总共
开销是n次移动，numValues次容器中的对象类型的拷贝构造函数，剩下的是类型的赋值操作符。

原因三：
重复使用单元素插入而不是一个区间插入就必须处理内存分配，每次都可能带来内存重新分配的可能性，而区间成员函数只会带来一次

list中，每当一个元素添加到一个链表时，持有元素的链表节点必须有它的next和prev指针集，而且当然新节点前面的节点必须设置它的next指针，新节点后面的节点必须设置它的prev指针
但区间成员函数只会修改一次next和prev

c:
区间构造：
	标准序列容器和标准关联容器
	container::container(InputIterator begin, InputIterator end);

区间插入：
	标准序列容器
	void container::insert(iterator position, InputIterator begin, InputIterator end);
	标准关联容器
	void container::insert(lnputIterator begin, InputIterator end);

区间删除
	标准序列容器
	iterator container::erase(iterator begin, iterator end);
	标准关联容器
	void container::erase(iterator begin, iterator end);

区间赋值	
	标准序列容器和标准关联容器
	void container::assign(InputIterator begin, InputIterator end);


6、警惕C++最令人恼怒的解析（疑惑）
函数：
int f(double d);
int f(double (d));
int f(double);
指针函数：
int g(double (*pf)());
int g(double pf());
int g(double ());

分析：
为什么错了？
ifstream dataFile("ints.dat");
list<int> data(
	istream_iterator<int>(dataFile), 
	istream_iterator<int>()
			  );
解决：
list<int> data(
	(istream_iterator<int>(dataFile)), 
	istream_iterator<int>()
		      );
不幸的是，目前并非所有编译器都知道它。
更好方法：
ifstream dataFile("ints.dat");
istream_iterator<int> dataBegin(dataFile);
istream_iterator<int> dataEnd;
list<int> data(dataBegin, dataEnd);

7、new一个存放指针的容器时，在销毁容器之前应该delete那些指针，否则内存泄露
a:
当一个指针的容器被销毁时，会销毁它（那个容器）包含的每个元素，但指针的“析构函数”是
无操作！它肯定不会调用delete。
如：
void doSomething()
{
	vector<Widget*> vwp;
	for (int i = 0; i < SOME_MAGIC_NUMBER; ++i)
		vwp.push_back(new Widget);
	... // 使用vwp
} // Widgets在这里泄漏！

解决：
void doSomething()
{
vector<Widget*> vwp;
... // 同上
for (vector<Widget*>::iterator i = vwp.begin();i != vwp.end(),++i) {
		delete *i;
	}	
}
新问题：
	问题一：新的for循环代码比for_each多得多，但没有使用for_each来的清楚
	问题二：如果在用指针填充了vwp和你要删除它们之间抛出了一个异常，你会再次资源泄漏。

	解决一:for_each中需要函数对象	
	template<typename T>
	struct DeleteObject : // 条款40描述了为什么
	public unary_function<const T*, void> { // 这里有这个继承
	void operator()(const T* ptr) const
		{
			delete ptr;
		}
	};

	void doSomething()
	{
	... // 同上
	for_each(vwp.begin(), vwp.end(), DeleteObject<Widget>);
	}
	不幸的是，这让你指定了DeleteObject将会删除的对象的类型，有的人恶意地故意从string继承，怎么办
	class SpecialString: public string { ... };
	void doSomething()
	{
		deque<SpecialString*> dssp;
		...
		for_each(dssp.begin(), dssp.end(), DeleteObject<string>()); // 恶意写成string，而string没有虚析构函数
	}//但for_each循环的作者告诉DeleteObject它将删除string*指针,导致并没有调用基类的析构函数

	把类模板改成函数模板
	struct DeleteObject { // 删除这里的
	// 模板化和基类
	template<typename T> // 模板化加在这里
	void operator()(const T* ptr) const
		{
			delete ptr;
		}
	}
	解决二：
	最简单的可能是用智能指针的容器来代替指针的容器，典型的是引用计数指针Boost的shared_ptr
	void doSomething()
	{
	typedef boost::shared_ ptr<Widget> SPW; 
	vector<SPW> vwp;
	for (int i = 0; i < SOME_MAGIC_NUMBER; ++i)
		vwp.push_back(SPW(new Widget)); // 从一个Widget建立SPW,
	// 然后进行一次push_back
	... // 使用vwp
	} // 这里没有Widget泄漏，
注：不可以通过建立auto_ptr的容器来形成可以自动删除的指针。那是很可怕的想法，非常危险。

8、不能建立auto_ptr的容器
a:
auto_ptr的容器（COAPs）是禁止的。试图使用它们的代码都不能编译

b:为什么不能建立auto_ptr的容器
当你拷贝一个auto_ptr时，auto_ptr所指向对象的所有权被转移到拷贝的auto_ptr，而被拷贝的auto_ptr被设为
NULL。你正确地说一遍：拷贝一个auto_ptr将改变它的值：

	auto_ptr<Widget> pw1(new Widget); // pw1指向一个Widget
	auto_ptr<Widget> pw2(pw1); // pw2指向pw1的Widget;// pw1被设为NULL。（Widget的// 所有权从pw1转移到pw2。）
	pw1 = pw2; // pw1现在再次指向Widget；// pw2被设为NULL

c:分析建立auto_ptr的容器时，会发生什么错误
bool widgetAPCompare(const auto_ptr<Widget>& lhs,
const auto_ptr<Widget>& rhs) {
	return *lhs < *rhs; // 对于这个例子，假设Widget
} // 存在operator<

vector<auto_ptr<Widget> > widgets; // 建立一个vector，然后用Widget的auto_ptr填充它；记住这将不能编译！
sort(widgets.begin(), widgets.end(), widgetAPCompare);

分析sort函数的实现过程：
template<class RandomAccessIterator, // 这个sort的声明
class Compare> // 直接来自于标准
void sort(RandomAccessIterator first,RandomAccessIterator last,Compare comp)
{
	// 这个typedef在下面解释
	typedef typename iterator_traits<RandomAccessIterator>::value_type  ElementType;
	RandomAccessIterator i;
	... // 让i指向主元
	ElementType pivotValue(*); // 把主元拷贝到一个
	// 局部临时变量中；参见
	// 下面的讨论
	... // 做剩下的排序工作
}
因为它把一个元素从保存的区间拷贝到局部临时对象中。在我们的例子里，这个元素是一个
auto_ptr<Widget>，所以这个拷贝操作默默地把被拷贝的auto_ptr——vector中的那个——设为NULL。另外，
当pivotValue出了生存期，它会自动删除指向的Widget。这时sort调用返回了，vector的内容已经改变了，而且
至少一个Widget已经被删除了。也可能有几个vector元素已经被设为NULL，而且几个widget已经被删除，因
为快速排序是一种递归算法，递归的每一层都会拷贝一个主元。

9、删除容器的若干元素时，应该仔细选择其正确的成员函数
