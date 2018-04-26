import operator
from GenericNetwork import GenericNetwork
from DegreeDistribution import DegreeDistribution
import Tools as Tools

class BioGRIDReader:
    '''Reads BioGRID tab files'''
    def __init__(self, filename):
        '''
        Initialization, read in file and build any data structure that makes you happy
        '''

        content_start = False

        # Temporary tab -> contains one line
        line_tab = []

        self.INTERACTOR_A = []
        self.INTERACTOR_B = []
        self.OFFICIAL_SYMBOL_A = []
        self.OFFICIAL_SYMBOL_B = []
        self.ALIASES_FOR_A = []
        self.ALIASES_FOR_B = []
        self.EXPERIMENTAL_SYSTEM = []
        self.SOURCE = []
        self.PUBMED_ID = []
        self.ORGANISM_A_ID = []
        self.ORGANISM_B_ID = []

        with open(filename, "r") as f:
            for line in f:
                if line.startswith("INTERACTOR_A"):
                    content_start = True
                    continue
                if content_start:
                    # Process data
                    line = line.rstrip()
                    line_tab = line.split('\t')

                    self.INTERACTOR_A.append(line_tab[0])
                    self.INTERACTOR_B.append(line_tab[1])
                    self.OFFICIAL_SYMBOL_A.append(line_tab[2])
                    self.OFFICIAL_SYMBOL_B.append(line_tab[3])
                    self.ALIASES_FOR_A.append(line_tab[4])
                    self.ALIASES_FOR_B.append(line_tab[5])
                    self.EXPERIMENTAL_SYSTEM.append(line_tab[6])
                    self.SOURCE.append(line_tab[7])
                    self.PUBMED_ID.append(line_tab[8])
                    self.ORGANISM_A_ID.append(line_tab[9])
                    self.ORGANISM_B_ID.append(line_tab[10])

        # The file has now been read and all infos are in lists
        # Tuples can store pairwise interactions



    def getMostAbundantTaxonIDs(self, n):

        interact = {}
        organism_pairs_list = zip(self.ORGANISM_A_ID, self.ORGANISM_B_ID)

        for A, B in organism_pairs_list:
            if not A in interact:
                interact[A] = 1
            else:
                interact[A] += 1

            # If both are the same, the interaction must be counted only once
            if A != B:
                if not B in interact:
                    interact[B] = 1
                else:
                    interact[B] += 1
        # Sort the dict to retrieve the n first
        # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

        sorted_interact = sorted(interact.items(), key=operator.itemgetter(1))


        nFirst = []
        for i in range(1, n+1):
            nFirst.append(sorted_interact[-i])

        return nFirst

    def getHumanInteraction(self):
        # Search for human-human interactions
        nb_human_human_interact = 0

        organism_pairs_list = zip(self.ORGANISM_A_ID, self.ORGANISM_B_ID)
        for A, B in organism_pairs_list:
            if A == B == "9606":
                nb_human_human_interact += 1

        print("HUMAN INTERACTIONS\n")
        print("\nNumber of Human-Human interactions (human id = 9606): ", nb_human_human_interact)

        # Now we need the indices of the human - human interactions
        # The code below extract the indices where ORGANISM A / ORGANISM B are human and take the intersection
        # Order dict: https://stackoverflow.com/questions/16772071/sort-dict-by-value-python

        # Get Indexes
        indexesA = [i for i, x in enumerate(self.ORGANISM_A_ID) if x == '9606']
        indexesB = [i for i, x in enumerate(self.ORGANISM_B_ID) if x == '9606']

        # Get intersection
        indexes = list(set(indexesA).intersection(indexesB))

        proteins = [self.OFFICIAL_SYMBOL_A[i] for i in indexes]
        proteins.extend([self.OFFICIAL_SYMBOL_B[i] for i in indexes])

        proteins_count = {}
        for prot in proteins:
            if prot not in proteins_count:
                proteins_count[prot] = 1
            else:
                proteins_count[prot] += 1
        proteins_count = sorted(proteins_count.items(), key=lambda x:x[1])

        # Obtain the n most used proteins
        n = 10
        nFirst = []
        for i in range(1, n + 1):
            nFirst.append(proteins_count[-i])

        print("\nThe ", n, " proteins with the highest degree are: ")
        print(nFirst)

    def writeInteractionFile(self, taxon_id, filename):

        organism_pairs_list = zip(self.ORGANISM_A_ID, self.ORGANISM_B_ID)
        file = open(filename, "w+")

        # Get Indexes
        indexesA = [i for i, x in enumerate(self.ORGANISM_A_ID) if x == taxon_id]
        indexesB = [i for i, x in enumerate(self.ORGANISM_B_ID) if x == taxon_id]

        # Get intersection
        indexes = list(set(indexesA).intersection(indexesB))

        for i in indexes:
            file.write(self.OFFICIAL_SYMBOL_A[i])
            file.write("\t")
            file.write(self.OFFICIAL_SYMBOL_B[i])
            file.write("\n")

        file.close()


if __name__== "__main__":

    path = "../../../../Bioinformatics3_data/assignment2/BIOGRID-ALL-3.4.159.tab.txt"
    bio = BioGRIDReader(path)
    abundantTaxon = bio.getMostAbundantTaxonIDs(5)
    print("The most abundent TaxonIDs are (id, qty): ", abundantTaxon)
    bio.getHumanInteraction()

    # Export human interactions to a file
    EXPORT_FILE_NAME = "humanFile.txt"
    EXPORT_ORGANISM = "9606"
    bio.writeInteractionFile(EXPORT_ORGANISM, EXPORT_FILE_NAME)

    # Create GenericNetwork with previously exported file
    gen = GenericNetwork(EXPORT_FILE_NAME)
    print(str(gen))
    print("The network has ", gen.degreeSum(), " links.\n")

    # Get distribution
    gen_degree = DegreeDistribution(gen).getNormalizedDistribution()
    # Plot the degree distribution
    Tools.plotDistributionComparisonLogLog([gen_degree], ["Human"],"Degree Distribution Generic network ")