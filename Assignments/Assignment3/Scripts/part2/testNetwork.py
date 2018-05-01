from GenericNetwork import GenericNetwork
import sys
net = GenericNetwork("GoT.txt")
nb_links = net.nb_links
removed_links_list = [None] * nb_links

print(net)


# for all the links

for current_link in range(nb_links):
    min_coeff = sys.maxsize

    # Iterate through all the links
    for node_a in net.nodes:
        for node_b in net.nodes:
            node1 = net.getNode(node_a)
            node2 = net.getNode(node_b)

            # if the two nodes are different and are linked, check if the coeff is smaller or equal than nim_coeff
            if(node1 != node2 and node1.hasLinkTo(node2) and net.edgeClusterCoeff(node1, node2) <= min_coeff):
                # We have a temp minimal cluster coeff between node1 and node2
                min_coeff = net.edgeClusterCoeff(node1, node2)
                removed_links_list[current_link] = (node1, node2, min_coeff)
                # Nodes to remove (for now, they will be after the loops)
                buffer_node1 = node1
                buffer_node2 = node2

    # Here we have the minimal cluster with (node1, node2, coeff) in removed_links_list

    # To be sure that there is no mistakes
    if(buffer_node1.hasLinkTo(buffer_node2)):
        net.removeLink(buffer_node1, buffer_node2)
        print("Link removed: ", buffer_node1, " ", buffer_node2 , " ", min_coeff)
    else:
        print("Warning: node ", buffer_node1, " and ", buffer_node2, " have no link. ")

    #print(net)
