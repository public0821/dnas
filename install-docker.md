# 在容器中安装DNas

本文假设主机的系统中已经安装了docker

## 获取镜像

1. 获取Dockfile
```bash
$ wget https://raw.githubusercontent.com/public0821/dnas/master/Dockerfile
```

2. 编译镜像(public0821/dnas-armhf可以是任意名称，public0821是user，dnas-armhf是name)
```bash
$ docker build -t public0821/dnas-armhf .
```

## 创建并启动容器

使用上面创建的镜像创建并容器
```bash
# 这里假设需要共享主机的/data目录
$ docker run -dit --network host -v /data:/data --name dnas-server public0821/dnas-armhf
```

如果机器重启，下次只需要使用start命令启动容器即可
```bash
$ docker start dnas-server
```

## 配置DNas

```bash
# 进入容器
$ docker exec -it dnas-server bash
root@raspberrypi:/#

# 检查samba是否已经启动起来
root@raspberrypi:/# dnas status
Samba: running...

# 检查/data目录有效
root@raspberrypi:/# ls /data
code  ebook  films  music  tools

# -h可以看到samba相关的所有命令的帮助
root@raspberrypi:/# dnas -h
Management tool of dnas

Usage: dnas [command]

Available Commands:
  samba   Configure Samba
  status  Show the status of each service

Use "dnas [command] --help" for more information about a command.

# 增加共享目录/data/films
root@raspberrypi:/# dnas samba add -n film -p /data/films/

# 重启服务使配置生效
root@raspberrypi:/# dnas samba restart
```

## 测试
在macbook和windows的网上邻居里面应该能看到共享的目录了，试试上传和下载，如果能看到共享的目录但没法操作的话，请检查共享目录的权限，比如本例中需要检查/data/films/的权限

## 设置开启启动
1. 如果docker版本高于1.2，建议通过配置[restart policy](https://docs.docker.com/config/containers/start-containers-automatically/)来设置自动重启
```bash
# 设置重启策略为unless-stopped，除非是显式的stop容器，否则都会在容器退出的时候重启容器
# 如果显示的调用stop停止容器，需要再次手动start，否则下次不会自动重启
$ docker update --restart=unless-stopped dnas-server

# 后面可以随时根据需要设置重启策略为no来取消自动启动
$ docker update --restart=no dnas-server
```

2. 如果docker版本低于1.2，可以通过配置systemd，来让容器每次开机自动启动
```bash
# 创建配置文件
$ sudo sh -c "cat > /etc/systemd/system/dnas.service" << EOF
[Unit]
Description=dnas service
Requires=docker.service
After=docker.service

[Service]
ExecStart=/usr/bin/docker start -a dnas-server 
ExecStop=/usr/bin/docker stop dnas-server 

[Install]
WantedBy=default.target

EOF

# 设置开机自动启动
$ sudo systemctl enable dnas

# 后面可以随时根据需要取消自动启动
$ sudo systemctl disable dnas
```
