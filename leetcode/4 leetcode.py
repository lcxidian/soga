注：树的遍历有两类：深度优先遍历 ———先根（次序）遍历
									后根（次序）遍历
					宽度优先遍历 ———层次遍历

	二叉树的先根遍历有：深度优先遍历 ———先序遍历(root->le->right)
										后序遍历(le->right->root)
										中序遍历(le->root->right)。
						宽度优先遍历 ———层次遍历

树的遍历一般有两种方式：递归和非递归
	注：非递归算法通过栈或队列来模拟递归，因此每次应该先得到递归的版本

参照树的选取条件————能模拟树大多情况的发生
       		O 
  		O  		O 
	O 				O 
		O 		O

通用接口构造：
struct TreeNode{
    int value;
    TreeNode *lchild;
    TreeNode *rchild;
    TreeNode(int x):value(x),lchild(nullptr),rchild(nullptr){}
}; 
#生成二叉树
void make_tree(TreeNode **proot)
{
    string input;
    string lchild_value,rchild_value;
    int number;
    deque<TreeNode *> dq;
    cin>>input;#输入根节点的值
    if(input == "#")
    {
        *proot = nullptr;
        return;
    }
    istringstream(input)>>number;
    *proot = new TreeNode(number);
    dq.push_back(*proot);#根节点地址入队
    while(!dq.empty())
    {
        TreeNode *pnode = dq.front();#
        dq.pop_front();
        if(pnode)
        {
            cin.clear();
            cin>>lchild_value>>rchild_value;
            if(!cin)
            break;

            if(lchild_value == "#")
            {
                pnode->lchild = nullptr;
                dq.push_back(nullptr);
            }
            else
            {
                istringstream(lchild_value)>>number;
                TreeNode *lnode = new TreeNode(number);
                pnode->lchild = lnode;
                dq.push_back(lnode);
            }
            if(rchild_value == "#")
            {
                pnode->rchild = nullptr;
                dq.push_back(nullptr);
            }
            else
            {
                istringstream(rchild_value)>>number;
                TreeNode *rnode = new TreeNode(number);
                pnode->rchild = rnode;
                dq.push_back(rnode);
            }
        }
    }
    return;
}

思路：先构造只有一个节点的根树，然后每次输入两个值，分别为父节点的两个孩子节点：value   value  
																				#       value
																				value	#
																				#		#


1、 Binary Tree Level Order Traversal
二叉树的层次遍历，从根到叶子，从左到右
输入：Given binary tree {3,9,20,#,#,15,7},
输出：return its level order traversal as:
	[
		[3],
		[9,20],
		[15,7]
	]
时间复杂度：
思路： 
        1
       /  \
      2     3
     / \     \
   4   5      6
    \         /
     7       8
#递归——————处理本节点，把本节点的左右孩子的处理交给递归，把节点信息放进vector<vector<int>>里即可
using size_type = vector<vector<int>>::size_type;
void print_level_root_left(TreeNode *root,size_type top,vector<vector<int>> &result)
{
    if(root == nullptr)
        return;
    else
    {
        if(top>result.size())
            result.push_back(vector<int>());
        result[top-1].push_back(root->value);
        print_level_root_left(root->lchild,top+1,result);
        print_level_root_left(root->rchild,top+1,result);
    }
}
#非递归————采用从队头出队尾进的方式，为了保持层次性关系，采用两个队列，一个队列dq用来保存下一层节点信息，一个队列save用来保存下一层节点信息
void print_level_root_left_2(TreeNode *root,vector<vector<int>> &result)
{
    if(root == nullptr)
        return;
    deque<TreeNode *> dq;
    if(root->lchild)
        dq.push_back(root->lchild);
    if(root->rchild)
        dq.push_back(root->rchild);
    size_type i = 0;
    result.push_back(vector<int>());
    result[0].push_back(root->value);
    while(!dq.empty())
    {
        deque<TreeNode *> save = dq;#为了保证层次性关系
        dq.clear();
        result.push_back(vector<int>());
        i++;
        while(!save.empty())
        {
            TreeNode *node = save.front();
            save.pop_front();
            result[i].push_back(node->value);
            if(node->lchild)
                dq.push_back(node->lchild);
            if(node->rchild)
                dq.push_back(node->rchild);
        }

    }
    return;
}

2、Binary Tree Level Order Traversal II
二叉树的层次遍历，但从叶子再到根，从左到右
输入：Given binary tree {3,9,20,#,#,15,7},
输出：return its boom-up level order traversal as:
	[
		[15,7]
		[9,20],
		[3],
	]
时间复杂度：
思路：
        1
       /  \
      2     3
     / \     \
   4   5      6
    \         /
     7       8
#递归——————
using size_type = vector<vector<int>>::size_type;
void print_level_root_left(TreeNode *root,size_type top,vector<vector<int>> &result)
{
    if(root == nullptr)
        return;
    else
    {
        if(top>result.size())
            result.push_back(vector<int>());
        result[top-1].push_back(root->value);
        print_level_root_left(root->lchild,top+1,result);
        print_level_root_left(root->rchild,top+1,result);
        return;
    }

}
void print_level_leaf_left(TreeNode *root,vector<vector<int>> &result)
{
    print_level_root_left(root,1,result);
    reverse(result.begin(),result.end());
    return;
}

#非递归————
void print_level_leaf_left_2(TreeNode *root,vector<vector<int>> &result)
{
    if(root == nullptr)
        return;
    deque<TreeNode *> dq;
    if(root->lchild)
        dq.push_back(root->lchild);
    if(root->rchild)
        dq.push_back(root->rchild);
    size_type i = 0;
    result.push_back(vector<int>());
    result[0].push_back(root->value);
    while(!dq.empty())
    {
        deque<TreeNode *> save = dq;
        dq.clear();
        result.push_back(vector<int>());
        i++;
        while(!save.empty())
        {
            TreeNode *node = save.front();
            save.pop_front();
            result[i].push_back(node->value);
            if(node->lchild)
                dq.push_back(node->lchild);
            if(node->rchild)
                dq.push_back(node->rchild);
        }

    }
    reverse(result.begin(),result.end());
    return;
}

int main()
{
    TreeNode *root;
    make_tree(&root);
    vector<vector<int>> result;
//    print_level_leaf_left(root,result);
    print_level_leaf_left_2(root,result);
    for(auto v:result)
    {
        for(auto item:v)
            cout<<item<<ends;
        cout<<endl;
    }
    return 0;

}

3、Binary Tree Zigzag Level Order Traversal
二叉树的层次遍历，从根到叶子，从右到左
输入：Given binary tree 3,9,20,#,#,15,7,
输出：return its zigzag level order traversal as:
	[
		[3],
		[20,9],
		[15,7]
	]
时间复杂度：
思路：
        1
       /  \
      2     3
     / \     \
   4   5      6
    \         /
     7       8
#递归——————
using size_type = vector<vector<int>>::size_type;
void print_level_root_right(TreeNode *root,size_type top,vector<vector<int>> &result)
{
    if(root == nullptr)
        return;
    else
    {
        if(top>result.size())
            result.push_back(vector<int>());
        result[top-1].insert(result[top-1].begin(),root->value);
        print_level_root_right(root->lchild,top+1,result);
        print_level_root_right(root->rchild,top+1,result);
    }
}

#非递归————
void print_level_root_right_2(TreeNode *root,vector<vector<int>> &result)
{
    if(root == nullptr)
        return;
    deque<TreeNode *> dq;
    if(root->lchild)
        dq.push_back(root->lchild);
    if(root->rchild)
        dq.push_back(root->rchild);
    size_type i = 0;
    result.push_back(vector<int>());
    result[0].insert(result[0].begin(),root->value);
    while(!dq.empty())
    {
        deque<TreeNode *> save = dq;
        dq.clear();
        result.push_back(vector<int>());
        i++;
        while(!save.empty())
        {
            TreeNode *node = save.front();
            save.pop_front();
            result[i].insert(result[i].begin(),node->value);
            if(node->lchild)
                dq.push_back(node->lchild);
            if(node->rchild)
                dq.push_back(node->rchild);
        }

    }
    return;
}
int main()
{
    TreeNode *node;
    make_tree(&node);
    vector<vector<int>> result;
    print_level_root_right(node,1,result);
//    print_level_root_right_2(node,result);
    for(auto v:result)
    {
        for(auto item:v)
            cout<<item<<ends;
        cout<<endl;
    }
    return 0;
}

#4、Binary Tree Inorder Traversal
中序遍历
输入：Given binary tree {1,#,2,3},
输出：return [1,3,2].
时间复杂度：
思路：
        1
       /  \
      2     3
     / \     \
   4   5      6
    \         /
     7       8
递归： 
	————思想： 
using size_type = vector<vector<int>>::size_type;
vector<int>& print_middle(TreeNode *root,vector<int> &result)
{
    if(root == nullptr )
        return result;
    print_middle(root->lchild,result);
    result.push_back(root->value);
    print_middle(root->rchild,result);
    return result;
}

非递归：
	————思想：和先序遍历一样，只是不再在进栈的时候访问，而是在出栈的时候访问，其他不变
void print_mid_root_left_2(TreeNode *root,vector<int> &result)
{
    if(root == nullptr)
        return;
    TreeNode *p = root;
    stack<TreeNode *> sk;
    while(p || !sk.empty())
    {
        if(p)
        {
            sk.push(p);
            p = p->lchild;
            continue;
        }
        p = sk.top();
        result.push_back(p->value);
        sk.pop();
        if(p->rchild)
        {
            p = p->rchild;
        }
        else
            p = nullptr;#置空是为了保证再次出栈
    }
}
int main()
{
    TreeNode *root;
    make_tree(&root);
    vector<int> result;
    print_mid_root_left_2(root,result);
    for(auto item:result)
        cout<<item<<ends;
    cout<<endl;
    return 0;
}
#引申
	#先序遍历
        1
       /  \
      2     3
     / \     \
   4   5      6
    \         /
     7       8
递归——————
void print_inorder_root_left(TreeNode *root,vector<int> &result)
{
    if(root == nullptr)
        return;
    else
    {
        result.push_back(root->value);
        print_inorder_root_left(root->lchild,result);
        print_inorder_root_left(root->rchild,result);
        return;
    }
}

非递归：
	————思想：
		初步思想是先访问本节点，再进栈:左节点不为空，则p下移到左节点上#(while循环一次)
									   左节点为空，则出栈，找到右节点，p下移到右节点上#(while循环一次)
									   					   找不到右节点，p赋值为空(这样才能保证再次出栈)
									   注：进栈的时候访问，出栈的时候不再访问，出栈是为了找到本节的右节点
			1(访并进) 	2(访并进) 	4(访并进) 	4(出) 	7(访并进) 	7(出) 	2(出) 	5(访并进) 	5(出) 	1(出) 	3(访并进) 	3(出) 	6(访并进) 	8(访并进) 	8(出) 	6(出)
  												右节点 				        右节点                      右节点               右节点                          
  		先序序列：1 2 4 7 5 3 6 8
  		while循环的深度是1层：访问本节点，“关心”左右节点
#本次算法的优点在于while下附有2种while循环的可能
void print_inorder_root_left_2(TreeNode *root,vector<int> &result)
{
    TreeNode *p = root;
    if(p == nullptr)
        return;
    stack<TreeNode *> sk;
    while(p || !sk.empty())
    {
        if(p)
        {
            result.push_back(p->value);
            sk.push(p);
            p = p->lchild;
            continue;
        }
        p = sk.top();
        sk.pop();
        if(p->rchild){
            p = p->rchild;
        }else
            p = nullptr;#置空是为了保证再次出栈
    }
}
其中：
        if(p->rchild){
            p = p->rchild;
        }else
            p = nullptr;
可以简化成：
		p = p->rchild;(但这样不便于理解)
int main()
{
    TreeNode *root;
    make_tree(&root);
    vector<int> result;
    print_inorder_root_left_2(root,result);
    for(auto item:result)
        cout<<item<<ends;
    cout<<endl;
    return 0;
}
	#后序遍历
        1
       /  \
      2     3
     / \     \
   4   5      6
    \         /
     7       8
递归——————
void print_post_root_left(TreeNode *root,vector<int> &result)
{
    if(root == nullptr)
        return;
    else
    {
        print_post_root_left(root->lchild,result);
        print_post_root_left(root->rchild,result);
        result.push_back(root->value);
        return;
    }
}

非递归：先本节点p进栈，若左节点不为空，则p下移到左节点
					   若左节点为空，提取栈首元素，找到右节点，则p下移到右节点
					   				 			   找不到右节点，则出栈并访问
	————思想：
#5、Recover Binary Search Tree
二叉搜索树中，其中Two elements of a binary search tree (BST) are swapped by mistake，因此需要恢复
输入：1	2 （7 4） 5 （6 3） 8 9
输出：发现这两处位置7和3，然后交换7和3即可
时间复杂度：
思路：利用二叉搜索树的中序遍历是有序的特点，中序遍历并找到出错的位置，再交换即可
void recover_binary_search_tree(TreeNode *root)
{
    if(root == nullptr)
        return;
    TreeNode *p = root;
    TreeNode *item1,*item2;
    bool flag = false;
    stack<TreeNode *> sk;
    vector<TreeNode *> v;
    while(p || !sk.empty())
    {
        if(p)
        {
            sk.push(p);
            p = p->lchild;
            continue;
        }
        p = sk.top();
        ///add begin
        if(!v.empty())
        {
            TreeNode *q = v.back();
            if(q->value > p->value)
            {
                if(!flag)
                {
                    item1 = q;#记录7的位置
                    flag = true;
                }
                else
                    item2 = p;#记录3的位置
            }

        }
        /// add end
        v.push_back(p);
        sk.pop();
        if(p->rchild)
            p = p->rchild;
        else
            p = nullptr;
    }
    swap(item1->value,item2->value);
}
int main()
{
    TreeNode *root;
    vector<int> result;
    make_tree(&root);
    recover_binary_search_tree(root);
    print_mid_root_left(root,result);
    for(auto item:result)
        cout<<item<<ends;
    cout<<endl;
    return 0;

}


#6、Same Tree
Given two binary trees, write a function to check if they are equal or not
比较两个树是否相同，包括判断结构和节点的值，同样还是用到递归，加上了空节点的判断可以避免访问空指针。
输入：
输出：
时间复杂度：
思路：

#7、Symmetric Tree
判断一个二叉树是否是轴对称的是一个经典的算法问题
输入：如：对称与不对称
	1
   / \
  2   2
 / \ / \
3  4 4  3
	1
   / \
  2   2
   \   \
   3    3
输出：
时间复杂度：
思路：
方法一：层次遍历，分别判断每一层是否对称
bool issymmetric(vector<int> &v)#动态数组是否对称
{
    size_t i=0,j=v.size()-1;
    while(i<j)
    {
        if(v[i++] == v[j--])
            continue;
        else
            return false;
    }
    return true;
}
bool symmetric_tree(TreeNode *root)
{
    if(root == nullptr)
        return false;
    vector<vector<int>> vv;
    deque<TreeNode *> dq;
    deque<TreeNode *> save;
    size_t i = 0;
    dq.push_back(root);
    while(!dq.empty())
    {
        save = dq;
        dq.clear();
        vv.push_back(vector<int>());
        while(!save.empty())
        {
            TreeNode *p = save.front();
            save.pop_front();
            vv[i].push_back(p->value);
            if(p->lchild)
                dq.push_back(p->lchild);
            if(p->rchild)
                dq.push_back(p->rchild);
        }
        if(issymmetric(vv[i]))
            i++;
        else
            return false;
    }
    return true;
}
int main()
{
    TreeNode *root;
    make_tree(&root);
    if(symmetric_tree(root))
        cout<<"is symmetric"<<endl;
    else
        cout<<"not symmetric"<<endl;
    return 0;
}
方法二：不采用层次遍历。直接比较对称位置：left的right和right的left比较，left的left和right的right比较。
#8、Balanced Binary Tree
是否是平衡二叉树
输入：
输出：
时间复杂度：
思路：用递归，分别判断左右两棵子树是不是平衡二叉树，如果都是并且左右两颗子树的高度相差不超过1，那么这棵树就是平衡二叉树。
size_t tree_high(TreeNode *root)#自底向上的递归：最常用的递归方式，从最底层开始计算树的高度
{
    if(root == nullptr)
        return 0;
    else
    {
        size_t left_high = tree_high(root->lchild);
        size_t right_high = tree_high(root->rchild);
        return 1 + (left_high>right_high?left_high:right_high);
    }
}
bool balanced_binary_tree(TreeNode *root)#自上而下的递归：若本节点是左右子树高度不超过1，则把本节点的左子树和右子树分别新的本节点
{
    if(root == nullptr)
        return true;
    else
    {
        size_t left = tree_high(root->lchild);
        size_t right = tree_high(root->rchild);

        if(abs(left - right)>1)
            return false;
        else
            return balanced_binary_tree(root->lchild)&&balanced_binary_tree(root->rchild);
    }
}
int main()
{
    TreeNode *root;
    make_tree(&root);
    if(balanced_binary_tree(root))
        cout<<"is balanced_binary_tree"<<endl;
    else
        cout<<"not balanced_binary_tree"<<endl;
    return 0;
}
#9、Flatten Binary Tree to Linked List
将二叉树转换为链表
输入：
         1
        / \
       2   5
      / \   \
     3   4   6
输出：
   1
    \
     2
      \
       3
        \
         4
          \
           5
            \
             6
时间复杂度：
思路：一趟先序遍历，选用lchild去做next指针，不能选用rchild做next指针，因为rchild还有用于查找右节点，所以不能“动用”
void binary_tree_to_list(TreeNode *root)
{
    if(root == nullptr)
        return;
    TreeNode *p = root;
    TreeNode *pre = nullptr;#用来记录上一个先序的节点(即前驱)
    TreeNode *q = root;#用于打印
    stack<TreeNode *> sk;
    while(p || !sk.empty())
    {
        if(p)
        {
            ///“访问” begin
            if(pre)
                pre->lchild = p;
            pre = p;
            ///“访问” end
            sk.push(p);
            p = p->lchild;
            continue;
        }
        p = sk.top();
        sk.pop();
        if(p->rchild)
            p = p->rchild;
        else
            p = nullptr;
    }
    while(q)
    {
        cout<<q->value<<ends;
        q = q->lchild;
    }
    return;
}
int main()
{
    TreeNode *root;
    make_tree(&root);
    binary_tree_to_list(root);
    return 0;
}
#10、Populating Next Right Pointers in Each Node II
struct TreeLinkNode {
      TreeLinkNode *left;
      TreeLinkNode *right;
      TreeLinkNode *next;
      int value;
}
输入：
        1
       /  \
      2     3
     / \   /  \
   4   5  6  	7
输出：
          1 -> NULL
       /    \
      2 -> 	3 -> NULL
     / \    /  \
   4->	5->6->	7 -> NULL
时间复杂度：
思路：层次遍历
首先构造一个函数用于创建全新的“二叉树”，然后层次遍历，并在遍历中作出一些改变即可
struct TreeLinkNode {
      TreeLinkNode *lchild;
      TreeLinkNode *rchild;
      TreeLinkNode *next;
      int value;
      TreeLinkNode(int x):value(x),lchild(nullptr),rchild(nullptr),next(nullptr){}
};
void make_tree_2(TreeLinkNode **proot)#生成全新的“二叉树”
{
    string input;
    string lchild_value,rchild_value;
    int number;
    deque<TreeLinkNode *> dq;
    cin>>input;
    if(input == "#")
    {
        *proot = nullptr;
        return;
    }
    istringstream(input)>>number;
    *proot = new TreeLinkNode(number);
    dq.push_back(*proot);
    while(!dq.empty())
    {
        TreeLinkNode *pnode = dq.front();
        dq.pop_front();
        if(pnode)
        {
            cin.clear();
            cin>>lchild_value>>rchild_value;
            if(!cin)
                break;
            if(lchild_value == "#")
            {
                pnode->lchild = nullptr;
                dq.push_back(nullptr);
            }
            else
            {
                istringstream(lchild_value)>>number;
                TreeLinkNode *lnode = new TreeLinkNode(number);
                pnode->lchild = lnode;
                dq.push_back(lnode);
            }
            if(rchild_value == "#")
            {
                pnode->rchild = nullptr;
                dq.push_back(nullptr);
            }
            else
            {
                istringstream(rchild_value)>>number;
                TreeLinkNode *rnode = new TreeLinkNode(number);
                pnode->rchild = rnode;
                dq.push_back(rnode);
            }
        }
    }
    return;
}
void binary_tree_add_next_pointer(TreeLinkNode *root,vector<vector<TreeLinkNode *>> &result)
{
    if(root == nullptr)
        return;
    deque<TreeLinkNode *> dq;
    TreeLinkNode *p = root;
    dq.push_back(p);
    deque<TreeLinkNode *> save;#
    TreeLinkNode *node = nullptr;
    TreeLinkNode *pre = nullptr;
    size_t i=0;
    while(!dq.empty())
    {
        save = dq;
        dq.clear();
        result.push_back(vector<TreeLinkNode *>());
        while(!save.empty())
        {
            node = save.front();
            save.pop_front();

            if(result[i].empty())#
                result[i].push_back(node);
            else
            {
                pre = result[i].back();#寻找前驱
                pre->next = node;#next赋值
                result[i].push_back(node);
            }

            if(node->lchild)
                dq.push_back(node->lchild);
            if(node->rchild)
                dq.push_back(node->rchild);
        }
        i++;
    }
}
int main()
{
    TreeLinkNode *root;
    make_tree_2(&root);
    vector<vector<TreeLinkNode *>> result;
    binary_tree_add_next_pointer(root,result);
    for(auto v:result)
    {
        for(auto item:v)
            cout<<item->value<<ends;
        cout<<endl;
    }
    return 0;
}
11、Construct Binary Tree from Preorder and Inorder Traversal
先序和中序，创建二叉树
输入：
	前序遍历结果为：6 5 4 8 7 9
	中序遍历结果为：4 5 6 7 8 9
输出：
时间复杂度：
思路：
12、Construct Binary Tree from Inorder and Postorder Traversal
中序和后序创建二叉树
输入：
	中序：BEDAC  
	后序：EDBCA
输出：
时间复杂度：
思路：
13、Unique Binary Search Trees
输入：
输出：
时间复杂度：
思路：动态规划思想
14、Unique Binary Search Trees II
输入：
输出：
时间复杂度：
思路：动态规划思想
15、Validate Binary Search Tree
判断一个二叉树是否为二分查找树
输入：
    5
   / \
  4   10
      / \
     3   11
该树不是二叉搜索树
输出：
时间复杂度：
思路：中序遍历一遍，如果有序则是二叉搜索树，否则不是
bool issearch_binary_tree(TreeNode *root)
{
    if(root == nullptr)
        return false;
    stack<TreeNode *> sk;
    TreeNode *p = root;
    vector<int> v;
    while(p || !sk.empty())
    {
        if(p)
        {
            sk.push(p);
            p = p->lchild;
            continue;
        }
        p = sk.top();
        sk.pop();
        v.push_back(p->value);
        if(p->rchild)
            p = p->rchild;
        else
            p = nullptr;
    }
    for(auto i : v)
        cout<<i<<ends;
    cout<<endl;
    if(is_sorted(v.begin(),v.end()))
        return true;
    else
        return false;
}
int main()
{
    TreeNode *root;
    make_tree(&root);
    if(issearch_binary_tree(root))
        cout<<"is search_binary_tree"<<endl;
    else
        cout<<"not search_binary_tree"<<endl;
}

16、Convert Sorted Array to Binary Search Tree
输入：
输出：
时间复杂度：
思路：搜索二叉树的建立
void array_to_binary_tree(int array[],size_t size,TreeNode **proot)
{

    *proot = new TreeNode(array[0]);
    TreeNode *p = *proot;
    TreeNode *q;
    TreeNode *save;
    size_t i = 1;
    while(i<size)
    {
        TreeNode *node = new TreeNode(array[i]);
        q = p;
        while(q)
        {
            if(array[i] < q->value)
            {
                save = q;
                q = q->lchild;
            }
            else
            {
                save = q;
                q = q->rchild;
            }
        }
        if(array[i] < save->value)
            save->lchild = node;
        else
            save->rchild = node;
        i++;
    }
    return;
}

int main()
{
    TreeNode *root;
    int array[5] = {6,1,3,7,15};
    vector<int> result;
    array_to_binary_tree(array,5,&root);
    print_mid_root_left(root,result);
    for(auto item:result)
        cout<<item<<ends;
    return 0;

}
17、Convert Sorted List to Binary Search Tree
输入：
输出：
时间复杂度：
思路：搜索二叉树的建立

18、Minimum Depth of Binary Tree
输入：
输出：
时间复杂度：
思路：层次遍历
size_t min_depth_binary_tree(TreeNode *root)
{
    if(root == nullptr)
        return 0;
    TreeNode *p = root;
    deque<TreeNode *> dq;
    deque<TreeNode *> save;
    dq.push_back(p);
    size_t depth = 0;
    bool flag = false;
    while(!dq.empty())
    {
        depth++;
        save = dq;
        dq.clear();
        flag = false;
        while(!save.empty())
        {
            TreeNode *node = save.front();
            save.pop_front();
            if(node->lchild)
                dq.push_back(node->lchild);
            else
                flag = true;#如果node->lchild == null或node->rchild == null,则最小深度就停留在这一层
            if(node->rchild)
                dq.push_back(node->rchild);
            else
                flag = true;
        }
        if(flag && !dq.empty())
            return depth;
    }
    return depth;
}
int main()
{
    TreeNode *root;
    make_tree(&root);
    cout<<min_depth_binary_tree(root)<<endl;
    return 0;
}
19、Maximum Depth of Binary Tree
输入：
输出：
时间复杂度：
思路：层次遍历
size_t max_depth_binary_tree(TreeNode *root)
{
    if(root == nullptr)
        return 0;
    TreeNode *p = root;
    deque<TreeNode *> dq;
    deque<TreeNode *> save;
    dq.push_back(p);
    size_t depth = 0;
    while(!dq.empty())
    {
        depth++;
        save = dq;
        dq.clear();
        while(!save.empty())
        {
            TreeNode *node = save.front();
            save.pop_front();
            if(node->lchild)
                dq.push_back(node->lchild);
            if(node->rchild)
                dq.push_back(node->rchild);
        }
    }
    return depth;
}
int main()
{
    TreeNode *root;
    make_tree(&root);
    cout<<max_depth_binary_tree(root)<<endl;
    return 0;
}
20、Path Sum
输入：
	5
   / \
  4   8
 /   / \
11  13  4
/ \  \
7  2  1
输出：return true, as there exist a root-to-leaf path 5->4->11->2 which sum is 22.
时间复杂度：
思路：动态规划思想
21、Path Sum II
输入：sum = 22
			  5
             / \
            4   8
           /   / \
          11  13  4
         /  \    / \
        7    2  5   1
输出：
[
   [5,4,11,2],
   [5,8,4,5]
]
时间复杂度：
思路：动态规划思想
22、Binary Tree Maximum Path Sum
输入：
输出：
时间复杂度：
思路：层次遍历时，把每一层的最大记录下来，加起来即可（这样不对）

23、Populating Next Right Pointers in Each Node(二叉树)
	与 Populating Next Right Pointers in Each Node II(完全二叉树)相似
给定一个二叉树，使每个节点的next指针指向它的右边的节点，和之前的Populating Next Right Pointers in Each Node类似，只是这次的二叉树不是完全二叉树，但是方法和思想与之前的一样。
输入：
输出：
时间复杂度：
思路：
24、Sum Root to Leaf Numbers
根节点到叶子结点的所有权值和
输入：
输出：
时间复杂度：
思路：







