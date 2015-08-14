图的算法有：存储、遍历、最小生成树、拓扑排序、关键路径、最短路径（某个顶点到其他顶点、每对顶点之间）

#特别注意：在做图的算法时，首先搞清楚：
#                                        图是有向图还是无向图，
#                                        图的存储结构是哪一种
#                                        图的边是否带权值

一、图的存储
#邻接矩阵(一个一维数组，一个二维数组)：
									一维数组存储图中顶点信息
									二维数组（邻接矩阵）存储图中的边信息
输入：
	第一行：顶点数，边数
	各顶点名字
	顶点i  顶点j  权值（循环n次）
输出：邻接矩阵的值
思想：根据顶点数创建一维数组vector<char> vertex,用来存放各顶点
	  再根据顶点数创建二维数组vector<vector<int>> array，用来存放边的权值，先array分配好大小合适的空间，并初始化为init_value（除了，自己对自己的权值为0）
	  （循环“顶点数”次）每输入一对“顶点i   顶点j   权值”，利用一维数组vertex找到每个顶点在array中对应的下标，根据在array中找个合适的位置，并存放该权值即可
	  	循环结束，邻接矩阵就创建成功了
const int init_value = 65535;

struct graph{#图的结构
    vector<char>        vertex;#存放顶点的数组
    vector<vector<int>> array;#存放边的权值的邻接矩阵
    int num_vertex;#顶点数
    int num_edge;#边的个数数
    graph(int num1,int num2):num_vertex(num1)
                            ,num_edge(num2)
    {#初始化邻接矩阵
        int i = 0;
        while(i < num_vertex)
        {
            array.push_back(vector<int>(num_vertex,init_value));
            array[i][i] = 0;
            i++;
        }

    }
};
int locate(graph *g,char c)#根据顶点值，找到对应的顶点下标
{
    int pos=0;
    while(pos<g->num_vertex)
    {
        if(g->vertex[pos] == c)
            break;
        pos++;
    }
    if(pos < g->num_vertex)
        return pos;
    else
        return -1;
}
void create_graph(graph **pg)#创建邻接矩阵
{
    int num1;
    int num2;
    char c;
    char src_char,des_char;#边的头顶点和尾顶点
    int weight;#边的权值
    int i=1;
    cout<<"num_vertex: "<<" "<<"num_edge: "<<endl;
    cin>>num1>>num2;#输入顶点个数和边的个数

    *pg = new graph(num1,num2);#生成一个图类对象
    graph *g = *pg;
    cout<<"every vertex:"<<endl;
    vector<char> &v = g->vertex;
    while(cin>>c)#把所有顶点存放到顶点数组中
        v.push_back(c);
    cin.clear();

    vector<vector<int>> &vv = g->array;

    while(i <= g->num_edge)#读取每一条边的信息，并存储在邻接矩阵中
    {
        cout<<"src_char: "<<"des_char: "<<"weight: "<<endl;
        cin>>src_char>>des_char>>weight;#
        int pos1 = locate(g,src_char);
        int pos2 = locate(g,des_char);
        vv[pos1][pos2] = weight;
        i++;
    }
    return;
}
void print_graph(graph *g)#打印邻接矩阵
{
    for(auto v:g->array)
    {
        for(auto item:v)
            cout<<setw(8)<<item<<ends;
        cout<<endl;
    }
    return;
}


int main()
{
    graph *g;
    create_graph(&g);
    print_graph(g);
    return 0;
}
#邻接表(一维数组和多个链表组成的)：
								一维数组存放多个链表头节点，其下标为图的顶点信息
								每个链表都存放每个顶点的邻接顶点
输入：
	第一行：顶点数，边数
	各顶点名字
	顶点i   顶点j   权值（循环n次）
输出：每行输出一个邻接链表（多行输出）
思想：根据顶点数创建一个顶点数大小的map<char,ListNode_2*>,用于存放顶点值和指向链表的指针，首先录入各顶点值，并初始化ListNode_2 *为nullptr
	  （循环“顶点数”次）每输入一对“顶点i   顶点j   权值”，根据顶点i在map中找个对应的位置，创建一个新节点ListNode_2，用于存放顶点值j和权值，并让map指向其链表
	  	循环结束，邻接表就创建成功了
struct ListNode_2{#邻接链表的节点
    char name;
    int weight;#边的权值
    ListNode_2 *next;#同一个链表下的下一个节点
    ListNode_2(char c,int x):name(c),weight(x),next(nullptr){}
};

void print_list_2(ListNode_2 *head)#打印list中所有节点的信息
{
    ListNode_2 *p = head->next;
    while(p){
        cout<<p->name<<ends;
        p = p->next;
    }
    cout<<endl;
    return;
}

struct graph_2{#图的结构
    map<char,ListNode_2 *>  vertex;#存放所有顶点和链表的头
    int num_vertex;#顶点数
    int num_edge;#边数
    graph_2(int num1,int num2):num_vertex(num1)
                                ,num_edge(num2){}#vertex初始化不分配空间
};
void create_graph_2(graph_2 **pg)
{
    int num1;
    int num2;
    char src_char,des_char;
    int weight;
    int i = 1;
    cout<<"num_vertex: "<<"num_edge: "<<endl;#读取顶点数和边数
    cin>>num1>>num2;
    *pg = new graph_2(num1,num2);
    graph_2 *g = *pg;
    cout<<"every vertex:"<<endl;#读取各顶点值：a b c d e
    char c;
    while(cin>>c)
    {
        g->vertex[c] = nullptr;
    }
    map<char,ListNode_2 *> &m = g->vertex;

    cin.clear();
     while(i<=g->num_edge)
     {
         i++;
         cout<<"src_char: "<<"des_char: "<<"weight: "<<endl;#读取顶点i 顶点j 权值
         cin>>src_char>>des_char>>weight;
         if(m[src_char] == nullptr)
         {
             m[src_char] = new ListNode_2(des_char,weight);
             continue;
         }
         ListNode_2 *p = m[src_char];
         ListNode_2 *q = nullptr;
         while(p)
         {
             q = p;
             p = p->next;
         }
         q->next = new ListNode_2(des_char,weight);
     }
     return;
}

void print_graph_2(graph_2 *g)
{
    for(auto pair:g->vertex)
    {
        ListNode_2 *p = pair.second;
        while(p)
        {
            cout<<p->name<<ends;
            p = p->next;
        }
        cout<<endl;
    }
    return;
}
int main()
{
    graph_2 *g;
    create_graph_2(&g);
    print_graph_2(g);
    return 0;
}
#十字链表（略）

二、遍历
1、按邻接矩阵存储的遍历：
#广度（非递归）
思想：
		从图的存储方式出发：有向图还是无向图、邻接矩阵还是邻接表、是否带权值------》按有向图，邻接矩阵存储、带权值的情况进行遍历：
		从矩阵的角度看该如何广度遍历，首先考虑到的是图中可能会有独立的顶点，因此少不了从每个顶点都出发一次：for(int i=0;i<顶点数;i++)
		（为了避免出现死循环，对已经遍历过的顶点做标记）从顶点i出发时，找到邻接矩阵中对应的那一行：将权值不为0且不为init_value，且flag不为true(未遍历)的顶点进行入队并访问....(层次遍历思想)，
		直到队列deque为空为止，进入一次for循环：for(int i=0;i<顶点数;i++)
void breadth_travel(graph *g,vector<char> &result)
{
    vector<vector<int>> &vv = g->array;
    deque<int> dq;
    bool flag[g->num_vertex];
    for(auto iflag:flag)
        iflag = false;
    for(int pos=0;pos<g->num_vertex&&flag[pos]!=true;pos++)#寻找那些还未做标记的顶点，开始遍历
    {

        result.push_back(g->vertex[pos]);
        flag[pos] = true;
        dq.push_back(pos);
        while(!dq.empty())
        {
                int vertex_i = dq.front();
                dq.pop_front();
                for(int j=0;j<g->num_vertex;j++)
                {
                    if(vv[vertex_i][j]!=0 && vv[vertex_i][j]!=init_value &&flag[j] != true)
                    {
                        dq.push_back(j);
                        flag[j] = true;
                        result.push_back(g->vertex[j]);
                    }
                }
        }
    }
    return;
}
int main()
{
    graph *g;
    vector<char> result;
    create_graph(&g);
    print_graph(g);
    breadth_travel(g,result);
    for(auto item:result)
        cout<<item<<ends;
    cout<<endl;
    return 0;
}
#深度（递归、非递归）
思想：从有向、带权、邻接矩阵发出：
		为了避免独立顶点的情况，从每个顶点开始遍历一遍：for(int i=0;g->vertex;i++)，遍历过了的做个标记
		深度递归遍历的思想：根据顶点值在邻接矩阵中找到对应的行，然后从行中找到未遍历过且权值不为0和init_value的顶点，从该顶点继续递归遍历...

2、按邻接表存储的遍历：
#广度（非递归）
思想：
		从图的存储方式出发：有向图还是无向图、邻接矩阵还是邻接表、是否带权值------》按有向图，邻接矩阵存储、带权值的情况进行遍历：
		从矩阵的角度看该如何广度遍历，首先考虑到的是图中可能会有独立的顶点，因此少不了从每个顶点都出发一次：for(int i=0;i<顶点数;i++)
		（为了避免出现死循环，对已经遍历过的顶点做标记）从顶点i出发时，找到邻接表中对应的那一个链表：将权值不为0且不为init_value，且flag不为true(未遍历)的顶点进行入队并访问....(层次遍历思想)，
		直到队列deque为空为止，进入一次for循环：for(int i=0;i<顶点数;i++)
void list_breadth_travel(graph_2 *g,vector<char> &result)
{
    deque<char> dq;
    map<char,ListNode_2 *> &m = g->vertex;#存放顶点值和链表指针的map
    map<char,bool> flag;#用于标记顶点是否访问过了
    for(auto item:m)
    {
        flag[item.first] = false;
    }
    for(auto item:m)#从每个顶点出发一遍，这样不会遗漏掉独立顶点的情况
    {
        char c = item.first;
        if(flag[c] != true)#这里条件判断必不可少
        {
            dq.push_back(c);
            result.push_back(c);
            flag[c] = true;
            while(!dq.empty())
            {
                char chr = dq.front();
                dq.pop_front();
                ListNode_2 *p = m[chr];
                while(p)
                {
                    if(flag[p->name] != true)
                    {
                        dq.push_back(p->name);
                        result.push_back(p->name);
                        flag[p->name] = true;
                    }

                    p =  p->next;
                }
            }
        }
    }

}
int main()
{
    graph_2 *g;
    create_graph_2(&g);
    print_graph_2(g);
    vector<char> result;
    list_breadth_travel(g,result);
    for(auto c:result)
        cout<<c<<ends;
    cout<<endl;
    return 0;
}
#深度（递归、非递归）
思想：
三、最小生成树
连通图的概念————在图论中，连通图基于连通的概念。在一个无向图 G 中，若从顶点vi到顶点vj有路径相连（当然从vj到vi也一定有路径），则称vi和vj是连通的。如果 G 是有向图，那么连接vi和vj的路径中所有的边都必须同向。如果图中任意两点都是连通的，那么图被称作连通图。如果此图是有向图，则称为强连通图（注意：需要双向都有路径）。

在 “无向图且带权且邻接矩阵” 的连通图中寻找最小生成树：含有图中全部顶点，但只有足以构成一棵树的n-1条边

找连通网的最小生成树，经典的有两种算法，普里姆算法和克鲁斯卡尔算法。
#普里姆——————搜索到的边子集所构成的树中，不但包括连通图里的所有顶点，且其所有边的权值之和亦为最小。
步骤：
	（1）输入：一个加权连通图，其中顶点集合为V，边集合为E；
	（2）初始化：Vnew = {x}，其中x为集合V中的任一节点（起始点），Enew = {}；
	（3）重复下列操作，直到Vnew = V：
		在集合E中选取权值最小的边（u, v），其中u为集合Vnew中的元素，而v则不是（如果存在
		有多条满足前述条件即具有相同权值的边，则可任意选取其中之一）；
		将v加入集合Vnew中，将（u, v）加入集合Enew中；
	（4）输出：使用集合Vnew和Enew来描述所得到的最小生成树。

思想： set<顶点>作为起始集合，只有一个顶点
	   map<map<char,char>,int>　存放最小生成树的边和权值
	   每一次循环都能挑出一个最小权值边：把“合适”的边都加入另一个集合map<map<char,char>,int>中，再利用min函数求出最小权值边

///并未验证该算法是否有bug
bool find_min_edge(pair<pair<char,char>,int> p1,pair<pair<char,char>,int> p2) 
{
    if(p1.second < p2.second)
        return true;
}
using iter = set<char>::iterator;
void find_min_tree(graph *g,map<pair<char,char>,int> &result)
{
    vector<vector<int>> &vv = g->array;
    set<char> set_char;#存放最小生成树的顶点集合
    map<pair<char,char>,int> mm_char;#把所有合适的边加入此集合中，利用min_element去找到最小权值边
    set_char.insert(set_char.begin(),g->vertex[0]);#先加入任意一个顶点到set_char中
    while(set_char.size() != g->num_vertex)#每一个循环都能找到一个最小权值边
    {
        iter t = set_char.begin();
        while(t != set_char.end())
        {
            int i = locate(g,*t);
            for(int j=0;j<g->num_vertex;j++)
            {
                if(vv[i][j] != 0 && vv[i][j] != init_value && set_char.end() != set_char.find(g->vertex[j]))
                    mm_char[make_pair(g->vertex[i],g->vertex[j])] = vv[i][j];#寻找“合适”的边，存放在mm_char中
            }
            t++;
        }

        auto p = min_element(mm_char.begin(),mm_char.end(),find_min_edge);#在mm_char中找到那个最小权值边
        result[(*p).first] = (*p).second;#存储最小权值边，以便打印
        set_char.insert(set_char.begin(),(*p).first.second);#将该顶点加入set_char
        mm_char.clear();#置空，以便下次循环使用
    }
}

int main()
{
    graph *g;
    create_graph(&g);
    print_graph(g);
    map<pair<char,char>,int> result;
    find_min_tree(g,result);
    for(auto item:result)
        cout<<item.first.first<<" "<<item.first.second<<endl;
    return 0;
}
#克鲁斯卡尔
思想：在E中选择最小代价的边，若该边依附的顶点落在T中不同的连通分量中，则将该边加入到T中，否则舍去此边而选择下一条代价最小的边，依次类推，直到T中所有顶点都在同一连通分量上为止。
未完待续：
bool min_edge(pair<pair<char,char>,int> p1,pair<pair<char,char>,int> p2)
{
    return p1.second<p2.second;
}
void find_min_tree_2(graph *g,map<pair<char,char>,int> &result)
{
    vector<vector<int>> &vv = g->array;
    map<pair<char,char>,int> mm_char;
    vector<set<char>> v_set;
    for(int i=0;i<g->num_vertex;i++)
        for(int j=0;j<g->num_vertex;j++)
        {
            if(vv[i][j] != 0 &&vv[i][j] != init_value)
                mm_char[make_pair(locate(g,i),locate(g,j))] = vv[i][j];
        }
    sort(mm_char.begin(),mm_char.end(),min_edge);
    while(result.size() != g->num_vertex)
    {
        map<pair<char,char>,int>::iterator t = mm_char.begin();
        auto  item =  *t;
        char c1 = *t.first.first;
        char c2 = *t.first.second;
        if(find_set(v_set,c1,c2) == 0)
        {
            set<char> s0;
            s0.insert(s0.begin(),c1);
            s0.insert(s0.begin(),c1);
            v_set.push_back(s0);
        }
        if(find_set(v_set,c1,c2) == 1)
            c1,c2加入旧的set中
        if(find_set(v_set,c1,c2) == 2)
            c1,c2分别加入旧的set1，旧的set2
    }
}

四、拓扑排序

五、关键路径

六、最短路径


---------------------------------------
1、Word Ladder
输入：
输出：
时间复杂度：
思想：
2、Word Ladder II
输入：
输出：
时间复杂度：
思想：
3、Surrounded Regions
输入：
输出：
时间复杂度：
思想：
4、Palindrome Partitioning
输入：
输出：
时间复杂度：
思想：
5、Unique Paths
输入：
输出：
时间复杂度：
思想：
6、Unique Paths II
输入：
输出：
时间复杂度：
思想：
7、N-Queens
输入：
输出：
时间复杂度：
思想：
8、N-Queens II
输入：
输出：
时间复杂度：
思想：
9、Restore IP Addresses
输入：
输出：
时间复杂度：
思想：
10、Combination Sum
输入：
输出：
时间复杂度：
思想：
11、Combination Sum II
输入：
输出：
时间复杂度：
思想：
12、Generate Parentheses
输入：
输出：
时间复杂度：
思想：
13、Sudoku Solver
输入：
输出：
时间复杂度：
思想：
14、Word Sear
输入：
输出：
时间复杂度：
思想：