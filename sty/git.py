0、git与github
git————版本控制系统
github————基于git的代码托管网站

最常用的 git 命令有：
===git配置===

git config --global user.name "robbin"  
git config --global user.email "fankai#gmail.com"
git config --global color.ui true
git config --global alias.co checkout
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.br branch
git config --global core.editor "mate -w"    # 设置Editor使用textmate
git config -1 #列举所有配置

用户的git配置文件~/.gitconfig

	===Git常用命令===
	1）、查看、添加、提交、删除、找回，重置修改文件

	git help <command>  # 显示command的help
	git show            # 显示某次提交的内容
	git show $id
	 
	git co  -- <file>   # 抛弃工作区修改
	git co  .           # 抛弃工作区修改
	 
	git add <file>      # 将工作文件修改提交到本地暂存区
	git add .           # 将所有修改过的工作文件提交暂存区
	 
	git rm <file>       # 从版本库中删除文件
	git rm <file> --cached  # 从版本库中删除文件，但不删除文件
	 
	git reset <file>    # 从暂存区恢复到工作文件
	git reset -- .      # 从暂存区恢复到工作文件
	git reset --hard    # 恢复最近一次提交过的状态，即放弃上次提交后的所有本次修改
	 
	git ci <file>
	git ci .
	git ci -a           # 将git add, git rm和git ci等操作都合并在一起做
	git ci -am "some comments"
	git ci --amend      # 修改最后一次提交记录
	 
	git revert <$id>    # 恢复某次提交的状态，恢复动作本身也创建了一次提交对象
	git revert HEAD     # 恢复最后一次提交的状态

	2）、查看文件diff

	git diff <file>     # 比较当前文件和暂存区文件差异
	git diff
	git diff <$id1> <$id2>   # 比较两次提交之间的差异
	git diff <branch1>..<branch2> # 在两个分支之间比较 
	git diff --staged   # 比较暂存区和版本库差异
	git diff --cached   # 比较暂存区和版本库差异
	git diff --stat     # 仅仅比较统计信息

	3）、查看提交记录

	git log
	git log <file>      # 查看该文件每次提交记录
	git log -p <file>   # 查看每次详细修改内容的diff
	git log -p -2       # 查看最近两次详细修改内容的diff
	git log --stat      #查看提交统计信息

	4）、tig

	Mac上可以使用tig代替diff和log，brew install tig
	Git 本地分支管理
		1）、查看、切换、创建和删除分支

	git branch    		# 查看所有分支
	git br -r           # 查看远程分支
	git br <new_branch> # 创建新的分支
	git br -v           # 查看各个分支最后提交信息
	git br --merged     # 查看已经被合并到当前分支的分支
	git br --no-merged  # 查看尚未被合并到当前分支的分支
	 
	git co <branch>     # 切换到某个分支
	git co -b <new_branch> # 创建新的分支，并且切换过去
	git co -b <new_branch> <branch>  # 基于branch创建新的new_branch
	 
	git co $id          # 把某次历史提交记录checkout出来，但无分支信息，切换到其他分支会自动删除
	git co $id -b <new_branch>  # 把某次历史提交记录checkout出来，创建成一个分支
	 
	git br -d <branch>  # 删除某个分支
	git br -D <branch>  # 强制删除某个分支 (未被合并的分支被删除的时候需要强制)

		2）、分支合并和rebase

	git merge <branch>               # 将branch分支合并到当前分支
	git merge origin/master --no-ff  # 不要Fast-Foward合并，这样可以生成merge提交
	 
	git rebase master <branch>       # 将master rebase到branch，相当于：
	git co <branch> && git rebase master && git co master && git merge <branch>

	Git补丁管理(方便在多台机器上开发同步时用)

	git diff > ../sync.patch         # 生成补丁
	git apply ../sync.patch          # 打补丁
	git apply --check ../sync.patch  #测试补丁能否成功

	Git暂存管理

	git stash                        # 暂存
	git stash list                   # 列所有stash
	git stash apply                  # 恢复暂存的内容
	git stash drop                   # 删除暂存区

	Git远程分支管理

	git pull                         # 抓取远程仓库所有分支更新并合并到本地
	git pull --no-ff                 # 抓取远程仓库所有分支更新并合并到本地，不要快进合并
	git fetch origin                 # 抓取远程仓库更新
	git merge origin/master          # 将远程主分支合并到本地当前分支
	git co --track origin/branch     # 跟踪某个远程分支创建相应的本地分支
	git co -b <local_branch> origin/<remote_branch>  # 基于远程分支创建本地分支，功能同上
	 
	git push                         # push所有分支
	git push origin master           # 将本地主分支推到远程主分支
	git push -u origin master        # 将本地主分支推到远程(如无远程主分支则创建，用于初始化远程仓库)
	git push origin <local_branch>   # 创建远程分支， origin是远程仓库名
	git push origin <local_branch>:<remote_branch>  # 创建远程分支
	git push origin :<remote_branch>  #先删除本地分支(git br -d <branch>)，然后再push删除远程分支

	Git远程仓库管理

	git remote -v                    # 查看远程服务器地址和仓库名称
	git remote show origin           # 查看远程服务器仓库状态
	git remote add origin git@ github:robbin/robbin_site.git         # 添加远程仓库地址
	git remote set-url origin git@ github.com:robbin/robbin_site.git # 设置远程仓库地址(用于修改远程仓库地址)
	git remote rm <repository>       # 删除远程仓库

	创建远程仓库

	git clone --bare robbin_site robbin_site.git  # 用带版本的项目创建纯版本仓库
	scp -r my_project.git git@ git.csdn.net:~      # 将纯仓库上传到服务器上
	 
	mkdir robbin_site.git && cd robbin_site.git && git --bare init # 在服务器创建纯仓库
	git remote add origin git@ github.com:robbin/robbin_site.git    # 设置远程仓库地址
	git push -u origin master                                      # 客户端首次提交
	git push -u origin develop  # 首次将本地develop分支提交到远程develop分支，并且track
	 
	git remote set-head origin master   # 设置远程仓库的HEAD指向master分支

	也可以命令设置跟踪远程库和本地库

	git branch --set-upstream master origin/master
	git branch --set-upstream develop origin/develop

1、	安装git，并在本地创建git仓库：
		在本地新建目录：/root/lcxidian
		进入该目录，执行命令：git init进行初始化，这时git就会对该目录下的所以文件进行版本控制
		
2、在github注册用户，并在github上创建一个远程仓库repository:soga
		远程仓库HTTPS：https://github.com/lcxidian/soga.git
				SSH：git@github.com:lcxidian/soga.git
3、git配置信息
git配置文件：
	/etc/gitconfig
	~/.gitconfig
	/root/lcxidian/.git/config
查看配置信息：git config --list
配置用户信息：
	git config --global user.name "lcxidian"
	git config --global user.email	lcxidian@outlook.com

4、git工作流：
	工作目录————受控目录lcxidian
	暂存区—————用来临时保存修改的内容
	HEAD——————最后一个提交的结果
说明：
	当在工作目录中新加入一个文件时,它处于未跟踪状态,这表示其没有纳入Git的版本控制。
	通过 git add 命令可以将其加入跟踪,并同时放入暂存区。
	一个已经被跟踪的文件,如果没有做过新的修改,就是未修改状态。
	一旦对其做了改动,就变成了已修改状态。通过 git add 命令可以将已修改的文件放入暂存区。
	初次克隆某个仓库时,工作目录中所有文件都是已跟踪且未修改的状态。
	git commit 命令会将暂存区中的文件提交至HEAD所指向的分支。当被commit之后,暂存区的文件将回到未修改状态

5、查看文件的状态git status
执行命令：
	git status
输出：
	位于分支 master
	初始提交
	无文件要提交（创建/拷贝文件并使用 "git add" 建立跟踪）
6、跟踪新文件或目录git add
git add 后面可以指明要跟踪的文件或目录路径。如果是目录的话,就说明要递归跟踪该目录下的所有文件。
如： （1）在空工作目录中，git status
	输出结果：位于分支 master
			初始提交
			无文件要提交（创建/拷贝文件并使用 "git add" 建立跟踪）
	在工作目录中，创建新文件：touch test.cpp
	（2）
	git add test.cpp
	git status
	输出结果：位于分支 master
			初始提交
			要提交的变更：
			  （使用 "git rm --cached <文件>..." 撤出暂存区）
				新文件：   test1.cpp
	（3）
	向test.cpp文件添加内容
	git status
	输出结果：位于分支 master
			初始提交
			要提交的变更：
			  （使用 "git rm --cached <文件>..." 撤出暂存区）
				新文件：   test1.cpp
			尚未暂存以备提交的变更：
			  （使用 "git add <文件>..." 更新要提交的内容）
			  （使用 "git checkout -- <文件>..." 丢弃工作区的改动）
				修改：     test1.cpp
	(4)
	git add test.cpp
	git status
	输出结果：位于分支 master
			初始提交
			要提交的变更：
			  （使用 "git rm --cached <文件>..." 撤出暂存区）
				新文件：   test1.cpp


注： git add 这是个多功能命令,根据目标文件的状态不同,此命令的效果也不同:可以用它开始跟踪新文件,或者把已跟踪的文件放到暂存区,还能用于合并时把有冲突的文件标记为已解决状态等
7、忽略某些文件，不需要跟踪某些文件
一般我们总会有些文件无需纳入 Git 的管理,也不希望它们总出现在未跟踪文件列表。通常都是些自动生成的文件，比如日志文件,或者编译过程中创建的临时文件等。
方法：工作目录中创建.gitignore
	gvim .gitignore，添加：
		*.[oa]
		*~
	第一行告诉 Git 忽略所有以 .o 或 .a 结尾的文件。一般这类对象文件和存档文件都是编译过程中出现的,我们用不着跟踪它们的版本。
	第二行告诉 Git 忽略所有以波浪符(~)结尾的文件,许多文本编辑软件(比如 Emacs)都用这样的文件名保存副本。

8、查看已暂存和未暂存的更新
		————可以查看当前做的哪些更新还没有暂存?有哪些更新已经暂存起来准备好了下次提交?
查看未暂存的文件更新了哪些部分：
	git diff
查看暂存起来的文件和上次提交时的快照之间的差异：
	git diff --cached
9、提交到HEAD区
	git commit -m "add test.cpp"
	输出结果：[master（根提交） 960adb3] add test.cpp
			 1 file changed, 1 insertion(+)
			 create mode 100644 test1.cpp
	
	git status
	输出结果：位于分支 master
			无文件要提交，干净的工作区
注：提交时记录的是放在暂存区域的快照,任何还未暂存的仍然保持已修改状态,可以在下次提交时纳入版本管理。每一次运行提交操作,都是对你项目作一次快照,以后可以回到这个状态,或者进行比较
注：如果直接运行git commit 会启动文本编辑器,一般都是vim或emacs

git commit -a -m "注释"
	————会把已跟踪过的文件暂存起来一并提交,从而跳过git add. 但是未跟踪过的文件就不可以这么用
如： 
[root@lcxidian lcxidian]# touch test2.cpp
[root@lcxidian lcxidian]# git status
位于分支 master
未跟踪的文件:
  （使用 "git add <文件>..." 以包含要提交的内容）

	test2.cpp

提交为空，但是存在尚未跟踪的文件（使用 "git add" 建立跟踪）
[root@lcxidian lcxidian]# git add test2.cpp 
[root@lcxidian lcxidian]# gvim test2.cpp 
[root@lcxidian lcxidian]# git commit -a -m "add test2.cpp"
[master 8ef9ae1] add test2.cpp
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 test2.cpp
[root@lcxidian lcxidian]# git status
位于分支 master
无文件要提交，干净的工作区

10、移除文件
	————从已跟踪文件清单中移除(确切地说,是从暂存区域移除)
git rm test2.cpp #即删除文件test2.cpp
git commit -m "remove test2.cpp"
11、移动文件
	————git mv 其实就相当于运行了3条命令:
			mv test.txt TEST
			git rm test.txt
			git add TEST
12、查看提交历史
	git log————全部提交历史
	git log -p -<number>————显示最近几次的提交内容差异
	git log --stat————显示增改行数统计
13、撤销操作
稍后完善
14、远程仓库操作
首先配置SSH:
第1步：创建SSH Key。在用户主目录下，看看有没有.ssh目录，如果有，再看看这个目录下有没有id_rsa和id_rsa.pub这两个文件，如果已经有了，可直接跳到下一步。如果没有，打开Shell（Windows下打开Git Bash），创建SSH Key：ssh-keygen -t rsa -C "youremail@example.com"
你需要把邮件地址换成你自己的邮件地址，然后一路回车，使用默认值即可，由于这个Key也不是用于军事目的，所以也无需设置密码。
如果一切顺利的话，可以在用户主目录里找到.ssh目录，里面有id_rsa和id_rsa.pub两个文件，这两个就是SSH Key的秘钥对，id_rsa是私钥，不能泄露出去，id_rsa.pub是公钥，可以放心地告诉任何人。
第2步：登陆GitHub，打开“Account settings”，“SSH Keys”页面：
然后，点“Add SSH Key”，填上任意Title，在Key文本框里粘贴id_rsa.pub文件的内容即可。

#添加远程仓库：
	git remote add soga git@github.com:lcxidian/soga.git
	git remote -v
	输出结果: soga	git@github.com:lcxidian/soga.git (fetch)
			 soga	git@github.com:lcxidian/soga.git (push)

#删除远程仓库：
	git remote rm soga #只是删除本地与远程仓库的关联而已，远程仓库还在github之上
	git remote -v #空
#修改远程仓库：
	git remote set-url --push [remote-name] [newUrl]
#重命名远程仓库：
	git remote rename <old-remote-name> <new-remote-name>
#查看远程仓库：
	git remote				#显示所有远程仓库名称
	git remote -v			#显示所有远程仓库的信息
	git remote -v 远程仓库名	#显示指定远程仓库的信息
#从远程仓库抓取数据：
	git fetch [remote-name]
注：1. 此命令会到远程仓库中拉取所有你本地仓库中还没有的数据。运行完成后,你就可以在本地访问该远程仓库中的所有分支
	2. fetch 命令只是将远端的数据拉到本地仓库,并不自动合并到当前工作分支,只有当你确实准备好了,才能手工合并

#拉取远程仓库：
	git pull [remote-name] [本地分支名]
注：一般我们获取代码更新都是用git pull, 目的是从原始克隆的远端仓库中抓取数据后,合并到工作目录中的当前分支

#推送远程仓库：
	git push [remote-name] [本地分支名]
注：只有在所克隆的服务器上有写权限,或者同一时刻没有其他人在推数据,这条命令才会如期完成任务。如果在你推数据前,已经有其他人推送了若干更新,那你的推送操作就会被驳回。你必须先把他们的更新抓取到本地git pull,合并到自己的项目中,然后才可以再次推送。
15、应用标签
善后完善
16、分支与合并分支————理解分支的概念并熟练运用后,你才会意识到为什么 Git 是一个如此强大而独特的工具,并从此真正改变你的开发方式。
#首先弄清楚什么是文件快照
	————文件快照分为两种：即写即拷快照　＋　分割镜像快照
	即写即拷贝————每次输入新数据或已有数据被更新时，生成对存储数据改动的快照，以便在发生硬盘写错误、文件损坏或程序故障时迅速地恢复数据。那什么才是快照呢———即所有的数据并没有被真正拷贝到另一个位置，只是指示数据实际所处位置的指针被拷贝。当已经有了快照时，如果有人试图改写原始的LUN(磁盘空间)上的数据，快照软件将首先将原始的数据块拷贝到一个新位置（专用于复制操作的存储资源池），然后再进行写操作。以后当你引用原始数据时，快照软件将指针映射到新位置，或者当你引用快照时将指针映射到老位置。
	分割镜像快照————引用镜像硬盘组上所有数据。每次应用运行时，都生成整个卷的快照，而不只是新数据或更新的数据。这种使离线访问数据成为可能，并且简化了恢复、复制或存档一块硬盘上的所有数据的过程。但是，这是个较慢的过程，而且每个快照需要占用更多的存储空间。

#Git是如何储存数据的
#使用
	每次comit，Git都把它们串成一条时间线，这条时间线就是一个分支。截止到目前，只有一条时间线，在Git里，这个分支叫主分支，即master分支。HEAD始终指向当前分支，由于当前只有一个主分支master，所以此时HEAD指向master分支。

注：由于叙述用图片加文字方式很形象，见./git_branch.doc



















