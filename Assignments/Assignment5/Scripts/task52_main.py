from UniprotReader import UniprotReader
from generic_network import GenericNetwork
from GOreader import GOReader

from annotated_network import AnnotatedNetwork

if __name__== "__main__":

    # ======================================================================================================= #
    print("----------------------------------------------------------------"
          "\n                   Chicken Annotated Network"
          "\n----------------------------------------------------------------\n")
    # ======================================================================================================= #

    path_chicken_network = "../Data/sup51/chicken_network.tsv"
    chicken_network = GenericNetwork()
    chicken_network.read_from_tsv(path_chicken_network)

    path_chicken_uniprot = "../Data/sup51/chicken_uniprot.tsv"
    chicken_uniprot = UniprotReader(path_chicken_uniprot)

    path_chicken_ontology = "../Data/sup51/chicken_GO.gaf"
    chicken_GO = GOReader(path_chicken_ontology)

    Anet_chicken = AnnotatedNetwork(path_chicken_network, path_chicken_ontology, path_chicken_uniprot)

    # GENERATE OVERVIEW
    Anet_chicken.generate_overview()

    # ANNOTATION ENRICHMENT
    print("\n\nInvestigating annotation enrichment for the chicken network\n")
    Anet_chicken.annotation_enrichment(5)

    # ANNOTATION COMBINATION
    print("\n\nInvestigating annotation combinations for the chicken network\n")
    Anet_chicken.annotation_combination(2, 100, 3)

    # ======================================================================================================= #
    print("\n\n----------------------------------------------------------------"
          "\n                     Pig Annotated Network"
          "\n----------------------------------------------------------------\n")
    # ======================================================================================================= #

    path_pig_network = "../Data/sup53/pig_network.tsv"
    pig_network = GenericNetwork()
    pig_network.read_from_tsv(path_pig_network)

    path_pig_uniprot = "../Data/sup53/pig_uniprot.tsv"
    pig_uniprot = UniprotReader(path_pig_uniprot)

    path_pig_ontology = "../Data/sup53/pig_GO.gaf"
    pig_GO = GOReader(path_pig_ontology)

    Anet_pig = AnnotatedNetwork(path_pig_network, path_pig_ontology, path_pig_uniprot)
    Anet_pig.generate_overview()

    # ======================================================================================================= #
    print("\n\n----------------------------------------------------------------"
          "\n                   Human Annotated Network"
          "\n----------------------------------------------------------------\n")
    # ======================================================================================================= #

    path_human_network = "../Data/sup53/human_network.tsv"
    human_network = GenericNetwork()
    human_network.read_from_tsv(path_human_network)

    path_human_uniprot = "../Data/sup53/human_uniprot.tsv"
    human_uniprot = UniprotReader(path_human_uniprot)

    path_human_ontology = "../Data/sup53/human_GO.gaf"
    human_GO = GOReader(path_human_ontology)

    Anet_human = AnnotatedNetwork(path_human_network, path_human_ontology, path_human_uniprot)
    Anet_human.generate_overview()

    common_human_GOids = Anet_human.get_common_GOid(5)
