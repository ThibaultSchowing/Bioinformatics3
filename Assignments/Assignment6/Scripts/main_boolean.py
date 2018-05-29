from boolean_network import BooleanNetwork

print("Assignment 6 - Wiebke Schmitt and Thibault Schowing")

# Indexes
# A = 5
# B = 4
# C = 3
# D = 2
# E = 1
# F = 0

# Number of possible states: 2^6 = 64

# A is the least significant bit (last one) and F the most.


#    F  E  D  C  B  A
propagation_matrix = [
    [0, 0, 1, 0, 0, 0],  # F - Activates D
    [1, 0, 0, 0, 0, 0],  # E - Activates F
    [-3, -3, 0, 0, -3, 0],  # D - Inhibits B, E and F
    [0, 1, 0, 0, 1, 0],  # C - Activates B and E
    [0, 0, 0, 1, 0, 0],  # B - Activates C
    [0, 0, 0, 0, 1, 1]  # A - Activates A and B
]

net = BooleanNetwork(propagation_matrix)






print("=========================================")
print("                Part 1")
print("=========================================\n")

print("Sequence from state 1")
print(net.get_states_sequence(1))
print("Sequence from state 4")
print(net.get_states_sequence(4))
print("Sequence from state 21")
print(net.get_states_sequence(21))
print("Sequence from state 33")
print(net.get_states_sequence(33))

print("\n\n=========================================")
print("                Part 2")
print("=========================================\n")


# Save: Start & Orbit-size & Attractors & Basin of Attraction coverage
# for the LaTeX report
tmp_file_line = ""
with open('Orbits.txt', 'w+') as f:
    f.write("Start State & Period & First Steps & Orbit Details & Coverage of basin \\\\ \\hline \n")

    for i in range(0, net.nb_states):
        orbit = net.orbit(i)


        # Relative state space coverage of the state space by the basins of attraction
        # Len orbit + other states leading to orbit
        relative_ssc = ((len(orbit[1]) + len(orbit[3])) / net.nb_states) * 100

        tmp_file_line = str(i) + " & " + str(orbit[0]) + " & " + str(orbit[3]) + " & " + str(orbit[1]) + " & " + str(
            relative_ssc) + "\%\\\\ \\hline \n"
        f.write(tmp_file_line)

    # TODO: Periodic orbit ?? Basin of attraction ?? WTF ?

    # Get and print the list of the basins of attractions


    # ATTENTION ! Because of frozenset, the order is not respected.
    list_attractors = net.count_attractors()
    print("\nPeriodic orbits, number of occurrences and state space coverage: \n")
    for orbit in list_attractors:
        print(list(orbit), ": ", list_attractors[orbit], " : ", (int(list_attractors[orbit]) / net.nb_states) * 100, "%")
    print()

    # For each orbit, get the average occupancy
    print("==============")
    print("Orbits details")
    print("==============")

    list_attractors = [[0],
                       [1, 3, 7, 23, 55, 63, 13],
                       [4, 18, 36, 26],
                       [5, 19, 39, 31]]


    for orbit in list_attractors:
        print("\nCurrent orbit: ", list(orbit))
        print("Binary evolution: ")
        percentages = net.average_occupancies_in_orbit(list(orbit), True)
        print("Average occupancy:\n", percentages)
