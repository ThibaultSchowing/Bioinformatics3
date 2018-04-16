#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
import matplotlib.pyplot as plt

def plotDistributionComparison(histograms, legend, title):
    '''
    Plots a list of histograms with matching list of descriptions as the legend
    '''
    # adjust size of elements in histogram 
        
    # plots histograms
    for h in histograms:
        plt.plot(range(len(h)), h, marker = 'x')
    
    # remember: never forget labels! :-)
    plt.xlabel('')
    plt.ylabel('')
    
    # you don't have to do something here
    plt.legend(legend)
    plt.title(title)
    plt.tight_layout()# might throw a warning, no problem
    plt.show()

def getPoissonDistributionHistogram(num_nodes, num_links, k):
    '''
    Generates a Poisson distribution histogram up to k
    '''