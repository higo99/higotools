#_*_ encoding:utf-8 _*_
import os
import sys
import ConfigParser
class Htools:
    #_CODE_="utf-8"
    p=[]
    apkdir="./app"   
    #恢复分区默认文件夹
    uploaddir="../upload"
    base={}
    
    #备份分区默认文件夹
    backupdir="../backup"
    
    # 脚本文件夹
    scriptdir="../script"
    
    adbdir = "./adb"
    
    pathname=""
    #__p=['DDR', 'aboot', 'boot', 'cache', 'cust', 'fsc', 'fsg', 'hyp', 'log', 'misc', 'modem', 'modemst1',\
         #'modemst2', 'oeminfo', 'pad', 'persist', 'recovery', 'rpm', 'sbl1', 'sec', 'ssd', 'system', 'tz']
    def __init__(self):
        #添加模块环境变量
        global _CODE_
        if(sys.platform == 'darwin'):
            _CODE_ ="utf-8"
        else:
            _CODE_ ="gbk"
            sys.path.append(os.getcwd())
            p=os.path.abspath(self.adbdir)+"; "+ os.environ.get("path")
            os.environ["path"]=p  #添加adb命令环境变量
            self.getconf()
            if self.isroot():
                print "Root Pass"
                self.getparts()
                #self.mountrw()
            
    
    def getimei(self):
        info=os.popen('adb shell "service call iphonesubinfo 1 "').read()
        doc='''
        Result: Parcel(
          0x00000000: 00000000 0000000e 00390039 00300030 '........9.9.0.0.'
          0x00000010: 00360030 00360034 00370034 00350035 '0.6.4.6.4.7.5.5.'
          0x00000020: 00370035 00000000                   '5.7.....        ')
          '''
        s=info.split("\r\n")
        if len(s)<2:
            return
        imei=""
        for i in s[1:]:
            i=i.replace(".","")
            a=i.split(" '")
            if len(a)>1:
                imei=imei+ a[1]
        imei=imei.replace("'","").replace(")","").strip()
        if len(imei)==14:
            return "MEID:"+imei
        elif len(imei)==15:
            return "IMEI:"+imei
        else:
            return
            
    def isroot(self):
        s=self.docmd("ls /sbin")
        #opendir failed, Permission denied
        #error: device '(null)' not found
        #print s
        if s=="":
            return False
        keys=("Permission","denied","error:","failed")
        for key in keys:
            if key in s:
                return False
        return True
        
    def mountrw(self,type="rw"):
        ss=self.docmd("mount")
        '''
        rootfs / rootfs ro,relatime 0 0
        tmpfs /dev tmpfs rw,nosuid,relatime,mode=755 0 0
        devpts /dev/pts devpts rw,relatime,mode=600 0 0
        proc /proc proc rw,relatime 0 0
        sysfs /sys sysfs rw,relatime 0 0
        none /acct cgroup rw,relatime,cpuacct 0 0
        none /sys/fs/cgroup tmpfs rw,relatime,mode=750,gid=1000 0 0
        tmpfs /mnt/secure tmpfs rw,relatime,mode=700 0 0
        tmpfs /mnt/asec tmpfs rw,relatime,mode=755,gid=1000 0 0
        tmpfs /mnt/obb tmpfs rw,relatime,mode=755,gid=1000 0 0
        none /dev/cpuctl cgroup rw,relatime,cpu 0 0
        /dev/block/platform/hi_mci.1/by-name/system /system ext4 ro,relatime,user_xattr,acl,barrier=1,data=ordered 0 0
        /dev/block/platform/hi_mci.1/by-name/cache /cache ext4 rw,nosuid,nodev,relatime,user_xattr,acl,barrier=1,data=ordered 0 0
        /dev/block/platform/hi_mci.1/by-name/userdata /data ext4 rw,nosuid,nodev,noatime,user_xattr,acl,barrier=1,data=ordered,noauto_da_alloc,discard 0 0
        /dev/block/platform/hi_mci.1/by-name/cust /cust ext4 ro,nosuid,nodev,noatime,user_xattr,acl,barrier=1,data=ordered 0 0
        /dev/block/platform/hi_mci.1/by-name/modemimage /modem/modem_image ext4 rw,nosuid,nodev,relatime,user_xattr,acl,barrier=1,data=ordered 0 0
        /dev/block/platform/hi_mci.1/by-name/modemnvm1 /modem/nvm1 ext4 rw,nosuid,nodev,relatime,user_xattr,acl,barrier=1,data=ordered 0 0
        /dev/block/platform/hi_mci.1/by-name/modemnvm2 /modem/nvm2 ext4 rw,nosuid,nodev,relatime,user_xattr,acl,barrier=1,data=ordered 0 0
        /dev/block/platform/hi_mci.1/by-name/splash2 /splash2 ext4 rw,nosuid,nodev,noatime,user_xattr,acl,barrier=1,data=ordered 0 0
        /sys/kernel/debug /sys/kernel/debug debugfs rw,relatime 0 0
        /dev/fuse /mnt/shell/emulated fuse rw,nosuid,nodev,relatime,user_id=1015,group_id=1015,default_permissions,allow_other 0 0
        
        '''
        keys=ss.split()
        #print keys
        i=0
        cmd =''
        for key in keys:
            #print key
            try:
                if key=="/system": 
                    print a , key                    
                    cmd="mount -o "+type +",remount "+a
            except:
                a=key
            a=key
        print cmd
        self.docmd(cmd)
                
    def __chose(self,s):
        for i in range(1,len(s)+1):
            print i,s[i-1]
        try:
            n=int(input("请选择".decode("utf-8").encode(_CODE_)))
            if n > len(s) or n == 0:
                return
            return s[n-1]
        except:
            return 
        
    def docmd(self,cmd):
        cmd='adb shell  ' + cmd
        return os.popen(cmd).read().strip()

    def install(self):
        print "请选择需要安装的文件".decode("utf-8").encode(_CODE_)
        try:
            s=self.__chose(os.listdir(self.apkdir))
        except:
            print "chose bank"
        if(s):
            os.system("adb install "+self.apkdir+"/"+s)
        
    def dump(self,filename):
        if not self.isroot():
            print "please root the diveces!"
            return
        if self.pathname=="":
            self.pathname=self.getpath()
        #os.system("adb push "+self.uploaddir+"/"+filename)
        cmd ="dd if="+self.pathname+"/"+filename + "  of=/sdcard/"+filename
        print self.docmd(cmd)
        print "开始下载...".decode("utf-8").encode(_CODE_)
        cmd = "adb pull /sdcard/"+filename +"  "+ self.backupdir+"/"+filename
        os.popen(cmd)
        print cmd
        self.docmd("rm /sdcard/"+filename)
    def write(self,filename=""):
        if not self.isroot():
            print "please root the diveces!"
            return
        if self.pathname=="":
            self.pathname=self.getpath()
        file2=os.path.basename(filename)
        file2 = os.path.splitext(file2)[0]
        if file2 in self.p:
            pass
        else:
            print "请选择要上传恢复的文件".decode("utf-8").encode(_CODE_)
            ph = os.path.abspath(self.uploaddir)+"\\"
            filename=self.__chose(os.listdir(ph))
            if not filename:
                print "chose bank"
                return
            print filename
            file2 = os.path.splitext(filename)[0]

        cmd="adb push "+ph+filename+ " /sdcard/"+file2
        #print cmd
        os.system(cmd)
        #self.push(self.uploaddir +"/"+filename)    
        cmd ="dd of="+self.pathname+"/"+file2 + "  if=/sdcard/"+file2
        #print cmd
        print self.docmd(cmd)
        self.docmd("rm /sdcard/"+filename)
    def doscript(self):
        path = os.path.abspath(self.scriptdir)
        lst = filter(lambda x: os.path.splitext(x)[1]==".bat",os.listdir(path))
        s = self.__chose(lst)
        os.system(path+"\\"+s)
        print path+s
        
    def push(self,filename,file2=""): 
        '''
###################################################
#上传本地文件到手机／Sdcard目录
#  函数名称   push
#  filename:  本地要上传的文件名称
#  file2:     上传到SD卡后面的名称
#  函数无返回值
##################################################
        '''
        if filename =="":
            return
        if os.path.exists(filename) and os.path.isfile(filename):
            if file2=="":
                file2=filename
        else:
            print "file not found:"+filename
            return
        file2=os.path.basename(filename)
        file2 = os.path.splitext(file2)[0]
                
        cmd = "adb push "+filename+"  /sdcard/"+file2
        print "push file :"+cmd
        os.system(cmd)
        
        
    def erase(self):
        if not self.isroot():
            print "please root the diveces!"
            return
        self.getparts()
        print self.p
        while True:
            s=raw_input("请输入要删除的分区名称,q退出".decode("utf-8").encode(_CODE_))
            if s=='q':
                break
            elif s in self.p:
                print "正在擦除分区".decode("utf-8").encode(_CODE_)+s+"..."
                cmd = "dd if=/dev/zero of="+self.pathname+"/"+s
                print cmd
                print self.docmd(cmd)
    def getpath(self):
        base = "/dev/block/platform"
        path=self.docmd("find "+base).split()
        for s in path:
            if "by-name" == s.split('/')[-1]:
                print s
                return s
    def getparts(self):
        #path=os.popen("adb shell ls /dev/block/").read()
        self.pathname=self.getpath()
        if(self.pathname):
            parts=self.docmd("ls "+self.pathname).split()
            self.p= parts
    def baseinfo(self):
        if len(self.p)<1:
            print "未找到分区项目".decode("utf-8").encode(_CODE_)
            return
            
        #找IMEI的办法   dumpsys iphonesubinfo
        #  Phone Type = CDMA
        #Device ID = A00000330E3FF2      
        txt='''
★获取基本系统信息功能★:

    主板型号:{board}        运行模式:{runmode}           序列号:{serialno}         
    硬件类型：{hardware}    imei1:{imei1}               imei2:{imei2}
    
    EFS版本：{efsversion}     硬件版本：{hardwareversion}          moden版本：{modemversion}
    recovery版本：{recoveryversion}    sbl版本：{sbl1version}     系统版本：{systemversion}

    USB功能:{USBfunctions}   usb默认配置:{usbdefault}    usb系统设置:{usbconfig}
    usb当前状态:{usbstate}
'''
        self.base['board']=os.popen("adb shell getprop ro.product.board").read().strip()
        self.base['runmode']=os.popen("adb shell getprop ro.runmode").read().strip()
        self.base['serialno']=os.popen("adb shell getprop ro.serialno").read().strip()
        self.base['hardware']=os.popen("adb shell getprop ro.hardware").read().strip()
	

        self.base['USBfunctions']=os.popen("adb shell getprop ro.hw.usb.update.functions").read().strip()
        self.base['usbdefault']=os.popen("adb shell getprop ro.sys.usb.default.config").read().strip()
        self.base['usbconfig']=os.popen("adb shell getprop sys.usb.config").read().strip()
        self.base['usbstate']=os.popen("adb shell getprop sys.usb.state").read().strip()
        self.base['efsversion']=os.popen("adb shell getprop ro.confg.hw_efsversion").read().strip()
        self.base['hardwareversion']=os.popen("adb shell getprop ro.confg.hw_hardwareversio").read().strip()
        self.base['modemversion']=os.popen("adb shell getprop ro.confg.hw_modemversion").read().strip()
        self.base['recoveryversion']=os.popen("adb shell getprop ro.confg.hw_recoveryversion").read().strip()
        self.base['sbl1version']=os.popen("adb shell getprop ro.confg.hw_sbl1version").read().strip()
        self.base['systemversion']=os.popen("adb shell getprop ro.confg.hw_systemversion").read().strip()
        
        self.base['imei1']=os.popen("adb shell getprop gsm.deviceid.imei1").read().strip()
        self.base['imei2']=os.popen("adb shell getprop gsm.deviceid.imei2").read().strip()
        
        txt=txt.format(board=self.base['board'],runmode=self.base['runmode'],serialno=self.base['serialno'],\
		hardware=self.base['hardware'],USBfunctions=self.base['USBfunctions'],usbdefault=self.base['usbdefault'],\
		usbconfig=self.base['usbconfig'],usbstate=self.base['usbstate'],efsversion=self.base['efsversion'],\
		hardwareversion=self.base['hardwareversion'],recoveryversion=self.base['recoveryversion'],\
		modemversion=self.base['modemversion'],systemversion=self.base['systemversion'],\
        sbl1version=self.base['sbl1version'],imei1=self.base['imei1'],imei2=self.base['imei2'])
	print txt.decode("utf-8").encode(_CODE_)

    
    
    def getconf(self):
        settingfile = os.path.dirname(__file__)+"\\setting.ini"
        print settingfile
        if not os.path.exists(settingfile):
            print "Make default config file:"+settingfile
            self.mkini(settingfile)
        else:
            print "Load conf"
            cf=ConfigParser.ConfigParser()
            cf.read(settingfile)
            self.adbdir = cf.get("APPPATH","adbdir")
            self.apkdir = cf.get("APPPATH","apkdir")
            self.uploaddir = cf.get("APPPATH","uploaddir")
            self.backupdir = cf.get("APPPATH","backupdir")
            self.scriptdir = cf.get("APPPATH", "scriptdir")
            
	
    def  mkini(self,configpath):
        cf=ConfigParser.ConfigParser()
        cf.add_section("APPPATH")
        cf.set("APPPATH","uploaddir",self.uploaddir)
        cf.set("APPPATH","scriptdir",self.scriptdir)
        cf.set("APPPATH","apkdir",self.apkdir)
        cf.set("APPPATH","backupdir",self.backupdir)        
        cf.set("APPPATH","adbdir",self.adbdir)
        cf.write(open(configpath,'w'))
        
if  __name__=="__main__":
    h = Htools()
    print h.adbdir
    