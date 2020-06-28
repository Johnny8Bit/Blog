'''
Roaming script, print basic wireless parameters on Windows client
Saves output to CSV
"SSID:XXXXXXXX BSSID:XX:XX:XX:XX:XX:XX Channel:XX Signal:XX% TX:XXX"

Tested on Windows 10

netpacket.net
'''
import subprocess, re, sys
#import necessary python modules
output_file_name = 'wifiroam.csv'
#set name of log file
try:
#try/except block for file I/O operations
    output_file = open(output_file_name, "w+")
    #creates new file, overwriting existing, in folder from which the script is executed
except PermissionError:
    print('Error writing file')
    sys.exit()
    #exits on permission error when writing file
try:
#try/except block for clean exit on CTRL+C
    while True:
    #loop indefinitely
        try:
        #try/except block for output parse fail
            output = subprocess.check_output('netsh wlan show interfaces').decode('ascii')
            #assign result of netsh wlan show interfaces command to variable
            ssid = 'SSID:' + re.search(r'(SSID.+?:\s)(.+)', output).group(2).rstrip()
            bssid = 'BSSID:' + re.search(r'(BSSID.+?:\s)(.+)', output).group(2).rstrip()
            channel = 'Channel:' + re.search(r'(Channel.+?:\s)(.+)', output).group(2).rstrip()
            txrate = 'TX:' + re.search(r'(Transmit rate.+?:\s)(.+)', output).group(2).rstrip()
            signal = 'Signal:' + re.search(r'(Signal.+?:\s)(.+)', output).group(2).rstrip()
            #search output for ssid, bssid, channel, txrate & signal and assign to variables
        except AttributeError:
            print('No output')
            pass
        else:
            print(ssid, bssid, channel, signal, txrate)
            #print results to screen if output was correctly parsed
            output_file.write(ssid + ',' + bssid + ',' + channel + ',' + txrate + ',' + signal + '\n')
            #writes output to file
except KeyboardInterrupt:
    output_file.close()
    sys.exit()
