import pandas as pd
from scipy import stats

class DataMatrix:
    def __init__(self, file_path):
        """
        :param file_path: path to the input matrix file
        """
        self.file_path = file_path
        # TODO: define and initialise the class fields you need for your implementation
        self.df = None
        # read the matrix in the input file, remove rows with empty values and merge duplicate rows
        self.read_data()

    def read_data(self):
        """
        Reads data from a given matrix file, where the first line gives the names of the columns and the first column
        gives the names of the rows. Removes rows with empty or non-numerical values and merges rows with the same
        name into one.
        """

        self.df = pd.read_csv(self.file_path, index_col=False, sep='\t')

        # Drop all NAN before setting the first columns as index
        self.df.dropna(axis=0, how="any", inplace=True)

        new_columns = self.df.columns.values
        new_columns[0] = "Index"
        self.df.columns = new_columns

        # Sort values for later use (to_tsv)
        self.df = self.df.sort_values('Index')

        # Group by index: remove duplicate rows by meaning the rows values
        # Set Index as index automatically
        self.df = self.df.groupby('Index').mean()

        print(self.df)


    def get_rows(self):
        """
        :return: dictionary with keys = row names, values = list of row values
        """
        rows = {}

        for index, row in self.df.iterrows():
            rows[index] = list(row)

        #print(rows)
        return rows



    def get_columns(self):
        """
        :return: dictionary with keys = column names, values = list of column values
        """
        cols = {}
        for name, values in self.df.iteritems():
            cols[name] = list(values)

        #print(cols)
        return cols

    def not_normal_distributed(self, alpha, rows):
        """
        Uses the Shapiro-Wilk test to compute all rows (or columns) that are not normally distributed.
        :param alpha: significance threshold
        :param rows: True if the Shapiro-Wilk p-values should be computed for the rows, False if for the columns
        :return: dictionary with keys = row/columns names, values = Shapiro-Wilk p-value
        """

        ret = {}

        if rows:
            tmp = self.get_rows()
        else:
            tmp = self.get_columns()

        for key, value in tmp.items():
            shapiro = stats.shapiro(tmp[key])
            pvalue = shapiro[1]

            if pvalue < alpha:
                ret[key] = pvalue

        #print(ret)
        return ret

    def to_tsv(self, file_path):
        """
        Writes the processed matrix into a tab-separated file, with the same column order as the input matrix and
        the rows in lexicographical order.
        :param file_path: path to the output file
        """
        self.df.to_csv(file_path, sep='\t')
