'''
Roaming script, print basic wireless parameters on Linux client
"SSID:XXXXXXXX BSSID:XX:XX:XX:XX:XX:XX Channel:XX Signal:-XX dBm TX:XXX Mb/s"

Tested on Raspberry Pi

netpacket.net
'''
import subprocess, re, sys
#import necessary python modules
try:
#try/except block for clean exit on CTRL+C
    while True:
    #loop indefinitely
        output = subprocess.check_output('iwconfig wlan0', shell=True).decode('ascii')
        #assign result of iwconfig wlan0 command to variable
        ssid = 'SSID:' + re.search(r'(ESSID:")(.+)(")', output).group(2)
        bssid = 'BSSID:' + re.search(r'(Access Point: )(.+)', output).group(2).rstrip()
        channel = 'Channel:' + re.search(r'(Frequency:)(.+GHz)', output).group(2).rstrip()
        signal = 'Signal:' + re.search(r'(Signal level=)(.+)', output).group(2).rstrip()
        txrate = 'TX:' + re.search(r'(Bit Rate=)(.+)(Tx)', output).group(2).rstrip()
        #search output for ssid, bssid, channel, txrate & signal and assign to variables
        print(ssid, bssid, channel, signal, txrate)
        #print results to screen
except KeyboardInterrupt:
    sys.exit()
