#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
import matplotlib.pyplot as plt
import math


def poisson(k, lambda_):

    #If k == 0, the first part is equal to 1
    if k == 0:
        return math.exp(-lambda_)
    else:
        return ((lambda_**k) / (math.factorial(k))) * math.exp(-lambda_)


def plotDistributionComparison(histograms, legend, title):
    '''
    Plots a list of histograms with matching list of descriptions as the legend
    '''
    # adjust size of elements in histogram

        
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
    plt.show()


def getPoissonDistributionHistogram(num_nodes, num_links, k):
    '''
    Generates a Poisson distribution histogram up to k
    '''

    lambda_ = (2 * num_links) / num_nodes

    poissonDistribution = []

    for i in range(0,k + 1):
        poissonDistribution.append(poisson(i, lambda_))

    print("Debug Poisson histogram", poissonDistribution)
    #print(type(poissonDistribution))
    return poissonDistribution






