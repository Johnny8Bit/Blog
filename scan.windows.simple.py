'''
Scanning script, shows information on available BSSIDs on Windows client
"
BSSID: XX:XX:XX:XX:XX:XX Signal: XX% Channel: XX
BSSID: XX:XX:XX:XX:XX:XX Signal: XX% Channel: XX
BSSID: XX:XX:XX:XX:XX:XX Signal: XX% Channel: XX
"
Tested on Windows 10

netpacket.net
'''
import subprocess, re, sys, time
#import necessary python modules
try:
#try/except block for clean exit on CTRL+C
    while True:
    #loop indefinitely
        output = subprocess.check_output('netsh wlan show interfaces').decode('ascii')
        #assign result of netsh wlan show interfaces command to output variable
        myssid = re.search(r'(SSID.+?:\s)(.+)', output).group(2).rstrip()
        #assign currently connected ssid to myssid variable
        output = subprocess.check_output('netsh wlan show networks mode=Bssid').decode('ascii')
        #assign result of netsh wlan show networks mode=Bssid command to output variable
        myAPs = re.search(r'(SSID\s[0-9]+\s:\s)' + myssid + '(.+?)(SSID\s[0-9]+\s:)', output, flags=re.DOTALL).group(2)
        #reduce output of netsh wlan show networks mode=Bssid to only connected ssid
        bssid_list = [bssid[1].rstrip('\r') for bssid in re.findall(r'(BSSID.+?:\s)(.+)', myAPs)]
        channel_list = [channel[1].rstrip('\r') for channel in re.findall(r'(Channel.+?:\s)(.+)', myAPs)]
        signal_list = [signal[1].rstrip('\r').rstrip() for signal in re.findall(r'(Signal.+?:\s)(.+)', myAPs)]
        #create lists for available bssids, available channels, available signal
        for ap in range(len(bssid_list)): print('BSSID:', bssid_list[ap], 'Signal:', signal_list[ap], 'Channel:', channel_list[ap])
        #print results to screen
        print('\n')
        #print blank line for readability
        time.sleep(0.3)
        #pause before next loop
except KeyboardInterrupt:
    sys.exit()
