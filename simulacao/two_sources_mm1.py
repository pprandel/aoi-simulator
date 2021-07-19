import queueing_tool as qt
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


RO = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95]
ARRIVAL_TIMES = [1/r for r in RO]

# Create a graph
g = nx.DiGraph()
# Add nodes
g.add_nodes_from([1, 2, 3])
# Add edges
g.add_edge(1,2)
g.add_edge(1,3)
# Queue classes
q_cl = {1: qt.QueueServer,2: qt.QueueServer,3: qt.QueueServer}
# Draw
# plt.subplot(121)
# nx.draw(g, with_labels=True)
# plt.show()

def arr(t): return t+ np.random.exponential(0.5)
def ser(t): return t + np.random.exponential(1)

net = qt.QueueNetworkDiGraph(g)
plt.subplot()
net.draw_graph()
plt.show()