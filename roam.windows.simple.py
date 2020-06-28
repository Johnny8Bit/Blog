'''
Roaming script, print basic wireless parameters on Windows client
"SSID:XXXXXXXX BSSID:XX:XX:XX:XX:XX:XX Channel:XX Signal:XX% TX:XXX"

Tested on Windows 10

netpacket.net
'''
import subprocess, re, sys
#import necessary python modules
try:
#try/except block for clean exit on CTRL+C
    while True:
    #loop indefinitely
        output = subprocess.check_output('netsh wlan show interfaces').decode('ascii')
        #assign result of netsh wlan show interfaces command to variable
        ssid = 'SSID:' + re.search(r'(SSID.+?:\s)(.+)', output).group(2).rstrip()
        bssid = 'BSSID:' + re.search(r'(BSSID.+?:\s)(.+)', output).group(2).rstrip()
        channel = 'Channel:' + re.search(r'(Channel.+?:\s)(.+)', output).group(2).rstrip()
        txrate = 'TX:' + re.search(r'(Transmit rate.+?:\s)(.+)', output).group(2).rstrip()
        signal = 'Signal:' + re.search(r'(Signal.+?:\s)(.+)', output).group(2).rstrip()
        #search output for ssid, bssid, channel, txrate & signal and assign to variables
        print(ssid, bssid, channel, signal, txrate)
        #print results to screen
except KeyboardInterrupt:
    sys.exit()
