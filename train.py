#!/usr/bin/python2

USAGE = """Usage {0} network_file.net action
    Actions:
        - train pattern_filename.pat
        - regress 
        - letter A-Z
        - test max_noise_num
"""

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

        filename = "{0}_{1}.net".format(name, up_to+1)
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

#        number of train runs does not affect the network
#        trained_up_to_times = int(argv[4])
        trained_up_to_times = 1

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
        if len(argv) < 4:
            print >> sys.stderr, USAGE.format(argv[0])
            exit(1)

        max_noise_num = int(argv[3])

        input, target = load_snns('letters.pat')

        regressions_for_noise_amount = {}
        # for all noise levels we want to check
        for noise_amount in range(1, max_noise_num+1):
            noised_input = add_noise_to_input(input, noise_amount)
            net = loadnet(net_filename)

            output, regress = net.test(noised_input, target)

            # store results for future use
            regressions_for_noise_amount[noise_amount] = regress

        # plot and save results
        print("Plotting results...")
        plot_save_regressions(regressions_for_noise_amount)

    pass

def add_noise_to_input(input, noise_amount):
    print("adding {} noises to each input letter pattern...".format(noise_amount))

    n = len(input)
    noised_input = map(lambda ar: add_noise_to_letter(ar, noise_amount), input)

#    debug print
    for i in range(n):
        letter = chr(i + 65)
        print("real   {0}: {1}".format(letter, input[i]))
        print("noised {0}: {1}".format(letter, noised_input[i]))

    return noised_input

# add noise to an array
def add_noise_to_letter(letter_array, noise_amount):
    letter_array = letter_array.copy()
    from random import randint
    for _ in range(noise_amount):
        noise_here = randint(0, len(letter_array) - 1)
        letter_array[noise_here] = not letter_array[noise_here]

    return letter_array

def plot_save_regressions(regressions_for_noise_amount):
    from pylab import (imshow,subplot,bar,xticks,xlim,axhline,title,xlabel,ylabel,arange,show,cm)

    subplot(212)
    N = len(regressions_for_noise_amount) # how many noise levels we have to draw
    print("Will plot for for {} noise levels...".format(N))

    ind = arange(N)   # the x locations for the groups
    print("ind = {}".format(ind))
    width = 0.35       # the width of the bars

#    projection id -> name, as returned into tuples by http://ffnet.sourceforge.net/apidoc.html#ffnet.ffnet.test
    y_name = {}
    y_name[1] = "slope"
    y_name[2] = "intercept"
    y_name[3] = "r-value"
    y_name[4] = "p-value"
    y_name[5] = "slope stderr"
    y_name[6] = "estim. stderr"

    for projection_id in range(1,6): # todo has bug? how do i select the data
        ylabel(y_name[projection_id])

        projections = map(lambda t: t[projection_id], regressions_for_noise_amount[projection_id])
        print("PROJECTIONS on [{}] = {}".format(projection_id, projections))

        bar(0, projections[0], width, color='b') # plot it

    xticks(ind+width/2., range(1, N+1)) # todo print noiselevels
    xlim(-width,N-width)
    axhline(linewidth=1, color='black')
    title("Trained network (35-10-26) guesses a letter above...")
    xlabel("Noise amount")

    show()


if __name__ == "__main__":
    import sys
    _main(sys.argv)

