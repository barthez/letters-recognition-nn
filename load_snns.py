import re
from pylab import array

def load_snns(filename):
    file = open(filename, 'r')
    params = {
            'patterns' : 0,
            'input' : 0,
            'output' : 0 
            }
    patterns = {
            'input' : [],
            'output' : []
            }
    while file:
        line = file.readline();
        if len(line) == 0:
            break
        p1 = re.match('^No\. of ([a-z]*)[^:]*: (\d+)$', line)
        p2 = re.match('^[#] ([A-Za-z]+)[^\d]*(\d+):$', line)
        if p1:
            what, how_much = p1.group(1,2)
            how_much = int(how_much)
            params[what] = how_much
#            print "%s: %d" % (what, params[what])
        elif p2:
            what, which = p2.group(1,2)
            which = int(which)
            what = what.lower() 
            ti = []
            it = 0
            while it < params[what]:
                l = file.readline()
                ti += map(int, l.split())
                it = len(ti)
#            print "%s: %d" % (what, which)
#            print ti
            patterns[what].append(array(ti))

    return (patterns['input'], patterns['output'])

#inputs, outputs = load_snns('letters.pat')
#a = inputs[0]

#from pylab import *

#imshow(a.reshape(7,5), interpolation = 'nearest')
#show()
