from data_matrix import DataMatrix
from network import CorrelationNetwork
from correlation import CorrelationMatrix
from cluster import CorrelationClustering

def dict_to_file(dict, path):
    fout = path
    fo = open(fout, "w")

    for k, v in dict.items():
        fo.write(str(k) + ' > ' + str(v) + '\n')

    fo.close()

def exercise_1():
    # Read data
    data_expression = DataMatrix("./expression.tsv")
    data_methylation = DataMatrix("./methylation.tsv")

    # Uses the Shapiro-Wilk test to test if the data follow a normal distribution

    ALPHA = 0.05

    not_normal_expression_genes = data_expression.not_normal_distributed(ALPHA, True)
    dict_to_file(not_normal_expression_genes, "./not_normal_expression_genes.txt")
    print("Number of genes whose data does not follow a normal distribution (EXPRESSION): ", len(not_normal_expression_genes))

    not_normal_expression_sample = data_expression.not_normal_distributed(ALPHA, False)
    dict_to_file(not_normal_expression_sample, "./not_normal_expression_sample.txt")
    print("Number of sample whose data does not follow a normal distribution (EXPRESSION): ", len(not_normal_expression_sample))

    not_normal_methylation_genes = data_methylation.not_normal_distributed(ALPHA, True)
    dict_to_file(not_normal_methylation_genes, "./not_normal_methylation_genes.txt")
    print("Number of genes whose data does not follow a normal distribution (METHYLATION): ", len(not_normal_methylation_genes))

    not_normal_methylation_sample = data_methylation.not_normal_distributed(ALPHA, False)
    dict_to_file(not_normal_methylation_sample, "./not_normal_methylation_sample.txt")
    print("Number of sample whose data does not follow a normal distribution (METHYLATION): ", len(not_normal_methylation_sample))


    # Write processed matrix to file
    data_expression.to_tsv("schmitt_schowing_expression.tsv")
    data_methylation.to_tsv("schmitt_schowing_methylation.tsv")


def exercise_3():
    # TODO
    cm = CorrelationMatrix(DataMatrix("./expression.tsv"), "Pearson", True)
    pass


def exercise_4():
    # TODO
    pass

# only execute the following if this module is the entry point of the program, not when it is imported into another file
if __name__ == '__main__':
    exercise_1()
    exercise_3()
    exercise_4()
