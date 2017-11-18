'''
Adds Cisco IOS ' | b'  style pipe functionality to Windows output

Usage sh.py <windows_command> <start_string> <number_of_output_lines>
Runs command and displays output starting from matching string
Output length can be specified as additional parameter, default is 20 lines

netpacket.net
'''
import sys, subprocess

__author__ = 'Michal Kowalik'
__version__= '0.1'
__status__ = 'Prototype'

if len(sys.argv) >= 2:
    runme = sys.argv[1]
    try:
        catch = subprocess.check_output(runme, shell=True).decode("utf-8")
    except subprocess.CalledProcessError:
        sys.exit()
    if len(sys.argv) >= 3:
        search = sys.argv[2]
        output_lines = 20
        if len(sys.argv) == 4:
            try:
                output_lines = int(sys.argv[3])
            except ValueError:
                output_lines == 20
        found, count = False, 0
        for line in catch.split('\n'):
            if search in line:
                found = True
            if found and count < output_lines:
                print(line)
                count += 1
    else:
        print(catch)
