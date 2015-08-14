2015-7-24
#基础算法：
快排：
归并：
二分查找：

整理针对数组和容器的排序算法和查找算法
一、内容
	线性表：23+10
	字符串：15
	栈、队列：3

    （8-1,8-2,8-3）
	树：10+2+5+7
    （8-4）
	排序：5
	查找：3
	枚举：6
    （8-5,8-6）
	广度优先搜索：3
	深度优先搜索：11
    (8-7)
    
	分治法：2
	贪心：6
    (8-8，8-9)
	动态规划：13
	图：1
    (8-10，8-11，8-12)
	细节：15

二、模板
	题意：
	输入： 
	输出： 
	思路：
	时间复杂度： 
	代码：
三、
	声明： 	能递归则一定不用栈；能用STL 则一定不自己实现。
			不需要检查malloc()/new 返回的指针是否为nullptr；不需要检查内部函数入口参数的有效性。
	手写算法和机试的不同：
	手写算法可改性不灵活，这就要求对算法一定要熟练再熟练，一次性算法可用
	手写算法很难验证正确性和极端情况

#1、删除有序数组中重复的元素
输入：3、3、3、7、7、7、7、9、11、23、23、37
输出：3、7、9、11、23、37
思路：i保持后续元素能找到应该插入的位置：i+1
	  count很重要，记录有多少重复的元素，以便最后把元素长度更新
	  j每次都去尝试是否元素重复，且很巧妙的借助了i的”新值“
时间复杂度：O(n)
#Code:
using index = size_t;
size_t del_duplicates(int array[],size_t size)
{
	index i = 0;
	unsigned int count = 0;
	size_t max_size = size;
	for(index j = 1;j < max_size;j++)
	{
		if(array[i] == array[j])
		{
			count++;
		}else{
			array[++i] = array[j];#只有在插入新值才才更新i，i在刚插入新元素的那个位置
		}
	}
	return size - (size_t)count;
}
int main()
{
    int a[] = {3,3,3,7,7,7,7,9,11,23,23,37};
    int len = del_duplicates(a,12);
    cout<<len<<endl;
    cout<<endl;
    for(auto &item:a)
        cout<<item<<" ";
    cout<<endl;
    return 0;
}

#2、删除有序数组中重复的元素，但可以允许重复次数不超过2次
输入：3、3、3、7、7、7、7、9、11、23、23、37
输出：3、3、7、7、9、11、23、23、37
思路：本题写一个通用的版本：删除有序数组中的重复元素，但允许可重复的次数为times次
	用一个局部变量n来保存元素已经重复的次数，初始值为1，即该元素只出现了一次，在适当的时候重n的值
	用i来保证新元素该插入的位置：i+1,即a[++i] = a[j]
	用j遍历每一个元素，每次都拿来与i的值做比较，会出现以下情况：
			若相等，并不超过指定次数，则n++，并把j插入到i的下一个位置:n++; a[++i] = a[j]
			若相等，等n已经等于或大于指定的次数了，则这个j元素是需要“删除”的:count++
			若不相等，说明已排序的序列中有新的元素出现了，这时重置n的值，并且把新元素j插入到i的下一个位置:a[++i] = a[j]

#时间复杂度： O(n)
size_t del_duplicate_n(int a[],size_t size,unsigned int times)
{
    size_t count = 0;
    size_t i = 0;
    size_t n = 1;
    for(size_t j=1;j<size;j++)
    {
        if(a[i] == a[j] && n<times)
        {
            n++;
            a[++i] = a[j];
        }
        else
        {
            if(a[i] == a[j] && n>=times)
                count++;
            else
            {
                n = 1;
                a[++i] = a[j];
            }
        }
    }
    return size-count;
}
int main()
{
    int a[] = {3,3,3,7,7,7,7,9,11,23,23,37};
    int len = del_duplicate_n(a,12,2);
    cout<<len<<endl;
    cout<<endl;
    for(auto &item:a)
        cout<<item<<" ";
    cout<<endl;
    return 0;
}
#3、在有序的旋转数组中查找某一个值（没有重复值）
注：旋转数组的旋转过程：
	目标：4,5,1,2,3
	旋转过程：1,2,3,4,5
			  5,4,3,2,1
			  4,5,3,2,1
			  4,5,1,2,3
输入：有序不可重复的旋转数组
输出：目标值下标
思路：旋转数组的特点：从旋转数组的中心位置划分开，必定有一半是有序的
		若左半边是有序的，目标值在左半边，则二分查找返回目标值的下标，目标值不在左半边，则删除左半边，再重新划分(递归)
		若右半边是。。。 
#时间复杂度： 
using pos = int;
///二分查找
pos find_(int a[],pos i,pos j,int value)
{
    if(i>j)
        return -1;
    pos mid = (i+j)/2;
    if(a[mid] == value)
        return mid;
    else
    {
        if(a[mid]>value)
            return find_(a,i,mid-1,value);
        else
            return find_(a,mid+1,j,value);
    }
}

pos find_value(int a[],pos i,pos j,int value)
{
    if(i == j)
    {
        if(a[i] == value)
            return i;
        else
            return -1;
    }
    else
    {
        auto mid = (i+j)/2;
        if(a[mid]>a[i]) ///zuo
        {
            if(a[i]<=value<=a[mid])
                return find_(a,i,mid,value);
            else
                return find_value(a,mid+1,j,value);
        }
        else ///you
        {
            if(a[mid+1]<=value<=a[j])
                return find_(a,mid+1,j,value);
            else
                return find_value(a,i,mid,value);
        }
    }
}

int main()
{
    int a[] = {574,46654,765765,1,3,5,76,211,321};
    cout<<find_value(a,0,9,76)<<endl;
    return 0;
}

#4、从一个旋转的“有序”数组中查找某个值（有重复值）
输入：有序可重复的旋转数组
输出：目标值的下标
思路：旋转数组的特点：从旋转数组的中间划分开，必定有一半是有序的
		若左半边是有序的，目标值在左半边，则返回目标值的下标，目标值不在左半边，则删除左半边，再重新划分
		若右半边是。。。
#时间复杂度： 


#5、给定两个已经排序好的数组，找到两者所有元素中中间值的元素。要求时间复杂度O(log(m + n))
通用形式：给定两个已经排序好的数组，找到两者所有元素中第k 大的元素。
时间复杂度m+n的解法：两个指针pA 和pB，分别指向A 和B 数组的第一个元素，然后开始需找第k的元素
时间复杂度log(m+n)解法：
输入：
输出：
思路： 
    方法一：先归并，在顺序查找第k个大小的值
    方法二：先归并，在利用二分查找
    方法三：假设数组AB的长度都大于等k/2，这时分别找到a的第k/2个元素和b的第k/2个元素，然后做比较分析：
            a[k/2-1] == b[k/2-1] 则a[k/2-1]就是第k大小的元素
            a[k/2-1] < b[k/2-1] 则表明a中前k/2个元素都在top K中，这时我们删除a中前k/2个元素，并递归查找第k/2大小的元素就是我们要找的元素
            a[k/2-1] > b[k/2-1] 则同理
            分析：方法三的遇到的问题：如何保证两个数组的长度都大于k/2，否则会出现越界，保证不了的话，就应该找min(最短数组长度，k/2)，即不一定非要取k/2，只要找到前k个元素的部分在最短数组中即可，当然也要判断极限情况
            						  如何确定谁是最短的那个数组？
            						  k等于1的情况

int find_k(int a[],size_t m,int b[],size_t n,size_t k)
{
    if(m>n) return find_k(b,n,a,m,k);
    if(k==1) return min(a[0],b[0]);
    if(m==0) return b[k-1];

    size_t pa = min(m,k/2);
    size_t pb = k - pa;
    if(a[pa-1] == b[pb-1]) return a[pa-1];
    if(a[pa-1] < b[pb-1])
        return find_k(a+pa,m-pa,b,n,k-pa);
    else
        return find_k(a,m,b+pb,n-pb,k-pb);
}
int main()
{
    int a[] = {1,2,5,7,13,25,67,89};
    int b[] = {3,21,45,66,74,82,99,101,322,456};
    cout<<find_k(a,8,b,10,5)<<endl;
    return 0;
}
回到本题上来，不再是第k个元素，而是两数组的中间值：
	什么叫中间值？
	平均值 平均值是算术平均数，由一组数相加然后除以这些数的个数计算得出。例如，2、3、3、5、7 和 10 的平均数是 30 除以 6，结果是 5。
    中值 中值是一组数中间位置的数；即一半数的值比中值大，另一半数的值比中值小。例如，2、3、3、5、7 和 10 的中值是 4。
    众数 众数是一组数中最常出现的数。例如，2、3、3、5、7 和 10 的众数是 3。


#6、给一个未排序的数组（无重复），找到数组中最长连续的序列的长度
输入：[100, 4, 200, 1, 3, 2],
输出: 1,2,3,4->4
时间复杂度：O(n)
思想：方法一：先排序，再定最长那个连续的序列 #时间复杂度为 O(nlogn)
	  方法二：很好的借助连续的序列若存放在按关键值大小的hash的特点，从而找到最大的连续序列 #O(n)
	  			用一个哈希表unordered_map<int, bool> used 记录每个元素是否使用，对每个元素，以该往左右扩张，直到不连续为止，记录下最长的长度。
unsigned int max_length_sequence(vector<int> &a)
{
    unordered_map<int,bool> m;
    unsigned longest = 0;
    unsigned length;
    for(auto item : a)
        m[item] = false;
    for(auto item:a)
    {
        if(m[item]) continue; #bool很好的解决了不用重复计算的问题
        m[item] = true;
        length = 1;
        for(auto i=item-1;m.find(i)!= m.end();i-- )
        {
            m[i] = true;
            length++;

        }
        for(auto j=item+1;m.find(j)!= m.end();j++)
        {
            m[j] = true;
            length++;
        }
        longest = max(longest,length);
    }
    return longest;
}

int main()
{
    vector<int> a = {12,32,3,43,65,1,4,2,67,8};
    cout<<max_length_sequence(a)<<endl;
    return 0;
}
#7、3Sum
给定一个无序的数组，并给定一个值，求数组中3个元素之和等于0的情况，返回满足3数之和等于value的所有3个元素组合
输入：{-1 0 1 2 -1 -4}，value = 0
输出:(-1, 0, 1)、(-1, -1, 2)
时间复杂度： 
思想：首先想到2sum的情况：先排序，再用两个指针来分别指向数组的首和尾：p,q
						a[p] + a[q] > value 说明需要移动q，来缩小差距
						a[p] + a[q] < value 说明需要移动p，来缩小差距
						a[p] + a[q] = value 保存p,q到容器中，并继续往下执行，直到p>q终止

	  3sum情况：把3sum转换成2sum的形式:a1+a2+a3=value ---> a1+a2 = new_value(value-a3)



#8、3Sum Closest
输入：
输出:
时间复杂度： 
思想：
#9、4Sum
输入：
输出:
时间复杂度： 
思想：
#10、Remove Element
输入：{1,2,3,2,3,2,5,6}，value=2
输出: 1,3,3,5,6
时间复杂度： O(n)
思想：迭代器遍历，再删除即可
void remove_element(vector<int> &v,int value)
{
    vector<int>::iterator t = v.begin();
    while(t != v.end())
    {
        if(*t == value)
            t = v.erase(t);
        else
            t++;
    }
}
int main()
{
    vector<int> v = {1,2,3,2,3,2,5,6};
    remove_element(v,3);
    for(auto item:v)
        cout<<item<<ends;
    cout<<endl;
    return 0;
}

快捷的解法：
int removeElement(int A[], int n, int elem) {
	int index = 0;
	for (int i = 0; i < n; ++i) {
		if (A[i] != elem) {
				A[index++] = A[i];
			}
		}
	return index;
}
#11、Next Permutation
输入：
输出:
时间复杂度： 
思想：主要是对题意的理解：
/*
		C++ STL中提供了std::next_permutation与std::prev_permutation可以获取数字或者是字符的全排列，其中std::next_permutation提供升序、std::prev_permutation提供降序。
		　　template <class BidirectionalIterator>
		　　bool next_permutation (BidirectionalIterator first, BidirectionalIterator last );
		　　template <class BidirectionalIterator, class Compare>
		　　bool next_permutation (BidirectionalIterator first,BidirectionalIterator last, Compare comp);
		说明：next_permutation，重新排列范围内的元素[第一，最后一个）返回按照字典序排列的下一个值较大的组合。
		返回值：如果有一个更高的排列，它重新排列元素，并返回true；如果这是不可能的（因为它已经在最大可能的排列），它按升序排列重新元素，并返回false。
		如：
		#include <iostream>
		#include <algorithm>    /// next_permutation, sort
		using namespace std;
		int main () {
		  int myints[] = {1,2,3,1};
		  sort (myints,myints+4);

		  do {
		    cout << myints[0] << ' ' << myints[1] << ' ' << myints[2] << ' '<< myints[3]<<'\n';
		  } while ( next_permutation(myints,myints+4) );    ///获取下一个较大字典序排列

		  cout << "After loop: " << myints[0] << ' ' << myints[1] << ' ' << myints[2] << ' '<< myints[3] <<'\n';
		  return 0;
		}
		运行结果：	1123
					1132
					1213
					1231
					1312
					1321
					2113
					2131
					2311
					3112
					3121
					3211

					1123
		算法描述：
		1、从尾部开始往前寻找两个相邻的元素 第1个元素i，第2个元素j（从前往后数的），且i<j
		2、再从尾往前找第一个大于i的元素k。将i、k对调
		3、[j,last)范围的元素置逆（颠倒排列）
*/	
以上所诉：next_permutation是依据现有的序列，若能提供一个更高的序列，则就地修改，并返回true，若没有一个更高的序列，则升序排序，并返回false

using pos = size_t;
void reserve(int a[],pos i,pos j)
{
    pos p = i;
    pos q = j;
    for(;p<=q;p++,q--)
        swap(a[p],a[q]);
}
int a[4];
bool _next_permutation(int a[],pos i,pos j)
{
    pos k1 = j;
    pos k2 = j - 1;
    while(a[k2] >= a[k1]&&k2>=i)#从尾部开始往前寻找两个相邻的元素 第1个元素i，第2个元素j（从前往后数的），且i<j
    {
        k1--;
        k2--;
    }
    if(k2<i) #若已经是最大序列了，则重新排序，并返回false
    {
//        sort(a,i,j);
        return false;
    }
    pos k3 = j;
    while(a[k3]<=a[k2])#从尾往前找第一个大于i的元素k
    {
        k3--;
    }
    swap(a[k2],a[k3]);#将i、k对调

    reserve(a,k1,j);#[j,last)范围的元素置逆
    return true;;
}
int main()
{
    int a[4] = {1,1,3,2};
    _next_permutation(a,0,3);
    for(auto &item:a)
        cout<<item<<ends;
    cout<<endl;
    return 0;
}


#12、Permutation Sequence
提供所有的组合序列，并按序输出
输入：一个vector序列
输出：所有的全排列
时间复杂度： 
思想：借助next_permutation算法来生成所有的全排列，再借助set容器的insert返回值的特性
set<vector<int>> all_permutation_sequence(set<vector<int>> &s,vector<int> &v)
{
    while(next_permutation(v.begin(),v.end()))
    {
        vector<int> i = v;
        if(!s.insert(i).second)#通过insert返回值来判断是否已经完成了所有的全排列
            break;
    }

    return s;
}

int main()
{
    set<vector<int>> s;
    vector<int> v = {1,3,2,1,5,6,7};
    s = all_permutation_sequence(s,v);
    for(auto &item:s)
    {
        for(auto &item2:item)
            cout<<item2<<ends;
        cout<<endl;
    }
    return 0;

}
#13、Valid Sudoku
输入：
输出:
时间复杂度： 
思想：
#14、Trapping Rain Water
输入：
输出:
时间复杂度： 
思想：
#15、Rotate Image
旋转图片：
1 2  	4 2  	3 1
3 4  	3 1  	4 2
输入：二维数组
输出: 二维数组
时间复杂度： 
思想：先“正(斜)对角线”交换，再“横”交换
using size_type = vector<int>::size_type;
vector<vector<int>>& rotate_1(vector<vector<int>> &vv)#“正(斜)对角线”交换
{
    size_t len = vv.size()-1;
    size_type j= 0;
    for(size_type i = 0;i<len;i++)
        for(size_type j = 0;j<len;j++)
            swap(vv[i][j],vv[len-i][len-j]);
    return vv;
}
vector<vector<int>>& rotate_2(vector<vector<int>> &vv)#“横”交换
{
    size_type i=0;
    size_type j=vv.size()-1;
    for(;i<j;i++,j--)
        swap(vv[i],vv[j]);
    return vv;
}
vector<vector<int>>& rotate_image(vector<vector<int>> &vv)
{
    rotate_1(vv);
    rotate_2(vv);
    return vv;
}
int main()
{
    vector<vector<int>> vv = {{1,2},{3,4}};
    rotate_image(vv);
    for(auto item:vv)
    {
        for(auto item2:item)
            cout<<item2<<ends;
        cout<<endl;
    }
    return 0;
}
#16、Plus One
用一个数组来代表一个非负整数，对这个整数进行+1操作，得到的结果也用数组进行表示。
输入：5319
输出: 5320
时间复杂度： 
思想：从数组最后一位开始，每个位需要判断是否需要进位，如果进位，自已设为0，否则自增即可
void plus_one(int a[],size_t n)
{
    size_t pos = n-1;
    while(pos>=0)
    {
        if(a[pos] != 9)
        {
            a[pos]++;
            break;
        }
        else
        {
            a[pos--] = 0;
        }
    }
    return;
}
int main()
{
    int a[4] = {9,9,9,9};
    plus_one(a,4);
    for(auto item:a)
        cout<<item<<ends;
    cout<<endl;
    return 0;
}
#17、Climbing Stairs
输入：
输出:
时间复杂度： 
思想：
#18、Gray Code
输入：
输出:
时间复杂度： 
思想：
#19、Set Matrix Zeroes
输入：
输出:
时间复杂度： 
思想：
#20、Gas Station
输入：
输出:
时间复杂度： 
思想：





























