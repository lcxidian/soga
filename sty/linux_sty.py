0、linux目录介绍
/

/home

/bin
/usr/bin
/usr/local/bin     	放置用户可执行的二进制文件的目录。

/sbin
/usr/sbin
/usr/local/sbin		一些系统管理员才会用到的可执行命令

/lib
/usr/lib
/usr/local/lib		系统使用的函数库的目录

/boot		放置Linux系统启动时用到的文件。

/dev		任何设备都以文件类型存放在这个目录中，例如键盘、鼠标、硬盘、光盘等。
	/dev/null、
	/dev/tty[1-6]、
	/dev/ttyS*、
	/dev/lp*、
	/dev/hd*、
	/dev/sd*

/etc
	/etc/inittab、init 的配置文件
	/etc/init.d、inetd 的配置文件
	/etc/modprobe.conf、
	/etc/X11、X 窗口系统的配置
	/etc/fstab、文件系统的静态信息
	/etc/sysconfig

/lost+found		系统出现异常，产生错误时，会将一些遗失的片段放于此目录下

/mnt/media		软盘与光盘的默认载入点

/opt		额外安装软件所放的目录

/usr 		/usr 是文件系统中的第二个重要的部分，/usr 是可共享的只读数据。包含系统的主要程序、图形界面所需要的文件、额外的函数库、本机自行安装的软件，以及共享的目录与文件。它有点像Windows操作系统中的“Program files”与“Windows”这两个目录的结合。
    /usr/bin,/usr/sbin：一般身份用户与系统管理员可执行文件放置目录
    /usr/include：c/c++等程序语言的文件头（header）与包含文件（include）放置处，当以tarball方式（*.tar.gz的方式安装软件）安装某些数据时，会使用到里面的许多包含文件。
    /usr/lib：各种应用软件的函数库文件放置目录。
    /usr/local：本机自行安装的软件默认放置的目录。当前也适用于/opt目录。在安装完Linux之后，基本上所有的配置都有了，但软件总是可以升级的，例如要升级代理服务，则通常软件默认的安装地方就是/usr/local中。当安装完之后所得到的执行文件，为了与系统原执行文件区分，升级后的执行文件通常放在/usr/local/bin中。建议将后来才安装的软件放在这里，便于管理。
    /usr/share：共享文件放置的目录，例如/usr/share/doc目录放置一些系统帮助文件、/usr/share/man放置manpage文件。
    /usr/src：Linux系统相关的程序代码放置目录，例如/usr/src/linux为核心源码。
    /usr/X11R6：系统内的X Window System所需的执行文件几乎都放在这里。

/var
    /var/cache：程序文件在运行过程中的一些暂存盘。
    /var/lib：程序执行的过程中，使用的数据文件放置的目录。例如locate数据库与MySQL及rpm等数据库系统，都写在这个目录中。
    /var/log：登录文件放置的目录，很重要。例如/var/log/messages就是总管所有登录文件的文件。
    /var/lock：某些设备具有一次性写入的特性，例如tab（磁带机），此时，为了避免被其他人干扰正在运行的操作，会将该设备lock（锁）起来，以确定该设备只能被单一程序所用。
    /var/run：某些程序或者是服务启动后，会将它们的PID放在这个目录下。
    /var/spool：是一些队列数据存放的地方。例如主机收到电子邮件后，就会放到/var/spool/mail中，若信件暂时发不出去，就会放到/var/spool/mqueue目录下，用户工作任务分配（cron）则是放在/var/spool/cron中。

/proc	是一个“虚拟文件系统”，它放置的数据都在内存中，例如系统核心、外部设备的状态及网络状态等。
	/proc/cpuinfo、
	/proc/dma、
	/proc/interrupts、
	/proc/ioports、
	/proc/net/*

/srv		一些服务启动之后，这些服务所需要访问的数据目录。

/tmp		让一般用户或者是正在执行的程序临时放置文件的地方。

/root/
	/root/.bashrc
	/root/.bash_profile

/etc/
	/etc/bashrc	为每一个运行bash shell的用户执行此文件.当bash shell被打开时,该文件被读取.
	/etc/profile	为系统的每个用户设置环境信息,当用户第一次登录时,该文件被执行.并从/etc/profile.d目录的配置文件中搜集shell的设置
	/etc/profile.d

1、boost源码安装与配置
	（1）下载boost源码包，解压
	（2）运行bootstrap.sh脚本文件，并设置相关的参数：
		./bootstrap.sh --with-libraries=all --with-toolset=gcc
		注：--with-libraries指定编译哪些boost库，all的话就是全部编译，只想编译部分库的话就把库的名称写上，之间用 , 号分隔即可
			-with-toolset指定编译时使用哪种编译器
		命令执行结束以后，生产二进制命令b2
	（3）开始编译boost源码：./b2 install --prefix=/usr
		注：--prefix=/usr  表示该软件的安装目录，如果安装目录是/usr时，该软件运行的库和头文件都自动放在系统默认的头文件目录/usr/include/和库文件目录/usr/lib下，这样我们可以省略配置环境变量，若不写--prefix参数，则系统自动将软件所用到库和头文件分别拷贝到/usr/local/lib和/usr/local/include/下
	（4）安装完成，把该软件所需的头文件和库的路径添加到环境变量配置文件~/.bashrc中：
		BOOST_INCLUDE=/usr/include/boost
		export BOOST_INCLUDE

		BOOST_LIB=/lib64/
		export BOOST_LIB	
	（5）安装与配置完成！测试boost库是否能正常使用即可。	
参考资料：http://ju.outofmemory.cn/entry/106397
		http://blog.csdn.net/this_capslock/article/details/47170313
2、boost使用遇到的error：
	(1):error:
		undefined reference to `boost::system::generic_category()'
		undefined reference to `boost::system::generic_category()'
		undefined reference to `boost::system::system_category()'
	分析：查看该函数所在的文件/usr/local/include/boost/system/error_code.hpp中缺少宏定义BOOST_ERROR_CODE_HEADER_ONLY
	解决办法： 
	在boost的system库的error_code.hpp源代码中添加：#define BOOST_ERROR_CODE_HEADER_ONLY

	(2):error：
		undefined reference to wsastartup
	分析：在windows系统下，缺少动态库lwsock32.dll而已
	解决办法：编译时加命令：-lwsock32
	(3):error：
	while loading shared libraries: libboost_thread.so.1.58.0: cannot open shared object file: No such file or director
	分析：linux系统找不到共享库libboost_thread.so的位置
	解决办法：在/etc/ld.so.conf配置文件中添加一行：/usr/local/lib即可，然后在终端执行ldconfig命令


3、区分二进制包和源码包：
	从文件命名上区分：
		二进制包：二进制格式的包名字很长，都带有版本号、适应平台、适应的硬件类型等，而源码格式仅仅就是一个版本号的tar包
		源码包：源码格式仅仅就是一个版本号的tar包
	从包的后缀名区分：
		（一）、*.rpm形式的二进制软件包 #常用
		安装:rpm –ivh packagename.rpm
		卸载：rpm -e packagename
		（二）、*.tar.gz/*.tgz、*.bz2形式的二进制软件包    
		安装：tar  zxvf  *.tar.gz  或  tar  yxvf  *.bz2    
		卸载：手动删除    
		说明：*.tar.gz/*.bz2形式的二进制软件包是用tar工具来打包、用gzip /bzip2压缩的，安装时直接解包即可。对于解压后只有单一目录的软件，卸载时用命令“rm  -rf  软件目录名”；如果解压后文件分散在多处目录中，则必须一一手动删除（稍麻烦），想知道解压时向系统中安装了哪些文件，可以用命令“tar  ztvf  *.tar.gz”/“tar  ytvf  *.bz2”获取清单。tar的参数z是调用gzip解压，x是解包，v是校验，f是显示结果，y是调用bzip2解压，t是列出包的文件清单。更多的参数请参看手册页：man  tar。如果你更喜欢图形界面的操作，可以在X-Window下使用KDE的ArK压缩档案管理工具。 
		 （一）*.src.rpm形式的源代码软件包
		以.src.rpm结尾的，这类软件包是包含了源代码的rpm包，在安装时需要进行编译。 这种包是源代码rpm包,如果直接用rpm -ivh来安装的话,会在/usr/src/redhat/SOURCES目录下找到一个tar.gz打包的源代码包.也就是说需要你自己手工解包编译安装.但是可以直接用:rpmbuild --rebuild xxxxx.src.rpm，来直接把源代码rpm包编译成普通的二进制rpm包.执行上述命令后,可以到/usr/src/redhat/RPMS /i386目录下找到可用的二进制rpm包.这类软件包有以下几种安装方法：
		方法1：
		rpmbuild --rebuild *.src.rpm（如果不能执行，则试试： rpm --rebuild *.src.rpm或rpm --recompile *.src.rpm）
		cd /usr/src/redhat/RPMS/i386
		rpm -ivh *.rpm

		方法2:
		1.　执行rpm -i you-package.src.rpm
		2.　cd /usr/src/redhat/SPECS
		3.　rpmbuild -bb your-package.specs 一个和你的软件包同名的specs文件
		这时，在/usr/src/redhat/RPM/i386/ （根据具体包的不同，也可能是i686,noarch等等) 在这个目录下，有一个新的rpm包，这个是编译好的二进制文件。执行：rpm –ivh new-package.rpm即可安装完成。
		
		方法3：
		1.　执行rpm -i your-package.src.rpm
		2.　cd /usr/src/redhat/SPECS
		3.　rpmbuild -bp your-package.specs 一个和你的软件包同名的specs文件
		4.　cd /usr/src/redhat/BUILD/your-package/ 一个和你的软件包同名的目录
		5.　./configure 这一步和编译普通的源码软件一样，可以加上参数
		6.　make
		7.　make install
		    卸载：rpm  -e  packgename

		（二）*.tar.gz/*.tgz、*.bz2形式的源代码软件包  #常用，慎用
		安装：tar  zxvf  *.tar.gz  或  tar  yxvf  *.bz2  先解压    
		然后进入解压后的目录：    
		./configure  配置    (./configure --help)
		make  编译    
		make  install  安装    
		卸载：make  uninstall  或 手动删除    
		说明：建议解压后先阅读说明文件，可以了解安装有哪些需求，有必要时还需改动编译配置。有些软件包的源代码在编译安装后可以用make  install命令来进行卸载，如果不提供此功能，则软件的卸载必须手动删除。由于软件可能将文件分散地安装在系统的多个目录中，往往很难把它删除干净，那你应该在编译前进行配置，指定软件将要安装到目标路径：./configure  --prefix=目录名，这样可以使用“rm  -rf  软件目录名”命令来进行干净彻底的卸载。与其它安装方式相比，需要用户自己编译安装是最难的。   
4、二进制包和源码包安装的区别：
	rpm包安装默认位置：
		/etc/ 配置文件安装目录
		/usr/bin/ 可执行的命令安装目录
		/usr/lib/ 程序所使用的函数库保存位置
		/usr/share/doc/ 基本的软件使用手册保存位置
		/usr/share/man/ 帮助文件保存位置
	源码包安装默认位置：
		一般是/usr/local/软件名/


5、rpm包和源码包启动的区别：
	RPM包安装的服务可以使用系统服务管理命令(service)来管理,例如RPM包安装的apache的启动方法是:
		service httpd start
		/etc/rc.d/init.d/httpd start
		service执行的默认路径是/etc/rc.d/init.d/

	源码包安装的服务则不能被服务管理命令管理,因为没有安装到默认路径中。所以只能用绝对路径进行服务的管理,如:
		/usr/local/apache2/bin/apachectl start
###############################
6、shell脚本学习的目的和必要性：###
###############################
	学习的目的是为了应对面试，简历上有些熟悉shell脚本，下次改写了解shell脚本变成
	打算彻底用python代替shell去实现自己想要的功能
	shell学习并不是目前最重要的，恰恰属于目前最不重要的一部分
	理解shell能干哪些事，从shell的几大模块了解，从利用python去替代他们

	shell的几个重要块：文件安全与权限
			 finds 和 args：exec
			 后台执行命令：crontab、at、&命令、nohup
			 文件名置换
			 输入输出：echo、printf、read、cat、管道、tee、文件重定向
			 命令执行顺序
			 正则表达式
			 grep家族
			 awk工具
			 sed工具
			 合并与分割
			 tr工具
			 系统环境
			 shell函数
			 向脚本传递参数
今后用python实现所有脚本功能！！！

8、安装fcitx输入法
分析：fedroa默认安装了ibus输入法，使用linux最沮丧的事情莫过于中文输入法切换不出来，甚至有人错误地认为，要使用中文输入法，必须把“区域和语言”(Region & Language)设置为中国-中文。输入法只是一个软件，和区域设置没有什么必然联系。
	（1）yum安装命令
		sudo yum erase	ibus
		sudo yum install fcitx-pinyin
		sudo yum install fcitx-configtool
		sudo yum install im-chooser
		
		sudo yum install sogoupinyin(安装sogoupinyin后，这时fcitx输入法下使用就是搜狗库，否则使用fcitx本身自己的库)
	（2）使用im-choose选择输入法为fcitx：在终端输入im-choose
		假如点击选择fcitx时，报错：GDBus.Error:org.gtk.GDBus.UnmappedGError.Quark. imsettings 2derror_2dquark.Code5: Current desktop isn’t targeted by IMSettings. 
		则在终端输入：gsettings set org.gnome.settings-daemon.plugins.keyboard active false
		再次重新使用im-choose选择fcitx输入法
		注：由于搜狗输入法嵌套在fcitx输入中，因此先在输入法配置中选择fcitx输入法，这样才算激活fcitx输入法，这时再点击屏幕左下方的键盘配置，选定输入法为搜狗输入法，这时就激活了搜狗输入法。
	（3）由于现在安装了fcitx和搜狗两种输入法，因此会出现两种输入法配置：
		fcitx设置（输入法配置）：
			该配置下有4个选项卡：输入法————全局配置————外观————附加组件
						输入法：键盘-英语  搜狗拼音
						全局配置：用来设置输入法激活的快捷键
		搜狗拼音输入法设置：用于设置搜狗输入法下具体的配置

	（4）这时候查看 设置——键盘——打字——输入源——区域和语言
		语言————english（United States）
		格式————Unitd States（english)
		输入源-汉语和libpinyin
参考：http://www.tuicool.com/articles/MfEzUnY
8 、inux下动态库和静态库——概念、制作、使用

9、linux符号链接

10、命令别名的方便
添加命令别名：
	alias 新命令 = '命令'
删除命名别名：
	unalias 新命令
如：
echo "alias lc = 'cd /root/lc'">>~/.bash_profile
echo "alias workplace = 'cd /root/workplace'">>~./bash_profile
11、linux包管理机制：yum、rpm、apt-get、dpkg、dnf




























