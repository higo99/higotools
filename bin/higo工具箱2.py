#!/usr/bin/env python
#_*_ encoding:utf-8 _*_

import os
import sys
import struct
import time
import ht

def mainmenu():
    f=ht.Htools()
    m='''
　　　　　　　　　　　　　［请选择功能］

          0.退出程序       1.查看分区信息       2. 查看版本信息
          3.备份分区表     4.安装程序           5. 运行命令
          6.恢复分区       7.擦除分区           8.备份所有分区
          a.备份串号       b.进Fastboot         c. 清空(fastboot)
          e.9008(adb)      f.重启(fastboot)     u.解锁boot(fastboot)
          r.重启手机(adb)  s.定制刷机(fastboot) w.获取root
'''
    while True:
        print m.decode("utf-8").encode(_CODE_)
        key = raw_input("请选择:".decode("utf-8").encode(_CODE_))
        if key in "1":
            f.getparts()
            print f.p
        elif key in "2":
            t=f.getimei()
            if t:
                print t
            f.baseinfo()
            
        elif key in ("3"):
            print "备份分区表".decode("utf-8").encode(_CODE_)
            doback()
        elif key in ("4"):
            f.install()
        elif key in ("5"):
            while True:
                cmd = raw_input("请输入要运行的命令:Q退出：\n".decode("utf-8").encode(_CODE_))
                if cmd in ("Q","q"):
                    break
                print f.docmd(cmd)
        elif key in ("6"):
            print "恢复分区".decode("utf-8").encode(_CODE_)
            #f=ht.Htools()
            f.write()
        elif key in ("7"):
            print "擦除分区".decode("utf-8").encode(_CODE_)
            f.erase()
        elif key in ("8"):
            print "备份所有分区".decode("utf-8").encode(_CODE_)
            dobackall()
        elif key in("a"):
            #f=ht.Htools()f.dump("nvram")f.dump("nvdata")f.dump("proinfo")
            f.getimei()
        elif key in("r","R"):
            os.system("adb reboot")
        elif key in('f',"F"):
            os.system("fastboot reboot")
        elif key in('w','W'):
            os.system("adb root")
            time.sleep(6)
            f.mountrw()
        elif key in('b','B'):
            os.system("adb reboot-bootloader")
        elif key in('c',"c"):
            os.system("fastboot -w")
        elif key in('e',"e"):
            os.system("adb reboot edl")
        elif key in('u','U'):
            n=raw_input("请输入解锁码：　".decode("utf-8").encode(_CODE_))
            os.system("fastboot oem unlock "+n)
        elif key in('s','S'):
            f.doscript()
        elif key in ("0",'q','x',"quit","exit"):
            exit()

def dobackall():
    f=ht.Htools()
    
    f.getparts()
    if len(f.p)<1:
        print "未找到分区项目".decode("utf-8").encode(_CODE_)
        return
    
    for a in f.p:
        if a in ("userdata","USERDATA","BOOT","CACHE","HIDDEN","RADIO","RECOVERY","SYSTEM"):
            pass
        else:
            print "开始备份分区".decode("utf-8").encode(_CODE_)+a
            f.dump(a)
            print a+"备份完成".decode("utf-8").encode(_CODE_)
    cmd="adb pull /dev/block/mmcblk0boot0 ./backup"
    os.system(cmd)
    cmd="adb pull /dev/block/mmcblk0boot1 ./backup"
    os.system(cmd)
    t=f.getimei()
    if t:
        os.system("touch ./backup/"+t)
        print t
        os.system("echo "+t+ " >./backup/info.txt")
    cmd="adb shell getprop >>./backup/info.txt"
    os.system(cmd)
    cmd="adb shell ls -la "+f.pathname+"/  >./backup/parts.txt"
    os.system(cmd)
    cmd="adb shell cat /proc/partitions  >> ./backup/parts.txt"
    os.system(cmd)
def doback():
    while True:
        print "当前手机分区,请选择要备份的分区序号:".decode("utf-8").encode(_CODE_)
        f=ht.Htools()
        f.getparts()
        f.outdir=os.path.split(os.path.realpath(__file__))[0]+"/backup"
        if len(f.p)<1:
            print "未找到分区项目".decode("utf-8").encode(_CODE_)
            return
        for i in range(1,len(f.p)+1):
            print i,f.p[i-1]

        n=int(input("请选择".decode("utf-8").encode(_CODE_)))
        if n > len(f.p):
            break
        #print "您输入了:"+f.p[n-1]
        p=f.p[n-1]
        n=raw_input("您选择了:".decode("utf-8").encode(_CODE_)+f.p[n-1]+"分区 确认请输入 y 退出请输入q\n".decode("utf-8").encode(_CODE_))
        if n=='y':
            print "开始备份分区".decode("utf-8").encode(_CODE_)+p
            f.dump(p)
        elif n=="q":
            break
        


if __name__ =="__main__":
    #mainmenu()
    if(sys.platform == 'darwin'):
        _CODE_ ="utf-8"
    else:
        _CODE_ ="gbk"
    #print "encode ",_CODE_
    path =os.path.split(os.path.realpath(__file__))[0]
    #print "change path",path
    os.chdir(path)
    #print os.getcwd()
    
    
    mainmenu()
