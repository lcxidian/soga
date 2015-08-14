1、tuple————类似于pair类型		
tuple操作：							
	tuple<T1,T2,...Tn> 	t;				 #未初始化的tuple对象
	tuple<T1,T2,...Tn> t(v1,v2,...vn);	 #初始化的tuple对象
	make_tuple(v1,v2,...vn);			 #生成一个匿名tuple对象	
	t1 == t2;							 	
	t1 != t2;								
	t1 relop t2;								
	get<i>(t)							 #tuple对象的第i个引用	
	tuple_size<TupleType>::value		 #特定的类模板tuple_size来获取 tuple的成员个数
	tuple_element<i,TupleType>::type	 #特定的类模板tuple_element来获取 tuple对象的第i个成员的类型		
应用：
#生成tuple对象
	tuple<size_t,size_t, size_t> threeD; 
	tuple<string, vector<double>, int, list<int>> someVal("constants", {3.14, 2.718}, 42, {0,1,2,3,4,5});
	tuple<size_t, size_t, size_t> threeD{1,2,3};      // ok
	tuple<size_t, size_t, size_t> threeD =  {1,2,3};  // 错误，tuple构造函数是explicit的
#生成匿名的tuple对象
	auto item = make_tuple("0-999-78345-X", 3, 20.00);
#获取tuple对象的第i个成员的值
	auto book = get<0>(item);      // returns the first member of item
	auto cnt = get<1>(item);       // returns the second member of item
	auto price = get<2>(item)/cnt; // returns the last member of item
	get<2>(item) *= 0.8;  
#获取tuple对象的成员个数，或某个成员的数据类型
	typedef decltype(item) trans; // trans is the type of item
	size_t sz = tuple_size<trans>::value;  // returns 3
	tuple_element<1, trans>::type cnt = get<1>(item); // cnt is an int
#关系运算符
	tuple<string, string> duo("1", "2");
	tuple<size_t, size_t> twoD(1, 2);
	bool b = (duo == twoD); // error: can't compare a size_t and a string
	tuple<size_t, size_t, size_t> threeD(1, 2, 3);
	b = (twoD < threeD);    // error: differing number of members
	tuple<size_t, size_t> origin(0, 0);
	b = (origin < twoD);    // ok: b is true

typedef tuple<vector<Sales_data>::size_type,
              vector<Sales_data>::const_iterator,
              vector<Sales_data>::const_iterator> matches;
2、bitset————处理二进制集合的类
bitset操作：
	bitset<n> b;
	bitset<n> b(u);
	bitset<n> b(str,pos,len,zero,one);#zero,one表示str中字符必须是zero或one，否则编译器报错
	bitset<n> b(c,pos,len,zero,one);
	b.any()
	b.all()
	b.none()
	b.count()
	b.size()
	b.test(pos)
	b.set(pos,v)
	b.set()
	b.reset(pos)
	b.reset()
	b.flip(pos)
	b.flip()
	b[pos]
	b.to_ulong()
	b.to_ullong()
	b.to_string(zero,one)
	os<<b
	is>>b
3、正则表达式
两步：熟悉正则表达式和会使用以下操作
regex			#regex类
regex_match		#将字符串与正则式进行匹配
regex_search	#寻找第一个与正则式匹配的子序列
regex_replace	#用指定的字符串去替换与正则式匹配的子串
sregex_iterator #用来遍历regex_search匹配的所有子串
smatch			#容器类，存放搜索结果
ssub_match		#string中匹配的子表达式的结果
4、随机数
随机数引擎类default_random_engine
分布类模板uniform_int_distribution<T>


