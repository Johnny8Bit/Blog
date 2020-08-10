'''
SSH script for interacting with network devices
Logs in to a device and displays the output of a given command
do_command() function can be run repeatedly if required

Tested against Cisco Catalyst 2960, Cisco Catalyst 9800, Cisco Virtual WLC (AireOS), Raspberry Pi 4B

https://netpacket.net/2020/08/scripting-ssh-to-network-devices/
'''
import paramiko, sys, socket, time

device_ip = '192.168.1.1'
login_username = 'admin'
login_password = 'password'
enable_password = 'password' #If required

receive_buffer = 256 #No need to change this
wait_time = 0.2 #Increase this for slow devices

my_command = 'show ip interface brief'

def do_login():
    device_session = paramiko.SSHClient()
    device_session.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Accept self-signed certificates
    device_session.connect(device_ip, port=22, username=login_username, password=login_password) #Initiate SSH connection
    device_ssh = device_session.invoke_shell() #Start interactive shell
    device_ssh.settimeout(3) #Set socket timeout
    device_ssh.keep_this = device_session  #Prevents closed socket after function returns
    time.sleep(wait_time) #Pause for device output
    device_ssh.recv(16384).decode('utf-8', 'backslashreplace').strip() #Clear login banner(s)
    device_ssh.send('\n') #Send new line
    time.sleep(wait_time) #Pause for device output
    device_prompt = device_ssh.recv(receive_buffer).decode('utf-8', 'backslashreplace').strip() #Read device prompt
    if device_prompt.endswith('(Cisco Controller) >'): #If AireOS, set config paging Disable
        device_ssh.send('config paging disable' + '\n')
        time.sleep(wait_time) #Pause for device output
        device_ssh.recv(receive_buffer).decode('utf-8', 'backslashreplace').strip() #Prevent config paging disable in output
    elif device_prompt.endswith('>'): #If in Disable mode, enter Enable mode
        device_ssh.send('enable' + '\n')
        time.sleep(wait_time) #Pause for device output
        device_ssh.recv(receive_buffer).decode('utf-8', 'backslashreplace') #Read password prompt
        device_ssh.send(enable_password + '\n') #Send enable mode password
        time.sleep(wait_time) #Pause for device output
        device_prompt = device_ssh.recv(receive_buffer).decode('utf-8', 'backslashreplace').strip() #Set new device prompt - enable mode
    if device_prompt.endswith('#'): #If enable mode, set terminal length 0
        device_ssh.send('terminal length 0' + '\n')
        time.sleep(wait_time) #Pause for device output
        device_ssh.recv(receive_buffer).decode('utf-8', 'backslashreplace').strip() #Prevent terminal length 0 in output
    return(device_ssh, device_prompt) #Return Paramiko channel and device prompt

def do_command(device_ssh, device_prompt, device_command):
    device_ssh.send(device_command + '\n') #Send command to device
    output = ''
    while not output.rstrip().endswith(device_prompt): #Read and append output until device prompt is matched
        try:
            output += device_ssh.recv(receive_buffer).decode('utf-8', 'backslashreplace')
        except socket.timeout: #Stop if no data returned for socket timeout duration
            print('Socket timeout on command')
            sys.exit()
    return(output)

if __name__ == '__main__':
    session, prompt = do_login()
    my_output = do_command(session, prompt, my_command)
    print(my_output)
    session.close()
