#1、Valid Palindrome
验证一个字符串是否是回文字符串,只考虑字母数字并且忽略大小写
输入:“A man, a plan, a canal: Panama”是一个回文
输出：“race a car”不是一个回文
时间复杂度：
思想：分别用两个指针指向首尾位置，然后依次比较并向中间位置靠拢即可
bool isvalid_palindrome(const string &str)
{
    using size_type = string::size_type;
    size_type i = 0,j = str.size()-1;
    while(i<=j)
    {
        while(!(('a'<=str[i]&&str[i]<='z')||('A'<=str[i]&&str[i]<='Z')||(0<=str[i]&&str[i]<=9)))#不是字母或数字则跳过
        {
            i++;
        }
        while(!(('a'<=str[j]&&str[j]<='z')||('A'<=str[j]&&str[j]<='Z')||(0<=str[j]&&str[j]<=9)))#不是字母或数字则跳过
        {
            j--;
        }
        if(str[i] == str[j] || abs(str[i]-str[j]) == 32)#比较是否“相等”
        {
            i++;
            j--;
        }
        else
            return false;
    }
    return true;
}

int main()
{
    string  str = "race a ca";
    if(isvalid_palindrome(str))
        cout<<"Valid Palindrome"<<endl;
    else
        cout<<"not Valid Palindrome"<<endl;
    return 0;
}

#2、Implement strStr()
判断一个字符串是否是另一个字符串的子串
输入:String strStr(String haystack, String needle)
输出：
时间复杂度：
思想：方法一：暴力枚举法
	  方法二：KMP算法
方法一：
bool issubstr(const string &str1,const string &str2)
{
    size_t len1 = str1.size();
    size_t len2 = str2.size();
    string item;
    for(int i=0;i<len1;i++)
    {
        item = str1.substr(i,len2);#提取子串，并比较是否相等
        if(item == str2)
            return true;
    }
    return false;
}

int main()
{
    string str1 = "BBC ABCDAB ABCDABCDABDE";
    string str2 = "ABCDEABD";
    if(issubstr(str1,str2))
        cout<<str1<<"'s substr is "<<str2<<endl;
    else
        cout<<str1<<"'s substr is not "<<str2<<endl;
    return 0;
}
方法二：KMP算法
分析：此算法跳过了不必要的比较，算法有两点：生成子串的匹配表
											利用匹配表去比较
#生成子串的匹配表
	1、生成子串的所有前缀和所有后缀
	如：以"ABCDABD"为例， 
		－　"A"的前缀和后缀都为空集，共有元素的长度为0；
	　　－　"AB"的前缀为[A]，后缀为[B]，共有元素的长度为0；
	　　－　"ABC"的前缀为[A, AB]，后缀为[BC, C]，共有元素的长度0；
	　　－　"ABCD"的前缀为[A, AB, ABC]，后缀为[BCD, CD, D]，共有元素的长度为0；
	　　－　"ABCDA"的前缀为[A, AB, ABC, ABCD]，后缀为[BCDA, CDA, DA, A]，共有元素为"A"，长度为1；
	　　－　"ABCDAB"的前缀为[A, AB, ABC, ABCD, ABCDA]，后缀为[BCDAB, CDAB, DAB, AB, B]，共有元素为"AB"，长度为2；
	　　－　"ABCDABD"的前缀为[A, AB, ABC, ABCD, ABCDA, ABCDAB]，后缀为[BCDABD, CDABD, DABD, ABD, BD, D]，共有元素的长度为0。	
	2、（进行str2.size()次操作）每一组前缀和对应的后缀进行set_intersection取交集操作，再计算交集结果的字符串长度
	3、返回非引用的匹配表
vector<unsigned> match_table(string str)
{
    map<string,set<string>> pre_set;#存放前缀的set集合，并分配与母穿相对应
    map<string,set<string>> suf_set;#存放后缀的set集合
    vector<string> vct;
    vector<string> table(1);#观察得知本情况下每次取交集最多只有一个交集元素，因此容量设为1个string
    for(int i=1;i<=str.size();i++)
        vct.push_back(str.substr(0,i));#根据子串生成对应的“母串”
//    for(auto item:vct)
//        cout<<item<<endl;
    for(auto &istr:vct)
    {
        if(istr.size() == 1)#母串只有一个字符时的特殊情况
        {
            pre_set[istr].insert("");
            suf_set[istr].insert("");
        }
        for(int i=1;i<istr.size();i++)
            pre_set[istr].insert(istr.substr(0,i));#生成本母串的所有前缀，并存放在set集合中
        for(int i=1;i<istr.size();i++)
            suf_set[istr].insert(istr.substr(i,istr.size()-i));#生成本母串的所有后缀，并存放在set集合中
    }

//    for(auto item:pre_set)#打印每个母串的前缀集合
//    {
//        cout<<item.first<<": ";
//        for(auto item2:item.second)
//            cout<<item2<<ends;
//        cout<<endl;
//    }
//    for(auto item:suf_set)#打印每个母串的后缀集合
//    {
//        cout<<item.first<<": ";
//        for(auto item2:item.second)
//            cout<<item2<<ends;
//        cout<<endl;
//    }

    vector<unsigned> result;
    for(auto istr:vct)
    {
        set_intersection(pre_set[istr].begin(),pre_set[istr].end(),
                         suf_set[istr].begin(),suf_set[istr].end(),
                         table.begin());#每个母串的前缀集合和后缀集合取交集，生成交集结果
        result.push_back(table.begin()->size());#保存交集结果的长度
        *table.begin() = "";#重置
    }
    return result;
}

bool issubstr(string str1,string str2)
{
    vector<unsigned>  table;
    unsigned match_counts = 0;
    table = match_table(str2);
    for(int i=0;i<str1.size();)
        for(int j=0;j<str2.size();)
        {
            if(match_counts == str2.size())
                return true;#表示匹配到了，则返回即可
            if(str1[i] == str2[j])
            {
                match_counts++;
                i++;
                j++;
            }
            else
            {
                j = 0;
                if(match_counts == 0) #特殊情况
                    i++;
                else
                {
                    unsigned len = match_counts - table[match_counts-1];
                    match_counts = 0;
                    if(len)
                        i += len;#匹配表让我们省去了不必要比较的操作
                    else
                        i++;
                }

            }

        }
    return false;
}

int main()
{
    string str1= "BBC ABCDAB ABCDABCDABDE";
    string str2 = "ABCDABDE";
    if(issubstr(str1,str2))
        cout<<"yes!!!"<<endl;
    else
        cout<<"no!!!"<<endl;
    return 0;
}

计算
#3、String to Integer
输入：一个表示数字的字符串，需要考虑不同的输入形式。
输出：换算成对应的整数 
	特殊输入形式：
		1.输入开始几个字符为空格
		2.考虑正负号
		3.数字字符不属于[0,9]时，输出当前结果
		4.字符串代表的数字大于INT_MAX或者小于INT_MIN时输出 INT_MAX或者 INT_MIN。  
时间复杂度：
思想：重点在于数的表示情况分类和整数浮点数范围
	输入字符的类型有数字(0-9)，符号(-、+、.、)，字母(e)

#4、Add Binary
（不考虑负数情况）二进制加法都是从最低位（从右加到左）。所以对两个字符串要从最后一位开始加，如果遇见长度不一的情况，就把短的字符串高位补0.
每轮计算要加上进位，最后跳出循环后要坚持进位是否为1，以便更新结果。 
输入:a = "11" b = "1"
输出：Return ”100”.
时间复杂度：
思想：
string add_binary(const string &str1,const string &str2)
{
    if(str1.size()<str2.size()) return add_binary(str2,str1);
    string obj(str1.size()+1,'0');
    size_type i = 0;
    bool flag = false;
    bool a,b;
    size_t len = str1.size() - str2.size();
    string _str2(len,'0');
    _str2.append(str2.begin(),str2.end());

    std::string::reverse_iterator  r_iter1 = str1.rbegin();
    std::string::reverse_iterator  r_iter2 = _str2.rbegin();
    while(r_iter1 != str1.rend())
    {
        if(*r_iter1 == '0')
            a = false;
        else
            a = true;
        if(*r_iter2 == '0')
            b = false;
        else
            b = true;

        r_iter1++;
        r_iter2++;

        if(a&&b)
        {
            if(flag)
            { while(r_iter1 != str1.rend())
    {
        if(*r_iter1 == '0')
            a = false;
        else
            a = true;
        if(*r_iter2 == '0')
            b = false;
        else
            b = true;

        r_iter1++;
                flag = true;
                obj[i] = '1';
            }
            else
            {
                flag = true;
                obj[i] = '0';
            }
        }
        if(a||b)
        {
            if(flag)
            {
                flag = true;
                obj[i] = '0';
            }
            else
            {
                obj[i] = '1';
            }
        }
        if(a == false && b == false)
        {
            if(flag)
            {
                flag = false;
                obj[i] = '1';
            }
            else
            {
                obj[i] = '0';
            }
        }
        i++;
    }
    return obj;

}

int main()
{
    string str1 = "11";
    string str2 = "1";
    string obj = add_binary(str1,str2);
    bool b = false;
    for(auto item:obj)
    {
        if(item == '1')
        {
            b = true;
        }
        if(b)
            cout<<item<<ends;
    }
    cout<<endl;
    return 0;
}

#5、Longest Palindromic Substring
在给出的一个序列中，找到最长的回文字串。譬如：一个序列 cabccba，它的最长回文子串是 abccba。
输入:
输出：
时间复杂度：
思想：
	思路一：暴力枚举，以每个元素为中间元素，同时从左右出发，复杂度O(n2)。
	思路二：记忆化搜索，复杂度O(n2)。设f[i][j] 表示[i,j] 之间的最长回文子串，递推方程


#6、Regular Expression Matching
实现支持 ' . '和 ' * '的正则表达式。（' . ' 匹配任何单字符。' * '匹配0或多个前向元素。）
输入:
	isMatch("aa","a") → false
	isMatch("aa","aa") → true
	isMatch("aaa","aa") → false
	isMatch("aa", "a*") → true
	isMatch("aa", ".*") → true
	isMatch("ab", ".*") → true
	isMatch("aab", "c*a*b") → true
	isMatch("abc",".fdsfs*")->false
输出：
时间复杂度：
思想：
#7、Wildcard Matching
Implement wildcard pattern matching with support for  '?'  and  '*'
输入:
	isMatch("aa","a") → false
	isMatch("aa","aa") → true
	isMatch("aaa","aa") → false
	isMatch("aa", "*") → true
	isMatch("aa", "a*") → true
	isMatch("ab", "?*") → true
	isMatch("aab", "c*a*b") → false
输出：
时间复杂度：
思想：主要是'*' 的匹配问题。p 每遇到一个'*'，就保留住当前'*' 的坐标和s 的坐标，然后s 从前
		往后扫描，如果不成功，则s++，重新扫描。
#8、最长公共子串
输入:
输出：
时间复杂度：
思想：
#9、Valid Number
输入:
	"0" => true
	" 0.1 " => true
	"abc" => false
	"1 a" => false
	"2e10" => true 
输出：
时间复杂度：
思想：

#10、Integer to Roman
阿拉伯数字和罗马数字之间的转换
	罗马数字规则：
		1， 罗马数字共有7个，即I（1）、V（5）、X（10）、L（50）、C（100）、D（500）和M（1000）。
		罗马数字中没有“0”。
		2， 重复次数：一个罗马数字最多重复3次。
		3， 右加左减：
		在较大的罗马数字的右边记上较小的罗马数字，表示大数字加小数字。
		在较大的罗马数字的左边记上较小的罗马数字，表示大数字减小数字。
		4， 左减的数字有限制，仅限于I、X、C，且放在大数的左边只能用一个。
		(*) V 和 X 左边的小数字只能用Ⅰ。
		(*) L 和 C 左边的小数字只能用X。
		(*) D 和 M 左 边的小数字只能用C。
输入:
输出：
时间复杂度：
思想：
#11、Roman to Integer
输入:
输出：
时间复杂度：
思想：从前往后扫描，用一个临时变量记录分段数字。
		如果当前比前一个大，说明这一段的值应该是当前这个值减去上一个值。比如IV = 5 – 1；否
		则，将当前值加入到结果中，然后开始下一段记录。比如VI = 5 + 1, II=1+1
#12、Count and Say
输入n，那么我就打出第n行的字符串。怎么确定第n行字符串呢？他的这个是有规律的。
	n = 1时，打印一个1。
	n = 2时，看n=1那一行，念：1个1，所以打印：11。
	n = 3时，看n=2那一行，念：2个1，所以打印：21。
	n = 4时，看n=3那一行，念：一个2一个1，所以打印：1211。
	以此类推。(注意这里n是从1开始的）
输入:
输出：
时间复杂度：
思想：如何计算i：
上一个map< i-1 ,vector<unsigned>>
                ^ 
                |
        用map<unsigned,unsigned> 计数
                ^ 
                |
        cout<<map.second<<map.first<<ends;
        new一个vector<unsigned>容器，把 map.second、map.first装入容器
                ^ 
                |
        再把该容器赋给map[i]的second             
void count_and_say(unsigned n)
{
    unsigned i = 2;
    map<unsigned,vector<unsigned>> map_v;
    vector<unsigned> v1;
    v1.push_back(1);
    map_v[1] = v1;
    while(i<=n)
    {
        cout<<i<<" :"<<ends;
        map<unsigned,unsigned> m;

        for(auto item2:map_v[i-1])
            ++m[item2];
        vector<unsigned> _v;
        for(auto item3:m)
        {
            cout<<item3.second<<" "<<item3.first<<ends;
            _v.push_back(item3.second);
            _v.push_back(item3.first);
        }
        map_v[i] = _v;
        cout<<endl;
        i++;
    }
}

int main()
{
    count_and_say(5);
    return 0;
}
#13、Anagrams回文构词法
Given an array of strings, return all groups of strings that are anagrams.
输入:"dormitory" 打乱字母顺序会变成"dirty room" ，，"tea" 会变成"eat"。
输出：
时间复杂度：
思想：回文构词法有一个特点：单词里的字母的种类和数目没有改变，只是改变了字母的排列顺序。
		因此，将几个单词按照字母顺序排序后，若它们相等，则它们属于同一组anagrams
		分析：用map<char,unsigned>记录一下，并比较map对象即可
map<char,unsigned> map_counts(string str) #利用map<char,unsigned>记录字符串
{
    map<char,unsigned> m;
    for(auto item:str)
    {
        if(item == ' ')
            continue;
        else
        {
            m[item]++;
        }
    }
    return m;
}
bool isAnagrams(const string &str1,const string &str2)
{
    map<char,unsigned> m1,m2;
    m1 = map_counts(str1);
    m2 = map_counts(str2);
    if(m1 == m2)
        return true;
    else
        return false;
}
int main()
{
    string str1 = "dormitory";
    string str2 = "dirty room";
    if(isAnagrams(str1,str2))
        cout<<"Anagrams"<<endl;
    else
        cout<<"not Anagrams"<<endl;
    return 0;
}
#14、Simplify Path
输入: "/home/" , => "/home"    
输出："/a/./b/../../c/" , => "/c"
时间复杂度：
思想：肯定是用栈来解决,由于string并没有提供split函数，我们需要先实现split接口
	当遇到“/../"则需要返回上级目录，需检查上级目录是否为空。"
	当遇到"/./"则表示是本级目录，无需做任何特殊操作。
	当遇到"//"则表示是本级目录，无需做任何操作。#未测试本条件
	当遇到其他字符则表示是文件夹名，无需简化。
	当字符串是空或者遇到”/../”，则需要返回一个"/"。
	当遇见"/a//b"，则需要简化为"/a/b"。 
using size_type = string::size_type;
vector<string> str_split(const string &path)#构造split函数
{
    vector<string> vstr;
    string item;
    size_type i = 0;
    while(i<path.size())
    {
        size_type pos = path.find('/',i);

        if(pos == string::npos) #特殊情况
        {
            vstr.push_back(path.substr(i));
            break;
        }

        string item = path.substr(i,pos-i);#提取
        if(item.size())
        {
            vstr.push_back(item);
            i = pos+1;#更新i到合适的位置，而不是低效的i++
        }
        else
            i++;
    }cout<<item<<endl;
    return vstr;

}
string simplify_path(string str)
{
    vector<string> v = str_split(str);
    stack<string> sk;
    string s_path;
    for(auto item:v)
    {
        cout<<item<<endl;
        if(item == "." || item == "..")
        {
            if(item == ".")
                continue;
            else
                sk.pop();
        }
        else
        {
            sk.push(item);
        }
    }
    if(sk.empty())
    {
        s_path = "/";
        return s_path;
    }
    while(!sk.empty())
    {
        s_path.insert(0,sk.top());#注意最后一个目录在栈顶，所以采用头插法
        s_path.insert(0,"/");
        sk.pop();
    }
    return s_path;
}
int main()
{
    string str = "/a/./b/../../c/";
    string s_path = simplify_path(str);
    cout<<s_path<<endl;
    return 0;
}
#15、Length of Last Word
输入一串带有空格的字符串，输出这个字符串最后一个单词的长度
输入：Given s = "Hello World",
输出：return 5. 
时间复杂度：
思想： 反向迭代器即可
size_type last_word_length(string str)
{
    string::reverse_iterator r_iter = str.rbegin();
    string::reverse_iterator r_iter1,r_iter2;
    while(r_iter != str.rend())
    {
        if(*r_iter != ' ')
        {
            r_iter1 = r_iter;
            break;
        }
        r_iter++;
    }
    while(r_iter != str.rend())
    {
        if(*r_iter == ' ')
        {
            r_iter2 = r_iter;
            break;
        }
        r_iter++;
    }
    return distance(r_iter1,r_iter2);

}

int main()
{
    string str = "Hello World  ";
    cout<<last_word_length(str)<<endl;
    return 0;
}
