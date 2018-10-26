# DNas

## 背景
家里有一个Raspberry Pi和移动硬盘，想把它们利用起来做一个家庭的文件共享服务器，这样下载的视频就可以在任何地方看了（手机，平板，笔记本，电视盒子），网上找到的NAS开源软件都比较复杂，功能也多，但使用起来不是很方便，于是就有了写一个简单的配置NAS服务器的脚本的想法。

## DNas
DNas是专门为Debian开发的NAS服务器配置脚本，只支持Debian，理论上在Ubuntu上跑应该也没问题，但没有在Ubuntu上测试过，不确定。

目前只支持配置简单的Samba服务器，后续会根据需要增加其它的服务，如ftp，nfs等。

**注意：DNas目前只支持配置供guest访问的共享点，所以有安全问题，不要使用它来共享敏感的数据** 

## 安装配置DNas
支持两种安装配置方法，分别是：

* [主机安装配置](install.md)
* [docker容器里安装配置](install-docker.md)

## 设置开机自动挂载移动硬盘

这里以Debian系统为例，如果不需要挂载硬盘，请跳过该步骤

1. 接入移动硬盘，获取硬盘的UUID
```bash
$ sudo blkid
/dev/mmcblk0: PTTYPE="dos"
/dev/mmcblk0p1: SEC_TYPE="msdos" LABEL="HypriotOS" UUID="7075-EEF7" TYPE="vfat"
/dev/mmcblk0p2: LABEL="root" UUID="2a81f25a-2ca2-4520-a1a6-c9dd75527c3c" TYPE="ext4"
/dev/sda1: LABEL="FreeAgent GoFlex Drive" UUID="606073A960738516" TYPE="ntfs" PARTUUID="5dbf9d86-01"
```
这里/dev/sda1是外接的移动硬盘

2. 安装NTFS驱动（如果移动硬盘不是NTFS文件系统请跳过此步骤）
```bash
$ sudo apt-get install ntfs-3g
```

3. 设置开机自动挂载 
```bash
$ mkdir /data   # 创建目录用于挂载硬盘
# 这里UUID 为上面获取到的uuid
$ sudo sh -c "echo 'UUID=606073A960738516 /data ntfs defaults 0 0' >> /etc/fstab"      
```

# 结束语
DNas的功能很简单，仅建议在跟我有同样需求的情况下使用，如果喜欢DNas的方式并且有新的需求，欢迎提issue。