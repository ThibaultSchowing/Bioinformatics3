class GOReader:
    '''Reads GO files'''
    def __init__(self, filename):
        '''
        Initialization, read in file and build any data structure that makes you happy
        '''

        self.DB_NAME = []
        self.ACCESS_NUMBER = []
        self.ALTERNATIVE_NAME = []
        self.GO_IDENTIFIER = []
        self.ONTOLOGY_INDICATOR = []

        with open(filename, "r") as f:
            for line in f:
                if line.startswith("UniProtKB"):
                    # Process data
                    line = line.rstrip()
                    line_tab = line.split('\t')

                    # Skip all entries not belonging to biological process ontology
                    if line_tab[8] != 'P':
                        continue

                    self.DB_NAME.append(line_tab[0])
                    self.ACCESS_NUMBER.append(line_tab[1])
                    self.ALTERNATIVE_NAME.append(line_tab[2])
                    self.GO_IDENTIFIER.append(line_tab[4])
                    self.ONTOLOGY_INDICATOR.append(line_tab[8])

#TODO use the reverse_mapping to associate the ALTERNATIVE_NAME with the protein name