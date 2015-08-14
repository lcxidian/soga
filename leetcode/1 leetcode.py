#1、Add Two Numbers
给你两个链表，表示两个非负整数。数字在链表中按反序存储，例如342在链表中为2->4->3。链表每一个节点包含一个数字（0-9）。
计算这两个数字和并以链表形式返回。
输入：
输出：
时间复杂度：
思想：
ListNode* add_two_number(ListNode *head1,ListNode *head2)
{
    unsigned value1 = 0,value2 = 0;
    ListNode *p = head1->next;
    ListNode *q = head1->next;
    unsigned i = 0;
    while(p)
    {
        unsigned pows = pow((float)10,(float)i++);#必须强转，否则数据不对
        cout<<pows<<endl;
        value1 += (p->data)*pows;
        p = p->next;
    }
    i = 0;
    while(q)
    {
        unsigned pows = pow((float)10,(float)i++);#
        cout<<pows<<endl;
        value2 += (q->data)*pows;
        q = q->next;
    }
    unsigned value = value1 + value2;
    ListNode *new_head = new ListNode(0);
    while(value)
    {

        unsigned item = value%10;
        value = value/10;
        ListNode *node = new ListNode(item);
        node->next = new_head->next;
        new_head->next = node;
    }
    return new_head;
}
int main()
{
    ListNode *head1 = new ListNode(0);
    make_list(head1);
    cin.clear();#必须重置，好进行第二次输入
    ListNode *head2 = new ListNode(0);
    make_list(head2);

    ListNode *new_head = add_two_number(head1,head2);
    print_list(new_head);
    return 0;
}
#2、Reverse Linked List II
“部分旋转”
输入：Given 1->2->3->4->5->nullptr, m = 2 and n = 4,
输出：return 1->4->3->2->5->nullptr.
时间复杂度：
思想：(从1开始计数)以第m个节点为新链表的尾部,从第m+1个节点开始，采用头插法进行n-m次即可
		p指向第m-1个节点位置，第m个节点保证不动，作为“尾节点”
		r指向第n个节点的下一个节点，并把r节点放在“尾节点”后面。
		从第m+1个节点开始采用头插法，用q去遍历每一个节点，s保存q的下一个节点位置，q插进p节点的后面，直到q到达r节点的前一个位置就结束

void rotate_list(ListNode *head,unsigned m,unsigned n)
{
    unsigned k = n-m+1;
    ListNode *r,*p;
    ListNode *s;
    p = head->next;
    r = head->next;
    while(m>2){#让p到达第m个节点的前一个节点位置
        m--;
        p = p->next;
    }

    while(n>0){#r到达第n个节点的后一个节点位置
        n--;
        r = r->next;
    }
    cout<<p->data<<endl;
    ListNode *q = p->next->next;#q从第m+1个节点开始工作
    p->next->next = r;#
    if(!q) return;
    while(q != r){#头插法
        s = q->next;
        q->next = p->next;
        p->next = q;
        q = s;
    }
    return;
}
int main()
{
    ListNode *head = new ListNode(0);
    make_list(head);
    print_list(head);
    rotate_list(head,4,7);
    print_list(head);
    return 0;
}
#3、Partition List
把后面比3小的节点移到3的前半部分，且放在合适位置
输入：Given 1->4->3->2->5->2 and x = 3，
输出：return 1->2->2->4->3->5.
时间复杂度：
思想：先到达值为x的节点的位置，并依次向后查找小于x的节点，摘除该节点，把该节点插入到“合适”的位置
		p指向第一个节点（始终不变）
		q指向第一个节点值为x的节点（始终不变）
		k1，k2用来需找小于x的节点，初始化时:k1 = q; k2 = q->next;

void insert_node(ListNode *first,ListNode *last,ListNode *q)#节点插入函数：first是第一个节点，last是最一个的节点的后一个节点
{
    while(first != last){
        if((first->data <= q->data) && (q->data < first->next->data)){
            q->next = first->next;
            first->next = q;
            return;
        }
        first = first->next;
    }
    return;
}
void partition_list(ListNode *head,int x)
{
    ListNode *p = head->next;#找到p的位置
    ListNode *q = p;
    while(q){#找到q的位置
        if(q->data == x)
            break;
        q = q->next;
    }
    ListNode *k1 = q;
    ListNode *k2 = q->next;

    while(k2){
        if(k2->data < x){#找到那些小于x的节点
            ListNode *r = k2;
            k1->next = k2->next;#摘除该节点
            r->next = nullptr;
            insert_node(p,q,r);#在合适的位置插入该节点
        }
        k1 = k2;
        k2 = k2->next;
    }
    return;
}
int main()
{
    ListNode *head = new ListNode(0);
    make_list(head);
    print_list(head);
    partition_list(head,3);
    print_list(head);
    return 0;
}

#4、Remove Duplicates from Sorted List
输入：Given 1->1->2->3->3,.
输出：return 1->2->3
时间复杂度：
思想：借助有序的特点，查找相邻节点值是否相等，相等则删除一个
	p指向本节点
	q指向本节点的下一个节点
	依次比较p，q节点的值，若相等，则删除q所指向的节点，若不相等，则p，q同时下移
void remove_duplicate(ListNode *head)
{
    ListNode *p = head->next;
    ListNode *q = p->next;
    ListNode *r;
    while(q){
        if(p->data == q->data){
            r = q;
            p->next = q->next;
            delete r;
        }else{
            p = q;
            q = q->next;
        }
    }
}
int main()
{
    ListNode *head = new ListNode(0);
    make_list(head);
    print_list(head);
    remove_duplicate(head);
    print_list(head);
    return 0;
}
#5、Remove Duplicates from Sorted List II
把重复的元素都删除，包括自己本身
输入：Given 1->2->3->3->4->4->5,
输出：return 1->2->5.
时间复杂度：
思想：采用4题的算法，先删除多余重复的节点，对于删除自身节点的办法采用“交换-删除”的思想
		借助bool变量很好的解决了是否要删除p自身节点，即bool变量item为真，代表刚刚有重复元素未删除干净。需要本次循环继续删除
		指针关系：h->p->q
void remove_duplicate(ListNode *head)
{
    ListNode *p = head->next;
    ListNode *q = p->next;
    ListNode *r1,*r2;
    ListNode *h = head;
    bool item = false;#很好的标记了刚刚是否有重复的元素未删干净
    while(q){
        if(p->data == q->data){
            item = true;
            r1 = q;
            p->next = q->next;
            delete r1;
        }else{
            if(item){#代表刚刚有重复的元素未删干净，即p自身没有删除
                r2 = p;
                h->next = p->next;
                delete r2;
                item = false;#重置
            }else{
                h = p;
                p = q;
                q = q->next;
            }

        }
    }
}
int main()
{
    ListNode *head = new ListNode(0);
    make_list(head);
    print_list(head);
    remove_duplicate(head);
    print_list(head);
    return 0;
}

#6、Rotate List
输入：Given 1->2->3->4->5->nullptr and k = 2,（k从0开始）
输出：return 4->5->1->2->3->nullptr
时间复杂度：
思想：将尾节点next 指针指向首节点，形成一个环，接着往后跑len -?? k 步，然后断开即可
void rotate_list_k(ListNode *head,int k)
{
    ListNode *p = head->next;
    ListNode *q = head;
    ListNode *r;
    ListNode *h = head->next;#保存第一个节点
    while(p)
    {
        q = p;
        p = p->next;
        if(--k == 0)
            r = p;
    }
    q->next = h;
    head->next = r->next;
    r->next = nullptr;
    return;
}
int main()
{
    ListNode *head = new ListNode(0);
    make_list(head);
    print_list(head);
    rotate_list_k(head,2);
    print_list(head);
    return 0;
}

#7、Remove Nth Node From End of List
删除倒数第k个节点
输入：Given linked list: 1->2->3->4->5, and n = 2.
输出：becomes 1->2->3->5.
时间复杂度：
思想：要想删除倒数第k个节点，必须找到倒数第k+1个节点的位置
void remove_Nth_end(ListNode *head, int k)
{
    ListNode *p = head->next;
    ListNode *q = p;
    int len = k;
    while(len>=0){
        p = p->next;
        len--;
    }
    while(p){
        p = p->next;
        q = q->next;
    }
    ListNode *r = q->next;
    q->next = q->next->next;
    delete r;
    return;
}

int main()
{
    ListNode *head = new ListNode(0);
    make_list(head);
    print_list(head);
    remove_Nth_end(head,2);
    print_list(head);
    return 0;
}
#8、Swap Nodes in Pairs
成对交换
输入：Given 1->2->3->4,
输出：2->1->4->3.
时间复杂度：
思想：两两成一对，交换其值，再找下一对，直到末尾
void swap_pair(ListNode *head)
{
    ListNode *q = head->next;
    ListNode *p = q->next;
    while(p)
    {
        swap(q->data,p->data);
        if(p->next)#防止p->next为空时，再去访问p->next->next时出现断言
        {
            q = p->next;
            p = q->next;
        }else{
            break;
        }
    }
}
int main()
{
    ListNode *head = new ListNode(0);
    make_list(head);
    print_list(head);
    swap_pair(head);
    print_list(head);
    return 0;
}
#9、Reverse Nodes in k-Group
输入：Given this linked list: 1->2->3->4->5
输出：For k = 2, you should return: 2->1->4->3->5
	  For k = 3, you should return: 3->2->1->4->5
时间复杂度：
思想：分成若干组，每组k个节，然后进行若干组的插头法即可
		p，q为每组的第一个节点和最后一个节点
		s为下一组的第一个节点
此题看似简单，但细节比较多
void reverse_list_group(ListNode *head,unsigned k)
{
    ListNode *q,*p;
    ListNode *s = head->next;
    ListNode *b,*new_head,*h = head;
    h->next = nullptr;
    bool item = true,first;#第一个bool变量表示分组是否有断组的出现，第二个bool变量为了更新每次的“头结点”
    while(s && item){
        q = s;#q，p重置为每组的第一个节点位置
        p = s;#
        while(--k>0)#让p到达每组的最后一个节点位置
        {
            if(p->next)
                p = p->next;
            else
            {
                item = false;#表示该组有断组的现象发生
                break;
            }
        }
        if(!item) #由于break只能跳出一层while循环，因此这里再加一个break，跳出最外层的while循环
            break;
        s = p->next;
        first = true;
        while(q != s)#开始只能每组的头插法
        {
            if(first)#保存新的“头结点”地址
            {
                new_head = q;
                first = false;
            }
            b = q->next;
            q->next = h->next;
            h->next = q;
            q = b;
        }
        h = new_head;#为下一组的插入更新“头节点”
    }
    if(!item)#处理有断组的那些尾巴节点(即不足k个节点的最后一组)
        h->next = q;
    return;
}

int main()
{
    ListNode *head = new ListNode(0);
    make_list(head);
    print_list(head);
    reverse_list_group(head,3);
    print_list(head);
    return 0;
}

#10、Copy List with Random Pointer
深拷贝一个链表，链表除了含有next指针外，还包含一个random指针，该指针指向链表中的某个节点或者为空。
输入：
输出：
时间复杂度：
思想：重点在于随机指针的深拷贝，如何保证一个节点不会被创建两次呢？set容器来做到














