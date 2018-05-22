from collections import defaultdict

class UniprotReader:
    '''Reads uniprot tab files'''
    def __init__(self, filename):
        '''
        Initialization, read in file and build any data structure that makes you happy
        '''

        # structure containing ENTRY : [list of other names]
        self.mapping = defaultdict(set)

        # structure containing other names : ENTRY
        self.reverse_mapping = defaultdict(set)

        self.ENTRY = []
        self.ENTRY_NAME = []
        self.STATUS = []
        self.PROTEIN_NAMES = []
        self.GENE_NAMES = []
        self.ORGANISM = []

        # Read file
        content_start = False
        with open(filename, "r") as f:
            for line in f:
                if content_start:
                    # Process data
                    line = line.rstrip()
                    line_tab = line.split('\t')

                    self.ENTRY.append(line_tab[0])
                    self.ENTRY_NAME.append(line_tab[1])
                    self.STATUS.append(line_tab[2])
                    # Split the different names
                    self.PROTEIN_NAMES.append(line_tab[3].split(' '))
                    self.GENE_NAMES.append(line_tab[4].split(' '))
                    self.ORGANISM.append(line_tab[5])

                if line.startswith("Entry"):
                    content_start = True
                    continue

        # Construct mapping and reverse mapping
        for i in range(0, len(self.ENTRY)):
            for gene in self.GENE_NAMES[i]:
                self.mapping[self.ENTRY[i]].add(gene)
                self.reverse_mapping[gene].add(self.ENTRY[i])


    def get_uniprot_names_mapping(self):
        return self.mapping

    def get_names_uniprot_mapping(self):
        return self.reverse_mapping


    # Print mapping to file or to console
    # OPTIONAL
    def print_mapping(self):
        print("TODO")

    def print_reverse_mapping(self):
        print("TODO")
