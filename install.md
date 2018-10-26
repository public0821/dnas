# 在Debian中安装DNas

本文假设主机的系统为Debian 8或者以上版本

## 获取DNas

1. 通过git从github拉取最新代码
```bash
$ git clone https://github.com/public0821/dnas.git
```

2. 创建软连接，便于后续访问
```bash
$ sudo ln -s `realpath ./dnas/src/dnas.py` /usr/local/bin/dnas
```

3. 安装samba
```bash
$ sudo dnas samba install
```

## 配置DNas

```bash
# -h可以看到samba相关的所有命令的帮助
$ dnas -h
Management tool of dnas

Usage: dnas [command]

Available Commands:
  samba   Configure Samba
  status  Show the status of each service

Use "dnas [command] --help" for more information about a command.

# 清除掉默认的共享项
$ sudo dnas samba clear

# 增加共享目录/data/films
$ sudo dnas samba add -n film -p /data/films/

# 重启服务使配置生效
$ sudo dnas samba restart
```

## 测试
在macbook和windows的网上邻居里面应该能看到共享的目录了，试试上传和下载，如果能看到共享的目录但没法操作的话，请检查共享目录的权限，比如本例中需要检查/data/films/的权限

## 设置开机启动
如果需要开机自动启动，可以通过systemctl来设置
```
$ sudo systemctl enable nmbd
$ sudo systemctl enable nmbd
```
