#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
import matplotlib.pyplot as plt
import math


def poisson(k, lambda_):

    #If k == 0, the first part is equal to 1 -> less computation (?)
    if k == 0:
        return math.exp(-lambda_)
    else:
        return ((lambda_**k) / (math.factorial(k))) * math.exp(-lambda_)


def plotDistributionComparison(histograms, legend, title):
    '''
    Plots a list of histograms with matching list of descriptions as the legend
    '''
    # adjust size of elements in histogram
    # https://stackoverflow.com/questions/13400876/python-length-of-longest-sublist

    maxlength = len(max(histograms,key=len))
    #print("Debug max len", maxlength)
    for h in histograms:
        # Expant the current histogram (table) to the size of the biggest one
        h.extend([0.0] * (maxlength - len(h)))

    fig = plt.figure()
    # plots histograms
    for h in histograms:
        plt.plot(range(len(h)), h, marker = 'x')
    
    # remember: never forget labels! :-)
    plt.xlabel('k')
    plt.ylabel('P(k)')
    
    # you don't have to do something here
    plt.legend(legend)
    plt.title(title)
    plt.tight_layout()# might throw a warning, no problem

    # Uncomment the line below to display normally
    #plt.show()

    # Comment the 2 lines below to display normally
    filename = title + ".png"
    fig.savefig(filename)


def getPoissonDistributionHistogram(num_nodes, num_links, k):
    '''
    Generates a Poisson distribution histogram up to k
    '''

    lambda_ = (2 * num_links) / num_nodes

    poissonDistribution = []

    # From 0 to k included
    for i in range(0, k + 1):
        poissonDistribution.append(poisson(i, lambda_))

    #print("Debug Poisson histogram", poissonDistribution)
    return poissonDistribution






