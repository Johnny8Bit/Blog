'''
Passes commands and returns output from Cisco WLC over SSH
Requires Paramiko - www.paramiko.org

Simplified demonstration script

netpacket.net
'''
import time, paramiko
wlc_session = paramiko.SSHClient()
wlc_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
wlc_session.connect('192.168.6.21', port='22', username='sdfhjg', password='null')
wlc_ssh_class = wlc_session.invoke_shell()
time.sleep(0.1)
wlc_ssh_class.send('admin'+'\n')
time.sleep(0.1)
wlc_ssh_class.send('password'+'\n')
time.sleep(0.1)
wlc_ssh_class.send('config paging disable'+'\n')
time.sleep(0.1)
strip_login_text = wlc_ssh_class.recv(1024).decode('utf-8')
wlc_ssh_class.send('show sysinfo'+'\n')
time.sleep(0.1)
output = wlc_ssh_class.recv(2048).decode('utf-8', 'backslashreplace')
print(output)
