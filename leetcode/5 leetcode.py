注：排序：
		插入排序：#
		归并排序：#
		希尔排序：
		快速排序：#
		冒泡排序：
		堆排序：#
		计数排序：#
		基数排序：#
		桶排序：
		选择排序
#内部排序是数据记录在内存中进行排序，
		——————基本上接触到的排序都是内部排序
	如： 
	插入系列：直接插入和希尔排序
#		———插入排序
			思想：key作哨兵，把每次要插的元素放到这里
				  0作已有序序列，1开始作为第一个要插的元素 #为了便于通用性，我们0作为已有序元素，而不再是1
				  “一边挪动一边寻找”
void insert_sort(int a[],size_t size)
{
    int key;
    int j;
    for(int i=1;i<size;i++)
    {
        key = a[i];#存放要插的元素
        j = i-1;#找到已有序序列的尾元素
        while(j>-1 && a[j]>key)#寻找到i最终合适的位置：j+1
        {
            a[j+1] = a[j];
            j--;
        }
        a[j+1] = key;
    }
    return;
}
int main()
{
    int a[] = {49,38,65,97,76,13,27,49};
    for(auto item:a)
        cout<<item<<ends;
    cout<<endl;

    insert_sort(a,8);

    for(auto item:a)
        cout<<item<<ends;
    cout<<endl;
    return 0;
}
#		————希尔排序
			思想：（d+1次直接插入排序）将 n 个记录分成 d 个子序列，再对每个子序列都进行直接插入排序，最后再对整个序列进行最后一次直接插入排序
					{ R[1]，R[1+d]，R[1+2d]，…，R[1+kd] }
					{ R[2]，R[2+d]，R[2+2d]，…，R[2+kd] }
						… 
					{ R[d]，R[2d]，R[3d]，…，R[kd]，R[(k+1)d] }

	选择系列：简单选择排序和堆排序
#		————简单选择排序
			思想：每趟都选择一个最小的元素，然后与“首部”元素交换
void select_sort(int a[],size_t size)
{
    int min;
    size_t pos;
    for(size_t i=0;i<size-1;i++)
    {
        min = a[i];
        for(int j = i;j<size;j++)
        {
            if(min > a[j])
            {
                min = a[j];
                pos = j;#记录最小值的下标
            }
        }
        swap(a[i],a[pos]);#把最小值放到“首部”
    }
    return;
}
int main()
{
    int a[] = {49,38,65,97,76,13,27,49};
    for(auto item:a)
        cout<<item<<ends;
    cout<<endl;

    select_sort(a,8);

    for(auto item:a)
        cout<<item<<ends;
    cout<<endl;
    return 0;
}
#		————堆排序（49，38，65，97，76，13，27，49）
			注：下标必须从1开始，否则不满足2*i为左孩子，2*i+1为右孩子
			思想：“一维数组存”储一个堆，则堆对应一棵“完全二叉树”
建堆：数组转换成堆build_min_heapify 
			1）n 个结点的完全二叉树，则最后一个结点是第个n/2结点的子树。
			2）筛选从第n/2个结点为根的子树开始，该子树成为堆。
			3）之后向前依次对各结点为根的子树进行筛选，使之成为堆，直到根结点。
调整堆：取出堆顶元素时，需要调整堆fix_min_heapify
			1）设有m 个元素的堆，输出堆顶元素后，剩下m-1 个元素。将堆底元素送入堆顶（（最后一个元素与堆顶进行交换），堆被破坏，其原因仅是根结点不满足堆的性质。
			2）将根结点与左、右子树中较小元素的进行交换。
			3）若与左子树交换：如果左子树堆被破坏，即左子树的根结点不满足堆的性质，则重复方法 （2）.
			4）若与右子树交换，如果右子树堆被破坏，即右子树的根结点不满足堆的性质。则重复方法 （2）.
			5）继续对不满足堆性质的子树进行上述交换操作，直到叶子结点，堆被建成。
堆排序：不断地取堆顶元素，不断地调整堆

	交换系列：冒泡和快速
#		————冒泡排序
			思想：不断交换，直到还剩一个元素为止
void bubble_sort(int a[],size_t size)
{
    for(size_t i=0;i<size-1;i++)# n-1次冒泡
    {
        for(size_t j=0;j<size-i;j++)#每一次冒泡的长度逐渐减小
        {
            if(a[j] > a[j+1])#最大值都到后面去
                swap(a[j],a[j+1]);
        }
    }
    return;
}
int main()
{
    int a[] = {49,38,65,97,76,13,27,49};
    for(auto item:a)
        cout<<item<<ends;
    cout<<endl;

    bubble_sort(a,8);

    for(auto item:a)
        cout<<item<<ends;
    cout<<endl;
    return 0;
}
#		————快速排序
			思想：递归做n次：
size_t _partition(int a[],size_t p,size_t r)#划分思想
{
    size_t low = p;
    size_t high = r;
    int pivot = a[p];
    while(low < high)
    {
        while(low<high && a[high] >= pivot)
            high--;
        swap(a[low],a[high]);
        while(low<high && a[low] <= pivot)
            low++;
        swap(a[low],a[high]);
    }
    a[low] = pivot;
    return low;
}
void quick_sort(int a[],size_t p,size_t r)#递归思想：自顶向下
{
    if(p < r)
    {
        size_t q = _partition(a,p,r);
        quick_sort(a,p,q-1);
        quick_sort(a,q+1,r);
    }
    return;
}

int main()
{
    int a[] = {49,38,65,97,76,13,27,49};
    for(auto item:a)
        cout<<item<<ends;
    cout<<endl;

    quick_sort(a,0,7);

    for(auto item:a)
        cout<<item<<ends;
    cout<<endl;
    return 0;
}
#	归并系列：归并排序
		————归并排序
			思想：递归
void merge(int a[],size_t p,size_t q,size_t r)#两个相邻的数组合并
{
    unsigned len1 = q-p+1;
    unsigned len2 = r-q;
    int item1[len1];
    int item2[len2];
    int i = 0;
    int j = 0;
    for(int ii=p;ii<=q;)
        item1[i++] = a[ii++];
    for(int ii=q+1;ii<=r;)
        item2[j++] = a[ii++];
    i = 0;
    j = 0;

    while(i<len1&&j<len2)
    {
        if(item1[i]<item2[j])
            a[p++] = item1[i++];
        else
            a[p++] = item2[j++];
    }
    if(i == len1)
        while(j<len2)
            a[p++] = item2[j++];
    else
        while(i<len1)
            a[p++] = item1[i++];
    return;
}
void merge_sort(int a[],size_t p,size_t r)#递归：自顶向下
{
    if(p < r)
    {
        size_t q = (p+r)/2;
        merge_sort(a,p,q);
        merge_sort(a,q+1,r);
        merge(a,p,q,r);
    }
    return;
}

int main()
{
    int a[] = {49,38,65,97,76,13,27,49};
    for(auto item:a)
        cout<<item<<ends;
    cout<<endl;

    merge_sort(a,0,7);

    for(auto item:a)
        cout<<item<<ends;
    cout<<endl;
    return 0;
}
	基数系列：
		基数排序
		计数排序：
		桶排序：
#外部排序是因排序的数据很大，一次不能容纳全部的排序记录，在排序过程中需要访问外存。 
	



1、归并排序(数组)
输入：
输出：
时间复杂度：
思想：已解！
2、归并排序(list)
输入：
输出：
时间复杂度：
思想：
3、Merge k Sorted Lists
输入：
输出：
时间复杂度：
思想：http://www.tuicool.com/articles/ZnuEVfJ
4、First Missing Positive
在数组中找到第一个丢失的正整数
输入：
Given  [1,2,0]  return  3 ,
and  [3,4,-1,1]  return  2 .
输出：
时间复杂度：
思想：
	1 排序之后查找
	2 把出现的数值放到与下标一致的位置，再判断什么位置最先出现不连续的数值，就是答案了。
	3 和2差不多，把出现过的数值的下标位置做好标识，如果没有出现过的数组的下标就没有标识，那么这个就是答案。5、Sort Colors
    4 利用unorder_map，先找到最小正整数的位置，再开始寻找第一个hash中断的位置即可
方法四：
int find_missing_positive(int a[],size_t n)
{
    unordered_set<int> s;
    unsigned min = 0;
    bool flag = false;
    size_t i=0;
    while(i<n)
    {
        s.insert(a[i]);
        if(a[i]>0 && !flag)
        {
            min = a[i];
            flag = true;
        }
        else
        {
            if(a[i]>0 && a[i]<min)
                min = a[i];
        }
        i++;
    }
    while(s.end() != s.find(++min));#
        
    return min;
}
int main()
{
    int a[] = {-1,-2};
    cout<<find_missing_positive(a,2)<<endl;
    return 0;
}
5、Sort Colors
Given an array with n objects colored red, white or blue, sort them so that objects of the same color
are adjacent, with the colors in the order red 0, white 1 and blue 2.
输入：给出colors=[2, 1, 1, 0, 2]，k=4
输出：你的代码应该在原地操作使得数组变成[0, 1, 1, 2, 2]
时间复杂度：
思想：
6、Search for a Range
输入：Given有序序列[5, 7, 7, 8, 8, 10] and target value 8, 
输出：return [3, 4].
	  If the target is not found in the array, return [-1, -1].
时间复杂度：二分查找思想（）
思想：http://blog.csdn.net/int64ago/article/details/7425727
vector<int>& search_k_range(int a[],size_t size,int k,vector<int> &result)
{
    size_t i = 0;
    size_t j = size-1;
    size_t pos,pos1 = -1,pos2 = -1;
    bool flag = false;
    while(i<=j && i>=0 && j<size)# 必须加上i>=0 && j<size，否则下标访问越界，所有的二分查找都会出现这样的问题，应该高度警惕，以避免犯这样的错误！
    {
        pos = (i+j)/2;
        if(k == a[pos])
        {
            flag = true;#代表已找到了
            break;
        }
        if(k > a[pos])
            i = pos+1;
        if(k < a[pos])
            j = pos-1;
    }
    if(flag)
    {
        while(a[--pos] == k);
        pos1 = pos+1;
        while(a[++pos] == k);
        pos2 = pos-1;
    }
    result.push_back(pos1);
    result.push_back(pos2);
    return result;
}
int main()
{
    int a[] = {5,7,7,8,8,8,10};
    vector<int> result;
    search_k_range(a,7,6,result);
    for(auto item:result)
        cout<<item<<ends;
    cout<<endl;
    return 0;
}
7、Search Insert Position
有一个已排序好且无重复元素的数组，给定一个目标值，让你找到一个位置把这个值插入，并保持升序。如果数组中有这个值那么就输出这个元素的位置。
输入：
[1,3,5,6], 5 → 2
[1,3,5,6], 2 → 1
[1,3,5,6], 7 → 4
[1,3,5,6], 0 → 0
输出：
时间复杂度：
思想：
方法一：依次查找
方法二：二分查找
size_t search_insert(vector<int> v,int key)
{
    int i = 0;
    int j = v.size()-1;
    int pos = -1;
    while(i<=j)
    {
        pos = (i+j)/2;
        if(v[pos] == key)
            return pos;
        if(v[pos] > key)
            j = pos-1;
        if(v[pos] < key)
            i = pos+1;
    }

    vector<int>::iterator t = v.begin();
    advance(t,pos);
    if(v[pos] > key)
    {
        v.insert(t,key);
        return pos;
    }
    else
    {
        v.insert(t+1,key);
        return pos+1;
    }
}
int main()
{
    vector<int> v = {1,3,5,6};
    cout<<search_insert(v,2)<<endl;
    return 0;
}
8、Search a 2D Matrix
在一个二维矩阵中找到给定的值。矩阵从上到下从左到右有序，矩阵满足：
	Integers in each row are sorted from le to right.
	first integer of each row is greater than the last integer of the previous row.
输入：
[
  [1,   3,  5,  7],
  [10, 11, 16, 20],
  [23, 30, 34, 50]
]
输出：Given target = 3, return true.
时间复杂度：
思想：先寻找行号，固定好行以后，（寻找行号不能用二分查找）再利用二分查找去寻找要找的元素
bool search_2d_matrix(const vector<vector<int>> &vv,int row,int rank,int key)
{
    int row_i = 0;
    int rank_i = 0;
    int rank_j = rank-1;
    int row_pos,rank_pos;
    while(row_i < row)
    {
        if(vv[row_i][rank-1]>= key)
            break;
        else
            row_i++;
    }
    row_pos = row_i;

    while(rank_i <= rank_j && rank_j>=0 && rank_i<rank)
    {
        rank_pos = (rank_i + rank_j)/2;
        if(vv[row_pos][rank_pos] == key)
            return true;
        if(vv[row_pos][rank_pos] > key)
            rank_j = rank_pos-1;
        if(vv[row_pos][rank_pos] < key)
            rank_i = rank_pos+1;
    }
    return false;
}
int main()
{
    vector<vector<int>> vv = { {1,3,5,7},{10,11,16,20},{23,30,34,50} };
    if(search_2d_matrix(vv,3,4,21))
        cout<<"find"<<endl;
    else
        cout<<"not find"<<endl;
    return 0;
}
9、Subsets
求数组的所有子集（不重复）
输入：For example, If S = [1,2,3], a solution is:
输出：
	[
		[3],
		[1],
		[2],
		[1,2,3],
		[1,3],
		[2,3],
		[1,2],
		[]
	]
时间复杂度：
思想：
11、Subsets II
求数组的所有子集（不重复）
输入：If S = [1,2,2], a solution is:
输出：
	[
		[2],
		[1],
		[1,2,2],
		[2,2],
		[1,2],
		[]
	]
时间复杂度：
思想：
12、next_permutation（不重复）
输入：[1,2,3]
输出：[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], and [3,2,1].
时间复杂度：
思想：
13、next_permutation II(重复)
输入：[1,1,2]
输出：[1,1,2], [1,2,1], and [2,1,1].
时间复杂度：
思想：
14、Combinations
Given two integers n and k, return all possible combinations of k numbers out of 1:::n.
输入：n = 4 and k = 2,
输出：
	[
		[2,4],
		[3,4],
		[2,3],
		[1,2],
		[1,3],
		[1,4],
	]
时间复杂度：
思想：
15、Letter Combinations of a Phone Number
输入：
输出：
时间复杂度：
思想：