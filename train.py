
from ffnet import ffnet, mlgraph, savenet
from utils import *

def create_and_train_bp(input, output, **kwargs):
    it = len(input[0])
    ot = len(output[0])

    connection = mlgraph((it, 10, ot))
    net = ffnet(connection)

    net.train_momentum(input, output, **kwargs)

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

input, output = load_snns('letters.pat')

net = create_and_train_bp(input, output)


from random import randint

pat = randint(0,25)

plot_net_output(net, input[pat])


filename = raw_input("File name (empty to skip saving): ")
if len(filename) > 0:
    savenet(net, filename)

