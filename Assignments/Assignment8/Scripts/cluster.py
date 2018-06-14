import itertools

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

        Structure of correlation matrix:
        {('Abhd15', 'Acvr1b'): -0.20814079896736404, ('Acvr1b', 'Abhd15'): -0.20814079896736404, ('Abhd15', 'Acvrl1'): -0.13245323570650439,
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
        # Create a set of unique correlation (a, b, corr) but not (b, a, corr)

        interactions = []
        for tup, corr in self.d.items():
            correlation = str(round(corr, 2))
            node0 = tup[0]
            node1 = tup[1]

            tmp = [node0, node1, correlation]
            tmp.sort(reverse=True)
            interactions.append(tmp)

        # create set of unique node connections (corr, src, dest)
        set_interractions = set(tuple(i) for i in interactions)

        # set of nodes (experiments)
        set_experiment = set(i[0] for i in interactions)

        all_individual_clusters = []
        for element in set_experiment:
            tmp_cluster = Cluster([element])
            all_individual_clusters.append(tmp_cluster)

        # while we have more than one cluster

        while len(all_individual_clusters) > 1:

            # Compute linkage for all pair
            all_pairs = list(itertools.combinations(all_individual_clusters, 2))

            index_max_linkage = 0
            max_linkage = 0
            for i in range(len(all_pairs)):
                tmp_linkage = self.average_linkage(all_pairs[i][0], all_pairs[i][1])
                if tmp_linkage > max_linkage:
                    max_linkage = tmp_linkage
                    index_max_linkage = i

            # Now we have the two clusters to merge: merge them and remove them from the list
            # First add them to the trace
            #self.trace.append(str(all_pairs[index_max_linkage][0]) + " - " + str(all_pairs[index_max_linkage][1]) + " - " + str(max_linkage) )
            self.trace.append([all_pairs[index_max_linkage][0], all_pairs[index_max_linkage][1], max_linkage])
            new_cluster = all_pairs[index_max_linkage][0].union(all_pairs[index_max_linkage][1])

            # Remove the two clusters that are gonna be merged from the list
            all_individual_clusters.remove(all_pairs[index_max_linkage][0])
            all_individual_clusters.remove(all_pairs[index_max_linkage][1])

            # Append the new cluster resulting from the merging of the two old ones blah
            all_individual_clusters.append(new_cluster)



    def average_linkage(self, cluster_1, cluster_2):
        """
        :return: average linkage between cluster 1 and cluster 2
        """

        sum_ = 0
        for key1 in cluster_1:
            for key2 in cluster_2:
                sum_ += abs(self.d[(key1, key2)])

        return 1/(len(cluster_1) * len(cluster_2)) * sum_

    def trace_to_tsv(self, file_path):
        """
        Writes the clustering trace into a tab-separated file. Each line represents a step in the clustering, in which
        two clusters are merged.
        Column 0: comma-separated names in cluster 1
        Column 1: comma-separated names in cluster 2
        Column 2: linkage value
        :param file_path: path to the output file
        """

        f = open(file_path, "w")  # opens file

        # At each step we have the two merged cluster and their linkage value
        # The linkage value is rounded to 4 digits to make it nice
        for step in self.trace:
            f.write(str(step[0]) + "\t" + str(step[1]) + "\t" + str(round(step[2], 4)) + "\n")

        f.close()

