'''
Displays client Wi-Fi statistics in real-time

Useful for testing how a Wi-Fi client roams from AP to AP
Uses standard OS calls to collect connection statistics from NIC driver
Works on Microsoft and Apple platforms
Use keyboard break to stop

Added ICMP check for Microsoft OS.

netpacket.net
'''

__author__ = 'Michal Kowalik'
__credits__= 'Johannes Jobst'
__version__= '1.0'
__status__ = 'Prototype'
__python__ = 'version 3.6.3'

import subprocess, time, re, os

def apple():
    """Outputs data for Apple OS
    """
    wifi = True
    command = 'exec /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I'
    output = subprocess.check_output(command,shell=True).decode('ascii')
    try:
        ssid = 'SSID:' + re.search(r' SSID.+', output).group(0).split()[-1]
        bssid = 'BSSID:' + re.search(r'BSSID.+', output).group(0).split()[-1]
        channel = 'Ch:' + re.search(r'channel.+', output).group(0).split()[-1]
        txrate = 'TX:' + re.search(r'lastTxRate.+', output).group(0).split()[-1]
        signal = 'Signal:' + re.search(r'CtlRSSI.+', output).group(0).split()[-1]
        noise = 'Noise' + re.search(r'agrCtlNoise.+', output).group(0).split()[-1]
    except AttributeError:
        wifi = False
        print('No RF data')
    if wifi:
        clock = time.asctime().split()[3]
        print(clock, ssid, bssid, channel, txrate, noise, signal)
    time.sleep(0.3)

def microsoft():
    """Outputs data for Microsoft OS
    """
    wifi = True
    output = subprocess.check_output('netsh wlan show interfaces').decode('ascii')
    try:
        ping_output = subprocess.check_output(ping_command).decode('ascii')
        ping_output = re.search(r'^Reply.+$', ping_output, re.MULTILINE).group(0)
    except subprocess.CalledProcessError:
        ping_output = 'No ICMP data'
    try:
        ssid = 'SSID:' + re.search(r'SSID.+', output).group(0).split()[-1]
        bssid = 'BSSID:' + re.search(r'BSSID.+', output).group(0).split()[-1]
        channel = 'Ch:' + re.search(r'Channel.+', output).group(0).split()[-1]
        txrate = 'TX:' + re.search(r'Transmit.+', output).group(0).split()[-1]
        rxrate = 'RX:' + re.search(r'Receive.+', output).group(0).split()[-1]
        signal = re.search(r'Signal.+', output).group(0).split()[-1][:-1]
    except AttributeError:
        wifi = False
        print('No RF data')
    if wifi:
        clock = time.asctime().split()[3]
        dbm = signal + '%'
        #dbm = 'dBm:' + str(int(signal) / 2 - 100)
        print(clock, ssid, bssid, dbm, channel, txrate, rxrate)
        print(ping_output)
    time.sleep(0.3)

def ping():
    """Collects IP of host for ICMP test, returns formatted Ping command
    """
    ping_timeout_ms = '300'

    ping_host = input('\nEnter IP to test [192.0.2.1]: ')
    if ping_host == '': ping_host = '192.0.2.1'
    if operating_system == 'posix': ping_cmd = ('ping -t ' + ping_timeout_ms + ' -c 1 ' + ping_host)
    if operating_system == 'nt': ping_cmd = ('ping -w ' + ping_timeout_ms + ' -n 1 ' + ping_host)
    return(ping_cmd)

if __name__ == '__main__':
    operating_system = os.name
    ping_command = ping()
    try:
        while True:
            if operating_system == 'posix': apple()
            if operating_system == 'nt': microsoft()
    except KeyboardInterrupt:
        print('Script stopped.')
