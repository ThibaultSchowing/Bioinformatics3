
from generic_network import GenericNetwork

# graph must be an adjacency matrix with 0 and 1

def N(vertex):
    return [i for i, n_v in enumerate(graph[vertex]) if n_v]


def Bron_Kerbosch(r, p, x):
    if len(p) == 0 and len(x) == 0:
        print(r)
    for vertex in p[:]:
        r_new = r[:]
        r_new.append(vertex)
        p_new = [val for val in p if val in N(vertex)]
        x_new = [val for val in x if val in N(vertex)]
        Bron_Kerbosch(r_new, p_new, x_new)
        p.remove(vertex)
        x.append(vertex)

