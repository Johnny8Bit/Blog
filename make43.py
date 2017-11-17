'''
Creates DHCP option 43 hex string from one or many WLC IP addreses
Written in Python 2, now broken in Python 3
'''
import sys
   
def end():
    print ('Usage: make43.py <WLC_IP_1> <WLC_IP_2> <WLC_IP_3> <WLC_IP_n>')
    print ('Space separated IPv4 Wireless LAN Controller addreses (x.x.x.x)')
    sys.exit()

def check_and_convert(octet_split):
    if len(octet_split) != 4:
        end()
    for octet in xrange(0, 4):
        if not octet_split[octet].isdigit() or int(octet_split[octet]) not in range(0, 256):
            end()
        else:
            octet_split[octet] = str(hex(int(octet_split[octet])))[2:]

        if len(octet_split[octet]) == 1:
               octet_split[octet] = '0' + octet_split[octet]
        var_value_list.append(octet_split[octet])
 
if len(sys.argv) <= 1:
    end()
    
ip_addresses, var_value_list = sys.argv[1:], []
for ip_address in xrange(0, len(ip_addresses)):
    ip_address_split = ip_addresses[ip_address].split('.')
    check_and_convert(ip_address_split)

var_type = 'f1'
var_value = ''
var_len = str(hex(len(ip_addresses) * 4))[2:]
if len(var_len) == 1: var_len = '0' + var_len
for item in var_value_list: var_value = var_value + item
print ('\noption 43 hex ' + var_type + var_len + var_value)
