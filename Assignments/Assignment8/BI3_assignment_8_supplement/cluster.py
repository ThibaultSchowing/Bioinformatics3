class Cluster(frozenset):
    """
    This class behaves like a frozenset, meaning it only contains unique items like a set but you cannot add or remove
    items, which makes it hashable and thus suitable for dictionary keys or as elements of a normal set.
    You can use the modified union method to merge two clusters as follows:
    merged_cluster = cluster_1.union(cluster_2)
    The to string method was modified as well to help with the trace_to_tsv() method in exercise 8.4.
    """
    def __str__(self):
        """
        :return: string with the sorted elements of the current cluster: element_1, element_2,...
        """
        return ', '.join(sorted(self))

    def union(self, iterable):
        """
        :param iterable: a Cluster, list, set, iterator,...
        :return: a new Cluster containing all elements in the current cluster and the iterable
        """
        return Cluster(list(self) + list(iterable))


class CorrelationClustering:
    def __init__(self, correlation_matrix):
        """
        Initialises and executes hierarchical clustering based on a correlation matrix.
        :param correlation_matrix: a CorrelationMatrix (see correlation.py)
        """
        # distance metric
        self.d = correlation_matrix
        # list of tuples: [(cluster 1 to merge, cluster 2 to merge, linkage value between the two clusters),...]
        self.trace = []
        # cluster the elements in the correlation matrix
        self.cluster()

    def cluster(self):
        """
        Hierarchically clusters the elements in the input correlation matrix and stores each step in the trace.
        """
        # TODO

    def average_linkage(self, cluster_1, cluster_2):
        """
        :return: average linkage between cluster 1 and cluster 2
        """
        # TODO

    def trace_to_tsv(self, file_path):
        """
        Writes the clustering trace into a tab-separated file. Each line represents a step in the clustering, in which
        two clusters are merged.
        Column 0: comma-separated names in cluster 1
        Column 1: comma-separated names in cluster 2
        Column 2: linkage value
        :param file_path: path to the output file
        """
        # TODO
