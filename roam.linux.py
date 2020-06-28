'''
Roaming script, print basic wireless parameters on Linux client
"SSID:XXXXXXXX BSSID:XX:XX:XX:XX:XX:XX Channel:XX Signal:-XX dBm TX:XXX Mb/s"

Tested on Raspberry Pi

netpacket.net
'''
def make_frequency_channel_map():
#funtion to create dictionary with channel to frequency mappings
    frequency_list, channel_list = [], []
    for frequency in range(2412, 2473, 5): frequency_list.append(str(frequency/1000))
    for frequency in range(5180, 5321, 20): frequency_list.append(str(frequency/1000))
    for frequency in range(5500, 5721, 20): frequency_list.append(str(frequency/1000))
    for frequency in range(5745, 5826, 20): frequency_list.append(str(frequency/1000))
    for channel in range(1, 14): channel_list.append(str(channel))
    for channel in range(36, 65, 4): channel_list.append(str(channel))
    for channel in range(100, 145, 4): channel_list.append(str(channel))
    for channel in range(149, 166, 4): channel_list.append(str(channel))
    return dict(zip(frequency_list, channel_list))

import subprocess, re, sys
#import necessary python modules

if __name__ == '__main__':
    interface = 'wlan1'
    #set wireless interface
    frequency_channel_map = make_frequency_channel_map()
    #create channel to frequency mappings
    try:
    #try/except block for clean exit on CTRL+C
        while True:
        #loop indefinitely
            output = subprocess.check_output('iwconfig ' + interface, shell=True).decode('ascii')
            #assign result of iwconfig command to variable
            ssid = 'SSID:' + re.search(r'(ESSID:")(.+?)(")', output).group(2)
            bssid = 'BSSID:' + re.search(r'(Access Point: )(.+)', output).group(2).rstrip()
            signal = 'Signal:' + re.search(r'(Signal level=)(.+?)(\s\s)', output).group(2).rstrip()
            txrate = 'TX:' + re.search(r'(Bit Rate[=:])(.+?)(\s\s)', output).group(2).rstrip()
            #search output for ssid, bssid, signal, txrate and assign to variables
            channel = 'Channel:' + frequency_channel_map[re.search(r'(Frequency:)(.+)(GHz)', output).group(2).rstrip()]
            #search output for frequency, map to channel number using dictionary, and assign to variable
            print(ssid, bssid, channel, signal, txrate)
            #print results to screen
    except KeyboardInterrupt:
        sys.exit()
