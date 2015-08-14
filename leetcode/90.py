
LeetCode题解整理版(二)

Leetcode开始支持Python了，本篇题解中的题目都是用Python写的。（更新中..）

已更新完，本篇题解中共96题，按照Leetcode上的顺序从上向下。可以用CTRL+F查找，如果没有的话就是在前一篇题解中了。

因为时间原因，题解写的并不是很详细，大多数题目都只给出了关键思路。
Reverse Words in a String

将abc def形式的字符串翻转成def abc，并且去掉多余的空格。
先将这个字符串翻转过来，再逐次翻转每个词。（当然不是效率最高的办法，只是为了好写。）
	

class Solution:
    # @param s, a string
    # @return a string
    def reverseWords(self, s):
        return ' '.join([word[::-1] for word in s[::-1].split()])

Recover Binary Search Tree

一棵二叉搜索树中两个节点错误，修正这棵树。
正确二叉树中序遍历应该是递增，而交换了两个节点后会导致有一处或者两处某节点值小于前一个节点，记录，最后交换即可。
	

class Solution:
    # @param root, a tree node
    # @return a tree node
    def recoverTree(self, root):
        self.pre = None
        self.n1 = self.n2 = None
        self.dfs(root)
        self.n1.val, self.n2.val = self.n2.val, self.n1.val
        return root
    
    def dfs(self, root):
        if not root:
            return
        self.dfs(root.left)
        if self.pre and root.val < self.pre.val:
            if not self.n1:
                self.n1, self.n2 = self.pre, root
            else:
                self.n2 = root
        self.pre = root
        self.dfs(root.right)

Validate Binary Search Tree

判断是否是BST
中序遍历，比较当前点的值是否大于前一点的值即可


class Solution:
    # @param root, a tree node
    # @return a boolean
    val = None
    def isValidBST(self, root):
        if root is None: 
            return True
        res = self.isValidBST(root.left)
        if self.val is None:
            self.val = root.val
        else:
            res = res and (root.val > self.val)
            self.val = root.val
        res = res and self.isValidBST(root.right)
        return res

Interleaving String

判断C串是否有A串和B串组成（就是说C中提取出A之后剩下B）
简单DP，dp[i][j]表示A[1..i]和B[1..j]是否可以组成C[1..i+j]
	

class Solution:
    # @return a boolean
    def isInterleave(self, s1, s2, s3):
        if len(s3) != len(s1) + len(s2):
            return False
        dp = [[False] * (len(s2) + 1) for i in range(len(s1) + 1)]
        for i in range(len(s1) + 1):
            for j in range(len(s2) + 1):
                if i == 0 and j == 0:
                    dp[i][j] = True
                elif i > 0 and dp[i-1][j] and s3[i+j-1] == s1[i-1]:
                    dp[i][j] = True
                elif j > 0 and dp[i][j-1] and s3[i+j-1] == s2[j-1]:
                    dp[i][j] = True
                else:
                    dp[i][j] = False
        return dp[len(s1)][len(s2)]

Unique Binary Search Trees II

给出N个节点二叉搜索树的所有形态。
要生成所有形态，也只有暴力枚举了。
	

class Solution:
    # @return a list of tree node
    treelist = None
    def generateTrees(self, n):
        return self.dfs(0, n)
    
    def dfs(self, l, r):
        ans = []
        if l == r:
            ans.append(None)
            return ans
        for i in range(l, r):
            lb, rb = self.dfs(l, i), self.dfs(i + 1, r)
            for lc in lb:
                for rc in rb:
                    node = TreeNode(i + 1)
                    node.left = lc
                    node.right = rc
                    ans.append(node)
        return ans

Reverse Linked List II

翻转链表的中间一段，要求常数空间，只遍历一遍
记录下第m个节点和它的前一个节点，中间直接翻，到第n个节点再进行一些处理。思想简单但很容易写错。


class Solution:
    # @param head, a ListNode
    # @param m, an integer
    # @param n, an integer
    # @return a ListNode
    def reverseBetween(self, head, m, n):
        prem, pre, next, now, nowm = None, None, None, head, None;
        ind = 1;
        while now is not None:
            next = now.next
            if ind >= m and ind <= n:
                now.next = pre
            if ind == m:
                prem, nowm = pre, now
            if ind == n:
                nowm.next = next
                if prem is None:
                    head = now
                else:
                    prem.next = now
            pre, now, ind = now, next, ind + 1
        return head

Subsets II

枚举一个集合中的不重复子集
既然枚举子集，想必题目中的集合不会有多少数，可以用二进制数来表示某个数选了没有，因为要保证不重复，所以对集合排序后，连续相同的数不能选相同数目，我们可以规定对于相同数，如果前面一个没选，后面一个就不能选来保证这一点。


class Solution:
    # @param num, a list of integer
    # @return a list of lists of integer
    def subsetsWithDup(self, S):
        S.sort()
        bset = []
        for x in range(2**len(S)):
            for i in range(1, len(S)):
                if (S[i] == S[i-1] and (x>>(i-1)&0x03 == 0x01)): break
            else:
                bset.append(x)
        return [[S[x] for x in range(len(S)) if i>>x&1] for i in bset]

Decode Ways

1->A..26->Z一一对应，给一个数字串，问有多少种解码方式。
动态规划，S[i]表示到i位有多少种组合方式，其值决定与S[i-1]与S[i-2]。
S[i] = if(S[i] ok) S[i-1] + if (S[i-1..i] ok) S[i-2]
	

class Solution:
    # @param s, a string
    # @return an integer
    def numDecodings(self, s):
        if len(s) == 0:
            return 0
        dp = [1] + [0] * len(s)
        ok = lambda x: x[0] != '0' and  int(x) >= 1 and int(x) <= 26;
        for i in range(1, len(s) + 1):
            dp[i] = dp[i-1] if ok(s[i-1:i]) else 0
            if i >= 2:
                dp[i]+= dp[i-2] if ok(s[i-2:i]) else 0
        return dp[len(s)]

GrayCode

排列0~2^N-1个二进制串，相邻串之间只有一位不同。
可以这样考虑，假设N-1的问题已经解决，已经有2^(N-1)个串符合条件，现在解决N的问题，那么还要再生成2^(N-1)个串，很显然，这后2^(N-1)个的最高位都为1，所以只要考虑其余N-1位即可。第2^(N-1)+1个串只能在第2^(N-1)个串的最高位加个1，然后我们又知道第2^(N-1)-1和第2^(N-1)个只差一位，所以第2^(N-1)+2个串只要在第2^(N-1)-1个串的第N位加个1，以此类推。

下面给个例子，很容易看懂
	

000 0
001 1
011 3
010 2
----后两位以此为对称轴
110 6
111 7
101 5
100 4


class Solution:
    # @return a list of integers
    def grayCode(self, n):
        self.res = [0]
        for i in [2**x for x in range(0, n)]:
            self.res.append(self.res[-1] + i)
            self.res.extend([i + v for v in self.res[-3:None:-1]])
        return self.res;

Merge Sorted Array

合并A、B两个有序数组到A中。
从前向后放不行，那就从后向前放吧


class Solution:
    # @param A  a list of integers
    # @param m  an integer, length of A
    # @param B  a list of integers
    # @param n  an integer, length of B
    # @return nothing
    def merge(self, A, m, B, n):
        for i in range(m + n - 1, -1, -1):
            if m == 0 or (n > 0 and B[n-1] > A[m-1]):
                A[i] = B[n-1]
                n -= 1
            else:
                A[i] = A[m-1]
                m -= 1
        return A

Scramble String

http://oj.leetcode.com/problems/scramble-string/
动态规划，用dp[lp][rp][len]表示s1[lp:lp+len]和s2[rp:lp+len]是Scramble String。


class Solution:
    # @return a boolean
    def isScramble(self, s1, s2):
        if len(s1) != len(s2):
            return False
        if len(s1) == 0:
            return True
        self.s1, self.s2 = s1, s2
        lens = len(s1)
        self.dp = [[[-1] * lens for i in range(lens)] * lens for i in range(lens)]
        return self.dfs(0, 0, len(s1))
    
    def dfs(self, lp, rp, len):
        if self.dp[lp][rp][len - 1] >= 0:
            return True if self.dp[lp][rp][len - 1] == 1 else False
        if len == 1:
            return self.s1[lp] == self.s2[rp]
        for i in range(1, len):
            if self.dfs(lp, rp, i) and self.dfs(lp + i, rp + i, len - i) \
                    or self.dfs(lp, rp + i, len - i) and self.dfs(lp + len - i, rp, i):
                self.dp[lp][rp][len - 1] = 1
                return True
        self.dp[lp][rp][len - 1] = 0 
        return False

Partition List

给定一个值，将链表中按该值分为前后两部分，要求保持原序。
拖两条链，一条大值链一条小值链，最后连起来即可。
	

class Solution:
    # @param head, a ListNode
    # @param x, an integer
    # @return a ListNode
    def partition(self, head, x):
        if head is None:
            return head
        sHead, bHead = ListNode(0), ListNode(0)
        sTail, bTail = sHead, bHead
        while head is not None:
            if head.val < x:
                sTail.next = head
                sTail = sTail.next
            else:
                bTail.next = head
                bTail = bTail.next
            head = head.next
        bTail.next = None
        sTail.next = bHead.next
        return sHead.next

Maximal Rectangle

给出0、1矩阵，找出最大的由1构成的矩阵。
就是对每一行依次用单调栈求以这行为底的最大矩形，最后取最大的就可以了，单调栈的解释见下一题。


class Solution:
    # @param matrix, a list of lists of 1 length string
    # @return an integer
    def maximalRectangle(self, matrix):
        if len(matrix) == 0:
            return 0
        ans = 0;
        for i in range(len(matrix)):
            stk = []
            for j in range(len(matrix[0]) + 1):
                if j < len(matrix[0]): matrix[i][j] = int(matrix[i][j])
                if i > 0 and j < len(matrix[0]) and matrix[i][j]:
                    matrix[i][j] += matrix[i-1][j]
                while len(stk) and (j == len(matrix[0]) or matrix[i][stk[-1]] >= matrix[i][j]):
                    top = stk.pop()
                    if len(stk) == 0:
                        ans = max(ans, matrix[i][top]*j)
                    else:
                        ans = max(ans, matrix[i][top]*(j-stk[-1]-1))
                stk.append(j)
        return ans

Largest Rectangle in Histogram

N块宽度相同，高度不同的木板连在一起，求最大矩形。
首先，我们知道暴力的方法，就是枚举每个木板作为它所在矩形最大高度，然后看最左和最右分别能延伸多长，复杂度O(N^2)。
基于暴力方法可以用单调栈优化，从左向右扫，同时入栈，入栈前将栈顶比它短的木板全部出栈，每个木板在出栈时计算以它为所在矩形最大高度的矩形的最大面积。每个木板入栈出栈各一次，复杂度O(n)。
其实不难理解，每个木板出栈时它(栈的)下面那块木板就是左边第一块比它短的，而使它出栈的那块木板则是右边第一块比它短的，也就很快找到了上面暴力方法中最左和最右能延伸的距离。
代码要注意细节处理。


class Solution:
    # @param height, a list of integer
    # @return an integer
    def largestRectangleArea(self, height):
        ans, lenh, stk = 0, len(height), []
        for i in range(lenh + 1):
            while len(stk) and (i == lenh or height[stk[-1]] >= height[i]):
                top = stk.pop()
                if len(stk) == 0:
                    ans = max(ans, height[top] * i)
                else:
                    ans = max(ans, height[top] * (i - stk[-1] - 1))
            stk.append(i)
        return ans

Remove Duplicates from Sorted List II

删除有序链表中的重复元素。
注意处理细节，首先，当一个元素的后两个连续节点值相同时删除下一个，其次，当后两个连续节点不同但上一次是删除操作时也要删除下一个，然后更改标记不继续删后面的。


class Solution:
    # @param head, a ListNode
    # @return a ListNode
    def deleteDuplicates(self, head):
        if not head:
            return head
        nHead, flag = ListNode(0), False
        nHead.next, head = head, nHead
        while head:
            if (head.next and head.next.next and head.next.next.val == head.next.val):
                head.next = head.next.next
                flag = True
            elif flag == True and head.next:
                head.next = head.next.next
                flag = False
            else:
                head = head.next
        return nHead.next

Remove Duplicates from Sorted List

有序链表中若有多个元素重复，只保持一个。
比上题简单，标记都省了。


class Solution:
    # @param head, a ListNode
    # @return a ListNode
    def deleteDuplicates(self, head):
        if not head:
            return head
        nHead = ListNode(0)
        nHead.next, head = head, nHead
        while head:
            if (head.next and head.next.next and head.next.next.val == head.next.val):
                head.next = head.next.next
            else:
                head = head.next
        return nHead.next

Search in Rotated Sorted Array II

一个有序数组循环右移若干后位之后，在之中搜索一个值。
在普通二分上做修改，需要注意的是A[l]=A[m]=A[n]时，无法知道往那边搜索，最坏复杂度可能有O(N)。

class Solution:
    # @param A a list of integers
    # @param target an integer
    # @return a boolean
    def search(self, A, target):
        l, h = 0, len(A) - 1
        while (l <= h):
            m = l + ((h - l) >> 1)
            if A[m] == target:
                return True
            if A[m] == A[l] and A[m] == A[h]:
                l, h = l + 1, h - 1
            elif (A[m] > A[l] and target < A[m] and target >= A[l]) or (A[m] < A[l] and not (target <= A[h] and target > A[m])):
                h = m - 1
            else:
                l = m + 1
        return False

Remove Duplicates from Sorted Array II

有序数组中的若有多个元素重复，只保持两个。
没做I的时候我用的是POP元素。。和I一样，往数组前段放就可以了，保证已放的重复元素不超过两个


class Solution:
    # @param A a list of integers
    # @return an integer
    def removeDuplicates(self, A):
        sz = 0
        for i in range(len(A)):
            if sz < 2 or A[sz - 2] != A[i]:
                A[sz] = A[i]
                sz = sz + 1
        return sz

Word Search

在一个矩阵中找一个单词。
暴力DFS。(我能说我一个暴力DFS写了半天么(┬＿┬))


class Solution:
    # @param board, a list of lists of 1 length string
    # @param word, a string
    # @return a boolean
    def exist(self, board, word):
        self.h = len(board)
        self.w = len(board[0])
        for i in range(self.h):
            for j in range(self.w):
                if board[i][j] == word[0]:
                    t, board[i][j] = board[i][j], ' '
                    if self.dfs(board, word, i, j, 1):
                        return True
                    board[i][j] = t
        return False
    
    def dfs(self, board, word, x, y, p):
        dx, dy = [1, -1, 0, 0], [0, 0, 1, -1]
        if (p == len(word)):
            return True
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx and nx < self.h and 0 <= ny and ny < self.w and board[nx][ny] == word[p]:
                t, board[nx][ny] = board[nx][ny], ' '
                if self.dfs(board, word, nx, ny, p + 1):
                    return True
                board[nx][ny] = t
        return False

Subsets

枚举所有子集。
二进制表示选了哪些数。
	

class Solution:
    # @param S, a list of integer
    # @return a list of lists of integer
    def subsets(self, S):
        S.sort()
        return [[S[x] for x in range(len(S)) if i>>x&1] for i in range(2**len(S))]

Combinations

枚举C(n, k)
暴力DFS枚举。

class Solution:
    # @return a list of lists of integers
    def combine(self, n, k):
        self.res = []
        tmp = []
        self.dfs(n, k, 1, 0, tmp)
        return self.res
    def dfs(self, n, k, m, p, tmp):
        if k == p:
            self.res.append(tmp[:])
            return
        for i in range(m, n+1):
            tmp.append(i)
            self.dfs(n, k, i+1, p+1, tmp)
            tmp.pop()

Minimum Window Substring

找出串S中最短的串，包含了串T中出现的每个字符。
思路是左右各一个指针，分别是pl、pr，pr先移动直到包含T中所有字符，然后pl尽量右移直到S[pl:pr]刚刚不能保证包含所有T中字符，那么S[pl-1:pr]就是一个可行的最短串。之后重复以上过程直到串尾，记下中间找到的最短段即可。


class Solution:
    # @return a string
    def minWindow(self, S, T):
        d, dt = {}, dict.fromkeys(T, 0)
        for c in T: d[c] = d.get(c, 0) + 1
        pi, pj, cont = 0, 0, 0
        ans = ""
        while pj < len(S):
            if S[pj] in dt:
                if dt[S[pj]] < d[S[pj]]:
                    cont += 1
                dt[S[pj]] += 1;
            if cont == len(T):
                while pi < pj:
                    if S[pi] in dt:
                        if dt[S[pi]] == d[S[pi]]:
                            break;
                        dt[S[pi]] -= 1;
                    pi+= 1
                if ans == '' or pj - pi < len(ans):
                    ans = S[pi:pj+1]
                dt[S[pi]] -= 1
                pi += 1
                cont -= 1
            pj += 1
        return ans

Sort Colors

给一个只有0，1，2的数组排序，要求only one pass。
貌似是USACO上的题，已经忘记当时怎么做的了。
一共三个指针，头指针、尾指针、”壹”指针(一开始和头指针都在开始)。从前向后，如果当前位置是1，头指针后移，而壹指针停在原地，如果是2，和尾指针指向的数交换，并且尾指针前移，如果是0，则交换0和壹指针上的数，并且头指针和壹指针都后移。
这里头尾指针都很容易理解，关键是对壹指针的理解，它总是在一串连续的一的开头，并且这串1的结尾就是头指针！每次头指针遇到一个0，都会将0交换到壹指针所在的位置，再将壹指针后移到下一个1。


class Solution:
    # @param A a list of integers
    # @return nothing, sort in place
    def sortColors(self, A):
        s, t, e = 0, 0, len(A) - 1
        while s <= e:
            if A[s] == 0:
                if s != t:
                    A[s], A[t] = A[t], A[s]
                s, t = s + 1, t + 1
            elif A[s] == 1:
                s = s + 1
            elif A[s] == 2:
                if s != e:
                    A[s], A[e] = A[e], A[s]
                e = e - 1
        return A

Search a 2D Matrix

把N*M个有序数按顺序排成矩阵，然后判断一个数是否在矩阵内。
变成矩阵难道就不是二分查找了？


class Solution:
    # @param matrix, a list of lists of integers
    # @param target, an integer
    # @return a boolean
    def searchMatrix(self, matrix, target):
        l, h = 0, len(matrix) * len(matrix[0]) - 1
        while (l <= h):
            m = l + ((h-l) >> 2)
            v =  matrix[m/len(matrix[0])][m%len(matrix[0])]
            if v < target:
                l = m + 1
            elif v > target:
                h = m - 1
            else:
                return True
        return False

Set Matrix Zeroes

给一个矩阵，若某格为0，该格所在行及所在列全部改为0，要求常数空间复杂度。
显然先扫一遍Mark的话空间复杂度是O(M+N)，这个Mark是必不可少的，不能用额外空间的话，就只能用原数组的某一行及某一列来记录了。最后再扫一遍数组，根据标记行及标记列的值来判断某格是否要置0。需要注意的是，该行及该列其它的格子要最后再置0。


class Solution:
    # @param matrix, a list of lists of integers
    # RETURN NOTHING, MODIFY matrix IN PLACE.
    def setZeroes(self, matrix):
        if len(matrix) == 0:
            return
        lenn, lenm = len(matrix), len(matrix[0])
        x, y = None, None
        for i in range(lenn):
            for j in range(lenm):
                if matrix[i][j] != 0:
                    continue
                if x is not None:
                    matrix[x][j] = matrix[i][y] = 0
                else:
                    x, y = i, j
        if x is None:
            return
        for i in range(lenn):
            for j in range(lenm):
                if i == x or j == y:
                    continue
                if matrix[x][j] == 0 or matrix[i][y] == 0:
                    matrix[i][j] = 0
        for i in range(lenn):
            matrix[i][y] = 0
        for i in range(lenm):
            matrix[x][i] = 0

Edit Distance

两个字符串的最短编辑距离，可以增删改。
经典DP，d[i][j]表示s1[1:i]和s2[1:j]的最短编辑距离，它可以由d[i-1][j]、d[i][j-1]、d[i-1][j-1]这三个状态转化而来，取最小的即可。
	

class Solution:
    # @return an integer
    def minDistance(self, word1, word2):
        dp = [[0] * (len(word2) + 1) for i in range(len(word1) + 1)]
        for i in range(1, len(word1) + 1): 
            dp[i][0] = i
        for i in range(1, len(word2) + 1): 
            dp[0][i] = i
        for i in range(1, len(word1) + 1):
            for j in range(1, len(word2) + 1):
                dp[i][j] = dp[i - 1][j - 1] + 1
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                dp[i][j] = min(dp[i][j], dp[i][j - 1] + 1)
                dp[i][j] = min(dp[i][j], dp[i - 1][j] + 1)
        return dp[len(word1)][len(word2)]

Climbing Stairs

爬楼梯，每次一步或两步，求爬法有多少种
菲波拉契数列，f[n] = f[n-1] + f[n-2]

class Solution:
    # @param n, an integer
    # @return an integer
    def climbStairs(self, n):
        f = [1, 1]
        while len(f) <= n:
            f.append(f[-1] + f[-2])
        return f[n]

Sqrt(x)

实现Sqrt(x)。
科普题，牛顿迭代，y = 1/2 * (y + x / y)。
	

class Solution:
    # @param x, an integer
    # @return an integer
    def sqrt(self, x):
        y0, y1 = 0, 1
        while int(y0) != int(y1):
            y0 = y1
            y1 = 1.0/2.0 * (y0 + x / y0)
        return int(y0)

Text Justification

数字排版，将一个字符串排列成每行N个字母。
恶心题，坑一堆。首先最后一行特判，单词间只有一个空格，其次关于空格均分的规则，假如8个空格3个空，就是(3,3,2)。


'''
words: ["This", "is", "an", "example", "of", "text", "justification."]
L: 16.
Return the formatted lines as:
[
   "This    is    an",
   "example  of text",
   "justification.  "
]
'''
class Solution:
    # @param words, a list of strings
    # @param L, an integer
    # @return a list of strings
    def fullJustify(self, words, L):
        ans, p, plen = [], 0, 0
        for i in range(len(words)):
            if plen + len(words[i]) + i - p - 1 >= L:
                spc = (L - plen) // (i - p - 1) if i - p > 1 else 0
                sps = (L - plen - spc * (i - p - 1))
                str = words[p]
                for j in range(p + 1, i):
                    if sps > 0:
                        str += ' '
                        sps -= 1
                    str += ' ' * spc + words[j] 
                ans.append(str + ' ' * (L - plen))
                plen, p = 0, i
            if i < len(words):
                plen += len(words[i])
        str = ''
        while p < len(words):
            str += words[p]
            if len(str) < L:
                str += ' '
            p = p + 1
        ans.append(str + ' ' * (L - len(str))) 
        return ans

Plus One

讲一个大数加1
加到不进位位置，注意头部有可能要加1


class Solution:
    # @param digits, a list of integer digits
    # @return a list of integer digits
    def plusOne(self, digits):
        for i in range(len(digits)-1, -1, -1):
            digits[i] = (digits[i] + 1) % 10
            if digits[i]:
                break;
        else:
            digits.insert(0, 1)
        return digits

Valid Number

判断一个数字是否合法
很麻烦的DFA，这里的合数字状况比较多，小数点前有没有数字要区别对待，WA了很多次，还参考了CSGrandeur的题解才过。


class Solution:
    # @param s, a string
    # @return a boolean
    def isNumber(self, s):
        s = s.strip();
        # dfa status 
        err = -1 # error
        srt = 0  # start
        sgd = 1  # integer part sign 
        did = 2  # integer part number
        ddp = 3  # xx. (there are some numbers before '.')
        dnp = 3  # .
        dii = 5  # decimal part number
        exe = 6  # e
        sge = 7  # exp part sign
        die = 8  # exp part number
        end = 9 # end
        # construct a dfa
        dfa = [[err] * 128 for i in range(9)]
        dfa[srt][ord('+')] = dfa[srt][ord('-')] = sgd
        dfa[srt][ord('.')] = dfa[sgd][ord('.')] = dnp
        dfa[did][ord('.')] = ddp
        dfa[did][ord('e')] = dfa[ddp][ord('e')] = dfa[dii][ord('e')] = exe
        dfa[exe][ord('+')] = dfa[exe][ord('-')] = sge
        dfa[dii][0] = dfa[ddp][0] = dfa[did][0] = dfa[die][0] = end
        for i in range(10):
            t =  ord('0') + i
            dfa[srt][t] = dfa[sgd][t] = dfa[did][t] = did
            dfa[ddp][t] = dfa[dnp][t] = dfa[dii][t] = dii
            dfa[exe][t] = dfa[sge][t] = dfa[die][t] = die
        # run dfa with s
        s = s.strip()
        status = srt
        for c in s:
            status = dfa[status][ord(c)]
            #print status
            if (status == err):
                return False
        return True if dfa[status][0] == end else False

Add Binary

大数加法，只是换成了二进制而已


class Solution:
    # @param a, a string
    # @param b, a string
    # @return a string
    def addBinary(self, a, b):
        a = [ord(c) - ord('0') for c in a][::-1]
        b = [ord(c) - ord('0') for c in b][::-1]
        if (len(a) < len(b)):
            a, b = b, a
        flag = 0
        for i in range(len(a)):
            if (i < len(b)):
                a[i] += b[i]
            a[i] += flag
            flag = a[i] // 2
            a[i] %= 2
        if flag:
            a.append(1)
        return ''.join([chr(c + ord('0')) for c in a][::-1])

Merge Two Sorted Lists

合并两个有序列表
归并排序了，加个临时头节点好写一些


class Solution:
    # @param two ListNodes
    # @return a ListNode
    def mergeTwoLists(self, l1, l2):
        nHead = ListNode(0)
        lt, rt, backHead = l1, l2, nHead
        while lt or rt:
            if lt is None:
                nHead.next, rt = rt, rt.next
            elif rt is None:
                nHead.next, lt = lt, lt.next
            elif lt.val < rt.val:
                nHead.next, lt = lt, lt.next
            else:
                nHead.next, rt = rt, rt.next
            nHead = nHead.next
        return backHead.next

Minimum Path Sum

从矩形格子的左上走到右下，经过的点和加起来最小
不是从上面过来就是从左边过来，DP。
	

class Solution:
    # @param grid, a list of lists of integers
    # @return an integer
    def minPathSum(self, grid):
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if i == 0 and j > 0:
                    grid[i][j] += grid[i][j-1]
                elif j == 0 and i > 0:
                    grid[i][j] += grid[i-1][j]
                elif i > 0 and j > 0:
                    grid[i][j] += min(grid[i-1][j], grid[i][j-1])
        return grid[len(grid) - 1][len(grid[0]) - 1]

Unique Paths II

从矩形格子的左上走到右下，有些格子不能走，求路径数
只能从左边过来或者上边过来，加起来就是到这个格子的路径数，不能走的话该点就是0


class Solution:
    # @param obstacleGrid, a list of lists of integers
    # @return an integer
    def uniquePathsWithObstacles(self, obstacleGrid):
        ans = [[0] * len(obstacleGrid[0]) for i in range(len(obstacleGrid))]
        for i in range(len(obstacleGrid)):
            if obstacleGrid[i][0] == 1: break
            else: ans[i][0] = 1
        for i in range(len(obstacleGrid[0])):
            if obstacleGrid[0][i] == 1: break
            else: ans[0][i] = 1
        for i in range(1, len(obstacleGrid)):
            for j in range(1, len(obstacleGrid[0])):
                if obstacleGrid[i][j] == 1:
                    ans[i][j] = 0
                else:
                    ans[i][j] = ans[i][j-1] + ans[i-1][j]
        return ans[len(ans)-1][len(ans[0])-1]

Unique Paths

从矩形格子的左上走到右下，有些格子不能走，求路径数
比上面一题还简单了，不用考虑不能走的格子


class Solution:
    # @return an integer
    def uniquePaths(self, m, n):
        g = [[0] * n for i in range(m)]
        for i in range(m): g[i][0] = 1
        for j in range(n): g[0][j] = 1
        for i in range(1, m):
            for j in range(1, n):
                g[i][j] = g[i][j-1] + g[i-1][j]
        return g[m-1][n-1]

Rotate List

链表循环右移K个元素(即后k个元素放到链表头)
注意K要模N，然后走len-K步，再将前半部链表接到后面即可。


class Solution:
    # @param head, a ListNode
    # @param k, an integer
    # @return a ListNode
    def rotateRight(self, head, k):
        if not head:
            return head
        p, len = head, 1
        while p.next:
            p, len = p.next, len + 1
        k = len - k % len
        if k == len:
            return head
        pp, len = head, 1
        while len < k:
            pp, len = pp.next, len + 1
        p.next, head, pp.next = head, pp.next, None
        return head

Permutation Sequence

对于集合[1,2..n]，给出它字典序第K大的排列
注意到[1,2..n]有n个排列，从第一位开始枚举没用过的数字，每枚举一个，剩下的m个位置就有m!种排序方法，K不断减去m!直到K<m!，然后继续枚举下一位。


class Solution:
    # @return a string
    def getPermutation(self, n, k):
        d, ans, use = [0, 1], [], ['0'] * n
        for i in range(2, 10) : d.append( i * d[-1])
        for i in range(n):
            ans.append(0)
            for j in range(n):
                if use[j] == 1:
                    continue;
                ans[i] = chr(ord('0') + j + 1)
                if k <= d[n-i-1]:
                    use[j] = 1
                    break
                k -= d[n-i-1]
        return ''.join(ans)

Spiral Matrix II

将1~n^n个数以如下方式填充到矩阵中
一直向某个方向走，走到不能走顺时针旋转90度继续走


[
 [ 1, 2, 3 ],
 [ 8, 9, 4 ],
 [ 7, 6, 5 ]
]
class Solution:
    # @return a list of lists of integer
    def generateMatrix(self, n):
        a = [[0] * n for i in range(n)]
        sx, sy = 0, 0
        dx, dy, dn = [0, 1, 0, -1], [1, 0, -1, 0], 0
        for i in range(n * n):
            a[sx][sy] = i + 1
            nx, ny = sx + dx[dn], sy + dy[dn]
            if nx < 0 or nx < 0 or nx >= n or ny >= n or a[nx][ny]:
                dn = (dn + 1) % 4
                nx, ny = sx + dx[dn], sy + dy[dn]
            sx, sy = nx, ny
        return a

Length of Last Word

求最后一个单词的长度
从后向前找，先找到第一个非空格，再从该位置向前找到第一个空格
	

class Solution:
    # @param s, a string
    # @return an integer
    def lengthOfLastWord(self, s):
        i = len(s) - 1
        while i >= 0 and s[i] == ' ': i -= 1
        j = i - 1
        while j >= 0 and s[j] != ' ': j -= 1
        return 0 if i < 0 else i - j

Insert Interval

将一个区间合并到一个连续不重叠区间集合，要求返回的区间也是连续不重叠的。
将和新区间有重叠的区间合并为一个大区间即可，其它区间不变。


class Solution:
    # @param intervals, a list of Intervals
    # @param newInterval, a Interval
    # @return a list of Interval
    def insert(self, intervals, newInterval):
        ans, inserted = [], False
        for i in range(len(intervals)):
            if intervals[i].end < newInterval.start:
                ans.append(intervals[i])
            elif intervals[i].start > newInterval.end:
                if not inserted:
                    inserted = True
                    ans.append(newInterval)
                ans.append(intervals[i])
            else:
                newInterval.start = min(newInterval.start, intervals[i].start)
                newInterval.end = max(newInterval.end, intervals[i].end)
        if len(ans) == 0 or newInterval.start > ans[-1].end:
            ans.append(newInterval)
        return ans

Merge Intervals

合并若个个区间。
先按左端点排序，合并时直到当前区间左端点比之前所有区间最右的端点还要靠右的时候将之前的区间合并。
	

class Solution:
    # @param intervals, a list of Interval
    # @return a list of Interval
    def merge(self, intervals):
        intervals.sort(cmp = lambda x, y: cmp(x.start, y.start) or (x.start == y.start and cmp(x.end,y.end)))
        ans, p, maxr = [], 0, 0
        for i in range(len(intervals) + 1):
            if i > 0 and (i == len(intervals) or intervals[i].start > maxr):
                ans.append(Interval(intervals[p].start, maxr))
                p = i
            if i < len(intervals):
                maxr = max(maxr, intervals[i].end)
        return ans

Jump Game

每个格子上的数字N表示从这个格子可以到后面的N格，问是否能从头走到尾。
x表示从当前位置最多还能走几步， 每走一步都将x-1和当前格子的值的较大值作为x的值。

class Solution:
    # @param A, a list of integers
    # @return a boolean
    def canJump(self, A):
        if len(A) == 0:
            return False
        maxj = A[0]
        for i in range(1, len(A)):
            maxj -= 1
            if (maxj < 0):
                return False
            maxj = max(maxj, A[i])
        return True

Spiral Matrix

和上面的Spiral Matrix II差不多，就是从填数变成了取数。


[
 [ 1, 2, 3 ],
 [ 4, 5, 6 ],
 [ 7, 8, 9 ]
]
return [1,2,3,6,9,8,7,4,5]
class Solution:
    # @param matrix, a list of lists of integers
    # @return a list of integers
    def spiralOrder(self, matrix):
        if len(matrix) == 0:
            return []
        a, ans, m, n = matrix, [], len(matrix), len(matrix[0])
        x = [[0] * n for i in range(m)]
        sx, sy = 0, 0
        dx, dy, dn = [0, 1, 0, -1], [1, 0, -1, 0], 0
        for i in range(m * n):
            ans.append(a[sx][sy])
            x[sx][sy] = 1
            nx, ny = sx + dx[dn], sy + dy[dn]
            if nx < 0 or nx < 0 or nx >= m or ny >= n or x[nx][ny]:
                dn = (dn + 1) % 4
                nx, ny = sx + dx[dn], sy + dy[dn]
            sx, sy = nx, ny
        return ans

Maximum Subarray

求子区间最大值
前缀和加到负数就重新累加，因为前面的数加进来只会减小总和。


class Solution:
    # @param A, a list of integers
    # @return an integer
    def maxSubArray(self, A):
        ans, sum = A[0], A[0]
        for i in range(1, len(A)):
            if (sum < 0):
                sum = A[i]
            else:
                sum += A[i]
            ans = max(ans, sum)
        return ans

N-Queens II

八(N)皇后问题求解数
位压缩DFS


class Solution:
    # @return an integer
    def totalNQueens(self, n):
        self.ans = 0
        self.full = ((1 << n) - 1)
        self.dfs(n, 0, 0, 0, 0)
        return self.ans
        
    def dfs(self, n, p, lt, rt, nt):
        if n == p:
            self.ans += 1
            return
        can = (~(lt | rt | nt) & self.full)
        while can:
           now = can&-can
           self.dfs(n, p+1, (lt|now)>>1, (rt|now)<<1, nt|now)
           can -= now

N-Queens

还是N皇后问题，只是要给出具体解
一样是未压缩DFS，py的字符串和list总要转来转去真是不怎么方便。
	

class Solution:
    # @return a list of lists of string
    def solveNQueens(self, n):
        self.ans, self.dt = [], {}
        self.full = ((1 << n) - 1)
        for i in range(n): self.dt[1<<i] = i
        tmp = [['.'] * n for i in range(n)]
        self.dfs(n, 0, 0, 0, 0, tmp)
        return self.ans
    def dfs(self, n, p, lt, rt, nt, tmp):
        if n == p:
            self.ans.append([''.join(s) for s in tmp])
            return
        can = (~(lt | rt | nt) & self.full)
        while can:
           now = can&-can
           tmp[p][self.dt[now]] = 'Q'
           self.dfs(n, p+1, (lt|now)>>1, (rt|now)<<1, nt|now, tmp)
           tmp[p][self.dt[now]] = '.'
           can -= now

Pow(x, n)

快速幂，二分

class Solution:
    # @param x, a float
    # @param n, a integer
    # @return a float
    def pow(self, x, n):
        if n == 0:
            return 1
        xx = pow(x, n >> 1)
        xx *= xx
        if n & 1: xx *= x
        return xx

Anagrams

真不知道题目这单词是什么意思。。其实就是列表里如果有多个单词由相同字母组成就加到结果里，比如cat,tac。
排序后map一下就OK了，注意处理重复问题，Map中添加新元素时记录该元素的下标，遇到Anagrams后将对应单词加进结果集并将下标改为-1，下次就不再添加该单词。


class Solution:
    # @param strs, a list of strings
    # @return a list of strings
    def anagrams(self, strs):
        ans, dt = [], {}
        for i in range(len(strs)):
            lt = list(strs[i])
            lt.sort()
            s = ''.join(lt)
            d = dt.get(s, -2)
            if d == -2:
                dt[s] = i
            elif d == -1:
                ans.append(strs[i])
            else:
                ans.append(strs[i])
                ans.append(strs[d])
                dt[s] = -1
        return ans

Rotate Image

将一个二维数组90度旋转，要求原地工作。
数学学的差，半天才把源坐标和目的坐标的对应关系算出来。四个一组进行旋转。


class Solution:
    # @param matrix, a list of lists of integers
    # @return a list of lists of integers
    def rotate(self, matrix):
        L = len(matrix)
        R = (L + 1) // 2
        for x in range(0, R):
            for y in range(0, L - R):
                #(x,y)->(y,l-1-x)->(l-1-x,l-1-y)->(l-1-y,x)
                matrix[x][y], matrix[y][L-1-x], matrix[L-1-x][L-1-y], matrix[L-1-y][x] \
                = matrix[L-1-y][x], matrix[x][y], matrix[y][L-1-x], matrix[L-1-x][L-1-y]
        return matrix

Permutations II
Permutations

这两题一样，都是给出一个集合，得到它的所有排列。只是一个有重复，一个没重复。按下面这种解法有没有重复都是一样的。
这里实现了一下STL里的next_permutation函数，用于得到当前排列的下一个排列（按字典序）。
next_permutation先从后向前找到第一个d[i]d[i]的数，最后swap(d[i],d[j])并且reverse(d[i+1…n])就得到了下一个排列。


class Solution:
    # @param num, a list of integer
    # @return a list of lists of integers
    def permuteUnique(self, num):
        num.sort()
        ans = [num[:]]
        while self.next_permutation(num):
            ans.append(num[:])
        return ans
    def next_permutation(self, num):
        for i in range(len(num)-2, -1, -1):
            if num[i] < num[i+1]:
                break
        else:
            return False
        for j in range(len(num)-1, i, -1):
            if num[j] > num[i]:
                num[i], num[j] = num[j], num[i]
                break
        for j in range(0, (len(num) - i)//2):
            num[i+j+1], num[len(num)-j-1] = num[len(num)-j-1], num[i+j+1] 
        return True

Jump Game II

每个格子上的数字N表示从这个格子可以跳到后面的1~N格，问从头到尾至少要跳几步。
一边遍历一边记录从前面的格子最远能够跳到的格子，假设前一步最远可以跳到第x格，那么遍历到第x格的时候，下一步的最远距离也已经知道了。
	

class Solution:
    # @param A, a list of integers
    # @return an integer
    def jump(self, A):
        maxj, maxn, tms = 0, 0, 0
        for i in range(len(A) - 1):
            maxn = max(maxn, A[i] + i)
            if i == maxj:
                maxj, tms = maxn, tms + 1
        return tms

Wildcard Matching

实现带?和*的模糊匹配，其中?匹配单字符，*匹配任意长度字符串
先写了个DP，超时了，模式串和匹配串都有可能非常长。对于这题的数据，搜索还快一些，对于号使用非贪婪匹配，优先匹配尽量少的字符。记录最后一次匹配到的时p和s扫描到的位置，失配时回溯（其实就是枚举*匹配的长度）。
	

class Solution:
    # @param s, an input string
    # @param p, a pattern string
    # @return a boolean
    def isMatch(self, s, p):
        ps, pp, lastp, lasts = 0, 0, -1, -1
        while ps < len(s):
            if pp < len(p) and (s[ps] == p[pp] or p[pp] == '?'):
                ps, pp = ps + 1, pp + 1
            elif pp < len(p) and p[pp] == '*':
                pp = pp + 1
                lastp, lasts = pp, ps
            elif lastp != -1:
                lasts = lasts + 1
                pp, ps = lastp, lasts
            else:
                return False
        while pp < len(p) and p[pp] == '*':
            pp = pp + 1
        return ps == len(s) and pp == len(p)

Multiply Strings

字符串模拟大数乘法
虽然py支持大数，但还是手写一下吧，再次觉得py处理字符串转来转去的不方便，也许是我太菜了吧。。


class Solution:
    # @param num1, a string
    # @param num2, a string
    # @return a string
    def multiply(self, num1, num2):
        num1 = [ord(i) - ord('0') for i in num1][::-1]
        num2 = [ord(i) - ord('0') for i in num2][::-1]
        ans = [0] * (len(num1) + len(num2) + 1)
        for i in range(len(num1)):
            for j in range(len(num2)):
                ans[i + j] += num1[i] * num2[j]
                ans[i + j + 1] += ans[i + j]
                #ans[i + j]
        while len(ans) > 1 and ans[len(ans) - 1] == 0:
            ans.pop()
        return ''.join([chr(i + ord('0')) for i in ans][::-1])

Trapping Rain Water

每个木板有高度，求最多能蓄多少水
分别求出每块木板左边最高的和右边最高的，然后取较小的就是该块木板的最高蓄水位。


class Solution:
    # @param A, a list of integers
    # @return an integer
    def trap(self, A):
        maxl, maxr, maxv, ans = [], [], 0, 0
        for i in range(len(A)):
            if A[i] > maxv: maxv = A[i]
            maxl.append(maxv)
        maxv = 0
        for i in range(len(A)-1, -1, -1):
            if A[i] > maxv: maxv = A[i]
            maxr.append(maxv)
        for i in range(len(A)):
            minh = min(maxl[i], maxr[len(A) - i - 1]) - A[i]
            ans += minh if minh > 0 else 0
        return ans

First Missing Positive

找第一个少了的正数。
如果1~N都有，N正好就是数组长度，所以用原数组做Hash就可以了，Hash的范围是1~N。具体实现是不断swap当前数和它应该在的位置上的数，直到当前数不能换了为止（每个数最多只会帮换一次，所以复杂度还是O(N)）。


class Solution:
    # @param A, a list of integers
    # @return an integer
    def firstMissingPositive(self, A):
        L = len(A)
        for i in range(L):
            while A[i] > 0 and A[i] <= L and A[i] != A[A[i] - 1] and i != A[i] - 1:
                A[A[i] - 1], A[i] = A[i], A[A[i] - 1]
                #A[i], A[A[i] - 1] = A[A[i] - 1], A[i]  dosen't work
        for i in range(L):
            if i != A[i] - 1:
                return i + 1
        return L + 1

Combination Sum II

在集合中选几个数和为N，每个数只能用一次，问有多少种解法。
这种有重复数字需要避免重复解的DFS，处理方法基本都一样，就是DFS的时候如果前一个数是相同的并且没用，那么这个数也不能用。


class Solution:
    # @param candidates, a list of integers
    # @param target, integer
    # @return a list of lists of integers
    def combinationSum2(self, candidates, target):
        candidates.sort()
        self.ans, tmp, use = [], [], [0] * len(candidates)
        self.dfs(candidates, target, 0, 0, tmp, use)
        return self.ans
    def dfs(self, can, target, p, now, tmp, use):
        if now == target:
            self.ans.append(tmp[:])
            return
        for i in range(p, len(can)):
            if now + can[i] <= target and (i == 0 or can[i] != can[i-1] or use[i-1] == 1):
                tmp.append(can[i]);
                use[i] = 1
                self.dfs(can, target, i+1, now + can[i], tmp, use)
                tmp.pop()
                use[i] = 0

Combination Sum

上一题的简化版，而且每个数可以用多次，直接DFS就可以了


class Solution:
    # @param candidates, a list of integers
    # @param target, integer
    # @return a list of lists of integers
    def combinationSum(self, candidates, target):
        candidates.sort()
        self.ans, tmp = [], []
        self.dfs(candidates, target, 0, 0, tmp)
        return self.ans
    def dfs(self, candidates, target, p, now, tmp):
        if now == target:
            self.ans.append(tmp[:])
            return
        for i in range(p, len(candidates)):
            if now + candidates[i] <= target:
                tmp.append(candidates[i])
                self.dfs(candidates, target, i, now+candidates[i], tmp)
                tmp.pop()

Count and Say

求以下序列的第N项，模拟即可。


1, 11, 21, 1211, 111221, ...
1 is read off as "one 1" or 11.
11 is read off as "two 1s" or 21.
21 is read off as "one 2, then one 1" or 1211.
class Solution:
    # @return a string
    def countAndSay(self, n):
        s, now = [str(1), ''], 0
        for i in range(1, n):
            now, pre, tot = now^1, now, 0
            s[now], p = "", 0
            while p  < len(s[pre]):
                tot, v, p = 1, s[pre][p], p + 1
                while p < len(s[pre]) and v == s[pre][p]:
                    p += 1
                    tot += 1
                s[now] += str(tot) +  v
        return s[now]

Sudoku Solver

求数独的解，dancing links不会，只能写个位压缩版了。。
	

class Solution:
    # @param board, a 9x9 2D array
    # Solve the Sudoku by modifying the input board in-place.
    # Do not return any value.
    def solveSudoku(self, board):
        lt, rt, bt = [0] * 9, [0] * 9, [0] * 9
        self.dt = {}
        for i in range(9): self.dt[1<<i] = chr(ord('1')+i)
        for i in range(9):
            board[i] = list(board[i])
            for j in range(9):
                if (board[i][j] == '.'):
                    continue;
                num = ord(board[i][j]) - ord('1')
                lt[i] |= 1 << num
                rt[j] |= 1 << num
                bt[j//3*3+i//3] |= 1 << num
        self.dfs(board, 0, lt, rt, bt)
        board = [''.join(s) for s in board]
    
    def dfs(self, board, p, lt, rt, bt):
        while p < 81 and board[p/9][p%9] != '.':
            p += 1
        if p == 81:
            return True
        i, j, k = p//9, p%9, p%9//3*3+p//9//3
        if board[i][j] != '.':
            self.dfs(board, p + 1, lt, rt, bt)
            return True
        can = (~(lt[i]|rt[j]|bt[k])) & (0x1ff)
        pre = board[i]
        while can:
            num = can&-can
            board[i][j] = self.dt[num]
            lt[i] |= num
            rt[j] |= num
            bt[k] |= num
            if self.dfs(board, p + 1, lt, rt , bt):
                return True
            board[i][j] = '.'
            lt[i] &= ~num
            rt[j] &= ~num
            bt[k] &= ~num
            can -= num
        return False

Valid Sudoku

判断数独初始局面是否合法，就是在上题初始化的过程中加上了判断。


class Solution:
    # @param board, a 9x9 2D array
    # @return a boolean
    def isValidSudoku(self, board):
        lt, rt, bt = [0] * 9, [0] * 9, [0] * 9
        for i in range(9):
            for j in range(9):
                print i, j
                if (board[i][j] == '.'):
                    continue;
                num = ord(board[i][j]) - ord('1')
                if 0 == (~(lt[i]|rt[j]|bt[j/3*3+i/3]) & (1<<num)):
                    return False
                lt[i] |= 1 << num
                rt[j] |= 1 << num
                bt[j/3*3+i/3] |= 1 << num
        return True

Search Insert Position

给一个排序数组和一个数，找出这个数应该插在哪个位置。
二分稍加变形，保证l最后停在第一个比它大的数的位置上。
	

class Solution:
    # @param A, a list of integers
    # @param target, an integer to be inserted
    # @return integer
    def searchInsert(self, A, target):
        l, h = 0, len(A) 
        while l < h:
            m = (l + h) // 2
            if A[m] < target:
                l = m + 1
            else:
                h = m
        return l

Search for a Range

找出排序数组中一个数第一次出现的位置和最后一次出现的位置。
也是二分变形，写对真不容易。。


class Solution:
    # @param A, a list of integers
    # @param target, an integer to be searched
    # @return a list of length 2, [index1, index2]
    def searchRange(self, A, target):
        return [self.lower_bound(A, target), self.upper_bound(A, target)]
    def lower_bound(self, A, target):
        l, h, m = 0, len(A), 0
        while l < h:
            m = (l + h) >> 1
            if A[m] < target:
                l = m + 1
            else:
                h = m
        return l if l < len(A) and A[l] == target else -1
    def upper_bound(self, A, target):
        l, h, m = 0, len(A),  0
        while l < h:
            m = (l + h) >> 1
            if A[m] <= target:
                l = m + 1
            else:
                h = m
        return l-1 if l-1 < len(A) and A[l-1] == target else -1

Search in Rotated Sorted Array

把一个有序数组循环右移若干位之后，查找某个数是否在这个数组中。
还是二分，只是到底是向左还是向右的时候判断要复杂一些。


class Solution:
    # @param A, a list of integers
    # @param target, an integer to be searched
    # @return an integer
    def search(self, A, target):
        l, h = 0, len(A) - 1
        while (l <= h):
            m = l + ((h - l) >> 1)
            if A[m] == target:
                return m
            elif (A[m] > A[l] and target < A[m] and target >= A[l]) or (A[m] < A[l] and not (target <= A[h] and target > A[m])):
                h = m - 1
            else:
                l = m + 1
        return -1

Longest Valid Parentheses

最长的合法括号序列。
写了好久，首先用栈可以找到每个右括号对应的左括号，如果它对应的左括号前面也是一个独立的合法括号序列，要累加起来。


class Solution:
    # @param s, a string
    # @return an integer
    def longestValidParentheses(self, s):
        stk, p ,ans = [], [0] * len(s), 0
        for i in range(len(s)):
            if s[i] == '(':
                stk.append(i)
            elif s[i] == ')':
                if len(stk) > 0:
                    p[i] = i - stk[-1] + 1
                    if i >= p[i] and p[i - p[i]]:
                        p[i] += p[i-p[i]]
                    ans = max(ans, p[i])
                    stk.pop()
        return ans

Next Permutation

求下一个序列，前面的Permutations题中已经用到了。(CTRL+F向上找。。)

class Solution:
    # @param num, a list of integer
    # @return a list of integer
    def nextPermutation(self, num):
        for i in range(len(num)-2, -1, -1):
            if num[i] < num[i+1]:
                break
        else:
            num.reverse()
            return num
        for j in range(len(num)-1, i, -1):
            if num[j] > num[i]:
                num[i], num[j] = num[j], num[i]
                break
        for j in range(0, (len(num) - i)//2):
            num[i+j+1], num[len(num)-j-1] = num[len(num)-j-1], num[i+j+1]
        return num

Substring with Concatenation of All Words

给出一个字符串集合L和字符串S，找出S从哪些位置开始恰好包含每个字符串各一次。
这类判断某一段包含了哪些内容的题做法都差不多，一个pre指针，一个last指针，用一个集合记录这之间出现的值，last指针不断往后扫直到扫到多余的元素，然后pre指针再从之前的位置扫到第一个有这个元素的位置之后，这时候last指针就可以继续后移了。
这个题就是要做一些变形，将S分成len(L(0))段，每段分别使用以上算法。比如len(L(0))=3,len(S)=10时，就分成S[0,3,6,9],S[1,4,7],S[2,5,8]三段。


class Solution:
    # @param S, a string
    # @param L, a list of string
    # @return a list of integer
    def findSubstring(self, S, L):
        LS, LL, LL0 = len(S), len(L), len(L[0])
        did, ids, dl = {}, 0, {}
        for s in L: 
            id = did.get(s, -1)
            if id == -1:
                 ids = ids + 1
                 id = ids
                 did[s] = id
            dl[id] = dl.get(id, 0) + 1
        
        pos, ans = [0] * LS, []
        for k, v in did.items():
            f = S.find(k)
            while f != -1:
                pos[f] = v
                f = S.find(k, f + 1)
                
        for sp in range(LL0):
            np, pp, tot, dt = sp, sp, 0, {}
            while np < LS:
                t = pos[np]
                if t == 0:
                    tot, dt = 0, {}
                    pp, np = np + LL0, np + LL0
                elif dt.get(t, 0) < dl[t]:
                    dt[t] = dt.get(t, 0) + 1
                    tot = tot + 1
                    if tot == LL:
                        ans.append(pp)
                    np = np + LL0
                else:
                    while pos[pp] != t:
                        tot = tot - 1
                        dt[pos[pp]] -= 1
                        pp = pp + LL0
                    pp = pp + LL0
                    dt[t] -= 1
                    tot = tot - 1
        return ans

Divide Two Integers

不使用乘除法实现加法。
二进制思想，用二进制去凑答案。


class Solution:
    # @return an integer
    def divide(self, dividend, divisor):
        flag, ans = 0, 0
        if dividend < 0:
            flag, dividend = flag^1, -dividend
        if divisor < 0:
            flag, divisor = flag^1, -divisor
        while dividend >= divisor:
            count, newDivisor = 1, divisor
            while newDivisor + newDivisor <= dividend:
                newDivisor = newDivisor + newDivisor
                count = count + count
            dividend -= newDivisor
            ans += count
        return ans if flag == 0 else -ans

Implement strStr()

实现strStr()函数
KMP了，好久不写真的写不出来了。。。


class Solution:
    # @param haystack, a string
    # @param needle, a string
    # @return a string or None
    def strStr(self, haystack, needle):
        lenh, lenn = len(haystack), len(needle)
        if lenn == 0:
            return haystack
        next, p = [-1] * (lenn), -1
        for i in range(1, lenn):
            while p >= 0 and needle[i] != needle[p + 1]:
                p = next[p]
            if needle[i] == needle[p + 1]:
                p  = p + 1
            next[i] = p
        p = -1
        for i in range(lenh):
            while p >= 0 and haystack[i] != needle[p + 1]:
                p = next[p]
            if haystack[i] == needle[p + 1]:
                p = p + 1
            if p + 1 == lenn:
                return haystack[i - p:] 
        return None

Remove Element

在数组中移除指定元素
不是指定的元素就往前面放就行了


class Solution:
    # @param    A       a list of integers
    # @param    elem    an integer, value need to be removed
    # @return an integer
    def removeElement(self, A, elem):
        sz = 0
        for i in range(0, len(A)):
            if A[i] != elem:
                A[sz] = A[i]
                sz += 1
        return sz

Remove Duplicates from Sorted Array

有序数组删除重复元素到只留一个
往数组前部放，放之前保证和已放的最后一个不一样即可


class Solution:
    # @param a list of integers
    # @return an integer
    def removeDuplicates(self, A):
        if len(A) == 0:
            return 0
        sz = 1
        for i in range(1, len(A)):
            if A[i] != A[i-1]:
                A[sz] = A[i]
                sz += 1
        return sz

Reverse Nodes in k-Group

链表，每K个一段进行reverse。
到每第K个元素的时候掉个头就行，中间就是正常的链表逆置，注意最后几个不要处理。


class Solution:
    # @param head, a ListNode
    # @param k, an integer
    # @return a ListNode
    def reverseKGroup(self, head, k):
        nHead = ListNode(0)
        nHead.next = head
        p2, lenl = head, 0
        while p2: p2, lenl = p2.next, lenl + 1
        now, pre, ind = head, nHead, 1
        preHead, preHeadNext = nHead, head
        while now:
            if lenl - ind < lenl % k:
                break
            next = now.next
            now.next = pre
            if ind % k == 0:
                preHead.next = now
                preHeadNext.next = next
                preHead = preHeadNext
                pre = preHead
                preHeadNext = next
            else:
                pre = now
            now, ind = next, ind + 1
        return nHead.next

Swap Nodes in Pairs

上一题的简化版，相当于 K=2
代码写的相当暴力，反正两个元素最多也就3个NEXT就能访问到下一段。。


class Solution:
    # @param a ListNode
    # @return a ListNode
    def swapPairs(self, head):
        if head is None or head.next is None:
            return head
        nHead = ListNode(0)
        nHead.next = head
        p1, p2 = nHead, head
        while p2 and p2.next:
            p2 = p2.next.next
            p1.next.next.next = p1.next
            p1.next = p1.next.next
            p1.next.next.next = p2
            p1 = p1.next.next
        return nHead.next

Merge k Sorted Lists

合并K个有序链表。
和归并一样，每次选K个链表头部最小的元素。这里的优化就是用一个堆来维护这K个元素的最小值，复杂度O(sum(len(Ki)) * logK)


class Solution:
    # @param a list of ListNode
    # @return a ListNode
    def mergeKLists(self, lists):
        self.heap = [[i, lists[i].val] for i in range(len(lists)) if lists[i] != None]
        self.hsize = len(self.heap)
        for i in range(self.hsize - 1, -1, -1):
            self.adjustdown(i)
            
        nHead = ListNode(0)
        head = nHead
        while self.hsize > 0:
            ind, val = self.heap[0][0], self.heap[0][1]
            head.next = lists[ind]
            head = head.next
            lists[ind] = lists[ind].next
            if lists[ind] is None:
                self.heap[0] = self.heap[self.hsize-1]
                self.hsize = self.hsize - 1
            else:
                self.heap[0] = [ind, lists[ind].val]
            self.adjustdown(0)
        return nHead.next
            
    def adjustdown(self, p):
        lc = lambda x: (x + 1) * 2 - 1
        rc = lambda x: (x + 1) * 2
        while True:
            np, pv = p, self.heap[p][1]
            if lc(p) < self.hsize and self.heap[lc(p)][1] < pv:
                np, pv = lc(p), self.heap[lc(p)][1]
            if rc(p) < self.hsize and self.heap[rc(p)][1] < pv:
                np = rc(p)
            if np == p:
                break
            else:
                self.heap[np], self.heap[p] = self.heap[p], self.heap[np]
                p = np

Generate Parentheses

生成所有可能的括号序列
DFS搜索了，注意右括号不能比左括号多即可


class Solution:
    # @param an integer
    # @return a list of string
    def generateParenthesis(self, n):
        self.ans, tmp = [], []
        lb = 0
        self.dfs(lb, 0, n, tmp)
        return self.ans
    
    def dfs(self, lb, p, n, tmp):
        if p == n * 2:
            self.ans.append(''.join(tmp))
            return
        if lb < n:
            tmp.append('(')
            self.dfs(lb + 1, p + 1, n, tmp)
            tmp.pop()
        if p - lb < lb:
            tmp.append(')')
            self.dfs(lb, p + 1, n, tmp)
            tmp.pop()

Valid Parentheses

判断括号序列是否合法，共有三种括号
用栈，遇到右括号时左括号必须和当前括号是一对，然后出栈
	

class Solution:
    # @return a boolean
    def isValid(self, s):
        dct = {'(':')', '[':']', '{':'}'}
        stk = []
        for c in s:
            if dct.get(c, None):
                stk.append(c)
            elif len(stk) == 0 or dct[stk[-1]] != c:
                return False
            else:
                stk.pop()
        return True if len(stk) == 0 else False

Remove Nth Node From End of List

删除链表的第N个元素，只能扫一遍
一个指针先走N-K步，然后另一个指针在开头，一起走直到先走的指针到达末尾，删除后走的指针


class Solution:
    # @return a ListNode
    def removeNthFromEnd(self, head, n):
        nHead = ListNode(0)
        nHead.next = head
        p, t = 0, head
        while p < n:
            t = t.next
            p += 1
        pre = nHead
        while t:
            t, pre = t.next, pre.next
        pre.next = pre.next.next
        return nHead.next

Letter Combinations of a Phone Number

按一串电话按键，求所有可能的字母组合
DFS
	

class Solution:
    # @return a list of strings, [s1, s2]
    def letterCombinations(self, digits):
        if len(digits) == 0:
            return [""]
        self.dglist = ["", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"]
        self.ans, tmp = [], []
        self.dfs(digits, 0, tmp)
        return self.ans
    
    def dfs(self, digits, p, tmp):
        if (p == len(digits)):
            self.ans.append(''.join(tmp))
            return
        for c in self.dglist[ord(digits[p]) - ord('0')]:
            tmp.append(c)
            self.dfs(digits, p + 1, tmp)
            tmp.pop()

4Sum

求集合中4个数的和为0的所有解。
做法和3sum一样，py超时，用c++写的，复杂度O(N^3)。


class Solution {
public:
    vector<vector<int> > fourSum(vector<int> &num, int target) {
        vector<vector<int> > ans;
        sort(num.begin(), num.end());
        for (int i = 0; i < num.size(); i++) {
            if (i > 0 && num[i] == num[i-1]) continue;
            for (int j = i + 1; j < num.size(); j++) {
                if (j > i + 1 && num[j] == num[j - 1]) continue;
                int l = j + 1, r = num.size() - 1;
                while (l < r) {
                    int sum = num[i] + num[j] + num[l] + num[r];
                    if (sum == target) {
                        ans.push_back({num[i], num[j], num[l], num[r]});
                        while (l < r && num[l] == num[l + 1]) l++; l++;
                        while (l < r && num[r] == num[r - 1]) r--; r--;
                    } else if (sum < target) {
                        l++;
                    } else {
                        r--;
                    }
                }
             }
        }
        return ans;
    }
};

3Sum Closest

求集合中3个数能够得到的距离target最近的和
和3Sum一样，而且不用处理重复解问题了。
	

class Solution:
    # @return an integer
    def threeSumClosest(self, num, target):
        num.sort()
        ans = None
        for i in range(len(num)):
            l, r = i + 1, len(num) - 1
            while (l < r):                    
                sum = num[l] + num[r] + num[i]
                if ans is None or abs(sum- target) < abs(ans - target):
                    ans = sum
                if sum <= target:
                    l = l + 1
                else:
                    r = r - 1
        return ans

3Sum

求3个数的和为target的所有解。
枚举第一个数，然后第二个数为这个数的后一个数，第三个数为最后一个数，如果和小于0，第二个数后移，如大于0第三个数前移，等于0的话记录结果并且都向中间移。注意处理重复解。


class Solution:
    # @return a list of lists of length 3, [[val1,val2,val3]]
    def threeSum(self, num):
        num.sort()
        dct, ans = {}, []
        for i in range(0, len(num)):
            if (i > 0 and num[i] == num[i-1]):
                continue
            l, r = i + 1, len(num) - 1
            while l < r:
                sum = num[l] + num[r] + num[i]
                if sum == 0:
                    ans.append([num[i], num[l], num[r]])
                    while l < r and num[l] == num[l + 1]: l = l + 1
                    while l < r and num[r] == num[r - 1]: r = r - 1
                    l, r = l + 1, r - 1
                elif sum < 0:
                    l = l + 1
                else:
                    r = r - 1   
        return ans

Longest Common Prefix

求所有的字符串的最长公共前缀
暴力直接一位位扫，直到遇到某位有不同的字符或者某个字符串结尾


class Solution:
    # @return a string
    def longestCommonPrefix(self, strs):
        if len(strs) <= 1:
            return strs[0] if len(strs) == 1 else ""
        end, minl = 0, min([len(s) for s in strs])
        while end < minl:
            for i in range(1, len(strs)):
                if strs[i][end] != strs[i-1][end]:
                    return strs[0][:end]
            end = end + 1
        return strs[0][:end]

Roman to Integer

罗马数字转阿拉伯数字。
右边比左边大就减对应值，否则就加对应值。


class Solution:
    # @return an integer
    def romanToInt(self, s):
        roval = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
        ans = 0
        for i in range(len(s)):
            if i + 1 < len(s) and roval[s[i]] < roval[s[i+1]]:
                ans -= roval[s[i]]
            else:
                ans += roval[s[i]]
        return ans

Integer to Roman

阿拉伯数字转罗马数字。
打表。
	

class Solution:
    # @return a string
    def intToRoman(self, num):
        ronum  = [['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'],
                  ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC'],
                  ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM'],
                  ['', 'M', 'MM', 'MMM', '  ', ' ', '  ', '   ', '    ', '  ']]
        ans, ind = '', 0
        while num:
            ans = ronum[ind][num%10] + ans
            num, ind = num / 10, ind + 1
        return ans

Container With Most Water

给出N个高度不同的挡板y,每个柱子距离1，找出两个挡板，使这两个挡板之间盛水最多
一开始题目理解错了，以为挡板都先放好了，其实是选两个挡板出来，其它挡板不用。。
从两边向中间枚举，假设两块挡板满足height[x]<height[y]，那么把y向中间移动肯定得不到更优的解，所以每次选较矮的一块往中间移


class Solution:
    # @return an integer
    def maxArea(self, height):
        l, r, ans = 0, len(height) - 1, 0
        while l <= r:
            ans = max(ans, (r - l) * min(height[r], height[l]))
            if height[l] < height[r]:
                l = l + 1
            else:
                r = r - 1
        return ans

Regular Expression Matching

实现带.和*的正则表达式匹配，其中.匹配任一字符，*表示重复之前内容0次以上。
DP做的，dp[i][j]表示s[1..i]和p[1..j]匹配，需要考虑的情况还是比较复杂的，搜索应该也可行。


class Solution:
    # @return a boolean
    def isMatch(self, s, p):
        s, p = ' ' + s, ' ' + p
        dp = [[False] * (len(p)) for i in range(len(s))]
        dp[0][0] = True
        ind = 2
        while ind < len(p) and p[ind] == '*':
            dp[0][ind], ind = True, ind + 2
        for i in range(1, len(s)):
            for j in range(1, len(p)):
                if (s[i] == p[j] or p[j] == '.') and dp[i-1][j-1]:
                    dp[i][j] = True
                if p[j] == '*' and (dp[i][j-2] or ((p[j-1] == '.' or p[j-1] == s[i]) and (dp[i-1][j-2] or dp[i-1][j]))):
                    dp[i][j] = True
        return dp[len(s) - 1][len(p) - 1]
s = Solution()
print s.isMatch("aa", "a")              # False
print s.isMatch("aa", "aa")             # True
print s.isMatch("aaa","aa")             # False
print s.isMatch("aa", "a*")             # True
print s.isMatch("aa", ".*")             # True
print s.isMatch("ab", ".*")             # True
print s.isMatch("aab", "c*a*b")         # True
print s.isMatch("aaa", "ab*a")          # Fasle
print s.isMatch("aaba", "ab*a*c*a")     # False
print s.isMatch("", ".*")               # True
print s.isMatch("bbab", "b*a*")         # False
print s.isMatch("aab", "b.*")           # False

Palindrome Number

判断一个数字是否是回文串
判断翻转后的数字和原数字是否相同即可。虽然翻转后可能溢出。。但是。。这种东西py没有。。
一开始还写了个数组存，其实不需要，一开始使a=x，然后不断b=b*10+a%10，b就是a翻转的结果了

class Solution:
    # @return a boolean
    def isPalindrome(self, x):
        if x <= 0:
            return False if x < 0 else True
        a, b = x, 0
        while a:
            b, a = b * 10 + a % 10, a / 10
        return b == x

String to Integer (atoi)

实现atoi
坑略多，主要是以下几个：
1.前面有空格；
2.遇到非法字符就不再分析后面的；
3.有可能越界。


class Solution:
    # @return an integer
    def atoi(self, str):
        if len(str) == 0:
            return 0
        sgn, num, p = 0, 0, 0
        imin, imax = -1<<31, (1<<31)-1
        while str[p] == ' ':
            p  = p + 1
        if str[p] == '-' or str[p] == '+':
            sgn = 1 if str[p] == '-' else 0
            p = p + 1
        while p < len(str) and str[p] >= '0' and str[p] <= '9':
            num = num * 10 + ord(str[p]) - ord('0')
            x = -num if sgn else num
            if x < imin: return imin
            if x > imax: return imax
            p = p + 1
        return -num if sgn else num

Reverse Integer

翻转一个数字
注意可能会溢出，py就不用管了，但是c的话记得用long long


class Solution:
    # @return an integer
    def reverse(self, x):
        a = 0
        b = x if x > 0 else -x
        while b:
            a, b = a * 10 + b % 10, b / 10 
        return a if x > 0 else -a

ZigZag Conversion

将一个字符串的字符Z形排列，然后按行顺序输出所有字母，下面有样例
找到规律，然后模拟

'''
P   A   H   N   1   5   ...
A P L S I I G   2 4 6 8 ...
Y   I   R       3   7   ...
convert("PAYPALISHIRING", 3) should return "PAHNAPLSIIGYIR".
'''
class Solution:
    # @return a string
    def convert(self, s, nRows):
        if nRows == 1 or len(s) == 0:
            return s
        res, lens = [], len(s)
        add, now = [nRows * 2 - 2, 0], 0
        for i in range(nRows):
            if i < lens:
                res.append(i)
            while res[-1] + add[now] < lens:
                if add[now] > 0:
                    res.append(res[-1] + add[now])
                now ^= 1
            add, now = [add[0] - 2, add[1] + 2], 0
        return ''.join([s[i] for i in res])
s = Solution()
print s.convert("A", 2)

Longest Palindromic Substring

求最大回文子串长度
这个O(n)算法看了不亚于三遍了，每次写都会忘。。可能是因为没理解透彻，然后也没怎么用吧。
核心思想就是利用了回文串的对称性质。


class Solution:
    # @return a string
    def longestPalindrome(self, s):
        arr = ['$', '#']
        for i in range(len(s)):
            arr.append(s[i])
            arr.append('#')
        p = [0] * len(arr)
        mx, pos, ansp = 0, 0, 0
        for i in range(1, len(arr)):
            p[i] = min(mx - i, p[2 * pos - i]) if mx > i else 1 
            while p[i] + i < len(arr) and arr[i + p[i]] == arr[i - p[i]]: 
                p[i] += 1
            if p[i] + i > mx:
                mx, pos = p[i] + i, i
            if p[i] > p[ansp]:
                ansp = i
        st = (ansp - p[ansp] + 1) // 2
        return s[st:st + p[ansp] - 1]

Add Two Numbers

链表版大数加法
和数组没什么区别吧。。？翻转都不用了。。


class Solution:
    # @return a ListNode
    def addTwoNumbers(self, l1, l2):
        nHead, flag = ListNode(0), 0
        head = nHead
        while flag or l1 or l2:
            node = ListNode(flag)
            if l1: 
                node.val += l1.val
                l1 = l1.next
            if l2: 
                node.val += l2.val
                l2 = l2.next
            flag = node.val // 10
            node.val %= 10
            head.next, head = node, node
        return nHead.next

Longest Substring Without Repeating Characters

求最长的没有重复字符的子串
维护两个指针，保证两个指针之间的串没有重复字符，后指针扫到某个字符重复时就将前指针向后移到第一个和当前字符相同的字符之后


class Solution:
    # @return an integer
    def lengthOfLongestSubstring(self, s):
        dict, ans, p1, p2 = {}, 0, 0, 0
        while p2 < len(s):
            p = dict.get(s[p2], None)
            if p == None:
                dict[s[p2]] = p2
                p2 += 1
                ans = max(ans, p2 - p1)
            else:
                while p1 <= p:
                    dict.pop(s[p1])
                    p1 += 1
                p1 = p + 1
        return ans

Median of Two Sorted Arrays

求两个有序数组的中位数。
我是用求两个有序数组的第K大数方法做的，复杂度没有细算。
假设A数组中取第x个数，Y数组取第y个数，并且满足x+y=K，若A[x] < B[y]，则比A[x]小的数必然小于K个，也就是说A[1]~A[x]都比第K小的数要小，可以舍弃掉然后求第K-x小的数；若A[x] > B[y]也是一样的道理。


class Solution:
    # @return a float
    def findMedianSortedArrays(self, A, B):
        totlen = len(A) + len(B)
        if (1 & totlen):
            return self.findK(A, B, (totlen + 1) / 2)
        else:
            return (self.findK(A, B, totlen / 2) + self.findK(A, B, totlen / 2 + 1)) / 2.0
        
    def findK(self, A, B, K):
        la, lb, pa, pb = len(A), len(B), min(K/2, len(A)), K - min(K/2, len(A))
        if (la > lb):
            return self.findK(B, A, K)
        if (la == 0):
            return B[K-1]
        if (K == 1):
            return min(A[0], B[0])
        if A[pa - 1] < B[pb - 1]:
            return self.findK(A[pa:], B, K - pa)
        elif A[pa - 1] > B[pb - 1]:
            return self.findK(A, B[pb:], K- pb)
        else:
            return A[pa - 1]

Two Sum

找出数组中的两个数，这两个数和为target
扫到x时看前面Hash的数里有没有target-x，然后将x也放进Hash表。

class Solution:
    # @return a tuple, (index1, index2)
    def twoSum(self, num, target):
        dict = {}
        for i in range(len(num)):
            if dict.get(target-num[i], None) == None:
                dict[num[i]] = i
            else:
                return (dict[target-num[i]] + 1, i + 1)