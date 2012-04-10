#!/usr/bin/python2

USAGE = """Usage {0} network_file.net action
    Actions:
        - train pattern_filename.pat [max_noise_level = 0]
        - regress 
        - letter A-Z"""

from ffnet import ffnet, mlgraph, savenet, loadnet
from pylab import array
from utils import *

def create_bp(input, output):
    it = len(input[0])
    ot = len(output[0])

    connection = mlgraph((it, 10, ot))
    net = ffnet(connection)

    print("Created new network...")
    return net

# trains a network, multiple times
def train_bp(net, input, output):
    net.train_momentum(input, output)
    return net

def plot_net_output(net, input):
    from pylab import (imshow,subplot,bar,xticks,xlim,axhline,
            title,xlabel,ylabel,arange,show,cm)

    subplot(211)
    imshow(input.reshape(7,5), interpolation = 'nearest', cmap=cm.Greys)
    subplot(212)
    N = 26

    ind = arange(N)   # the x locations for the groups
    width = 0.35       # the width of the bars
    bar(ind, net(input), width, color='b') #make a plot
    xticks(ind+width/2., tuple('abcdefghijklmnopqrstuvwxyz'))
    xlim(-width,N-width)
    axhline(linewidth=1, color='black')
    title("Trained network (35-10-26) guesses a letter above...")
    xlabel("Letter")
    ylabel("Network outputs")

    show()

def regression_analysis(net, input, target):
    from pylab import plot, legend, show, linspace
    output, regress = net.test(input, target, iprint = 2)
#   plot(array(target).T[n], output.T[n], 'o',
#           label='targets vs. outputs')
#   slope = regress[n][0]; 
#   intercept = regress[n][1]
#   x = linspace(0,1)
#   y = slope * x + intercept
#   plot(x, y, linewidth = 2, label = 'regression line')
#   legend()
#   show()

def create_then_save_network_trained_on(name, pattern, trained_up_to_times):
    input, output = load_snns(pattern)
    net = create_bp(input, output)

    for up_to in range(trained_up_to_times):
        print("Training the net for the {0}th time...".format(up_to+1)),
        net = train_bp(net, input, output)

        filename = "{0}_trained_{1}_times.net".format(name, up_to+1)
        savenet(net, filename)
        print("saved as: {0}".format(filename))

def _main(argv):
    if len(argv) < 3:
        print >> sys.stderr, USAGE.format(argv[0])
        exit(1)

    net_filename = argv[1]

    if argv[2] == 'train':
        if len(argv) < 4:
            print >> sys.stderr, USAGE.format(argv[0])
            exit(1)
        pattern_filename = argv[3]
        trained_up_to_times = int(argv[4])
        print("Will train networks on: {0}...".format(pattern_filename))
        create_then_save_network_trained_on(net_filename, pattern_filename, trained_up_to_times)

    elif argv[2] == 'regress':
        input, output = load_snns('letters.pat')
        net = loadnet(net_filename)
        regression_analysis(net, input, output)

    elif argv[2] == 'letter':
        if len(argv) < 4:
            print >> sys.stderr, USAGE.format(argv[0])
            exit(1)
        input, _ = load_snns('letters.pat')
        net = loadnet(net_filename)
        letter = ord(argv[3][0])-65
        if letter < 0 or letter > 25:
            print >> sys.stderr, "Letter must be uppercase A-Z"
            exit(1)
        plot_net_output(net, input[letter])

    elif argv[2] == 'test':
        input, _ = load_snns('letters.pat')
        net = loadnet(net_filename)

        output, regress = net.test(input, target)
    pass

if __name__ == "__main__":
    import sys
    _main(sys.argv)

