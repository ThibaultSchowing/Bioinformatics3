#!/usr/bin/python
#Bioinformatics 3 : Wiebke Schmitt & Thibault Schowing
from RandomNetwork import RandomNetwork
from DegreeDistribution import DegreeDistribution
import Tools

plot1 = [(50,100),(500,1000),(5000,10000),(50000,100000)]
plot2 = [(20000,5000),(20000,17000),(20000,40000),(20000,70000)]

plot_data = []
plot_legend = []
for nodes, edges in plot1:
    # build random network
    rand_net = RandomNetwork(nodes, edges)
    rand_degree = DegreeDistribution(rand_net).getNormalizedDistribution()
    plot_data.append(rand_degree)
    plot_legend.append("r:"+str(nodes)+"/"+str(edges))
    
    # build Poisson
    poisson_degree = Tools.getPoissonDistributionHistogram(nodes, edges, len(rand_degree))
    plot_data.append(poisson_degree)
    plot_legend.append("p:"+str(nodes)+"/"+str(edges))

Tools.plotDistributionComparison(plot_data, plot_legend, "Plot 1")

plot_data = []
plot_legend = []
for nodes, edges in plot2:
    # build random network
    rand_net = RandomNetwork(nodes, edges)
    rand_degree = DegreeDistribution(rand_net).getNormalizedDistribution()
    plot_data.append(rand_degree)
    plot_legend.append("r:"+str(nodes)+"/"+str(edges))
    
    # build Poisson
    poisson_degree = Tools.getPoissonDistributionHistogram(nodes, edges, len(rand_degree))
    plot_data.append(poisson_degree)
    plot_legend.append("p:"+str(nodes)+"/"+str(edges))

Tools.plotDistributionComparison(plot_data, plot_legend, "Plot 2")