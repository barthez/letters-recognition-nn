#!/usr/bin/python2

USAGE = """Usage {0} network_file.net action
    Actions:
        - train pattern_filename.pat (bfgs|cg|genetic|momentum|rprop|tnc)
        - regress 
        - letter A-Z
        - test max_noise_num
"""

from ffnet import ffnet, mlgraph, savenet, loadnet
from pylab import array, mean
from utils import *
from re import sub as re_sub

def create_bp(input, output):
    it = len(input[0])
    ot = len(output[0])

    connection = mlgraph((it, 10, ot))
    net = ffnet(connection)

    print("Created new network...")
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
    print regress
#   plot(array(target).T[n], output.T[n], 'o',
#           label='targets vs. outputs')
#   slope = regress[n][0]; 
#   intercept = regress[n][1]
#   x = linspace(0,1)
#   y = slope * x + intercept
#   plot(x, y, linewidth = 2, label = 'regression line')
#   legend()
#   show()

def create_then_save_network_trained_on(name, pattern, train_method):
    input, output = load_snns(pattern)
    net = create_bp(input, output)

    print("Training the net with {0} algorithm...".format(train_method))
    training = getattr(net, "train_" + train_method)
    training(input, output)

    filename = "{0}_{1}.net".format(name, train_method)
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

        train_method = "momentum"
        if len(argv) > 4:
            train_method = argv[4]

#        number of train runs does not affect the network
#        trained_up_to_times = int(argv[4])
        trained_up_to_times = 1

        print("Will train networks on: {0}...".format(pattern_filename))
        create_then_save_network_trained_on(
                net_filename,
                pattern_filename,
                train_method)

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

        regressions_for_noise_amount = []
        # Load net
        net = loadnet(net_filename)

        # for all noise levels we want to check
        for noise_amount in range(max_noise_num+1):
            noised_input = add_noise_to_input(input, noise_amount)

            output, regress = net.test(noised_input, target, iprint = 0)

            # store results for future use
            regressions_for_noise_amount.append( mean(regress, 0) )

        # plot and save results
        print("Plotting results...")
        plot_save_regressions(array(regressions_for_noise_amount), net_filename)

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

def plot_save_regressions(regressions_for_noise_amount, net_filename):
    from pylab import (imshow,subplot,bar,xticks,xlim,axhline,title,
            xlabel,ylabel,arange,show,cm,figure,savefig,save,imsave)

    name = net_filename.rsplit('.', 1)[0]

    # how many noise levels we have to draw
    N = len(regressions_for_noise_amount) 
    print("Will plot for for {} noise levels...".format(N))

    ind = arange(N)   # the x locations for the groups
    print("ind = {}".format(ind))
    width = 0.35       # the width of the bars

#    projection id -> name, as returned into tuples by http://ffnet.sourceforge.net/apidoc.html#ffnet.ffnet.test
    y_name = ["slope",
        "intercept",
        "r-value",
        "p-value",
        "slope stderr",
        "estim. stderr"]

    for projection_id in range(6): # todo has bug? how do i select the data
        #subplot(11 + projection_id * 100) # a new plot
        figure()

        projection_name = y_name[projection_id]
        ylabel(projection_name)
        print("Plotting for projection: " + projection_name)

        projections = regressions_for_noise_amount.T[projection_id]
        print("Projections on {} tuple field ({}) = {}".format(projection_id, projection_name, projections))

        title(projection_name + " for noise levels...") # todo change me?

        for i in ind:
            bar(i, projections[i], width, color='b') # plot it
#        bar(ind, projections[ind], width, color='b') # plot it

        xticks(ind+width/2., range(0, N)) # todo print noise levels
        xlim(-width,N-width)
        axhline(linewidth=1, color='black')
        xlabel("Noise amount")

#        debug uncomment to look at graphs
#        show()
        plot_output_formats = ['png', 'eps']
        for format in plot_output_formats:
            plot_name = re_sub(
                    "[^a-z]",
                    "_",
                    y_name[projection_id].lower() )

            plot_filename = "{}_plot_{}.{}".format(
                    name, 
                    plot_name,
                    format)
            savefig(plot_filename, orientation='portrait')
            print("Saved plot as: {}.".format(plot_filename))


if __name__ == "__main__":
    import sys
    _main(sys.argv)

