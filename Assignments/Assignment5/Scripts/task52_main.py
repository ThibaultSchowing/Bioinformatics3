from UniprotReader import UniprotReader
from generic_network import GenericNetwork
from GOreader import GOReader

if __name__== "__main__":

    path_pig_network = "../Data/sup53/pig_network.tsv"
    pig_network = GenericNetwork()
    pig_network.read_from_tsv(path_pig_network)

    path_pig_uniprot = "../Data/sup53/pig_uniprot.tsv"
    pig_uniprot = UniprotReader(path_pig_uniprot)

    path_pig_ontology = "../Data/sup53/pig_GO.gaf"
    pig_GO = GOReader(path_pig_ontology)