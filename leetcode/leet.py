1、size_t
size_t 类型定义在cstddef头文件中，该文件是C标准库的头文件stddef.h的C++版。它是一个与机器相关的unsigned类型，其大小足以保证存储内存中对象的大小。
例如：bitset的size操作返回bitset对象中二进制位中的个数，返回值类型是size_t。
例如：在用下标访问元素时，vector使用vector::size_type作为下标类型，而数组下标的正确类型则是size_t。vector使用的下标实际也是size_t，源码是typedef size_t size_type。
2、size_type
由string类类型和vector类类型定义的类型，用以保存任意string对象或vector对象的长度，标准库类型将size_type定义为unsigned类型

#总结：在搞不清区别的情况下，用size_t好一些

3、std::next 和 std::pre
	std::next（英文原版）
template< class ForwardIt >	ForwardIt next( ForwardIt it, 
                       						typename std::iterator_traits<ForwardIt>::difference_type n = 1 );
	Parameters
	   it  -- 迭代指针
	   n  -- 向前进的元素个数，缺省默认为1
	Return value
		The nth successor of iterator it.（返回it的第n个后继迭代指针）
内部实现：
template<class ForwardIt>
ForwardIt next(ForwardIt it, typename std::iterator_traits<ForwardIt>::difference_type n = 1)
{
    std::advance(it, n);
    return it;
}

    std::prev（英文原版）
使用方法与next相似，不同的是prev返回的是it的第n个前驱迭代指针
template< class BidirIt > BidirIt prev( BidirIt it, 
										typename std::iterator_traits<BidirIt>::difference_type n = 1 );
内部实现：
template<class BidirIt>
BidirIt prev(BidirIt it, typename std::iterator_traits<BidirIt>::difference_type n = 1)
{
    std::advance(it, -n);
    return it;
}

4、
　　ForwardIter lower_bound(ForwardIter first, ForwardIter last,const _Tp& val)算法
		返回一个非递减序列[first, last)中的第一个大于等于值val的位置。
    ForwardIter upper_bound(ForwardIter first, ForwardIter last, const _Tp& val)算法
    	返回一个非递减序列[first, last)中第一个大于val的位置。
如：upper_bound(first,last,4)
1 		2 		2 		3 		4 		4 		4 		4 		5 		6 		7 		8 		9
^								^								^
first					lower_bound(first,last,4)		upper_bound(first,last,4)

5、
初始化一个vector<vector<int>> vv;
vv的第一层容器还没有分配空间，vv的第二层容器也没有分配空间
6、大端小端模式
首先清楚高字节和低字节，还有高地址和低地址
#高低字节：
0X 12 34 56 78
高字节      低字节

#高低地址：
高地址位    低地址位

大端模式：正好相反
78 56 34 12
小端模式：
12 34 56 78

附上程序内存结构图：
					_______________________ 最高内存地址 0xffffffff
					栈底
					栈
					栈顶
					_______________________

					NULL (空洞)
					_______________________
					堆
					_______________________
					未初始 化的数据
					_______________________ 统称数据段
					初始化的数据
					_______________________
					正 文段(代码段)
					_______________________ 最低内存地址 0x00000000

7、内存对齐原则

8、size_t在64位系统下是64位的
9、正数的上溢出overflow，没有判断负数的下溢出underflow
10、
11、
12、
13、
14、
15、
16、
17、
18、
19、
20、

