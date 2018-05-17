from collections import defaultdict

class UniprotReader:
    '''Reads uniprot tab files'''
    def __init__(self, filename):
        '''
        Initialization, read in file and build any data structure that makes you happy
        '''

        content_start = False

        # structure containing ENTRY : [list of other names]
        self.mapping = defaultdict(list)

        # structure containing other names : ENTRY
        other_gene_names = set()
        self.reverse_mapping = defaultdict(set)

        self.ENTRY = []
        self.ENTRY_NAME = []
        self.STATUS = []
        self.PROTEIN_NAMES = []
        self.GENE_NAMES = []
        self.ORGANISM = []

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


        #TODO separate protein names into a table (space separated entries)

        # Construct mapping
        for i in range(0, len(self.ENTRY)):
            self.mapping[self.ENTRY[i]] = self.GENE_NAMES[i]

            # Construct the reverse mapping:  Gene_names : ENTRY
            for names in self.GENE_NAMES[i]:
                # .add() on a set add only if value is not already present
                self.reverse_mapping[names].add(self.ENTRY[i])


    def get_uniprot_names_mapping(self):
        return self.mapping

    def get_names_uniprot_mapping(self):
        return self.reverse_mapping
