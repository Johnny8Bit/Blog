'''
Basic Wi-Fi scanner - captures Beacons and displays information about discovered Wi-Fi networks
Tested on Debian

netpacket.net/2020/08/building-a-wi-fi-scanner-with-scapy/
'''
from scapy.all import *
from subprocess import run

class colour:
    DEFAULT = '\033[m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    MAGENTA = '\033[35m'

cipher_list = ['Group', 'WEP-40', 'TKIP', 'N/A', 'CCMP', 'WEP-104']
akm_list = ['N/A', '802.1X', 'PSK', '802.1X (FT)']

def dump(packet):
    if packet.haslayer(Dot11Beacon):
        timestamp = time.time()
        radiotap = packet.getlayer(RadioTap)
        signal = radiotap.fields['dBm_AntSignal']
        frequency = radiotap.fields['ChannelFrequency']
        rate = radiotap.fields['Rate']
        dot11_fcs = packet.getlayer(Dot11FCS)
        bssid = dot11_fcs.fields['addr2']
        beacon = packet.getlayer(Dot11Beacon)
        beacon_payload = beacon.payload
        beacon_ssid = beacon_payload.fields['info'].decode('utf-8')
        if packet.haslayer(RSNCipherSuite):
            rsn_cipher_suite = packet.getlayer(RSNCipherSuite)
            cipher = cipher_list[rsn_cipher_suite.fields['cipher']]
        else:
            cipher = 'Open'
        if packet.haslayer(AKMSuite):
            akm_suite = packet.getlayer(AKMSuite)
            akm = akm_list[akm_suite.fields['suite']]
        else:
            akm = 'Open'
        ap[bssid] = {'RSSI' : signal, 'SSID': beacon_ssid, 'Time': timestamp, 'Rate': rate, 'Frequency': frequency, 'Cipher': cipher, 'AKM': akm}
        run('clear')
        print(f" {'BSSID':20} {'SSID':35} {'RSSI':>10} {'Rate':>10} {'Frequency':>13} {'Cipher':>13} {'Suite':>15} {'Age(sec)':>15}")
        for bssid in sorted(ap, key=lambda x: ap[x]['RSSI'], reverse=True):
            beacon_age = timestamp - ap[bssid]['Time']
            if  beacon_age < beacon_max_age:
                if ap[bssid]['RSSI'] < -65:
                    print(f"{colour.GREEN} {bssid:20} {ap[bssid]['SSID']:35} {ap[bssid]['RSSI']:10} {ap[bssid]['Rate']:10} {ap[bssid]['Frequency']:13} {ap[bssid]['Cipher']:>13} {ap[bssid]['AKM']:>15} {beacon_age:15.1f} {colour.DEFAULT}")
                if ap[bssid]['RSSI'] in range (-65, -49):
                    print(f"{colour.YELLOW} {bssid:20} {ap[bssid]['SSID']:35} {ap[bssid]['RSSI']:10} {ap[bssid]['Rate']:10} {ap[bssid]['Frequency']:13} {ap[bssid]['Cipher']:>13} {ap[bssid]['AKM']:>15} {beacon_age:15.1f} {colour.DEFAULT}")
                if ap[bssid]['RSSI'] in range (-49, -39):
                    print(f"{colour.RED} {bssid:20} {ap[bssid]['SSID']:35} {ap[bssid]['RSSI']:10} {ap[bssid]['Rate']:10} {ap[bssid]['Frequency']:13} {ap[bssid]['Cipher']:>13} {ap[bssid]['AKM']:>15} {beacon_age:15.1f} {colour.DEFAULT}")
                if ap[bssid]['RSSI'] > -40:
                    print(f"{colour.MAGENTA} {bssid:20} {ap[bssid]['SSID']:35} {ap[bssid]['RSSI']:10} {ap[bssid]['Rate']:10} {ap[bssid]['Frequency']:13} {ap[bssid]['Cipher']:>13} {ap[bssid]['AKM']:>15} {beacon_age:15.1f} {colour.DEFAULT}")
            else:
                del ap[bssid]

if __name__ == '__main__':
    beacon_max_age = 30 #seconds
    ap = {}
    int='wlan0'
    sniff(iface=int, prn=dump)
