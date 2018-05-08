import matplotlib.pyplot as plt
from itertools import combinations


def plot_layout(layout, title):
    """
    Plots the layout of a network.
    :param layout: Layout-object
    :param title: plot title
    """
    for node_1, node_2 in list(combinations(layout.network.nodes.values(), 2)):
        if layout.network.has_edge(node_1, node_2):
            # plot the edge between the two nodes, if it exists
            plt.plot([node_1.pos_x, node_2.pos_x], [node_1.pos_y, node_2.pos_y], linestyle='-', color='black')

    # plot the nodes
    for node in layout.network.nodes.values():
        plt.plot(node.pos_x, node.pos_y, marker='H', color='red')

    # set the title, clean up the plot layout and show it
    plt.title(title)
    plt.tight_layout()
    plt.show()
    plt.clf()


def plot_energies(energy_lists, legend, title):
    """
    Plots list(s) of total energies.
    :param energy_lists: a list that contains a list of total energies
    :param legend: a list of curve labels
    :param title: plot title
    """
    # plot each list of total energies
    for energy_list in energy_lists:
        plt.plot(energy_list)

    # set the x-axis and y-axis labels
    plt.xlabel('iteration')
    plt.ylabel('E')

    # set the legend, title, clean up the plot layout and show it
    plt.legend(legend)
    plt.title(title)
    plt.tight_layout()
    plt.show()
    plt.clf()