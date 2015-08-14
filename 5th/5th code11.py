1、关联容器
#按关键字顺序存储
map #关键字唯一，按严格弱序存放
set #关键字唯一，按严格弱序存放
multimap #允许有多个相同关键字，且相邻存放
multiset #允许有多个相同关键字，且相邻存放

#不再按关键字顺序
unordered_map #关键字唯一，乱序存放
unordered_set #关键字唯一，乱序存放
unordered_multimap #允许有多个相同关键字，乱序存放
unordered_multiset #允许有多个相同关键字，乱序存放
2、定义关联容器
如：
map<string, size_t> word_count; // empty
set<string> exclude = {"the", "but", "and", "or", "an", "a",
						"The", "But", "And", "Or", "An", "A"};
map<string, string> authors = { {"Joyce", "James"},
								{"Austen", "Jane"},
								{"Dickens", "Charles"} };
3、有序关联容器(map，set，multimap，multiset)必须定义元素比较的方法，因为关键字是按序存放的
	默认是使用关键字类型<运算符，因此关键字类型必须要定义<运算符才行
如：
multiset<Sales_data> bookstore;#错误
改正：
bool compareIsbn(const Sales_data &lhs, const Sales_data &rhs)
{
	return lhs.isbn() < rhs.isbn();
}
multiset<Sales_data, decltype(compareIsbn)*>
						bookstore(compareIsbn);#用compareIsbn来初始化bookstore对象，表示当我们向容器添加新元素时，按这种方式进行关键字排序

4、弄清pair和map的关系
map是容器，而pair是map容器中元素的数据类型

pair的两个数据成员是public的：分别命名为first和second
如：
pair<string, string> anon; // holds two strings
pair<string, size_t> word_count; // holds a string and an size_t
pair<string, vector<int>> line;
pair<string, string> author{"James", "Joyce"};
cout << w.first << " occurs " << w.second
	<< ((w.second > 1) ? " times" : " time") << endl;

pair提供的操作：
	pair<T1,T2> p;
	pair<T1,T2> p(v1,v2);
	pair<T1,T2> p = {v1,v2};
	make_pair(v1,v2);#生成一个pair对象
	p.first;
	p.second
	p1 == p2
	p1 != p2

5、关联容器的元素数据类型
key_type #关键字的数据类型
mapped_type #关联值的数据类型
value_type #对set来时，是关键字的数据类型
		   #对map来时，是pair<const key_tye,mapped_type>数据类型
如：
set<string>::value_type v1; // v1 is a string
set<string>::key_type v2; // v2 is a string
map<string, int>::value_type v3; // v3 is a pair<const string, int>
map<string, int>::key_type v4; // v4 is a string
map<string, int>::mapped_type v5; // v5 is an int

#注：由以上可知，map容器的关键字类型是const的，故不能更改其关键字的值，只能删除
即map容器的元素是一个pair类型，其first成员是const的
如：
auto map_it = word_count.begin();
cout << map_it->first; 
cout << " " << map_it->second;
map_it->first = "new key"; #错误
++map_it->second; 
6、关联容器的迭代器
# map中的关键字类型是const的，set中关键字类型也是const的
即便set中有两种迭代器:iterator和const_iterator，但都是只能读，不能写
如：
set<int> iset = {0,1,2,3,4,5,6,7,8,9};
set<int>::iterator set_it = iset.begin();
if (set_it != iset.end()) {
	*set_it = 42; #错误
	cout << *set_it << endl; // ok: can read the key
}
8、由于map和set中关键字类型都是const的，所以大多泛型算法都不支持关联容器

9、添加新元素
操作：
	c.insert(v)
	c.emplace(args)
	c.insert(iter1,iter2)
	c.insert({列表})
	c.insert(iter,v)
	c.emplace(iter,args)

#insert和emplace返回值：
对不可重复的容器(set、map)来说，insert(emplace)返回一个pair类型， 其first是一个迭代器，指向关键字，
																	second是bool类型，反应插入是否成功
如：
map<string, size_t> word_count; 
while (cin >> word) {
	auto ret = word_count.insert({word, 1});
	if (!ret.second) 
		++ret.first->second; 
}
对于可重复的容器(multiset、multimap)来说，insert(emplace)返回一个迭代器，指向其刚插入的这个新元素
如：
multimap<string, string> authors;
authors.insert({"Barth, John", "Sot-Weed Factor"});
authors.insert({"Barth, John", "Lost in the Funhouse"});

set
vector<int> ivec = {2,4,6,8,2,4,6,8}; // ivec has eight elements
set<int> set2; // empty set
set2.insert(ivec.cbegin(), ivec.cend()); // set2 has four elements
set2.insert({1,3,5,7,1,3,5,7}); // set2 now has eight elements

map
记住，map.insert操作时，由于map的元素类型是pair类型，因此需要构造pair对象才行
// four ways to add word to word_count
word_count.insert({word, 1});
word_count.insert(make_pair(word, 1));#推荐
word_count.insert(pair<string, size_t>(word, 1));
word_count.insert(map<string, size_t>::value_type(word, 1));

10、删除元素
关联容器有三个版本的erase：
	c.erase(key)
	c.erase(iter)
	c.erase(iter1,iter2)
当删除不可重复容器的元素，erase返回0或1
当删除可重复容器的元素，erase返回删除个数

11、map的[] 和 at()
map和unorder_map都要此操作，但[]可能会添加新元素，当关键字不在容器时，[]会向容器中添加该关键字
map <string, size_t> word_count; // empty map
word_count["Anna"] = 1;
注：由于multimap和unorder_multimap中同一个关键字关联多个值，所以[]和at不可能支持它们

12、查找操作
c.find(key)
c.count(key)
c.lower_bound(key) //返回一个迭代器，指向第一个不小于k的元素
c.upper_bound(key) //返回一个迭代器，指向第一个不大于k的元素
c.equal_range(key) //返回一个pair迭代器，指向一个等于k的范围
如：
string search_item("Alain de Botton"); 
auto entries = authors.count(search_item); // number of elements
auto iter = authors.find(search_item); // first entry for this author
while(entries) {
	cout << iter->second << endl; // print each title
	++iter; // advance to the next title
	--entries; 
}
如：
for (auto beg = authors.lower_bound(search_item),
			end = authors.upper_bound(search_item);
			beg != end; ++beg)
	cout << beg->second << endl; // print each title
如：
for (auto pos = authors.equal_range(search_item);
		pos.first != pos.second; ++pos.first)
		cout << pos.first->second << endl; // print each title
#以上十几条基本都是有序关联容器的操作
13、无序关联容器
无序容器不是使用比较运算符来组织元素，而是使用hash函数来组织元素的
注：除了提供hash操作之外，还提供与有序容器相同的操作
桶接口：
桶迭代：
哈希策略：


14、大小写转换函数：
	---用C语言标准库函数toupper,tolower(只能通过依次转换字符来完成)
	---用C++语言标准库函数_strlwr_s, _strupr_s (形参必须是char*)
	---string 没有提供大小写转换的功能，所以只能用STL中的transform结合toupper/tolower完成。
	---boost库中string_algorithm 提供了大小写转换函数to_lower 和 to_upper

transform函数是：将某操作应用于指定范围的每个元素。
	transform(first,last,result,op);//first是容器的首迭代器，last为容器的末迭代器，result为存放结果的容器，op为要进行操作的一元函数对象或sturct、class。
	transform(first1,last1,first2,result,binary_op);//first1是第一个容器的首迭代器，last1为第一个容器的末迭代器，first2为第二个容器的首迭代器，result为存放结果的容器，binary_op为要进行操作的二元函数对象或sturct、class。

15、multimap中，find和count经常结合使用
    std::multimap<string, string> authors{
        {"alan", "DMA"},
        {"pezy", "LeetCode"},
        {"alan", "CLRS"},
        {"wang", "FTP"},
        {"pezy", "CP5"},
        {"wang", "CPP-Concurrency"}
    };
    // want to delete an element that author is [Alan], work is [112].
    string author = "pezy";
    string work = "CP5";
    
    auto found = authors.find(author);
    auto count = authors.count(author);
    while (count) { #有效的控制迭代次数
        if (found->second == work) {
            authors.erase(found);
            break;   
        }
        ++found;
        --count;
    }
