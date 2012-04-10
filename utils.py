import re
from pylab import array, imshow, imsave, imread, cm

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
        line = file.readline()
        if not len(line):
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

def export_letter(filename, arr, rows = 7, cols = 5):
    if not re.search('\.png$', filename):
        filename += '.png'
    imsave(filename, arr.reshape(rows,cols), cmap=cm.Greys)

def import_letter(filename):
    if not re.search('\.png$', filename):
        filename += '.png'
    arr = imread(filename)
    return array(
            map(lambda y: map(lambda z: abs(z[0]-1), y), arr)
           ).flatten()
    
def export_all_letters():
    inputs, _ = load_snns('letters.pat')
    for ipt, let in zip(inputs, "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        export_letter("letters/" + let, ipt)

def show_letter(arr, rows=7, cols=5):
    imshow(arr.reshape(rows,cols), cmap=cm.Greys)
