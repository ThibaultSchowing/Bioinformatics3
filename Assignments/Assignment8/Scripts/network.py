import collections
import pandas as pd
import math

class CorrelationNetwork:
    def __init__(self, correlation_matrix, threshold):
        """
        Constructs a co-expression network from a correlation matrix by adding edges between nodes with absolute
        correlation bigger than the given threshold.
        :param correlation_matrix: a CorrelationMatrix (see correlation.py)
        :param threshold: a float between 0 and 1
        """

        interactions = []
        for tup, corr in correlation_matrix.items():

            correlation = str(round(corr, 2))
            node0 = tup[0]
            node1 = tup[1]

            tmp = [node0, node1, correlation]
            tmp.sort(reverse=True)
            interactions.append(tmp)

        # create set of unique node connections (src, dest, corr)
        set_interractions = set(tuple(i) for i in interactions)

        # Sort the set
        set_interractions = sorted(set_interractions)

        #for tup in set_interractions:
            #print(tup)


        df_interractions = pd.DataFrame.from_records(set_interractions)

        df_interractions.columns = ['src','dest','corr']
        #print(df_interractions)

        # Creating a dictionary with the structure as below:
        #   dict (src, corr): [dest]
        #
        self.dc_interact = collections.defaultdict(list)

        # Fill the dictionary with unique src - correlation id and a dest. list
        for index, row in df_interractions.iterrows():
            # Skip too small correlations (threshold vs absolute value)
            if math.fabs(float(row['corr'])) < threshold:
                continue

            # If the correlation is big enough, add it to the dictionary
            tmp_tuple = (row['src'], row['corr'])
            self.dc_interact[tmp_tuple].append(row['dest'])

        # Debug printing for verification
        #for key, value in self.dc_interact.items():
        #    print(key, ": ", self.dc_interact[key])




    def to_sif(self, file_path):
        """
        Write the network into a simple interaction file (SIF).
        Column 0: label of the source node
        Column 1: interaction type
        Columns 2+: label of target node(s)
        :param file_path: path to the output file
        """

        f = open(file_path, "w")  # opens file

        for key, value in self.dc_interact.items():
            dests = ""
            for dest in self.dc_interact[key]:
                dests += "\t" + dest

            f.write(str(key[0]) + "\t" + str(key[1]) + dests + "\n")
        f.close()
