1、IO类结构图
流：控制台窗口流iostream、文件流fstream、字符流ssteam

a:iostream流与fstream流

istream ----> ifstream
ostream ----> ofstream
istream + ostream ----> iostream ----> fstream

b:iostream流与sstream流

istream ----> istringstream
ostream ----> ostringstream
istream + ostream ----> iostream ----> stringstream

c:此外，还定义的与宽字符类型wchar_t对应的流对象:wcin、wcout、wcerr

2、IO对象不可拷贝和赋值
out1 = out2; // 错误
ofstream print(ofstream); // 错误，ofstream& print(ofstream&)
out2 = print(out2);//错误

3、IO类定义了一些函数和标志
strm::iostate  			机器相关的整型名，由各个 iostream 类定义，用于定义条件状态
	strm::badbit  			strm::iostate 类型的值，用于指出被破坏的流（不可恢复）
	strm::failbit  # 4			strm::iostate 类型的值，用于指出失败的 IO 操作 
	strm::eofbit   # 6		strm::iostate 类型的值，用于指出流已经到达文件结束符
	strm::goodbit  # 0

s.eof()  				如果设置了流 s 的 eofbit 值，则该函数返回 true 
s.fail()  				如果设置了流 s 的 failbit 值，则该函数返回 true 
s.bad()  				如果设置了流 s 的 badbit 值，则该函数返回 true 
s.good() 	 			如果流 s 处于有效状态，则该函数返回 true 

s.clear()  				将流 s 中的所有状态值都重设为有效状态 
s.clear(flag)  			将流 s 中的某个指定条件状态设置为有效。flag 的类型是strm::iostate 
s.setstate(flag)  		给流 s 添加指定条件。flag 的类型是 strm::iostate #与上面完全等价
s.rdstate()  			返回流 s 的当前条件，返回值类型为 strm::iostate 

如：
auto old_state = cin.rdstate(); // remember the current state of cin
cin.clear(); # 使用前，最好重新置位才行
process_input(cin); // use cin
cin.setstate(old_state);
4、流一旦发生了错误，后续的IO操作都会失败，所有在进行IO操作之前必须先判断该IO流是否处于无错状态
其判断IO流无错误最简单的办法就是 while(cin>>word)
5、管理输出缓存
导致缓存刷新的原因：
	程序正常结束
	缓存区已满
	遇到endl操作符
	遇到unitbuf操作符
	当使用cin或cerr时，会自动把cout的缓存区刷新
b:各操作符解释
	endl———换行并刷新缓存区
	ends————输出空格并刷新缓存区
	flush—————只刷新缓存区

	unitbuf————之后，所有的输出操作都立即刷新缓存区
	nounitbuf————恢复到正常的系统管理缓存区状态

6、文件输入输出流所特有的操作，当然由于文件输入输出流从io流继承而来，因此文件输入输出流必然可以使用io流的所有操作
	fstream		fstrm
	fstream 	fstrm(file)
	fstream		fstrm(file,文件模式mode)

	fstrm.open(file)
	fstrm.close()
	fstrm.is_open()
7、要求使用基类对象的地方，我们可以使用继承类型的对象来代替

8、一旦一个文件流被打开，它就保持与之对应的文件相关联。
因此，对一个已打开的文件流调用open操作会导致failbit置位。想要使用现有已被打开的文件流，必须先关闭被关联的文件
注：如果文件流是局部对象，则每次离开作用域时，文件流相关联的文件会被自动关闭,即：自动构造和析构
如：
ifstream in(ifile);
in.close(); // 必须先关闭，才能与另一个文件关联
in.open(ifile + "2"); // open another file

10、文件模式
in 			读方式
out 		写方式
app			追加写
ate 		定位到文件末尾
trunc  		截断文件 #就是把文件的内容全部删掉,变成长度为零的文件
binary		以二进制方式进行

注：与ifstream关联的文件默认以读模式打开
	与ofstream关联的文件默认以写模式打开
	与fstream关联的文件默认以读写模式打开
10、文件流可以一次读一行也一次读一个单词
	注：可以先读一行，借助istringstream再分解生每个单词
11、在文件流中，每次读入一行的操作：getline
getline( cin, s );
  #include <fstream>
  istream& getline( char* buffer, streamsize num );#string不可行
  istream& getline( char* buffer, streamsize num, char delim );
如：#已验证
    ifstream in;
    char str[1000];
    in.open(filepath);
    while(in.getline(str,1000,'\n'))
如：
ifstream fin("tmp.dat");
fin.getline(line, MAX_LENGTH)

12、在文件流中，每次读入一个单词的操作，以空格为分界：
如：#已验证
    ifstream in;
    string str;
    in.open(filepath);
    while(in>>str) #每次读一个单词，以空格为分界符
 如：#未验证
 #include <fstream>
  int get();
  istream& get( char& ch );
  istream& get( char* buffer, streamsize num );
  istream& get( char* buffer, streamsize num, char delim );
  istream& get( streambuf& buffer );
  istream& get( streambuf& buffer, char delim );

13、
D:/github_dir/5th/tt.txt#正确
14、string流所特有的操作，当然由于string流从io流继承而来，因此string流必然可以使用io流的所有操作
sstream strm;
sstream strm(str);//用字符串str来 初始化 string流对象
strm.str(); #从string流中读取字符串，并返回
strm.str(str); #把string流的内容写入字符串str中

如：
string line, word;
vector<PersonInfo> people;
while (getline(cin, line)) {
	PersonInfo info; 
	istringstream record(line); #初始化
	record >> info.name; #每次向info.name中读入一个string
	while (record >> word) 
		info.phones.push_back(word);
	people.push_back(info); 
}

istringstream的过程：字符串---->istringstream对象：record----> record >> info.name;