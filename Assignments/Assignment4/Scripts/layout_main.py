from layout import Layout
from tools import plot_layout, plot_energies


file_paths = ['star.txt', 'square.txt', 'star++.txt', 'dog.txt']
file_paths = ['dog.txt']

for file_path in file_paths:
    # read the file into your layout class

    layout = Layout(file_path)

    # run the normal layout for 1000 iterations and store the total energies
    # plot the normal layout

    energies1 = layout.layout(1000)
    plot_layout(layout, file_path + " - Normal Layout")

    # run the simulated annealing layout for 1000 iterations and store the total energies
    # plot the simulated annealing layout

    energies2 = layout.simulated_annealing_layout(1000)
    plot_layout(layout, file_path + " - Simulated Annealing Layout")

    # plot the total energies of the normal layout and the simulated annealing layout

    plot_energies([energies1,energies2], ["Normal layout", "Simulated Annealing Layout"], "Layout energies")
    pass
