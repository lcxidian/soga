1、顺序容器
		vector
		deque
		list
		foward_list(特殊)：不能对当前迭代器位置进行相应的操作(如：删除)，因为找到前驱比较费时
		array(特殊)：不能有改变容器大小的操作：添加、删除、resize

顺序容器————为了提供了快速顺序访问的
同时也付出了添加和删除的代价(vector) 或 非顺序访问的代价(list,forward_list)
注：deque能够在两端快速的添加和删除元素，它是一种复杂的数据结构
2、选择容器类型的原则

3、顺序容器所提供的基本操作：
#类型别名
	iterator
	const_iterator
	size_type
	difference_type
	value_type
	reference
	const_reference
#构造函数
	vector<int> v;
	vector<int> v(v2);
	vector<int> v = v2;
	vector<int> v(iter1,iter2); #除array
	vector<int> v{1,2,3,4};
	vector<int> v = {1,2,3,4};
	vector<int> v(n);
	vector<int> v(n,10);
		#array 与其他容器不容，array一开始就不是为空的大小
		array<int,10> a;
		注：内置数组不支持拷贝和赋值，但array可以做到
		int digs[10] = {0,1,2,3,4,5,6,7,8,9};
		int cpy[10] = digs; # error: no copy or assignment for built-in arrays
		array<int, 10> digits = {0,1,2,3,4,5,6,7,8,9};#这是初始化，并没有改变其容器的大小
		array<int, 10> copy = digits; # ok: so long as array types match		

		易错：array是支持赋值操作的，但必须满足类型相同，大小也相同才可以赋值
		    array<int,10> a;
		    array<int,9> b;
		    a = b;#编译不过

		    array<int,10> a;
		    array<int,10> b;
		    a = b;#编译通过
		易错：
		    array<int,10> a;
		    a = {10};	#正确
		    for(auto item : a)
		        cout<<item<<endl;
		    return 0;
		    输出结果:10,0,0,0,0,0,0,0,0,0,0
#赋值和swap
	v1 = v2;#array必须满足类型和大小都相同才可以，其他顺序容器满足类型相同即可
	v1 = {1,2,3,4};
	v.swap(v2);
	swap(v,v2);

#大小
	v.size();
	c.max_size();
	c.empty();
#添加和删除
	v.insert(args);
	c.emplace(inits);
	v.erase(args);
	v.clear();
#获取迭代器
	v.begin();v.end();
	v.cbegin();v.cend();
#支持反向容器的额外成员(除forward_list外)
	reverse_iterator
	const_reverse_iterator
	c.rbegin();c.rend();
	c.crbegin();c.crend();

############################################################################################################

4、顺序容器中还可以这样赋值：assign(替换容器中原来所有的元素)   #除array外
	v.assign(iter1,iter2);
	v.assign({初始化列表})
	v.assign(n,元素)

5、swap特别说明
除arrayy以为，顺序容器的swap效率特别高：只交换了两个容器内部的数据结构，而不改变数据的位置
因此，swap操作以后，容器的迭代器、引用、指针都还未失效

swap两个array容器对象时，是真正交换它们的元素，所有效率不高。

6、容器的关系运算符使用其内部元素的关系运算符比较。若元素的关系运算符没有定义，则容器的关系运算符就不能使用

7、顺序容器添加元素还可以这样：但并不是以下每个操作都有效，可能是部分有效 #除array外，且 forward_list有自己版本的insert和emplace
	c.push_front(t)
	c.push_back(t)
	c.emplace_front(args)
	c.emplace_back(t)
	c.emplace(iter,args)
	c.insert(iter,t)
	c.insert(iter,n,t)
	c.insert(iter,iter1,iter2)
	c.insert(iter,{初始化列表})
注：emplace_back操作是利用初始化参数args直接在内存中创建新元素
	push_back操作而是先创建一个临时对象，在将其压入容器中
8、顺序容器删除元素还可以这样：但并不是以下每个操作都有效，可能是部分有效 #除array外，且forward_list有自己版本的erase
	c.pop_front()
	c.pop_back()
	c.erase(iter)
	c.erase(iter1,iter2)
	c.clear()

9、顺序容器还有front和back操作，#除forward_list没有back操作之外
front()————返回首元素的引用
back()————返回尾元素的引用
at()————返回下标元素的引用，自动检查是否越界
[]————返回下标元素的引用，不检查越界

10、特殊容器forward_list
特殊在于单链表无法简单的获取前驱节点的迭代器，故无法在本节点之前进行插入或删除操作，只能在本节点之后进行
因此forward_list并未定义insert、emplace、erase，而是定义了insert_back、emplace_back、erase_after操作，为了支持完整的支持这些操作，定义一个“首前迭代器”。
这个迭代器可以在首元素之前并不存在的元素之后插入或删除元素
	flist.before_begin() #获取首前元素的迭代器
	flist.cbegin_begin()
	flist.insert_after(iter,t)
	flist.insert_after(iter,n,t)
	flist.insert_after(iter,iter1,iter2)
	flist.insert_after(iter,{初始化列表})
	emplace_after(iter,args)
	flist.erase_after(iter)
	flist.erase_after(iter1,iter2)
11、改变容器的大小，#除array外
v.resize() #缩小容器的size()，但容器的conpacity并没有改变

12、容器的某些操作可能会使迭代器，引用，指针失效
添加操作——vector，string的存储空间被重新分配，因此迭代器，引用，指针失效
		  list、forward_list容器的迭代器，引用，指针仍然有效
删除操作——vector，string的存储空间被重新分配，被删除元素之前的迭代器，引用，指针仍有效
		  list、forward_list容器的迭代器，引用，指针仍然有效

13、容器大小
v.begin()-------v.size(),v.end()--------------v.capacity()
	v.shrink_to_fit()
	v.size()
	v.capacity()
	v.resize() #更改size
	v.reserve(n) #更改capacity
==========================================================	
14、string
注：string除了可以使用顺序容器那些共同的操作之外，还有一些量身定制的操作
#即string使用顺序容器通用的那些操作之外，还有它自己特有的操作
string的其他构造函数：
	string str(chr,n)
	string str(str2,pos)
	string str(str2,pos,len)

15、string的substr操作
	str.substr(pos,n=0)
16、string自己版本的insert和erase，当然，它也接受顺序容器的insert和erase
	str.insert(pos,n,'a')
	str.erase(pos,n)
17、string特有的两个操作：append和replace
	str.append("abc")
	str.replace(pos1,pos2,"instead")
18、修改string的操作
	str.insert(pos,args)
	str.erase(pos,len)
	str.assign(args)
	str.append(args)
	str.replace(pos1,pos2,args)

args可以是以下形式：
					str
					str,pos,len
					chr,len
					chr
					n,'a'
					iter1,iter2
					初始化列表
18、string提供6个搜索函数，每个函数进行了4次重载
str.find(args)					#查找args第一次出现的位置
str.rfind(args)					#查找args最后一次出现的位置
str.find_first_of(args)			#查找args中任何一个字符在str中第一次出现的位置
str.find_last_of(args)			#查找args中任何一个字符在str中最后一次出现的位置
str.find_first_not_of(args)		#查找第一不在args中的字符
str.find_last_not_of(args)		#查找最后一个不在args中的字符

args必须是以下形式之一：
c,pos
s2,pos
chr,pos 	 #chr为字符数组指针
chr,pos,n

19、string的compare操作
20、数值转换
	to_string(val)
	stoi(s,p,b)
	stl(s,p,b)
	stul(s,p,b)
	stll(s,p,b)
	stull(s,p,b)
	stof(s,p)
	stod(s,p)
	stold(s,p)
21、容器适配器 stack、queue、priority_queue

22、迭代器之间的比较用 ==，而不要用>或<，因为有的容器并不适合
注：list容器的迭代器不能用<或>来比较
如：
list<int> lst1;
list<int>::iterator iter1 = lst1.begin(),
iter2 = lst1.end();
while (iter1 < iter2) /* ... */ #错误
23、const容器对象，其begin()和end()的返回值是const_iterator类型，而不是iterator类型
vector<int> v1;
const vector<int> v2;
auto it1 = v1.begin(),  it2 = v2.begin();#易错
auto it3 = v1.cbegin(), it4 = v2.cbegin();
	#`it1` is `vector<int>::iterator`
	#`it2`,`it3` and `it4` are `vector<int>::const_iterator`

24、一个类型的容器如何初始化另一个类型不同的容器
如：
list<string> names;
vector<const char*> oldstyle;
names = oldstyle; # 错误
names.assign(oldstyle.cbegin(), oldstyle.cend());#正确

25、空容器
    vector<int> v;
    v.front() = 10;#执行出错，因为空容器没有元素，则无法返回

26、error: error: 'stoi' is not a member of 'std'|
The C++11 string conversion functions (to_string, stoi, stol, etc.) don't work in MinGW 
(which is what comes with Code::Blocks by default).
解决办法：
http://www.cplusplus.com/forum/beginner/120836/