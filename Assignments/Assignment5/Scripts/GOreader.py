from collections import defaultdict

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
                    self.ACCESS_NUMBER.append(line_tab[1]) # Protein name to map
                    self.ALTERNATIVE_NAME.append(line_tab[2])
                    self.GO_IDENTIFIER.append(line_tab[4])
                    self.ONTOLOGY_INDICATOR.append(line_tab[8])

        # Create a data structure with all information

        self.DATA = []
        for i in range(0, len(self.DB_NAME)):

            entry_line = [self.DB_NAME[i],
                              self.ACCESS_NUMBER[i], # real name in uniprot
                              self.ALTERNATIVE_NAME[i],
                              self.GO_IDENTIFIER[i],
                              self.ONTOLOGY_INDICATOR[i]]

            self.DATA.append(entry_line)

        # Create 4 dictionaries to map all GO ids of the GO file with the other data (prot names)
        # dict {GOID : access_number}
        # dict {GOID : alternative_name}
        # dict {alternative_name : GOID}
        # dict {access_number : GOID}

        self.goid_accessnb = defaultdict(set)
        self.accessnb_goid = defaultdict(set)
        self.alternativename_goid = defaultdict(set)
        self.goid_alternativename = defaultdict(set)

        # For readability

        idx_db_name = 0
        idx_access_nb = 1
        idx_alter_name = 2
        idx_go_id = 3
        idx_onto_id = 4

        # For every entry, fill the mappers.
        # The commented mappers are not used but could be useful
        for entry_line in self.DATA:
            #self.goid_accessnb[entry_line[idx_go_id]].add(entry_line[idx_access_nb])
            self.accessnb_goid[entry_line[idx_access_nb]].add(entry_line[idx_go_id])
            #self.alternativename_goid[entry_line[idx_alter_name]].add(entry_line[idx_go_id])
            #self.goid_alternativename[entry_line[idx_go_id]].add(entry_line[idx_alter_name])

    def get_GO_IDs(self, proteinID):
        """
        Get a protein name, returns all GO ids related to it
        :param proteinID:
        :return:
        """
        lst1 = []
        for prot in proteinID:
            tmp = self.accessnb_goid[prot]
            lst1.extend(list(tmp))

        return lst1

    def get_data(self):
        return self.DATA

