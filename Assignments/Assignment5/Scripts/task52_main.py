from UniprotReader import UniprotReader
from generic_network import GenericNetwork
from GOreader import GOReader

from annotated_network import AnnotatedNetwork

from collections import defaultdict
import collections

if __name__== "__main__":

    # For pig
    path_pig_network = "../Data/sup53/pig_network.tsv"
    pig_network = GenericNetwork()
    pig_network.read_from_tsv(path_pig_network)

    path_pig_uniprot = "../Data/sup53/pig_uniprot.tsv"
    pig_uniprot = UniprotReader(path_pig_uniprot)

    path_pig_ontology = "../Data/sup53/pig_GO.gaf"
    pig_GO = GOReader(path_pig_ontology)

    # For human
    path_human_network = "../Data/sup53/human_network.tsv"
    human_network = GenericNetwork()
    human_network.read_from_tsv(path_human_network)

    path_human_uniprot = "../Data/sup53/human_uniprot.tsv"
    human_uniprot = UniprotReader(path_human_uniprot)

    path_human_ontology = "../Data/sup53/human_GO.gaf"
    human_GO = GOReader(path_human_ontology)


    Anet = AnnotatedNetwork(path_human_network, path_human_ontology, path_human_uniprot)
    Anet.generate_overview()


