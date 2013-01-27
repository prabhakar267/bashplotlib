#!/usr/bin/python
import math
from collections import Counter
import optparse
import sys


bcolours = {
    "white": '\033[97m',
    "aqua": '\033[96m',
    "pink": '\033[95m',
    "blue": '\033[94m',
    "yellow": '\033[93m',
    "green": '\033[92m',
    "red": '\033[91m',
    "grey": '\033[90m',
    "ENDC": '\033[0m'
}

def get_colour(colour):
    return bcolours.get(colour, bcolours['white'])

def printcolor(txt, sameline=False, color=get_colour("white")):
    if sameline:
        print color + txt + bcolours["ENDC"],
    else:
        print color + txt + bcolours["ENDC"]

def drange(start, stop, step=1.0):
    "generate between 2 numbers w/ optional step"
    r = start
    while r < stop:
        yield r
        r += step

def calc_bins(n, min_val, max_val, h=None):
    "calculate number of bins for the histogram"
    if not h:
        h = math.log(n + 1, 2) 
    bin_width = (max_val - min_val) / h
    for b in drange(min_val, max_val, bin_width):
        yield b

def read_numbers(numbers):
    if isinstance(numbers, list):
        for n in numbers:
            yield float(n.strip())
    else:
        for n in open(numbers):
            yield float(n.strip())

def plot_hist(f, height=20, bincount=None, pch="o", colour="white"):
    "plot a histogram given a file of numbers"
    #first apss
    if pch is None:
        pch = "o"
    
    colour = get_colour(colour)

    min_val, max_val = None, None
    n = 0.
    for number in read_numbers(f):
        n += 1

        if not min_val or number < min_val:
            min_val = number
        if not max_val or number > max_val:
            max_val = number

    bins = list(calc_bins(n, min_val, max_val, bincount))
    hist = Counter()
    for number in read_numbers(f):
        for i, b in enumerate(bins):
            if number < b:
                hist[i-1] += 1
             #   print "breaking"
                break



    min_y, max_y = min(hist.values()), max(hist.values())

    ys = list(drange(min_y, max_y, (max_y-min_y)/height))
    ys.reverse()

    nlen = max(len(str(min_y)), len(str(max_y))) + 1


    for y in ys:
        ylab = str(y)
        ylab += " "*(nlen - len(ylab)) + "|"

        printcolor(ylab, True, colour)

        for i in range(len(hist)):
            if y < hist[i]:
                printcolor(pch, True, colour)
            else:
                printcolor(" ", True, colour)
        print
    xs = hist.keys() * 2

    printcolor(" "*(nlen+1) + "-"*len(xs), False, colour)

    for i in range(0, nlen):
        printcolor(" "*(nlen+1), True, colour)
        for x in range(0, len(hist)):
            num = str(bins[x])
            if x%2==0:
                printcolor(" ", True, colour)
            elif i < len(num):
                printcolor(num[i], True, colour)
        print

    summary = "Summary\n--------\nMax: %s\nMin: %s\nCount: %s" % (min_val, max_val, int(n))
    print summary


if __name__=="__main__":

    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', help='a file containing a column of numbers',
                      default=None, dest='f')
    parser.add_option('-b', '--bins', help='number of bins in the histogram',
                      default=None, dest='b')
    parser.add_option('-s', '--height', help='height of the histogram (in lines)',
                      default=20, dest='h')
    parser.add_option('-p', '--pch', help='shape of each bar', default='o', dest='p')
    parser.add_option('-c', '--colour', help='colour of the plot', default='white', dest='colour')

    (opts, args) = parser.parse_args()
    
    if opts.f is None:
        opts.f = args[0]
    
    plot_hist(opts.f, opts.h, opts.b, opts.p, opts.colour)

