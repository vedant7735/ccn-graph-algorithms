# LIBRARIES

import networkx as nx
import matplotlib.pyplot as plt


# NETWORK

G = nx.Graph()
edges = [
    (0,1,4), (0,2,3), (1,2,1),
    (1,3,2), (2,3,4), (3,4,2),
    (4,5,6), (5,6,5), (4,6,3)
]
G.add_weighted_edges_from(edges)


# COMPUTATION

mst = nx.minimum_spanning_tree(G, weight='weight')


# VISUALIZATION (before/after)

pos = nx.spring_layout(G, seed=42)

plt.figure(figsize=(8,6))
nx.draw(G, pos, with_labels=True, node_color="#D5F5E3", node_size=700)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'weight'))
plt.title("Original Network")
plt.show()

plt.figure(figsize=(8,6))
nx.draw(G, pos, with_labels=True, node_color="#D5F5E3", node_size=700)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G,'weight'))
nx.draw_networkx_edges(G, pos, edgelist=mst.edges(), edge_color="red", width=3)
plt.title("MST Highlighted")
plt.show()

plt.figure(figsize=(8,6))
nx.draw(mst, pos, with_labels=True, node_color="#D5F5E3", node_size=700)
nx.draw_networkx_edge_labels(mst, pos, edge_labels=nx.get_edge_attributes(mst,'weight'))
plt.title("Minimum Spanning Tree")
plt.show()


# OUTPUT

edges_sorted = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])

parent = {node: node for node in G.nodes()}
rank = {node: 0 for node in G.nodes()}


def find(node):
    if parent[node] != node:
        parent[node] = find(parent[node])
    return parent[node]


def union(u, v):
    root_u = find(u)
    root_v = find(v)

    if root_u == root_v:
        return False

    if rank[root_u] > rank[root_v]:
        parent[root_v] = root_u
    elif rank[root_u] < rank[root_v]:
        parent[root_u] = root_v
    else:
        parent[root_v] = root_u
        rank[root_u] += 1

    return True


mst_edges = []
total_cost = 0

with open("mst_process.txt", "w") as f:

    f.write("MINIMUM SPANNING TREE (KRUSKAL)\n")
    f.write("="*50 + "\n\n")
    f.write("Step-by-step edge selection:\n\n")

    step = 1

    for u, v, data in edges_sorted:
        w = data['weight']

        f.write(f"Step {step}: Considering edge ({u}, {v}) weight={w}\n")

        if union(u, v):
            mst_edges.append((u, v, w))
            total_cost += w
            f.write(" -> Added to MST\n\n")
        else:
            f.write(" -> Rejected (cycle detected)\n\n")

        step += 1

    f.write("="*50 + "\n")
    f.write("FINAL MST:\n\n")

    for u, v, w in mst_edges:
        f.write(f"{u} -- {v} == {w}\n")

    f.write(f"\nTotal Cost: {total_cost}\n")


print("\nMST:\n")
for u, v, w in mst_edges:
    print(f"{u} -- {v} == {w}")

print("Total Cost:", total_cost)