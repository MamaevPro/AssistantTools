import socket
import sys
import winreg

tests=["id.as.admhmao.ru:44334",
"trs2.as.admhmao.ru:44444",
"trs2.as.admhmao.ru:44334",
"trs3.as.admhmao.ru:44444",
"trs3.as.admhmao.ru:44334",
"updater.as.admhmao.ru:44334"]

# ip_list = []
# ais = socket.getaddrinfo("www.ya.ru",0,0,0,0)
# for result in ais:
  # ip_list.append(result[-1][0])
# ip_list = list(set(ip_list))
# print(ip_list)
def dns_check(host):
    ip_list = []
    try:
        ais = socket.getaddrinfo(host,0,0,0,0)
    except:
        print("DNS Check error")
    for result in ais:
        ip_list.append(result[-1][0])
    ip_list = list(set(ip_list))
    return ip_list

def port_check(host,port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host,int(port)))
        if result == 0:
           return ("is open")
        else:
           return ("is not open")
        sock.close()
    except:
        return ("check error")
    
    
print("TCP port check:")
for t in tests:
    host,port=t.split(":")
    print(host+":"+port+" "+port_check(host,port))

print("\nDNS Check:")
for host in ['id.as.admhmao.ru','trs2.as.admhmao.ru','trs3.as.admhmao.ru']:
    print(host+" - "+(" ".join(dns_check(host))))
    
print("\nProxy settings:")
INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
    r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
    0, winreg.KEY_ALL_ACCESS)
try:  
    proxy_enable = winreg.QueryValueEx(INTERNET_SETTINGS, 'ProxyEnable')[0]
except:
    print("Ошибка получения настроек проки")
if(proxy_enable==1):
    print("Enabled: yes")
    try:
        proxy_server = winreg.QueryValueEx(INTERNET_SETTINGS, 'ProxyServer')[0]
        print(proxy_server)
    except:
        print("Ошибка получения настроек проки")
else:
    print("Enabled: no")

winreg.CloseKey(INTERNET_SETTINGS)
print("\nTest end")
input()