class DataMatrix:
    def __init__(self, file_path):
        """
        :param file_path: path to the input matrix file
        """
        self.file_path = file_path
        # TODO: define and initialise the class fields you need for your implementation
        # read the matrix in the input file, remove rows with empty values and merge duplicate rows
        self.read_data()

    def read_data(self):
        """
        Reads data from a given matrix file, where the first line gives the names of the columns and the first column
        gives the names of the rows. Removes rows with empty or non-numerical values and merges rows with the same
        name into one.
        """
        # TODO

    def get_rows(self):
        """
        :return: dictionary with keys = row names, values = list of row values
        """
        # TODO

    def get_columns(self):
        """
        :return: dictionary with keys = column names, values = list of column values
        """
        # TODO

    def not_normal_distributed(self, alpha, rows):
        """
        Uses the Shapiro-Wilk test to compute all rows (or columns) that are not normally distributed.
        :param alpha: significance threshold
        :param rows: True if the Shapiro-Wilk p-values should be computed for the rows, False if for the columns
        :return: dictionary with keys = row/columns names, values = Shapiro-Wilk p-value
        """
        # TODO

    def to_tsv(self, file_path):
        """
        Writes the processed matrix into a tab-separated file, with the same column order as the input matrix and
        the rows in lexicographical order.
        :param file_path: path to the output file
        """
        # TODO
