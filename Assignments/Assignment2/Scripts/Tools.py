import matplotlib.pyplot as plt
import math


def plotDistributionComparison(histograms, legend, title):
    '''
    Plots a list of histograms with matching list of descriptions as the legend
    '''
    # determine max. length
    max_length = max(len(x) for x in histograms)
    
    # extend "shorter" distributions
    for x in histograms:
        x.extend([0.0]* (max_length-len(x)) )
        
    # plots histograms
    for h in histograms:
        plt.plot(range(len(h)), h, marker = 'x')
    
    # remember: never forget labels!
    plt.xlabel('degree')
    plt.ylabel('P')
    
    # you don't have to do something stuff here
    plt.legend(legend)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def plotDistributionComparisonLogLog(histograms, legend, title):
    '''
    Plots a list of histograms with matching list of descriptions as the legend
    '''
    fig = plt.figure()
    ax = plt.subplot()
    # determine max. length
    max_length = max(len(x) for x in histograms)
    
    # extend "shorter" distributions
    for x in histograms:
        x.extend([0.0]* (max_length-len(x)) )
    
    ax.set_xscale("log")
    ax.set_yscale("log")
      
    # plots histograms
    for h in histograms:
        ax.plot(range(len(h)), h, marker = 'x', linestyle='')
    
    # remember: never forget labels!
    plt.xlabel('degree')
    plt.ylabel('P')
    
    # you don't have to do something stuff here
    plt.legend(legend)
    plt.title(title)
    plt.tight_layout()

    # Uncomment the line below to display normally
    # plt.show()

    # Comment the 2 lines below to display normally
    filename = title + ".png"
    fig.savefig(filename)


def getScaleFreeDistributionHistogram(gamma, k):
    '''
    Generates a Power law distribution histogram with slope gamma up to degree k
    '''
    histogram = []
    # NORMALISATION_CONSTANT \
    # Todo here or in ScaleFreeTest.py

    for i in range(1, k):
        histogram.append(i**-gamma)


    return histogram


def simpleKSdist(histogram_a, histogram_b):
    '''
    Simple Kolmogorov-Smirnov distance implementation
    '''
    #print("KSDIST: size hist 1: ", len(histogram_a), "  Size hist2: ", len(histogram_b))
    D = 0
    # Assume that the two hists have the same length
    for i in range(0, len(histogram_a)-1):
        D = max(D, (histogram_a[i] - histogram_b[i]))

    return D