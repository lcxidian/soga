2015-7-12
0、static全局变量和static局部变量只是作用域不同，声明周期相同
1、指针作形参交换两个数，这样是错误的
a:易错
void func(int *i,int *j)
{
    int *temp;
    temp = i;
    i = j;
    j = temp;
    return;
}//因为指针的非引用传递的
改正
void func(int *i,int *j)
{
    int temp;
    temp = *i;
    *i = *j;
    *j = temp;
    return;
}
b：指针做形参的细节
void reset(int *temp) #指针和普通形参一样
{
    *temp = 9;
    temp = NULL;
}
int main()
{
    int s = 5;
    reset(&s);
    cout<<s<<" "<<&s<<endl;
    return 0;
}
运行结果：9 0x22fefc
2、不同的意义
    string s = "aDSFDSASasadfa";
    for(char item:s)
    与
    string s = "aDSFDSASasadfa";
    for(char &item:s)//引用
3、字母大小写
a
小写  = 大写 + 32
大写 = 小写 -32
b
是否是大写：isupper，小写：islower
转换成大写：toupper，小写：tolower

如：
int main()
{
    string s = "aDSFDSASasadfa";
    for(char &item:s)
    {
        if(isupper(item))
            item = tolower(item);

    }
    cout<<s<<endl;
    return 0;
}

4、
a
数组的两个性质：不应许拷贝和赋值数组时，编译器会将其转换成指针
void print(const int*);
void print(const int[]); // shows the intent that the function takes an array
void print(const int[10]);
以上等价
b
3种方式让数组做形参：
方法一：void print(const char *cp)
方法二：void print(const int *beg, const int *end)
方法三：void print(const int ia[], size_t size)
c
让数组引用做形参：
void print(int (&arr)[10]);//维数不可少，因此在调用的时候不能超出最大的维数
d
区别一：
f(int &arr[10]) // error: declares arr as an array of references
f(int (&arr)[10]) // ok: arr is a reference to an array of ten ints
区别二：
int *matrix[10]; // array of ten pointers
int (*matrix)[10]; // pointer to an array of ten ints
5、
int main(int argc, char *argv[])
命令行：prog -d -o ofile data0
因此：
argc等于5，不是6
argv[0] = "prog"; // or argv[0] might point to an empty string
argv[1] = "-d";
argv[2] = "-o";
argv[3] = "ofile";
argv[4] = "data0";
argv[5] = 0;

6、可变形参的函数
3种方式：
方式一：void error_msg(initializer_list<string> il)
注：在调用时，initializer_list<string> 中必须都是常用才行
方式二：类型可变形参，即可变参数模板
方式二：void foo(parm_list, ...);
7、初始化列表做返回值
vector<string> process()
{
if (expected.empty())
	return {}; // return an empty vector
else if (expected == actual)
		return {"functionX", "okay"}; // return list-initialized vector
	else
		return {"functionX", expected, actual};
}
8
函数的返回值类型为引用，可以作左值，其余都做右值
int &get(int *arry, int index) { return arry[index]; }
int main() {
	int ia[10];
	for (int i = 0; i != 10; ++i)
		get(ia, i) = i;//作左值
}
9、递归输出vector中的元素
void func(vector<int> &v)//必须用引用参数
{
    if(!v.empty())
    {
        auto reverse_iter = v.rbegin();
        cout<<*reverse_iter<<endl;
        v.pop_back();
        return func(v);
    }
    else
        return;
}
int main()
{
    vector<int> v = {1,2,4,54};
    func(v);
    return 0;
}
10、数组指针作返回值的类型
方法一：
typedef int arrT[10]; 或 using arrtT = int[10]; 
arrT* func(int i); 
方法二：
返回数组指针的函数形式如下：
Type (*function(parameter_list))[dimension] //固定写法
方法三：使用decltype提取变量的类型
int odd[] = {1,3,5,7,9};
int even[] = {0,2,4,6,8};
decltype(odd) *arrPtr(int i)
{
return (i % 2) ? &odd : &even; // returns a pointer to the array
}
11、返回值类型不能是一个数组，用数组指针来完成
返回数组指针的函数形式如下：
Type (*function(parameter_list))[dimension] 
如：
string (*func(string (&str)[10]))[10]
{
    str[0] = "dada";
    str[1] = "dadasdas";
    return &str;//返回一个指向数组的指针
}
#特别注意：数组的首地址和指向数组的指针不是一回事

12、函数重载
这不是重载，顶层const并不影响非引用参数的传递，因此无意义
Record lookup(Phone);
Record lookup(const Phone); // 不是新函数，因为是拷贝值传递
Record lookup(Phone*);
Record lookup(Phone* const); // 不是新函数

Record lookup(Account&); // function that takes a reference to Account
Record lookup(const Account&);//新函数
Record lookup(Account*); // new function, takes a pointer to Account
Record lookup(const Account*); // 新函数

13 constexpr变量
字面值类型————只有内置类型存在字面值,没有类(class)类型字面值.如：算术类型，引用，指针
constexpr类型变量————表明编译器来验证该变量是不是常量表达式，即显式表明该表达式必须是常量表达式才行
如：
const int max_files = 20;  // 常量表达式
const int limit = max_files + 1; // 常量表达式
int staff_size = 27; // 常量表达式
const int sz = get_size(); // 不是常量表达式，但系统难以识别是不是常量表达式
改进：
constexpr int mf = 20; // 20 is a constant expression
constexpr int limit = mf + 1; // mf + 1 is a constant expression
constexpr int sz = size(); // 编译不会通过

14 constexpr函数————用于常量表达式的函数。（不常用）
必须满足以下几点：
    函数的返回值和所有形参都是字面值类型，并且只有一个return语句
其执行过程：编译器把constexpr函数的调用替换成其函数体内容。因此constexpr函数被隐式指定为内联函数
15、调试帮助
方式一：
assert（语句）——是否进行调试依赖于有没有定义宏NDEBUG
若定义了#define NDEBUG 则不进行调试，反之亦然
方式二：
void print(const int ia[], size_t size)
#ifndef NDEBUG
    cerr << _ _func_ _ << ": array size is " << size << endl;
#endif
注：
_ _FILE_ _ 文件名
_ _LINE_ _ 当前行号
_ _TIME_ _ 文件编译时间
_ _DATE_ _ 文件编译日期
16、编译器会拒绝编译其调用具有二义性的语句。
void f(int, int)
void f(double, double)
   f(2.56, 42); #二义性
17、函数指针作形参
函数不可以作形参，但可以用函数指针来做形参
bool lengthCompare(const string &, const string &);
typedef decltype(lengthCompare) Func2; // 与等价 typedef bool Func(const string&, const string&); #func为函数类型的变量
a
void useBigger(const string &s1, const string &s2,
                                bool (*pf)(const string &, const string &));
typedef bool Func(const string&, const string&);
void useBigger(const string&, const string&, Func); #Func和 &Func 等价

b
bool lengthCompare(const string &, const string &);
bool (*pf)(const string &, const string &); 
pf = lengthCompare; //与等价 pf = &lengthCompare; 

c
不可以返回一个函数，但可以返回一个函数指针
using F = int(int*, int); 
using PF = int(*)(int*, int); 
PF f1(int); // 正确
F f1(int); // 错误
F *f1(int); // 正确
#函数类型和函数指针类型不是一回事，但pf = lengthCompare; //与等价 pf = &lengthCompare; 

