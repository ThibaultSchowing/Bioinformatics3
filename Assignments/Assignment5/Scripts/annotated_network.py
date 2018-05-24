from UniprotReader import UniprotReader
from generic_network import GenericNetwork
from GOreader import GOReader
import numpy as np
from collections import defaultdict
import itertools
from itertools import combinations
import math


def nCr(n,r):
    """
    # https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
    :param n: Total number of object in the set
    :param r: Number of object in the subset
    :return: Number of possible subset
    """
    return math.factorial(n) // math.factorial(r) // math.factorial(n-r)


class AnnotatedNetwork:

    def __init__(self, network_path, GO_path, uniprot_path):

        self.network = GenericNetwork()
        self.network.read_from_tsv(network_path)

        self.uniprot = UniprotReader(uniprot_path)
        self.GO = GOReader(GO_path)

        self.to_uniprot_mapper = self.uniprot.get_names_uniprot_mapping()

        #self.to_othername_mapper = self.uniprot.get_uniprot_names_mapping()

        # dict containing network node {network node id : go ids}
        self.net_go = defaultdict(list)

        # Mapping protein to GOs
        # {nodeid : [GO, GO, ...]}
        for id, node in self.network.nodes.items():

            # Convert the protein id
            uniprot_id = self.to_uniprot_mapper[id]

            # uniprot_id can contains 0, 1 or more names
            # map the protein names with the GO ids
            goids = self.GO.get_GO_IDs(uniprot_id)
            self.net_go[id] = goids

        # Reverse mapping GO to proteins(net)
        # {GO annot : [node, node, ...]}
        self.go_net = defaultdict(set)

        for node in self.net_go:
            list_annot = self.net_go[node]

            for annot in list_annot:
                self.go_net[annot].add(node)

        # Completing GO in the network and quantity
        # {GO : qty}
        self.go_qty = defaultdict(int)

        for key in self.go_net:
            self.go_qty[key] = len(self.go_net[key])

        # COMPUTE ANNOTATION QUANTITY OCCURRENCE
        # number of protein
        self.nb_prot = 0
        # number of protein without annotation
        self.nb_prot_wo_annotation = 0
        # {number of annotation : occurence}
        self.nb_annotqty_occurence = dict()
        # total annotation (Not unique, see total_annot_unique
        self. total_annot = 0

        # for every node
        for key in self.net_go:
            self.nb_prot += 1
            nb_annotation = len(self.net_go[key])

            self.total_annot += nb_annotation

            if nb_annotation == 0:
                self.nb_prot_wo_annotation += 1

            # increment quantity of annotation
            if nb_annotation in self.nb_annotqty_occurence:
                self.nb_annotqty_occurence[nb_annotation] += 1
            else:
                self.nb_annotqty_occurence[nb_annotation] = 1


        # PROTEIN PER ANNOTATION

        self.total_prot_per_annot = 0

        # dict {number of prot/annot : occurence}
        self.nb_prot_occurence = dict()

        # for every annotation in {GO : nodes}
        for annot in self.go_net:
            nb_prot = len(self.go_net[annot])
            self.total_prot_per_annot += nb_prot

            # increment quantity of annotation
            if nb_prot in self.nb_prot_occurence:
                self.nb_prot_occurence[nb_prot] += 1
            else:
                self.nb_prot_occurence[nb_prot] = 1
            #print annotation: proteins
            #print(annot, "\t\t", self.go_net[annot])




    def generate_overview(self):
        """
        Generate the overview of the network
        :return: nada
        """
        # Task 52
        print("\n--------Annotated Network Overview--------\n")
        print("Total protein in the network: ", len(self.network.nodes))
        print("Total interactions in the network: ", self.network.nb_edges)
        print("Total unique annotation: ", len(self.go_net))

        print("Nb prot: ", self.nb_prot, "\t\tNb without annotation: ", self.nb_prot_wo_annotation, "\t\tPercentage: ",
              (self.nb_prot_wo_annotation / self.nb_prot) * 100)

        print("Smallest number of annotation: ", sorted(self.nb_annotqty_occurence)[0], "\t\tAverage number of annotation: ",
              self.total_annot / self.nb_prot, "\t\tBiggest number of annotation: ", sorted(self.nb_annotqty_occurence)[-1])

        print("Smallest number of protein per annotation: ", sorted(self.nb_prot_occurence)[0], "\t\tAverage number of protein: ",
              self.total_prot_per_annot / len(self.go_net), "\t\tBiggest number of protein: ", sorted(self.nb_prot_occurence)[-1])

        print("\n\n")

    def get_common_GOid(self, n):
        """
        Return the n most common GO identifiers of the annotated network
        :param n: number of GO wanted
        :return: tuple of lists (n most common, n least common)
        """
        #sorted_go_qty = sorted(self.go_qty.items(), key=lambda x: x[1])

        # Table of sorted GO quantity (DESC) and sorted GO id (ASC)
        sorted_go_qty1 = [v[0] for v in sorted(self.go_qty.items(), key=lambda kv: (-kv[1], kv[0]))]

        # Table of sorted GO quantity (ASC) and sorted GO id (ASC)
        sorted_go_qty2 = [v[0] for v in sorted(self.go_qty.items(), key=lambda kv: (kv[1], kv[0]))]


        print("Most common GO ids")
        n_most_common = list(itertools.islice(sorted_go_qty1, n))

        for goid in n_most_common:
            print(goid, "\t", self.go_qty[goid])

        print("Least common GO ids")
        n_least_common = list(itertools.islice(sorted_go_qty2, n))

        for goid in n_least_common:
            print(goid, "\t", self.go_qty[goid])

        return (n_most_common, n_least_common)

    def annotation_enrichment(self, top):
        """

        :param top: number of top annotation probability
        :return: the n highest and lowest p(a)
        """

        # List of all possible protein pairs in the network
        protein_pairs = list(itertools.combinations(self.network.nodes, 2))
        # Number of possible pair
        N = len(protein_pairs)
        # Number of interacting protein pairs
        n = self.network.nb_edges

        # Annotation and interacting pairs {GO : [(prot1,prot2),(prot2,prot3),...]}
        self.annot_all_pairs = defaultdict(list)
        self.annot_interaction_pairs = defaultdict(list)
        self.annot_probability = defaultdict(float)


        ncr_Nn = nCr(N, n)

        # For each annotation in the network
        for A in self.go_net:

            # For every possible pair in the network, check if both have annotation A
            # If they have both annotation A, check if the two proteins are interacting (connected in the network)
            for pair in protein_pairs:
                if A in self.net_go[pair[0]] and A in self.net_go[pair[1]]:
                    self.annot_all_pairs[A].append(pair)

                    # if pair 0 and pair 1 are interacting
                    if self.network.get_node(pair[0]).has_edge_to(self.network.get_node(pair[1])):
                        self.annot_interaction_pairs[A].append(pair)

            # Ka = number of protein pairs where both proteins have annotation A
            Ka = len(self.annot_all_pairs[A])

            # ka = number of interacting protein pairs where both proteins have annotation A
            ka = len(self.annot_interaction_pairs[A])

            N_minus_Ka = N - Ka

            # Trying to optimize here ! (not bad, can do better !)
            if ka == 0:
                self.annot_probability[A] = 1
                # print(A, "\t pA: ", 1)
                continue

            pA = 0
            for i in range(ka, min(Ka, n) + 1):
                nCr_Ka_i = nCr(Ka, i)
                nCr_N_minus_Ka_n_i = nCr(N_minus_Ka, n - i)

                pA += (nCr_Ka_i * nCr_N_minus_Ka_n_i) / ncr_Nn

            self.annot_probability[A] = pA

        # The number and percentage of annotations A with pA < 0.05, pA > 0.5, pA > 0
        pa_005 = pa_05 = pa_095 = 0
        for A in self.annot_probability:
            if self.annot_probability[A] <= 0.05:
                pa_005 += 1
            if self.annot_probability[A] < 0.95:
                pa_05 += 1
            if self.annot_probability[A] >= 0.95:
                pa_095 += 1

        # Percentages
        tot_annot = len(self.go_net)
        pct_005 = pa_005 / tot_annot
        pct_05 = pa_05 / tot_annot
        pct_095 = pa_095 / tot_annot

        print("Number of annotation with pA < 0.05         : ", pa_005, "-> ", pct_005*100, "%")
        print("Number of annotation with pA > 0.5 & < 0.95 : ", pa_05, "-> ", pct_05*100, "%")
        print("Number of annotation with pA > 0.95         : ", pa_095, "->", pct_095*100, "%")
        print("\n")

        # The n annotations with the smallest pA and the n annotations with the highest pA.
        # If there are several annotations with the same pA, choose the ones that are associated
        # with more proteins first

        # Create a (GO, pA, Nb-prot) list for the later sort
        annot_prob_prot = []
        for A in self.annot_probability:
            annot_prob_prot.append((A, self.annot_probability[A], len(self.go_net[A]), len(self.annot_interaction_pairs[A])))

        # gives  [('GO-id', p(A), nb_protein), (..., ..., ...)] with P(a) ordered ASC
        sorted_probabilities_ASC = [(v[0], v[1], v[2], v[3]) for v in sorted(annot_prob_prot, key=lambda kv: (kv[1], kv[2]))]

        # gives  [('GO-id', p(A), nb_protein), (..., ..., ...)] with P(a) ordered DSC
        sorted_probabilities_DSC = [(v[0], v[1], v[2], v[3]) for v in sorted(annot_prob_prot, key=lambda kv: (-kv[1], -kv[2]))]

        # Take the "top" firsts
        smallest_prob = list(itertools.islice(sorted_probabilities_ASC, top))
        biggest_prob = list(itertools.islice(sorted_probabilities_DSC, top))

        print("\n\n(GO:id  |  pA  |  Nb Protein | Nb Interact. Protein)\n")
        print("Five smallest Pa: \n")
        for e in smallest_prob:
            print(e)

        print("\nFive biggest Pa: \n")
        for e in biggest_prob:
            print(e)

    def annotation_combination(self, k, r, m):
        """

        :param k: combination size
        :param r: number of random distribution
        :param m: m combinations with the smallest pc and the m annotations with the highest pc
        :return:
        """
        annotation_probability = defaultdict(float)

        # number of protein in the network
        n = self.network.size()

        # number of protein with annotation A
        # len(self.go_net[A]

        # For each annotation, compute its probability
        # go_net -> {GO_id : [prot1, prot2, ...]}
        for A in self.go_net:
            annotation_probability[A] = len(self.go_net[A]) / n

        # Generate a list of all annotation combinations of size k that occur in the annotated network
        # https://stackoverflow.com/questions/22799053/combinations-of-elements-of-different-tuples-in-the-list
        #all_combinations = list(combinations(self.go_net, k))

        # Combination set contains all combination of k annotation contained in the network
        combination_dict = defaultdict(list)
        for node in self.net_go:
            if len(self.net_go[node]) < k:
                continue

            tmp_combinations = combinations(self.net_go[node], k)

            # For each k-combination for this node
            for combination in tmp_combinations:
                # The combination are sorted in order to avoid adding (a,b) and (b,a)
                s_combination = tuple(sorted(combination))
                if s_combination in combination_dict:
                    combination_dict[s_combination][0] += 1
                else:
                    combination_dict[s_combination].append(1)

        # for A in annotation_probability:
        #     print(A, "\t", len(self.go_net[A]), "\t\t", annotation_probability[A])

        # For each combination (C1, C2, ...) in the network...
        for C in combination_dict:
            # Cn = how often this combination occurs in the network
             #nc = combination_dict[C]

            Pe_c = annotation_probability[C[0]] * annotation_probability[C[1]]
            combination_dict[C].append(Pe_c)

        for key in combination_dict:
            # probability_list = [combination_dict[key][1]] * n
            prob = combination_dict[key][1]

            # nr = number of random sample in which C occurs at least as much as in the original network
            nr = 0
            for _ in range(0, r):
                random_list = np.random.choice([0, 1], size=n, p=[1 - prob, prob])

                # C in the actual network appears combination_dict[key][0] times
                # number of occurence in random network
                nb_occ = np.count_nonzero(random_list)

                if nb_occ >= combination_dict[key][0]:
                    nr += 1
            # Calculating and adding the probability pc to the dict "combination_dict"
            pc = nr / r
            combination_dict[key].append(pc)

        # IMPORTANT - structure of combination dict.
        # combination_dict = (c1, c2) : [nb_occ, expect_prob, rand_prob]

        pc_0001 = pc_005 = pc_05 = 0
        nb_C = len(combination_dict)
        for c in combination_dict:
            pc = combination_dict[c][2]
            if pc < 0.001:
                pc_0001 += 1
            elif pc < 0.005:
                pc_005 += 1
            elif pc > 0.05:
                pc_05 += 1

        # percentages
        pct_0001 = pc_0001/nb_C
        pct_005 = pc_005/nb_C
        pct_05 = pc_05/nb_C

        print("pc < 0.001 : ", pc_0001, "-> ", pct_0001 * 100, "%")
        print("pc < 0.005 : ", pc_005, "-> ", pct_005 * 100, "%")
        print("pc < 0.05  : ", pc_05, "-> ", pct_05 * 100, "%")

        combination_dict_sorted_ASC = sorted(combination_dict.items(), key=lambda e: e[1][2])
        combination_dict_sorted_DSC = sorted(combination_dict.items(), key=lambda e: -e[1][2])

        # Take the "m" firsts
        smallest_prob = list(itertools.islice(combination_dict_sorted_ASC, m))
        biggest_prob = list(itertools.islice(combination_dict_sorted_DSC, m))

        print("\n\n(GO:ids  |  Occurence in the data  |  Pe(C) | Pc)\n")
        print("Three smallest Pc: \n")
        for e in smallest_prob:
            print(e)

        print("\nThree biggest Pc: \n")
        for e in biggest_prob:
            print(e)
