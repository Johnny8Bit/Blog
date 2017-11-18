'''
Removes leading whitespace and empty lines from text file

Usage: lstrip.py <filename.txt>
Overwrites existing file
Useful for cleaning up output from messy log files
'''
import sys

__author__ = 'Michal Kowalik'
__version__= '0.2'
__status__ = 'Prototype'

infile, outputlist = open(sys.argv[1]), []
for line in infile: outputlist.append(line.lstrip())
infile.close()
outfile = open(sys.argv[1], 'w')
for line in outputlist: outfile.write(line)
outfile.close()
