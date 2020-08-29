'''
https://netpacket.net/2020/08/finding-hidden-ssids/
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
    if packet.haslayer(Dot11FCS):
        dot11_fcs = packet.getlayer(Dot11FCS)
        bssid = dot11_fcs.fields['addr2']
    if packet.haslayer(Dot11ProbeResp):
        probe_response = packet.getlayer(Dot11ProbeResp)
        probe_response_payload = probe_response.payload
        probe_response_ssid = probe_response_payload.fields['info'].decode('utf-8')
        hidden[bssid] = probe_response_ssid
    if packet.haslayer(Dot11Beacon):
        timestamp = time.time()
        radiotap = packet.getlayer(RadioTap)
        signal = radiotap.fields['dBm_AntSignal']
        frequency = radiotap.fields['ChannelFrequency']
        rate = radiotap.fields['Rate']
        beacon = packet.getlayer(Dot11Beacon)
        beacon_payload = beacon.payload
        beacon_ssid = beacon_payload.fields['info'].decode('utf-8')
        if beacon_ssid == '':
            is_hidden = 'Yes'
            if bssid in hidden:
                beacon_ssid = hidden[bssid]
        else:
            is_hidden = 'No'
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
        ap[bssid] = {'RSSI' : signal, 'Hidden' : is_hidden, 'SSID': beacon_ssid, 'Time': timestamp, 'Rate': rate, 'Frequency': frequency, 'Cipher': cipher, 'AKM': akm}
        run('clear')
        print(f" {'BSSID':18} {'Hidden':7} {'SSID':35} {'RSSI':>6} {'Rate':>6} {'Frequency':>10} {'Cipher':>10} {'Suite':>12} {'Age(sec)':>10}")
        for bssid in sorted(ap, key=lambda x: ap[x]['RSSI'], reverse=True):
            beacon_age = timestamp - ap[bssid]['Time']
            if beacon_age < beacon_max_age: #and ap[bssid]['Hidden'] == 'Yes':
                if ap[bssid]['RSSI'] < -65:
                    print(f"{colour.GREEN} {bssid:18} {ap[bssid]['Hidden']:7} {ap[bssid]['SSID']:35} {ap[bssid]['RSSI']:6} {ap[bssid]['Rate']:6} {ap[bssid]['Frequency']:10} {ap[bssid]['Cipher']:>10} {ap[bssid]['AKM']:>12} {beacon_age:10.1f} {colour.DEFAULT}")
                if ap[bssid]['RSSI'] in range (-65, -49):
                    print(f"{colour.YELLOW} {bssid:18} {ap[bssid]['Hidden']:7} {ap[bssid]['SSID']:35} {ap[bssid]['RSSI']:6} {ap[bssid]['Rate']:6} {ap[bssid]['Frequency']:10} {ap[bssid]['Cipher']:>10} {ap[bssid]['AKM']:>12} {beacon_age:10.1f} {colour.DEFAULT}")
                if ap[bssid]['RSSI'] in range (-49, -39):
                    print(f"{colour.RED} {bssid:18} {ap[bssid]['Hidden']:7} {ap[bssid]['SSID']:35} {ap[bssid]['RSSI']:6} {ap[bssid]['Rate']:6} {ap[bssid]['Frequency']:10} {ap[bssid]['Cipher']:>10} {ap[bssid]['AKM']:>12} {beacon_age:10.1f} {colour.DEFAULT}")
                if ap[bssid]['RSSI'] > -40:
                    print(f"{colour.MAGENTA} {bssid:18} {ap[bssid]['Hidden']:7} {ap[bssid]['SSID']:35} {ap[bssid]['RSSI']:6} {ap[bssid]['Rate']:6} {ap[bssid]['Frequency']:10} {ap[bssid]['Cipher']:>10} {ap[bssid]['AKM']:>12} {beacon_age:10.1f} {colour.DEFAULT}")
            else:
                del ap[bssid]

if __name__ == '__main__':
    beacon_max_age = 30 #seconds
    ap, hidden = {}, {}
    int='wlan0'
    sniff(iface=int, prn=dump)
