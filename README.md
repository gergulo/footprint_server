#### 介绍
格格足迹小程序服务端1.0.0，使用python Django 2.2，数据库使用mysql5.7。

#### 使用说明
~~~
以windows为例
一、下载安装phthon 3.*（建议3.7及以上）。
    官网下载地址：https://www.python.org/downloads
二、项目的安装、启动，以项目放置目录为D:\Workspace\PythonWorkspace\footprint_server为例
    1、建立数据库，并将数据库配置写入D:\Workspace\PythonWorkspace\footprint_server\footprint_server\settings.py中的DATABASES配置。
    2、启动一个命令提示符窗口，cd到项目目录D:\Workspace\PythonWorkspace\footprint_server；
        d:
        cd D:\Workspace\PythonWorkspace\footprint_server
    3、执行下列命令，建立数据库表：
        python manage.py makemigrations common
        python manage.py migrate common
    4、执行下列命令，启动项目：
        python manage.py runserver 0.0.0.0:9000
~~~