from UniprotReader import UniprotReader
from generic_network import GenericNetwork
from GOreader import GOReader

from collections import defaultdict

class AnnotatedNetwork:

    def __init__(self, network_path, GO_path, uniprot_path):

        self.network = GenericNetwork()
        self.network.read_from_tsv(network_path)

        self.uniprot = UniprotReader(uniprot_path)
        self.GO = GOReader(GO_path)

        self.to_uniprot_mapper = self.uniprot.get_names_uniprot_mapping()
        self.to_othername_mapper = self.uniprot.get_uniprot_names_mapping()

        # dict containing network node {network node id : go ids}
        self.net_go = defaultdict(list)

        for id, node in self.network.nodes.items():
            uniprot_id = self.to_uniprot_mapper[id]

            # uniprot_id can contains 0, 1 or more names
            # map the protein names with the GO ids
            goids = self.GO.get_GO_IDs(uniprot_id)
            self.net_go[id] = goids

        # We now have a dictionary containing our nodes with the GO identifiers

    def generate_overview(self):
        # Task 52
        print("Total protein in the network: ", len(self.network.nodes))
        print("Total interactions in the network: ", self.network.nb_edges)

        # number of protein
        nb_prot = 0
        # number of protein without annotation
        nb_prot_wo_annotation = 0
        # {number of annotation : qty}
        nb_annot_qty = dict()
        # total annotation (Not unique, see total_annot_unique
        total_annot = 0

        for key in self.net_go:
            nb_prot += 1
            nb_annotation = len(self.net_go[key])

            total_annot += nb_annotation

            if nb_annotation == 0:
                nb_prot_wo_annotation += 1

            # increment quantity of annotation
            if nb_annotation in nb_annot_qty:
                nb_annot_qty[nb_annotation] += 1
            else:
                nb_annot_qty[nb_annotation] = 1

        print("Nb prot: ", nb_prot, "\t\tNb without annotation: ", nb_prot_wo_annotation, "\t\tPercentage: ",
              (nb_prot_wo_annotation / nb_prot) * 100)
        print("Smallest number of annotation: ", sorted(nb_annot_qty)[0], "\t\tAverage number of annotation: ",
              total_annot / nb_prot, "\t\tBiggest number of annotation: ", sorted(nb_annot_qty)[-1])

        # Protein per annotation

        # mapper
        annot_prots = self.GO.goid_accessnb

        # infos
        total_annot = 0
        total_prot_per_annot = 0
        # reuse
        nb_prot = 0
        # dict {number of prot/annot : qty}
        nb_prot_qty = dict()
        for key in annot_prots:
            total_annot += 1
            nb_prot = len(annot_prots[key])
            total_prot_per_annot += nb_prot

            # increment quantity of annotation
            if nb_prot in nb_prot_qty:
                nb_prot_qty[nb_prot] += 1
            else:
                nb_prot_qty[nb_prot] = 1

        print("Smallest number of protein per annotation: ", sorted(nb_prot_qty)[0], "\t\tAverage number of protein: ",
              total_prot_per_annot / total_annot, "\t\tBiggest number of protein: ", sorted(nb_prot_qty)[-1])
