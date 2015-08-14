1、泛型算法————特别之处在于使用迭代器做形参，便于可以用于不同类型的元素和多种容器

2、迭代器令算法不依赖与容器，但依赖容器的元素类型的操作

3、泛型算法可改变容器的值，可以在容器中移动元素，但不会改变底层容器的大小，保持通用性

4、STL算法的三个头文件：
	#include<algorithm>
	#include<numeric>
	#include<functional>
5、算法分类
质变算法————会改变操作对象之值：#拷贝copy、互换swap、替换replace、填写fill、排序sort、删除remove、分割partition、随机重排random shuffing
注：质变算法通常提供两个版本：
				一个是in-place版，#就地改变其操作对象
				另一个是copy版，以_copy结尾，#将操作对象复制一份副本，再在副本上进行修改，并返回副本

非质变算法————不改变操作对象之值：#查找find、匹配search、计数count、巡防for_each、比较equal、寻找极值max min

#注：许多算法不止支持一个版本：缺省行为版本，还提供一个版本：提供额外参数版本，该参数是仿函数类型（函数对象）
如：
unique unique
find  	find_if
replace	replace_if
6、find算法
#include <algorithm>
iterator find( iterator start, iterator end, const TYPE& val );

6、非质变函数：accumulate，equal
#include <numeric>
  TYPE accumulate( iterator start, iterator end, TYPE val );
  TYPE accumulate( iterator start, iterator end, TYPE val, BinaryFunction f );
注：如果第三个参数不能是字面值类型，因为字面值类型是const，导致无法进行写操作
string sum = accumulate(v.cbegin(), v.cend(), "");#错误
改正：
string sum = accumulate(v.cbegin(), v.cend(), string(""));
7、写容器算法（不一定都是质变算法）
特别注意：算法不会检查写操作
 #include <algorithm>
#void fill( iterator start, iterator end, const TYPE& val );
	fill(vec.begin(), vec.begin() + vec.size()/2, 10);

#iterator fill_n( iterator start, size_t n, const TYPE& val );
	vector<int> vec; // empty vector
	fill_n(vec.begin(), vec.size(), 0); #错误，vec并没有分配空间
	改正：
	vector<int> vec; // empty vector
	fill_n(back_inserter(vec), 10, 0);#back_iterator返回一个插入迭代器，该插入迭代器在容器尾部插入新元素（包括分配空间），类似于emplace函数

#iterator copy( iterator start, iterator end, iterator dest );
	int a1[] = {0,1,2,3,4,5,6,7,8,9};
	int a2[sizeof(a1)/sizeof(*a1)]; // a2 has the same size as a1
	auto ret = copy(begin(a1), end(a1), a2);

#iterator copy_n( iterator from, size_t num, iterator to );

#void replace( iterator start, iterator end, const TYPE& old_value, const TYPE& new_value );
	replace(ilst.begin(), ilst.end(), 0, 42);

#iterator replace_copy( iterator start, iterator end, iterator result, const TYPE& old_value, const TYPE& new_value );
	vector<int> ivec; // empty vector
	replace_copy(ilst.cbegin(), ilst.cend(), back_inserter(ivec), 0, 42);
8、重排算法
void sort( iterator start, iterator end );
void sort( iterator start, iterator end, StrictWeakOrdering cmp );

iterator unique( iterator start, iterator end );
iterator unique( iterator start, iterator end, BinPred p );

iterator unique_copy( iterator start, iterator end, iterator result );
iterator unique_copy( iterator start, iterator end, iterator result, BinPred p );


9、向算法传递 函数
bool isShorter(const string &s1, const string &s2){
	return s1.size() < s2.size();
}
sort(words.begin(), words.end(), isShorter);

注：还有一种稳定排序：
	stable_sort(words.begin(), words.end(), isShorter);

10、尾置返回类型
任何函数都可以使用尾置返回类型，即返回类型不再是函数名前面，而是在函数参数列表后面
形式：auto func(参数列表) -> 返回值类型
auto func(int i) -> int(*)[10] #func函数返回一个数组指针

11、lambba表达式（重要）
由于标准库算法只能接受一元谓词和二元谓词，有的算法只能接受一元谓词：find_if
但我们可以向算法传递 可调用对象
可调用对象——————函数
				函数指针
				函数对象（即重载函数调用运算符的类）
				lambba
lambba形式：[捕获列表] (参数列表) -> return 返回值类型 { .... }
#注：参数列表和return 返回值类型可以不写
捕获列表为空，代表在函数体内没有任何局部变量
如：
a
	auto f = [] { return 42; };
	cout << f() << endl; // prints 42
b
	[](const string &a, const string &b)
		{ return a.size() < b.size();}
	使用：
	// sort words by size, but maintain alphabetical order for words of the same size
	stable_sort(words.begin(), words.end(),
						[](const string &a, const string &b)
						{ return a.size() < b.size();});
c
	auto wc = find_if(words.begin(), words.end(),
					[sz](const string &a)#一元谓词
					{ return a.size() >= sz; });

捕获列表可以是值拷贝，也可以是引用
#注：值拷贝是在lambba创建的发生，而不运行的时候
如：
值拷贝：
void fcn1()
{
	size_t v1 = 42; // local variable
	auto f = [v1] { return v1; };#值拷贝
	v1 = 0;
	auto j = f(); // j is 42; f stored a copy of v1 when we created it
}

值引用：
void fcn2()
{
	size_t v1 = 42; // local variable
	auto f2 = [&v1] { return v1; };#值引用
	v1 = 0;
	auto j = f2(); // j is 0; f2 refers to v1; it doesn't store it
}
#注：有的时候，不能进行值拷贝：如IO对象
如：
void biggies(vector<string> &words,vector<string>::size_type sz,
							ostream &os = cout, char c = ' ')
{
	for_each(words.begin(), words.end(),
							[&os, c](const string &s) 
							{ os << s << c; });
}
分析：当定义个lambba时，编译器生成一个与lambba相对应的新类型和该类型的匿名对象
		auto定义了一个从lambba生成的类类型的对象。

隐式捕获：
	[]				#空捕获列表
	[=]				#隐式值拷贝，自动推断其局部变量
	[&]				#隐式值引用
	[捕获列表]		#值拷贝	
	[&捕获列表]		#值引用

返回值类型：
	若函数体只有一个return语句，则返回值类型可以不写，编译器自动推断
12、for_each算法
UnaryFunction for_each( iterator start, iterator end, UnaryFunction f );

如：
for_each(wc, words.end(),[](const string &s){cout << s << " ";});
	cout << endl;

13、参数绑定
如果很多地方都要使用相同的操作，应该定一个函数，而不是多次编写相同的lambba表达式，但标准库算法最多接受二元谓词，
解决办法：bind函数将可调用对象（函数、函数指针、函数对象、lambba）变成一个新的可调用对象，目的是缩小参数个数

bind函数形式：auto newCallable = bind(callable, arg_list);
如： 
bool check_size(const string &s, string::size_type sz)
{
	return s.size() >= sz;
}
auto check6 = bind(check_size, _1, 6);
string s = "hello";
bool b1 = check6(s);
如： 
auto wc = find_if(words.begin(), words.end(),
							bind(check_size, _1, sz));
14、名字_n定义在std::placeholders命名空间中，因此：
	using namespace std::placeholders;

参数绑定bind的参数列表：
那些不是占位符的参数默认是值拷贝方式传递，但有时有的参数不能进行值拷贝：IO对象
ostream &print(ostream &os, const string &s, char c)
{
	return os << s << c;
}
for_each(words.begin(), words.end(), bind(print, os, _1, ' '));#错误
改正： 
for_each(words.begin(), words.end(),
						bind(print, ref(os), _1, ' '));#ref函数生成其引用，cref函数生成其const引用


15、其他迭代器

插入迭代器————向容器插入元素(自己分配空间并初始化)
	back_inserter(容器对象)————创建一个使用push_back的迭代器 # 总是在容器的首元素之后插入元素     常用
	front_inserter(容器对象)————创建一个使用push_front的迭代器 #总是在容器的首元素之前插入元素
	inserter(容器对象，iter)——————————创建一个使用insert的迭代器 #在指定位置iter之前插入元素
注：只有支持push_front的容器才能有front_inserter操作，如：vector就没有push_front，因此vector容器不能用front_inserter算法
	只有支持push_front的容器才能有back_inserter操作，如：
如： 
list<int> 1st = {1,2,3,4};
list<int> lst2, lst3; // empty lists
copy(1st.cbegin(), lst.cend(), front_inserter(lst2));
copy(1st.cbegin(), lst.cend(), inserter(lst3, lst3.begin()));

流迭代器——————被绑定到输入输出流上，用来遍历相关的IO流
特别注意：流迭代器没有属于哪一个容器，它就和流对象绑定在一起，像使用流对象那样使用流迭代器

如： 
istream_iterator<int> in_iter(cin); 
istream_iterator<int> eof; 
while (in_iter != eof) 
		vec.push_back(*in_iter++);
反向迭代器————除了forward_list外，都有
	reverse_iterator
	const_reverse_iterator
移动迭代器————不能用来拷贝其元素，只能用于移动

16、迭代器的分类
	输入迭代器
	输出迭代器
	前向迭代器
	双向迭代器
	随机双向迭代器

17、list和forward_list特有的容器算法
	lst.merge(lst2)
	lst.merge(lst2,comp)
	lst.remove()
	lst.remove_if(pred)
	lst.reverse()
	lst.sort()
	lst.sort(comp)
	lst.unique()
	lst.unique(pred)

	lst.splice(iter,lst2)
	lst.splice(iter1,lst2,iter2)
	lst.splice(iter,lst2,iter1,iter2)

	lst.splice_after(iter,lst2) #ctr+x的功能
	lst.splice_after(iter1,lst2,iter2)
	lst.splice_after(iter,lst2,iter1,iter2)
18、
    vector<int> v;
    v.reserve(10);
    fill_n(v.begin(), 10, 0);#有容量，但size()为0,
    // ^ (b)No error, but not any sense. v.size() still equal zero.
    改正：
    // Fixed: 1. use `v.resize(10);`
    //    or  2. use `fill_n(std::back_inserter(v), 10, 0)
19、unique算法必须在sort算法之后才能使用，即使用unique算法的前提条件是有序

20、容易疑惑的地方
    vector<int> v1,v2,v3;
    vector<int> v{1,2,3,4,5,6,7,8,9};
    copy(v.begin(),v.end(),inserter(v3,v3.begin()));

结果是1,2,3,4,5,6,7,8,9，而不预想的9,8,7,6,5,4,3,2,1
why:
inserter算法调用容器的insert成员函数：
iterator insert( iterator loc, const TYPE& val );
# inserts val before loc, returning an iterator to the element inserted













































