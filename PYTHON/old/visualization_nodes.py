import networkx as nx
import matplotlib.pyplot as plt

# G=nx.Graph()

# G.add_node("a")
# G.add_nodes_from(["b","c"])

# G.add_edge(1,2)
# edge = ("d", "e")
# G.add_edge(*edge)
# edge = ("a", "b")
# G.add_edge(*edge)

# print("Nodes of graph: ")
# print(G.nodes())
# print("Edges of graph: ")
# print(G.edges())
# # adding a list of edges:
# G.add_edges_from([("a","c"),("c","d"), ("a",1), (1,"d"), ("a",2)])

G=nx.path_graph(4)

cities = {0:"Toronto",1:"London",2:"Berlin",3:"New York"}

H=nx.relabel_nodes(G,cities)
print("Nodes of graph: ")
print(H.nodes())
print("Edges of graph: ")
print(H.edges())

nx.draw(H, with_labels = True)
plt.savefig("simple_path.png") # save as png
plt.show() # display