
LeetCode题解整理版(一)

本篇题解中共55题，都是用C++写的，按照Leetcode上的顺序从上向下。可以用CTRL+F查找，如果没有的话就在题解二中。
Evaluate Reverse Polish Notation

逆波兰表达式求值，经典问题。
遇到数字入栈，遇到符号取栈顶的两个出来运算，再将结果入栈，最后栈里剩下的一个元素就是结果了。

class Solution {
public:
    int evalRPN(vector<string> &tokens) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        stack<int> st;
        for (auto &s: tokens) {
            if (s.length() > 1 || isdigit(s[0])) st.push(stoi(s));
            else {
                int num1 = st.top(); st.pop();
                int num2 = st.top(); st.pop();
                if (s[0] == '+') num2 += num1;
                if (s[0] == '-') num2 -= num1;
                if (s[0] == '*') num2 *= num1;
                if (s[0] == '/') num2 /= num1;
                st.push(num2);
            }
        }
        return st.top();
    }
};

Max Points on a Line

求经过点最多的直线。
没想到什么好算法，枚举每个点，其它点以它为原点按斜率排序（我这里直接用MAP了，复杂度是一样的），复杂度O(n^2*logn)。这道题trick比较多，注意无斜率以及点重合的情况。

	

/**
 * Definition for a point.
 * struct Point {
 *     int x;
 *     int y;
 *     Point() : x(0), y(0) {}
 *     Point(int a, int b) : x(a), y(b) {}
 * };
 */
class Solution {
public:
    int maxPoints(vector<Point> &points) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        int size = points.size();
        int ans = 0, horz, same;
        map<double, int> mp;
        map<double, int>::iterator it;
        for (int i = 0; i < size; i++) {
            mp.clear(); horz = same = 0;
            for (int j = 0; j < points.size(); j++) {
                if (points[j].x == points[i].x && points[j].y == points[i].y) same++;
                else if (points[j].x == points[i].x) horz ++;
                else mp[(points[j].y-points[i].y)*1.0/(points[j].x-points[i].x)]++;
            }
            if (horz + same > ans) ans = horz + same;
            for (it = mp.begin(); it != mp.end(); it++)
                if (it->second + same > ans) ans = it->second + same;
        }
        return ans;
    }
};

Sort List

在常数空间内使用O(nlogn)时间复杂度算法对链表排序。
这题写了蛮久的，首先选择排序方法，因为链表不能够随机访问，可以想到使用归并排序，由此问题简化为如何对两个有序链表进行合并。常规的归并排序需要额外的空间来存排序好的数组，而这里因为是指针，我们只要将上一个排序好的节点的next指针指到当前两个链表中较小的节点即可，这样就不在需要额外空间了。这里有一个问题，递归中我们分别处理两段的时候，这两段链表中间的指针的next可以随便改，但是头尾指针的位置是不能改的，否则在左右两段递归出来后就可能不是一个完整的链表了。我这里的处理方法比较笨拙，强制左链表第一个端点是最小的值，而后面只处理到右端点的前一个（左递归处理的是l~m-1，右递归处理的是m~r-1，一开始传进去的r是NULL）。


class Solution {
public:
    ListNode *sortList(ListNode *head) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        if (head == NULL) return head;
        ListNode *tail = head;
        int size = 0;
        for (; tail!= NULL; tail = tail->next, size++);
        MergeSort(head, tail, size);
        return head;
    }
    void MergeSort(ListNode *l, ListNode *r, int size) {
        if (l->next == r) return;
        ListNode *m = l;
        for (int i = 0; i < size / 2; i++, m = m->next);
        MergeSort(l, m, size / 2);
        MergeSort(m, r, size - size / 2);
        ListNode *lp = l, *rp = m, *s;
        if (l->val > m-> val) {
            swap(l->val, m->val);
            for (ListNode *t = m; t->next != r && t->val > t->next->val;
                swap(t->val, t->next->val), t = t->next);
        }
        s = lp, lp = lp->next;
        for (int i = 1; i < size; i++) {
            if (rp == r || (lp !=m && lp->val < rp->val))
                s->next = lp, lp = lp->next;
            else
                s->next = rp, rp = rp->next;
            s = s->next;
        }
        s->next = r;
    }
    void swap (int &x, int &y) {
        x^=y^=x^=y;
    }
};

Insertion Sort List

不使用值交换实现插入排序
插入排序就是不断将值插入到一个有序数组中，我这里新建了一个链表作为有序链表，插入的节点依次比较到下一个节点比它大即可插入。

class Solution {
public:
    ListNode *insertionSortList(ListNode *head) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        if (head == NULL) return head;
        ListNode *newHead = new ListNode(0);
        ListNode *nextHead = head->next, *now;
        newHead->next = head, head->next = NULL;
        while (nextHead != NULL){
            now = nextHead, nextHead = nextHead->next;
            for (ListNode *h = newHead; h != NULL; h = h->next) {
                if (h->next == NULL || now->val < h->next->val) {
                    ListNode *tmp = h->next;
                    h->next = now, now->next = tmp;
                    break;
                }
            }
        }
        head = newHead->next;
        delete newHead;
        return head;
    }
};

LRU Cache

LRU缓存算法实现，这个算法就是在缓存已满时，将最久未使用的元素移出缓存。
经典实现就是双向链表加哈希，每次使用(get or set)都使用哈希值找到这个元素在双链表中的位置，然后将它移到最前面，如果缓存已满就删除队尾的元素。哈希中放的是元素的地址，在新增、移动和删除元素的时候都要在Hash表中作对应修改，而双向链表主要是为了方便删除。

class Node{
public:
    int key, val;
    Node *pre, *next;
    Node(int k, int v): key(k), val(v), pre(NULL), next(NULL) {}
};
class LRUCache{
    map<int, Node*> mp;
    map<int, Node*>::iterator iter;
    int used, cap;
    Node *head, *tail;
public:
    LRUCache(int capacity) {
        mp.clear();
        used = 0, cap = capacity;
        head = new Node(0, 0);
        tail = new Node(0, 0);
        head->next = tail, tail->pre = head;
    }
    ~LRUCache(){
        for (Node *n = head, *nnext; n; n = nnext) {
            nnext = n->next;
            delete n;
        }
    }
    int get(int key) {
        if ((iter = mp.find(key)) != mp.end()) {
            movetoFirst(iter->second);
            return iter->second->val;
        }else
            return -1;
    }
    void set(int key, int value) {
        if ((iter = mp.find(key)) != mp.end()) {
            iter->second->val = value;
            movetoFirst(iter->second);
        } else {
            Node *node;
            if (used == cap) {
                mp.erase(tail->pre->key);
                node = tail->pre;
                node->key = key, node->val = value;
            } else {
                node = new Node(key, value);
                used++;
            }
            mp[node->key] = node;
            movetoFirst(node);
        }
    }
    void movetoFirst(Node *node) {
        if (node->pre && node->next) {
            node->pre->next = node->next;
            node->next->pre = node->pre;
        }
        node->pre = head, node->next = head->next;
        head->next->pre = node, head->next = node;
    }
};

Binary Tree Postorder Traversal
Binary Tree Preorder Traversal

二叉树的非递归遍历
这两道题见博文另一种二叉树非递归遍历的实现，里面对我自己的算法和传统非递归算法都进行了实现。
Reorder List

将链表L0→L1→…→Ln-1→Ln转变成L0→Ln→L1→Ln-1→L2→Ln-2，不能使用额外空间。
将后半部分链表倒置，然后轮流合并即可。

class Solution {
public:
    void reorderList(ListNode *head) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        int len = 0, i;
        ListNode *p, *last, *pnext, *tmp;
        for (p = head; p; p = p->next, len++);
        if (len <= 2) return;
        for (p = head, i = 0; i < len/2; p = p->next, i++);
        tmp = p, p = p->next, tmp->next = NULL;
        for (pnext = p->next, p->next = NULL; pnext;) {
            tmp = pnext;
            pnext = pnext->next;
            tmp->next = p;
            p = tmp;
        }
        last = p;
        for (p = head; p; p = tmp){
            tmp = p->next;
            if (last) {
                p->next = last;
                last = last->next;
                p->next->next = tmp;
            }
        }
    }
};

Linked List Cycle

判断一个链表是否有环(Q形，圈圈拖个尾巴)。
两个指针，一个一次走一步，一个一次走两步，如果有圈必然会相遇。（都进圈后相当于追及问题，一次追一步，必然会追上而且不会错过）。



class Solution {
public:
    bool hasCycle(ListNode *head) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        ListNode *h1, *h2;
        for(h1 = h2 = head; h1 && h2;){
            if (!h1->next || !h2->next || !h2->next->next)
                return false;
            h1 = h1->next;
            h2 = h2->next->next;
            if (h1 == h2 && h1) return true;
        }
        return false;
    }
};

Linked List Cycle II

找到入环指针，就是Q形链表从尾巴进入O之后的第一个指针。
首先按照前一题的做法走到重合，这时再让其中一个指针回到起点，两者重新开始每次走一步，最后相遇的地方就是交点。为什么呢？假设尾巴长度为x，慢指针进入圈后走了一段弧长y，则第一次重合时，慢指针走了x+y。而快指针除了走了x+y外，还多绕了几个圈（假设多走了长度z），设圈的长度为k，则必有z=nk。快指针走的路程是慢指针的两倍，所以x+y+nk=2(x+y)，即nk=x+y。这时都回到起点，起点指针走了x步后到达交点，而这时另一个指针走了x=nk-y后也必然在交点。


class Solution {
public:
    ListNode *detectCycle(ListNode *head) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        ListNode *h1, *h2;
        for(h1 = h2 = head; h1 && h2;){
            if (!h1->next || !h2->next || !h2->next->next)
                return false;
            h1 = h1->next;
            h2 = h2->next->next;
            if (h1 == h2 && h1) break;
        }
        if (!h1 || !h2) return NULL;
        h2 = head;
        while(h1 != h2) h1 = h1->next, h2 = h2->next;
        return h1;
    }
};

Word Break

判断一个字符串是否可以拆成字典里的词。
DP，假设原串为s[1..n]，用d[i][j]表示s[i..j]是否可以有字典里的词组成，有DP方程 d[i][j] = true if (d[i][k]&&d[k+1][j] == true,i<=k<j)
我写的是记忆化搜索，复杂度O（n^3）。


class Solution {
public:
    bool wordBreak(string s, unordered_set<string> &dict) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        vector<vector<int> > dp(s.length(), vector<int>(s.length(), -1));
        return dpit(dp, s, dict, 0, s.length() - 1);
    }
    bool dpit(vector<vector<int> > &dp, string &s, unordered_set<string> &dict, int l, int r) {
        if (dp[l][r] != -1) return dp[l][r];
        if (dict.find(s.substr(l, r - l + 1)) != dict.end()) return dp[l][r] = 1;
        for (int i = l; i < r; i++) {
            if (dpit(dp, s, dict, l, i) && dpit(dp, s, dict, i+1, r))
                return dp[l][r] = 1;
        }
        return dp[l][r] = 0;
    }
};

Word Break II

上一题的加强版，需要给出所有可能的拆词方法。
要找出所有的拆词方法，DFS是避免不了的，但是需要剪枝来优化。
剪枝一：假设原串是s[1...n]，我们用dp[i][j]=k,k>0表示s[i..j]是字典中的第k个串，这里暴力就可以了，复杂度是O(∑(n+m[k]))，m[k]表示第字典中第k个串的长度，这样在搜索的时候，可以快速判断s[i..j]是否在字典中，以及是字典中的哪一个词。
剪枝二：在搜索的时候，如果知道s[i...n]不能由字典中的词组成，就没必要往下搜了，这里可以用上一题的方法来DP，dp[i][j]=0表示不可以。

PS：其实这一题可以构造出有2^(n-1)个解的数据，令s="a..a",dict={"a","aa","aaa",...,"a..a"}即可，这组数据无法在多项式时间内求解。


class Solution {
public:
    vector<string> strRes;
    vector<int> seqRes;
    vector<string> setVec;
    vector<string> wordBreak(string s, unordered_set<string> &dict) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        unordered_set<string>::iterator iter;
        vector<vector<int> > dp(s.length(), vector<int>(s.length(), -1));
        setVec.clear();
        strRes.clear();
        seqRes.clear();
        for (string ds: dict) {
            setVec.push_back(ds);
            int pos = 0;
            while ((pos = s.find(ds, pos)) != string::npos)
                dp[pos][pos+ds.length()-1] = setVec.size(), pos ++;
        }
        dfs_result(dp, 0, s.length()-1);
        return strRes;
    }
    void dfs_result(vector<vector<int> > &dp, int s, int e) {
        if (s > e) {
            string s;
            for (int i = 0; i < seqRes.size(); i++) {
                s.append(setVec[seqRes[i] - 1]);
                if (i != seqRes.size() - 1) s.append(" ");
            }
            strRes.push_back(s);
            return;
        }
        if (dpit(dp, s, e) == 0) return;
        for (int i = s; i <= e; i++) {
            if (dp[s][i] > 0) {
                seqRes.push_back(dp[s][i]);
                dfs_result(dp, i + 1, e);
                seqRes.pop_back();
            }
        }
    }
    int dpit(vector<vector<int> > &dp, int l, int r) {
        if (dp[l][r] != -1) return dp[l][r];
        for (int i = l; i < r; i++) {
            if (dpit(dp, l, i) && dpit(dp, i+1, r))
                return dp[l][r] = -2;
        }
        return dp[l][r] = 0;
    }
};

Copy List with Random Pointer

深拷贝一个链表，这个链表中除了next指针外，还有一个random指针指向链表中的某个节点。
当然，可以Hash原链表和新链表的地址来做，这样没有什么难度，我想到了一种不使用额外空间的做法。
用a表示原链表，b表示拷贝链表，a[i],b[i]分别表示a和b中的第i个节点。下面这段话可能比较绕，但是自己画一下应该很容易明白。
首先第一遍遍历new出b[1]->b[n]，并将b[i]放在a[i]->random中,a[i]->random放在b[i]->next中。然后第二遍遍历将b[i]->random指向b[i]->next->random（b[i]->next放的实际是a[i]->random，假设a[j]=a[i]->random，那b[i]->next->random中放的正是b[j]的地址！），这样就完成了b[i]->random=b[j]。最后，现在a[i]->next和b[i]->random都是正确的，而a[i]->random存在b[i]->next中，b[i]->next也可以通过a[i]->next->random得到，所以遍历一遍就可以将a和b都修复了。



class Solution {
public:
    RandomListNode *copyRandomList(RandomListNode *head) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        if (!head) return NULL;
        RandomListNode *bhead, *anow, *bnow;
        for (anow = head; anow; anow = anow->next) {
            bnow = new RandomListNode(anow->label);
            bnow->next = anow->random;
            anow->random = bnow;
        }
        for(anow = head; anow; anow = anow->next) {
            bnow = anow->random;
            bnow->random = bnow->next?bnow->next->random:NULL;
        }
        bhead = head->random;
        for(anow = head; anow; anow = anow->next) {
            bnow = anow->random;
            anow->random = bnow->next;
            bnow->next = anow->next?anow->next->random:NULL;
        }
        return bhead;
    }
};

Single Number

找出只出现了一次的数，其它数都出现两次
根据x^x=0以及x^y=y^x（交换律）,只要将所有数异或就完了。


class Solution {
public:
    int singleNumber(int A[], int n) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        int x = 0;
        while (--n >= 0) x ^= A[n];
        return x;
    }
};

Single Number II

找出只出现了一次的数，其它数都出现三次
上一题的扩展，其实上一题也可以这么想，将每个数看做一个32位的二进制数，统计每一位出现1的个数，假设某个数出现两次，那就为它为1的位每个位贡献了两次。如果每个数都是两个，那每位出现1的个数必然是偶数个，假设有一个位上的1出现了奇数次，那必然有一个只出现了一次的数贡献了一个1，所以只要找到哪些位1出现了奇数次就可以找到这个数了。也是基于这种思想才用异或操作来实现的。
这一题虽然不能用异或操作来实现，但是还是可以根据上面这种思想来解。找出哪些位出现了3n+1次即可。我这里用位运算来实现的，x[0]表示出现3n+1 or 3n+2次的，x[1]表示出现3n+2次的，x[2]表示出现了3n次的。


class Solution {
public:
    int singleNumber(int A[], int n) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        int x[3] = {0};
        while (--n >= 0) {
            x[2] = x[1] & A[n];
            x[1] |= x[0] & A[n];
            x[0] |= A[n];
            x[0] &= ~x[2], x[1] &= ~x[2];
        }
        return x[0];
    }
};

Candy

已知a[1..n]，给b[1..n]分配值，需满足若a[i]>a[j]则b[i]>b[j]>0。求min∑b。
很简单，找到所有满足a[i]<=a[i+1]且a[i]<=a[i-1]的点，都取b[i]=1，然后沿着两边递增加1直到波峰即可。需要注意波峰可能会被两边上来的更新，要取较大的。
总的复杂度O(n)。



class Solution {
public:
    int candy(vector<int> &ratings) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        int size = ratings.size(), ans = 0;
        if (size == 1) return 1;
        vector<int> candies(size, 1);
        for (int i = 0; i < size; i++) {
            if (i == 0 && ratings[i] <= ratings[i + 1] ||
                i == size - 1 && ratings[i] <= ratings[i - 1] ||
                ratings[i] <= ratings[i + 1] && ratings[i] <= ratings[i - 1]) {
                for (int j = i - 1; j >=0 && ratings[j] > ratings[j + 1]; j--)
                    candies[j] = max(candies[j], candies[j + 1] + 1);
                for (int j = i + 1; j < size && ratings[j] > ratings[j - 1]; j++)
                    candies[j] = max(candies[j], candies[j - 1] + 1);
            }
        }
        //for (int i = 0; i < size; i++) printf("%d ", candies[i]);
        for (int i = 0; i < size; i++) ans += candies[i];
        return ans;
    }
};

Gas Station

n个点围成一个圈，1->2..->n->1，到达i点可以加油gas[i]，i到i+1点需要花费cost[i]，求是否能找到一个起点保证有油转一整圈。
这题还真的想了很久，想的比较复杂，其实正确的解法非常简单，我们可以依次推出以下两个结论。
结论一：我们用d[i][j]表示从i出发到j后剩余的油量，也就是sum(gas[i]..gas[j-1])-sum(cost[i]..cost[j-1])，假设依次有i,j,k三个点，如果i->k可以保持油量一直为正，并且j->k也可以保持油量一直为正，那么选择j做起点一定不如选择i做起点好，因为d[i][k]= d[i][j]+d[j][k]>d[j][k]。

根据结论一，我们假如从i点出发，到达j点后无法到达j+1点，那么i~j点都不可能作为起点，因为从这之间的任一一点出发到达j点后剩的油都不会比从i出发剩的多。
而下一个最佳起点必然选j+1，因为假设j+1之后有点k，那么选j+2到~k之间的任一一点都不会比j+1好，原因同上。

结论二：如果总的gas大于总的cost，则必然有解。根据以上方法我们会不断更新最佳起点，假设这个序列是k1,k2..kn，有d[k1][k2]<0,d[k2][k3]<0…最后到达kn，我们知道kn必然是可以到达k1的，根据总gas大于总cost，有d[kn][k1]+d[k1][k2]+..+d[k(n-1)][kn]>0，于是d[kn][k1-1]>-(d[k1][k2-1]+..+d[kn-1][kn])，也就是说从kn走到k1后多的油量足够经过之前那些不能经过的点最终回到kn了。
根据以上两个结论，我们可以知道当总gas大于总cost时，kn必然是一个可行解。



class Solution {
public:
    int canCompleteCircuit(vector<int> &gas, vector<int> &cost) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        int remain = 0, totgas = 0, startp = 0;
        for (int i = 0; i < gas.size(); i++) {
            remain += gas[i] - cost[i];
            totgas += gas[i] - cost[i];
            if (remain < 0) remain = 0, startp = i + 1;
        }
        startp %= gas.size();
        return totgas >= 0 ? startp : -1;
    }
};

Clone Graph

clone一张图
将原图NODE和新图NODE之间的地址MAP映射一下，然后就是遍历原图邻接表建新图就可以了。

#define UNODE UndirectedGraphNode
class Solution {
public:
    map<UNODE*, UNODE*>::iterator iter;
    UndirectedGraphNode *cloneGraph(UndirectedGraphNode *node) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        map<UNODE*, UNODE* > nodeMap;
        if (node == NULL) return node;
        UNODE *nnode = new UNODE(node->label);
        nodeMap[node] = nnode;
        dfsGraph(nodeMap, node, nnode);
        return nnode;
    }
    void dfsGraph(map<UNODE*, UNODE*> &nodeMap, UNODE *node, UNODE *nnode) {
        for (int i = 0; i < node->neighbors.size(); i++) {
            UNODE *now = node->neighbors[i];
            if ((iter = nodeMap.find(now)) != nodeMap.end()) {
                 nnode->neighbors.push_back(iter->second);
            } else {
                UNODE *nnow = new UNODE(now->label);
                nodeMap[now] = nnow;
                nnode->neighbors.push_back(nnow);
                dfsGraph(nodeMap, now, nnow);
            }
        }
    }
};

Palindrome Partitioning

划分一个字符串为，使每个子串都是回文串，返回所有划分
这种所有划分的必然要DFS了，只是要进行适当的剪枝。
预处理字符串，找出所有回文串，枚举对称轴，O(n^2)的算法。我这里用vector[i]存了所有以第i个字符开头的回文串，然后DFS到第i位的时候，只要枚举vector[i]中的字符串就可以了。


class Solution {
public:
    vector<vector<string> > vecResult;
    vector<vector<string> > partition(string s) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        vecResult.clear();
        vector<string> vecStr;
        vector<vector<string> > parStart(s.length());
        for (int i = 0; i < s.length(); i++) {
            for (int j = i; 2*i-j < s.length() && j >= 0 && s[j] == s[2*i-j]; j--)
                parStart[j].push_back(s.substr(j, 2*i-2*j+1));
            for (int j = i; 2*i-j+1 < s.length() && j >= 0 && s[j] == s[2*i-j+1]; j--)
                parStart[j].push_back(s.substr(j, 2*i-2*j+2));
        }
        dfs(parStart, vecStr, 0, s.length());
        return vecResult;
    }
    void dfs(vector<vector<string> > &parStart, vector<string> &vecStr, int sp, int ep) {
        if (sp == ep) {
            vecResult.push_back(vecStr);
        } else {
            for (int i = 0; i < parStart[sp].size(); i++) {
                vecStr.push_back(parStart[sp][i]);
                dfs(parStart, vecStr, sp + parStart[sp][i].length(), ep);
                vecStr.pop_back();
            }
        }
    }
};

Palindrome Partitioning II

划分一个字符串，使每个子串都是回文串，要求划分次数最少
DP，用minC[i]表示s[1..i]需要几刀，显然minC[i]最大是i。DP方程
minC[i] = min(i, minC[j]+1)(1<=j<=i&&isPar[j+1][i])，isPar[i][j]在DP的过程中可以顺便求出来，isPar[i][j] = true if (isPar[i+1][j-1]&&s[i]==s[j])。
总的复杂度O(n^2)。


class Solution {
public:
    int minCut(string s) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        vector<vector<bool> > isPar(s.length(), vector<bool>(s.length(), false));
        vector<int> minC(s.length(), 0);
        for (int i = 0; i < s.length(); i++) {
            minC[i] = i + 1;
            for (int j = 0; j <= i; j++) {
                if ((j + 2 > i || isPar[j+1][i-1]) && s[j] == s[i]) {
                    isPar[j][i] = true;
                    minC[i] = min(minC[i], j ? (minC[j-1] + 1) : 1);
                }
            }
        }
        return minC[s.length() - 1] - 1;
    }
};

Surrounded Regions

给一个n*m的由X和O组成的矩阵，要求把那些被X包围的O变成X。
如果有一块O其中的一个或多个接触到了外边界，就不用变成X，所以从接触边缘的O开始BFS即可，BFS到的点都不用变X。我这里用Y表示一个点原本是O并且所在块没有被X全包围。最后除了Y点其它点都变成X即可。


class Solution {
public:
    void solve(vector<vector<char> > &board) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        queue<pair<int, int> > q;
        int dx[] = {1, -1, 0, 0}, dy[] = {0, 0, 1, -1};
        if (board.size() == 0) return ;
        int lenh = board.size(), lenw = board[0].size();
        for (int i = 0; i < lenh; i++)
            for (int j = 0; j < lenw; j++)
                if ((i == 0 || j == 0 || i == lenh - 1 || j == lenw - 1)
                        && board[i][j] == 'O') {
                    board[i][j] = 'Y';
                    q.push(make_pair(i, j));
                }
        while (!q.empty()) {
            pair<int, int> p = q.front(); q.pop();
            for (int i = 0; i < 4; i++) {
                int ni = p.first + dx[i], nj = p.second + dy[i];
                if (ni >= 0 && ni < lenh && nj >= 0 && nj < lenw
                    && board[ni][nj] == 'O') {
                    board[ni][nj] = 'Y';
                    q.push(make_pair(ni, nj));
                }
            }
        }
        for (int i = 0; i < lenh; i++)
            for (int j = 0; j < lenw; j++)
                board[i][j] = (board[i][j] == 'Y' ? 'O' : 'X');
    }
};

Sum Root to Leaf Numbers

从根到叶的每条路径构成一个数，求这些数的和。
直接DFS，每次到叶子时加就可以了。其实随便一条路径长度超过9结果就超int了，想LeetCode OJ上还不至于要写BigInteger，随便用int写下果然过了。。



class Solution {
public:
    int sumNumbers(TreeNode *root) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        int ans = 0;
        if (!root) return 0;
        dfsTree(root, root->val, ans);
        return ans;
    }
    void dfsTree(TreeNode *fa, int now, int &ans) {
        if (!(fa->left || fa->right)) ans += now;
        else {
            if (fa->left) dfsTree(fa->left, now*10+fa->left->val, ans);
            if (fa->right)dfsTree(fa->right,now*10+fa->right->val,ans);
        }
    }
};

Longest Consecutive Sequence

再一个数组中挑出一些连续的数，求最多能挑出多少
想来想去也只能Hash了，把所有数都放到Hash里，重复的算一个就行。然后随意拿出一个数，以它为中心依次找比它大一的数以及小一的数，找到就擦除，然后记录它所在序列的长度。重复操作直到set为空为止。
感谢unordered_set，要不然还得自己写Hash。(直接用原来的set是O(nlogn)。)

	
class Solution {
public:
    int longestConsecutive(vector<int> &num) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        unordered_set<int> uset;
        for (int i = 0; i < num.size(); i++)
            uset.insert(num[i]);
        int ans = 0, tmpAns = 0, now, nowb;
        while (!uset.empty()) {
            now = *uset.begin(), tmpAns = 1;
            uset.erase(now);
            for (nowb = now + 1; uset.count(nowb); uset.erase(nowb), tmpAns++, nowb++);
            for (nowb = now - 1; uset.count(nowb); uset.erase(nowb), tmpAns++, nowb--);
            if (tmpAns > ans) ans = tmpAns;
        }
        return ans;
    }
};

Word Ladder

给出字符串S，T以及一个词典，这些字符串长度均为N，每次可以修改S中的一个字母让它变为词典中的某个词，求从S到T最少要几步。
边权为一的最短路，显然是BFS，我一开始使用N^2枚举建图超时了，这样复杂度是O(N^2*len)。后来想一下如果N很大的话，不如枚举改变每个字母是否可以变成字典中的某个词，复杂读是O(N*len*26)。


class Solution {
public:
    int ladderLength(string start, string end, unordered_set<string> &dict) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        queue<string> q;
        unordered_map<string, int> vis;
        int len = start.length();
        q.push(start);
        vis[start] = 1;
        while (!q.empty()) {
            string s = q.front(); q.pop();
            int step = vis[s];
            for (int i = 0; i < len; i++) {
                string news = s;
                for (char c = 'a'; c <= 'z'; c++) {
                    if (s[i] == c) continue;
                    news[i] = c;
                    if (news == end) return step + 1;
                    if (dict.count(news) && !vis[news]) {
                        vis[news] = step + 1;
                        q.push(news);
                    }
                }
            }
        }
        return 0;
    }
};

Word Ladder II

同上，只是要打印出所有最短路径。
打印所有结果必然要DFS，重点是剪枝。
我们称在最短路径中第N次转化后得到的字符串在第N层，可以证明，如果一个字符串在最短转化A中处于第N层，那么它在最短转化B中也处于第N层，否则A和B必然有一个不是最短转化，另外，如果第N层的a节点，可以转化为N+1层的b和c节点，那么a无论走b和c，只要最后能到目标字符串，都必然是最短路。也就是说，在BFS出的树形结构中，我们可以加一些树枝表示其它最短转化的路径，但这些树枝肯定只会连接第N～N+1层的点。所以我们先BFS一遍，用邻接表的形式存从图，每次第一次扫描到一个点时记录这个点的所在层次。这样构造了图并记录了每个点的所在层次。
之后再从起点开始DFS,但是在相邻的点中，只走层次比自己大一的点，最后每次走到终点时将路径存入结果集即可。


class Solution {
public:
    vector<vector<string> > ans;
    vector<vector<string> > findLadders(string start, string end, unordered_set<string> &dict) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        dict.insert(end);
        int dsize = dict.size(), len = start.length();
        unordered_map<string, vector<string> > next;
        unordered_map<string, int> vis;
        queue<string> q;
        vector<string> path;
        ans.clear();
        q.push(start);
        vis[start] = 0;
        while (!q.empty()) {
            string s = q.front(); q.pop();
            if (s == end) break;
            int step = vis[s];
            vector<string> snext;
            for (int i = 0; i < len; i++) {
                string news = s;
                for (char c = 'a'; c <= 'z'; c++) {
                    news[i] = c;
                    if (c == s[i] || dict.find(news) == dict.end()) continue;
                    auto it = vis.find(news);
                    if (it == vis.end()) {
                        q.push(news);
                        vis[news] = step + 1;
                    }
                    snext.push_back(news);
                }
            }
            next[s] = snext;
        }
        path.push_back(start);
        dfspath(path, next, vis, start, end);
        return ans;
    }
    void dfspath(vector<string> &path,  unordered_map<string, vector<string> > &next,
                 unordered_map<string, int> &vis, string now, string end){
       //cout << now << endl;
        if (now == end) ans.push_back(path);
        else {
            auto vec = next[now];
            int visn = vis[now];
            for (int i = 0; i < vec.size(); i++) {
                if (vis[vec[i]] != visn + 1) continue;
                path.push_back(vec[i]);
                dfspath(path, next, vis, vec[i], end);
                path.pop_back();
            }
        }
    }
};

Valid Palindrome

判断是否是回文串。
注意只有大小写字母和数字才算作串的内容，其它字符都跳过。左右两个指针逐渐往中间逼近就可以了。


class Solution {
public:
    bool isPalindrome(string s) {
        // IMPORTANT: Please reset any member data you declared, as
        // the same Solution instance will be reused for each test case.
        int len = s.length(), l = 0, r = len - 1;
        while (l < r) {
            if (!isalnum(s[l])) l++;
            else if (!isalnum(s[r])) r--;
            else if (tolower(s[l]) == tolower(s[r])) l++, r--;
            else return false;
        }
        return true;
    }
};

Binary Tree Maximum Path Sum

在二叉树中找一条路径，路径上点和加起来最大，求最大值。
树形DP。首先应该知道最近公共祖先的概念，所谓最近公共祖先，就是从两个点(u,v)分别向根走，相遇的第一个点(s)，记为LCA(u,v)=s，那么最大权路径可以记为u~s~v，其中u~s从s的左子树上来，v~s从v的右子树上来，当然s可能等于u或者v。
然后我们用dp[x]记录以x为一个端点向下走，最大能走多少。为了公式写起来方便，先假设节点的权值都大于0。当我们走到某个点x时，有可能x就是最大权路径中的s点，那么构造出来的最长路径就是dp[x[left]->val]+dp[x[right]->val]+x->val，之后求出dp[x]并往上传，dp[x]=x->val+max(dp[x[left]->val],dp[x[right]->val])。当DP回根节点的时候，我们已经枚举了每个节点作为s时的最大权路径，取其中最大的作为结果。
注意如果有节点权值为负值，那么某个dp[x]可能为负，就是说宁愿不走，算做0就可以了。


class Solution {
public:
    int maxPathSum(TreeNode *root) {
        int ans = root->val;
        dfsTree(root, ans);
        return ans;
    }
    int dfsTree(TreeNode *fa, int &ans) {
        if (fa == NULL) return 0;
        int tmp = fa->val, lmax, rmax;
        if ((lmax = dfsTree(fa->left, ans)) > 0) tmp += lmax;
        if ((rmax = dfsTree(fa->right, ans)) > 0) tmp += rmax;
        ans = max(ans, tmp);
        return max(fa->val, max(fa->val+lmax, fa->val+rmax));
    }
};

Best Time to Buy and Sell Stock

石头的价格每天不同，可以选择一天买进，在之后某一天卖出，求最大收益。全程只能交易一次。
记录到i为止最低的价格，算出当天卖出的最大收益，然后取最大的就可以了。


class Solution {
public:
    int maxProfit(vector<int> &prices) {
        if (prices.size() == 0) return 0;
        int ans = 0, minv = prices[0];
        for (int i = 1; i < prices.size(); i++) {
            ans = max(ans, prices[i] - minv);
            minv = min(minv, prices[i]);
        }
        return ans;
    }
};

Best Time to Buy and Sell Stock II

与上面题面相同，只是不限买卖次数，但同一时刻只能持有一个石头。
贪心，记录之前最低的价格，遇到比最低价格高就卖。并从当前开始继续记录最低价格。
这题我并没有证明，只是想了几种情况，觉的是正确的（贪心题往往都是这样。。）。


class Solution {
public:
    int maxProfit(vector<int> &prices) {
        if (prices.size() == 0) return 0;
        int minv = prices[0], ans = 0;
        for (int i = 1; i < prices.size(); i++) {
            if (prices[i] > minv)
                ans += prices[i] - minv, minv = prices[i];
            minv = min(minv, prices[i]);
        }
        return ans;
    }
};

Best Time to Buy and Sell Stock III

题面与上题一样，买卖次数最多为两次，同一时刻只能持有一个石头。
Stock1里，我们从前向后依次能求出当天卖出一颗石头的最大收益pre[i]，同理，我们也能从后向前依次求出当天买入一颗石头能得到的最大收益last[i]，再用maxlast[i]=max(last[k](i<=k<=n))表示从i~n天内买入一颗石头的最大收益，所以，ans=max(pre[i]+maxlast[i])(1<=i<=n)，就是说再第i天完成第一笔交易，并在第i天之后的某一天完成第二笔交易。
总的复杂度O(n)（程序中第二次for循环的minv实际上是指从后面到当前的最大值）。


class Solution {
public:
    int maxProfit(vector<int> &prices) {
        int size = prices.size(), ans = 0;
        if (size <= 1) return 0;
        vector<int> p(size, 0);
        int minv = prices[0], maxv;
        for (int i = 1; i < size; i++)
            p[i] = prices[i] - minv,
            minv = min(prices[i], minv);
        ans = max(ans, p[size-1]);
        minv = prices[size-1], maxv = 0;
        for (int i = size-2; i >= 0; i--)
            maxv = max(maxv, minv - prices[i]),
            ans = max(ans, p[i] + maxv),
            minv = max(prices[i], minv);
        return ans;
    }
};

Triangle

给一个三角形数组，从顶端开始向下走，每次可以走到旁边的两个，直到底端为止，使路径上的数的和最小。
很经典的DP了，从下向上，每次可以从左下或右下上来，记录到当前点的最大值即可。


class Solution {
public:
    int minimumTotal(vector<vector<int> > &triangle) {
        int size = triangle.size();
        vector<int> ans(triangle[size-1]);
        for (int i = size-2; i >= 0; i--) {
            for (int j = 0; j <= i; j++)
                ans[j] = triangle[i][j] + min(ans[j], ans[j+1]);
        }
        return ans[0];
    }
};

Pascal’s Triangle

生成杨辉三角,ans[i][j] = ans[i-1][j-1] + ans[i-1][j]。


class Solution {
public:
    vector<vector<int> > ans;
    vector<vector<int> > generate(int numRows) {
        ans.clear();
        ans.resize(numRows);
        for (int i = 0; i < numRows ;i++) {
            ans[i].resize(i+1);
            ans[i][0] = ans[i][i] = 1;
            for (int j = 1; j < i; j++)
                ans[i][j] = ans[i-1][j-1] + ans[i-1][j];
        }
        return ans;
    }
};

Pascal’s Triangle II

生成杨辉三角第N行，第N行第i项就是二项展开式系数C(N,i)。
而C(N, i)=C(N, i-1)*(N-i+1)/i，递推即可。


class Solution {
public:
    vector<int> ans;
    vector<int> getRow(int rowIndex) {
        ans.resize(rowIndex + 1);
        ans[0] = 1;
        for (int i = 1; i <= rowIndex; i++)
            ans[i] = (long long)ans[i-1] * (rowIndex - i + 1) / i;
        return ans;
    }
};

Populating Next Right Pointers in Each Node

一棵完全二叉树，找到每个节点在这一层右边的点。
直接DFS，将每个点左儿子向右全部指向右儿子向左上对应的节点。比如下图DFS到1时会将2的next指向3，5指向6。


	

         1
       /   \
      2 --> 3
     / \   / \
    4   5->6  7
class Solution {
public:
    void connect(TreeLinkNode *root) {
        if (root == NULL) return;
        connect(root->left);
        connect(root->right);
        for (TreeLinkNode *nl = root->left, *nr = root->right; nl;
            nl->next = nr, nl = nl->right, nr = nr->left);
    }
};

Populating Next Right Pointers in Each Node II

与上题一样，但不是完全二叉树，并且不能用额外空间。
既然不能用额外空间，递归堆栈这些就直接不能用了。只能用上一层已经生成的next指针来逐层生成，代码还是有很多问题要注意的。


class Solution {
public:
    TreeLinkNode *next(TreeLinkNode* p) {
        while (p && !p->left && !p->right) p = p->next;
        return p;
    }
    void connect(TreeLinkNode *root) {
        TreeLinkNode *nextHead, *preHead, *nextPreHead;
        for (TreeLinkNode *head = root; head; preHead = head, head = nextHead) {
            head = next(head);
            if (head != NULL)
                nextHead = head->left ? head->left : head->right;
            else
                break;
            for (preHead = NULL; head; preHead = head, head = next(head->next)) {
                if (head->left && head->right) head->left->next = head->right;
                if (preHead) {
                    nextPreHead = head->left ? head->left : head->right;
                    if (preHead->right == NULL)
                        preHead->left->next = nextPreHead;
                    else
                        preHead->right->next = nextPreHead;
                }
            }
        }
    }
};

Distinct Subsequences

求T作为S的子串出现了多少次(不一定连续出现)
基础DP，dp[i][j]表示T[1..i]作为S[1..j]的子串出现了多少次。


class Solution {
public:
    int numDistinct(string S, string T) {
        int lent = T.length(), lens = S.length();
        vector<vector<int> > dp(lent+1, vector<int>(lens+1, 0));
        for (int i = 0; i <= lens; i++) dp[0][i] = 1;
        for (int i = 1; i <= lent; i++) {
            for (int j = 1; j <= lens; j++) {
                dp[i][j] = dp[i][j-1];
                if (S[j-1] == T[i-1])
                    dp[i][j] += dp[i-1][j-1];
            }
        }
        return dp[lent][lens];
    }
};

Flatten Binary Tree to Linked List

树转链表
前序遍历，顺便把点链到链表上去。


class Solution {
public:
    void flatten(TreeNode *root) {
        now = root;
        dfs(root);
    }
    TreeNode *now;
    void dfs(TreeNode *root) {
        if (!root) return;
        TreeNode *right = root->right;
        if (root->left) {
            now = now->right = root->left;
            dfs(root->left);
        }
        root->left = NULL;
        if (right) {
            now = now->right = right;
            dfs(right);
        }
    }
};

Path Sum

求树上有没有一条从根到叶子的路节点的值加起来为N
DFS，到叶子判断累加值是否等于Sum
	

class Solution {
public:
    bool hasPathSum(TreeNode *root, int sum) {
        return root && dfs(root, 0, sum) ;
    }
    bool dfs(TreeNode *node, int now, int sum) {
        if (node ->left == NULL && node->right == NULL)
            return now + node->val == sum ;
        if (node->left && dfs(node->left, now + node->val, sum)) return true;
        if (node->right && dfs(node->right, now + node->val, sum)) return true;
        return false;
    }
};

Path Sum II

同上，只是要打印所有路径
一样DFS，用一个vector存路径即可


class Solution {
public:
    vector<vector<int> > ans;
    vector<int> path;
    vector<vector<int> > pathSum(TreeNode *root, int sum) {
        ans.clear();
        path.clear();
        if (root) dfs(root, 0, sum) ;
        return ans;
    }
    void dfs(TreeNode *node, int now, int sum) {
        if (node ->left == NULL && node->right == NULL) {
            if (now + node->val == sum) {
                path.push_back(node->val);
                ans.push_back(path);
                path.pop_back();
            }
            return;
        }
        if (node->left) {
            path.push_back(node->val);
            dfs(node->left, now + node->val, sum);
            path.pop_back();
        }
        if (node->right) {
            path.push_back(node->val);
            dfs(node->right, now + node->val, sum);
            path.pop_back();
        }
    }
};

Minimum Depth of Binary Tree

求最近的叶子深度
跟最大长度没什么不一样，注意处理下只有一个儿子的情况即可


class Solution {
public:
    int minDepth(TreeNode *root) {
        if (!root) return 0;
        if (!root->left && !root->right) return 1;
        int ltval = -1, rtval = -1;
        if (root->left) ltval = minDepth(root->left);
        if (root->right) rtval = minDepth(root->right);
        return 1+ (ltval == -1 ? rtval : (rtval == -1 ? ltval : min(ltval, rtval)));
    }
};

Balanced Binary Tree

判断一棵树是否是平衡树，所谓平衡树，是指每个节点的左右孩子最大深度之差不超过1
DFS返回该节点的最大深度，过程中比较左孩子和右孩子为根的子树的最大深度即可。
	

class Solution {
public:
    bool isBalanced(TreeNode *root) {
        bool ans = true;
        dfs(root, ans);
        return ans;
    }
    int dfs(TreeNode *root, bool &ans) {
        if (!root) return 0;
        int ltval = dfs(root->left, ans);
        int rtval = dfs(root->right, ans);
        if (!(ltval - rtval <= 1 && ltval - rtval >= -1))
            ans = false;
        return max(ltval, rtval) + 1;
    }
};

Convert Sorted List to Binary Search Tree

有序链表转平衡二叉树。
要求平衡，一半放左边，一半放右边即可，递归生成。


class Solution {
public:
    TreeNode *sortedListToBST(ListNode *head) {
        int len = 0;
        for (ListNode *p = head; p; p = p->next, len++);
        return dfs(head, len);
    }
    TreeNode *dfs(ListNode *head, int len) {
        if (len <= 0) return NULL;
        int mid = (len + 1) >> 1;
        ListNode *rhead = head;
        for (int i = 1; i < mid; rhead=rhead->next, i++);
        TreeNode *node = new TreeNode(rhead->val);
        node->left = dfs(head, mid - 1);
        node->right = dfs(rhead->next, len - mid);
        return node;
    }
};

Convert Sorted Array to Binary Search Tree

有序数组转平衡二叉树。
和上面一样，而且还不用找中点了，更简单一些


class Solution {
public:
    TreeNode *sortedArrayToBST(vector<int> &num) {
        return dfs(0, num.size()-1, num);
    }
    TreeNode *dfs(int left, int right, vector<int> &num) {
        if (left > right) return NULL;
        int mid = (left + right) >> 1;
        TreeNode *node = new TreeNode(num[mid]);
        node->left = dfs(left, mid-1, num);
        node->right = dfs(mid+1, right, num);
        return node;
    }
};

Binary Tree Level Order Traversal II

记录树的每一层
BFS当然可以，我是直接DFS然后每一层一个vector存该层的数。。
	

class Solution {
public:
    vector<vector<int> > vec;
    vector<vector<int> > levelOrderBottom(TreeNode *root) {
        vec.clear();
        dfs(root, 0, vec);
        reverse(vec.begin(), vec.end());
        return vec;
    }
    void dfs(TreeNode *root, int dep, vector<vector<int> > &vec) {
        if (root == NULL) return;
        if (vec.size() <= dep) vec.push_back(vector<int>());
        vec[dep].push_back(root->val);
        dfs(root->left, dep+1, vec);
        dfs(root->right, dep+1, vec);
    }
};

Construct Binary Tree from Inorder and Postorder Traversal

根据中序和后序序列遍历构造树
数据结构题，后序结构为[left of x][right of x][x]，中序结构为[left of x][x][right of x]，根据这样的结构递归构造即可


class Solution {
public:
    TreeNode *buildTree(vector<int> &inorder, vector<int> &postorder) {
        return build(0, inorder.size()-1, 0, postorder.size()-1, inorder, postorder);
    }
    TreeNode *build(int il, int ir, int pl, int pr, vector<int> &ivec, vector<int> &pvec) {
        if (pl > pr) return NULL;
        TreeNode *node = new TreeNode(pvec[pr]);
        int ip;
        for (ip = il; ip <= ir; ip++) {
            if (ivec[ip] == pvec[pr]) break;
        }
        if (il<=ip-1) node->left = build(il, ip-1, pl, pl+ip-il-1, ivec, pvec);
        if (ip+1<=ir) node->right = build(ip+1, ir, pl+ip-il, pr-1, ivec, pvec);
        return node;
    }
};

Construct Binary Tree from Preorder and Inorder Traversal

根据前序中序遍历序列构造树
数据结构题，前序结构为[x][left of x][right of x]，中序结构为[left of x][x][right of x]，根据这样的结构递归构造即可


class Solution {
public:
    TreeNode *buildTree(vector<int> &preorder, vector<int> &inorder) {
        return build(0, preorder.size()-1, 0, inorder.size()-1, preorder, inorder);
    }
    TreeNode *build(int pl, int pr, int il, int ir, vector<int> &pvec, vector<int> &ivec) {
        if (pl > pr) return NULL;
        TreeNode *node = new TreeNode(pvec[pl]);
        int ip;
        for (ip = il; ip <= ir; ip++) {
            if (ivec[ip] == pvec[pl]) break;
        }
        if (il<=ip-1) node->left = build(pl+1, pl+ip-il, il, ip-1, pvec, ivec);
        if (ip+1<=ir) node->right = build(pl+ip-il+1, pr, ip+1, ir, pvec, ivec);
        return node;
    }
};

Maximum Depth of Binary Tree

树的最大深度
直接DFS返回当前节点最大深度



class Solution {
public:
    int maxDepth(TreeNode *root) {
        if (root == NULL) return 0;
        return 1 + max(maxDepth(root->left), maxDepth(root->right));
    }
};

Binary Tree Zigzag Level Order Traversal

记录树的每一层，跟上面某题一样，就要前后输出顺序依次交替
也是DFS然后vector记录每一层，奇数层reverse一下
	

class Solution {
public:
    vector<vector<int> > vec;
    vector<vector<int> > zigzagLevelOrder(TreeNode *root) {
        vec.clear();
        dfs(root, 0, vec);
        for (int i = 1; i < vec.size(); i += 2)
            reverse(vec[i].begin(), vec[i].end());
        return vec;
    }
    void dfs(TreeNode *root, int dep, vector<vector<int> > &vec) {
        if (root == NULL) return;
        if (vec.size() <= dep) vec.push_back(vector<int>());
        vec[dep].push_back(root->val);
        dfs(root->left, dep+1, vec);
        dfs(root->right, dep+1, vec);
    }
};

Binary Tree Level Order Traversal

还是记录树的每一层，换个输出顺序。。
解法一样，vector记录每一层。。


class Solution {
public:
    vector<vector<int> > vec;
    vector<vector<int> > levelOrder(TreeNode *root) {
        vec.clear();
        dfs(root, 0, vec);
        return vec;
    }
    void dfs(TreeNode *root, int dep, vector<vector<int> > &vec) {
        if (root == NULL) return;
        if (vec.size() <= dep) vec.push_back(vector<int>());
        vec[dep].push_back(root->val);
        dfs(root->left, dep+1, vec);
        dfs(root->right, dep+1, vec);
    }
};

Symmetric Tree

判断一棵树是不是以根为对称轴中心对称的
我是用vector保存下一层的节点，然后从两边向中间依次对比


class Solution {
public:
    bool isSymmetric(TreeNode *root) {
        vector<TreeNode *> now, next;
        if (root) now.push_back(root);
        bool flag = true;
        while(now.size() > 0) {
            next.clear();
            int size = now.size();
            for (int l = 0, r = size - 1; l <= r; l++, r--) {
                if (!nodeeql(now[l]->left, now[r]->right) ||
                    !nodeeql(now[l]->right, now[r]->left))
                    flag = false;
            }
            if (!flag) break;
            for (int i = 0; i < size; i++) {
                if (now[i]->left) next.push_back(now[i]->left);
                if (now[i]->right)next.push_back(now[i]->right);
            }
            now = next;
        }
        return flag;
    }
    bool nodeeql(TreeNode *l1, TreeNode *l2) {
        if ((!l1 && l2) || (l1 && !l2)) return false;
        return !l1 && !l2 || l1->val == l2->val;
    }
};

Same Tree

判断两棵树是否相同
递归比较左子树和右子树了


class Solution {
public:
    bool isSameTree(TreeNode *p, TreeNode *q) {
        if (!p || !q) return !p && !q;
        if (p->val != q->val) return false;
        return isSameTree(p->left, q->left) &&
            isSameTree(p->right, q->right);
    }
};

Unique Binary Search Trees

计算N个节点的树有多少种
经典的DP了，dp[n]表示n个节点的树有dp[n]种，dp方程见代码


class Solution {
public:
    int numTrees(int n) {
        int *dp = new int[n+1];
        for (int i = 0; i <= n; i++)
            dp[i] = (i <= 1 ? 1 : -1);
        return dpit(dp, n);
    }
    int dpit(int dp[], int n) {
        if (dp[n] != -1) return dp[n];
        dp[n] = 0;
        for (int i = 0; i < n; i++)
            dp[n] += dpit(dp, i) * dpit(dp, n-i-1);
        return dp[n];
    }
};

Binary Tree Inorder Traversal

树的中序遍历，数据结构题，简单的遍历其实不容易写好
	

class Solution {
public:
    vector<int> vec;
    vector<int> inorderTraversal(TreeNode *root) {
        stack<TreeNode*> st;
        vec.clear();
        TreeNode *T = root;
        while (T || !st.empty()) {
            if (T) {
                st.push(T);
                T = T->left;
            } else {
                T = st.top(); st.pop();
                vec.push_back(T->val);
                T = T->right;
            }
        }
        return vec;
    }
};

Restore IP Addresses

将一个数字串转化成合法IP
DFS，注意一些细节
	

class Solution {
public:
    vector<string> ans;
    vector<string> restoreIpAddresses(string s) {
        ans.clear();
        dfs(ans, s, "", 0, 0);
        return ans;
    }
    void dfs(vector<string> &ans, string s, string str, int pos, int dep) {
        if (dep >= 4) {
            if (dep == 4 && pos == s.length()) ans.push_back(str);
        } else {
            for (int i = pos; i < s.length(); i++) {
                string sub = s.substr(pos, i-pos+1);
                if (sub.length() <= 3 && stoi(sub) >= 0 && stoi(sub) <= 255 &&
                    to_string(stoi(sub)) == sub) {
                    string common = (dep == 3 ? "": ".");
                    dfs(ans, s, str+sub+common, i+1, dep+1);
                }
            }
        }
    }
};

Simplify Path

对Linux系统下的绝对路径进行简化
以/为分界，以栈来保存每一段，/和/.都没有意义，不用管，/..需要退栈，最后记得栈为空要加上根目录/

class Solution {
public:
    string simplifyPath(string path) {
        //cout << "here" << endl;
        vector<string> resVec;
        string ans = "";
        int pos = 0, rpos;
        while ((rpos = path.find("/", pos+1)) != string::npos) {
            resVec.push_back(path.substr(pos, rpos-pos));
            cal(resVec);
            pos = rpos;
        }
        resVec.push_back(path.substr(pos));
        cal(resVec);
        if (resVec.size() == 0) resVec.push_back("/");
        for (auto &s: resVec) ans.append(s);
        return ans;
    }
    void cal(vector<string> &vec) {
        string s = vec[vec.size() - 1];
        if (s == "/" || s == "/.") {
            vec.pop_back();
        } else if (s == "/..") {
            vec.pop_back();
            if (vec.size()) vec.pop_back();
        }
    }
};