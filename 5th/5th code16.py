1、模板——关键字template、模板参数组成	
如：
template <typename T>
int compare(const T &v1, const T &v2)
{
    if (v1 < v2) return -1;
    if (v2 < v1) return 1;
    return 0;
}
cout<< compare(1, 0) << endl;       // T is int
分析：
	推断模板实参————根据函数实参来推断模板实参的类型
	实例化模板——————编译器用推断的模板参数类型为我们实例化一个特定版本的函数
	如：实例化的特定版本函数
	int compare(const int &v1, const int &v2)
	{
		if (v1 < v2) return -1;
		if (v2 < v1) return 1;
		return 0;
	}
	
	关键字typename和class可以互换，但typename更直观
2、类型模板参数——模板参数是数据类型（内置类型或类类型）
   非类型模板参数——模板参数是一个常量值，而非一个类型
如： 
template<unsigned N, unsigned M>
int compare(const char (&p1)[N], const char (&p2)[M])
{
    return strcmp(p1, p2);
}
实例化一个：
int compare(const char (&p1)[3], const char (&p2)[4])
使用：
compare("hi", "mom")；

3、函数模板可以声明为inline或constexpr的
如：
	template <typename T> inline T min(const T&, const T&);
4、编译器遇到一个模板定义时，并不立即生产代码，而是当我们使用模板时才会生成代码。
	调用一个函数时，编译器只需要掌握函数的声明
	调用一个函数模板时，编译器必须掌握函数模板或类模板成员函数的定义才行，否则无法生成一个实例化版本
编译器经历3个过程：编译器遇到模板的定义———》编译器遇到模板使用时———》编译器将模板实例化
5、类模板
如：
template <typename T> class Blob {
public:
    typedef T value_type;
    typedef typename std::vector<T>::size_type size_type;
    // constructors
    Blob();
    Blob(std::initializer_list<T> il);
    // number of elements in the Blob
    size_type size() const { return data->size(); }
    bool empty() const { return data->empty(); }
    // add and remove elements
    void push_back(const T &t) {data->push_back(t);}
    // move version; see § 13.6.3 (p. 548)
    void push_back(T &&t) { data->push_back(std::move(t)); }
    void pop_back();
    // element access
    T& back();
    T& operator[](size_type i); // defined in § 14.5 (p. 566)
private:
    std::shared_ptr<std::vector<T>> data;
    // throws msg if data[i] isn't valid
    void check(size_type i, const std::string &msg) const;
};
编译器实例化类模板等价与：
template<> class Blob<int> {
    typedef typename std::vector<int>::size_type size_type;
    Blob();
    Blob(std::initializer_list<int> il);
    // ...
    int& operator[](size_type i);
private:
    std::shared_ptr<std::vector<int>> data;
    void check(size_type i, const std::string &msg) const;
};
分析：类模板的成员函数即可在类内部定义，又可以在类的外部定义
	 类模板的成员函数只有当程序使用到时，它才会被编译器实例化
如：
template <typename T>
void Blob<T>::check(size_type i, const std::string &msg) const
{
    if (i >= data->size())
        throw std::out_of_range(msg);
}
	 类内部，可以直接使用模板名而不用加模板实参，但在类外部，必须加
如：
template <typename T> class BlobPtr
public:
    BlobPtr(): curr(0) { }
    BlobPtr(Blob<T> &a, size_t sz = 0):
            wptr(a.data), curr(sz) { }
    T& operator*() const
    { auto p = check(curr, "dereference past end");
      return (*p)[curr];  // (*p) is the vector to which this object points
    }
    BlobPtr& operator++();        #在类内部，直接使用模板名，而不用加模板实参
    BlobPtr& operator--();
private:
    std::shared_ptr<std::vector<T>>
        check(std::size_t, const std::string&) const;
    std::weak_ptr<std::vector<T>> wptr;
    std::size_t curr;      // current position within the array
};
template <typename T>
BlobPtr<T> BlobPtr<T>::operator++(int) #在类外部，使用模板名，还要加模板实参
{
    // no check needed here; the call to prefix increment will do the check
    BlobPtr ret = *this;  // save the current value
    ++*this;    // advance one element; prefix ++ checks the increment
    return ret;  // return the saved state
}
6、类模板与友元
template <typename T> class Pal;
class C {  //  C is an ordinary, nontemplate class
    friend class Pal<C>; 
    template <typename T> friend class Pal2;
};
7、模板类型别名
typedef Blob<string> StrBlob;
template<typename T> using twin = pair<T, T>;
twin<string> authors;
8、typename与class的一点区别
在普通代码中，由于编译器掌握类的定义，所以它通过作用域运算符::访问的名字明白该名字是类型还是static成员，如：tring::size_type
但在模板代码中，对于编译器不知道这样的代码T::men中，men是T的类型还是T的static成员，因此我们使用关键字typename显式的告诉编译器这是类型(即模板参数)，不是static成员
9、类模板可以有默认模板实参
如：
template <class T = int> class Numbers {   // by default T is int
public:
    Numbers(T v = 0): val(v) { }
    // various operations on numbers
private:
    T val;
};
Numbers<long double> lots_of_precision;
Numbers<> average_precision; // 使用默认模板参数

10、成员模板————不能是虚函数
	1)普通类中的成员模板
	如：
	class DebugDelete {
	public:
		DebugDelete(std::ostream &s = std::cerr): os(s) { }
		template <typename T> void operator()(T *p) const
		  { os << "deleting unique_ptr" << std::endl; delete p; }
	private:
		std::ostream &os;
	};
	使用:
	double* p = new double;
	DebugDelete d;    // an object that can act like a delete expression
	d(p); // calls DebugDelete::operator()(double*), which deletes p
	int* ip = new int;
	DebugDelete()(ip);
	2)模板类中的成员模板
	如：
	template <typename T> class Blob {
		template <typename It> Blob(It b, It e);
		// ...
	};
	template <typename T>     // type parameter for the class
	template <typename It>    // type parameter for the constructor
		Blob<T>::Blob(It b, It e):
		          data(std::make_shared<std::vector<T>>(b, e)) { }
	使用：
	int ia[] = {0,1,2,3,4,5,6,7,8,9};
	vector<long> vi = {0,1,2,3,4,5,6,7,8,9};
	list<const char*> w = {"now", "is", "the", "time"};
	Blob<int> a1(begin(ia), end(ia));
	Blob<int> a2(vi.begin(), vi.end());
	Blob<string> a3(w.begin(), w.end());
11、未完！但不想续
