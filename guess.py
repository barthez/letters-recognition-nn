
def _main(argv):
    from ffnet import loadnet
    from utils import import_letter
    if len(argv) < 3:
        print >> sys.stderr, 'Usage: {0} network_file.net letter_file.png'.format(argv[0])
        exit(1)
    net = loadnet(argv[1])
    ipt = import_letter(argv[2])
    output = net(ipt)
    letter = output.argmax()
    print chr(65+letter)

if __name__ == "__main__":
    import sys
    _main(sys.argv)
