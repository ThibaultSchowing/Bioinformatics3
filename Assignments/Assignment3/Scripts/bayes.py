import math
import copy

# For all features, compute the probability (prior) to have 0, 1, 2 or 3 depending on the output (0 or 1)
def priors(features, output_indexes):
    priors = {}
    # Start to 1 to match the instructions
    feature_nb = 1
    for feature in features:
        P_Si_Output = {}
        # Values of the feature for a certain output (0 or 1)
        S = [feature[i] for i in output_indexes]
        # for all possible feature values -> [0,1,2,3], set dynamically here
        for value in set(feature):
            # Prob of having this 'value' when output is 0 or 1 (depend on output_indexes)
            P_Si_Output[value] = S.count(value) / float(len(S))

        priors[feature_nb] = P_Si_Output
        feature_nb += 1
    return priors


def log_likelihood(Prior_C, Prior_not_C, P_S_C, P_S_notC):
    log_like = [[0.0]*4 for _ in range(len(P_S_C))]

    #For each feature
    # Careful, in P_S_C it's a dict -> start at 1 as "feature 1"
    # in log_like it's a list of list -> feature 1 == [0]
    for feat in P_S_C:
        for val in [0,1,2,3]:
            p = math.log((P_S_C[feat][val] * Prior_C)/P_S_notC[feat][val] * Prior_not_C)
            log_like[feat-1][val] = p
    return log_like

# Returns the N max likelihood ratios
def getNMaxLikelihoodRatio(likelihoods, N):
    # As we have to loop N times, we'll need to set the max value to zero
    # in order not to pick it more than once.
    likelihoods_copy = copy.deepcopy(likelihoods)
    t = []
    for out in range(N):
        # Will contain (feature number, variant, absolute likelihood ratio)
        info = (0,0,0)
        max = 0

        for feat in range(len(likelihoods_copy)):
            for val in range(len(likelihoods_copy[feat])):
                if abs(likelihoods_copy[feat][val]) > max:
                    max = abs(likelihoods_copy[feat][val])
                    # Max is calculated with the abs, but the real value is stored
                    info = (feat, val, likelihoods_copy[feat][val])
                    likelihoods_copy[feat][val] = 0.0


        t.append(info)
    return t

# Read data file

def readFile(filename):
    lines = []
    with open(filename) as f:
        for line in f:
            line = line.split('\t')
            map(str.strip, line)
            lines.append(line)

    # Convert all the elements in float instead of chars
    lines = [[float(i) for i in line] for line in lines]
    return lines

lines = readFile("data/training1.tsv")

# Number of features
nb_features = len(lines[0]) - 1
print("Nb features: ", nb_features)

# Get the data by columns: https://stackoverflow.com/questions/44360162/how-to-access-a-column-in-a-list-of-lists-in-python
data_columns = list(zip(*lines))
# Problem, columns are now tuples
data_columns = [list(elem) for elem in data_columns]

# Features only
features = data_columns[1:]

# Output only
outputs = list(data_columns[0])

# Indexes according to outputs (1 or 0, first column)
interaction_indexes = [i for i,x in enumerate(outputs) if x == 1]

no_interaction_indexes = [i for i,x in enumerate(outputs) if x == 0]

# Prior probabilities

Prior_C = outputs.count(1) / float(len(outputs))
print("Prior probability of having a connection: ", Prior_C)
Prior_not_C = 1 - Prior_C
print("Prior probability of not having a connection: ", Prior_not_C)

# For each feature and possible value, calculate the probability according to the output

# P_S_C = Probability of having S (feature) according to output 1
P_S_C = priors(features, interaction_indexes)

# P_S_notC = Probability of having S (feature) according to output 0
P_S_notC = priors(features, no_interaction_indexes)

# Print every probabilities for every feature's values
# print("Features's values's probabilities if connection: \n")
# for p in P_S_C:
#     print("Feature ", p, ": ")
#     for val in P_S_C[p]:
#         print("\tValue: ", val, " prob: ", P_S_C[p][val])
#
# print("Features's values's probabilities if no connection: \n")
# for p in P_S_notC:
#     print("Feature ", p, ": ")
#     for val in P_S_notC[p]:
#         print("\tValue: ", val, " prob: ", P_S_notC[p][val])


# Now we compute the log likelihood for every features and possible output

log_like = log_likelihood(Prior_C, Prior_not_C, P_S_C, P_S_notC)
#print(log_like)

# Get the N (ABSOLUTE) max log-likelihood ratios.
maxLikelihoods = getNMaxLikelihoodRatio(log_like, 10)

# Nice printing
for _ in maxLikelihoods:
    print(_)

# Part D

lines = readFile("data/test1.tsv")
data_columns = list(zip(*lines))
data_columns = [list(elem) for elem in data_columns]
features = data_columns[1:]
outputs = list(data_columns[0])

print("Real test outputs: ")
print(outputs)

predictiontmp = []

for f in range(len(features)):
    tmp_output = 0
    for v in [0,1,2,3]:
        tmp_output += log_like[f][v]
    predictiontmp.append(tmp_output)

prediction = [0 if x < 0 else 1 for x in predictiontmp]
print(prediction)
