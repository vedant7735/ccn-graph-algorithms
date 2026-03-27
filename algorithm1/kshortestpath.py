# LIBRARIES

import heapq
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx



# NETWORK

NODES = {n: str(n) for n in range(1, 15)}

EDGES = [
    (1,2,4), (1,3,7), (2,3,3), (2,4,5), (3,4,6),
    (4,5,3), (4,7,9), (5,6,4), (5,7,5), (6,7,3),
    (1,8,18), (3,10,15),(4,9,11), (6,11,12),
    (7,8,4), (7,10,8), (8,9,3), (8,11,7),
    (9,10,4), (9,12,6), (10,11,5),
    (11,12,3),(11,13,5),(12,13,2),(12,14,7),(13,14,4),
    (2,11,20),(5,12,16),(6,14,19),
]

POS = {
     1:(0.0,7.5),  2:(1.0,9.0),  3:(1.0,6.0),
     4:(2.5,7.5),  5:(3.5,9.0),  6:(3.5,6.0),
     7:(5.0,7.5),  8:(6.5,9.0),  9:(6.5,6.5),
    10:(6.0,5.0), 11:(8.0,8.0), 12:(9.5,9.0),
    13:(9.5,6.5), 14:(10.5,7.5),
}

COLORS = ["#00E5FF", "#FF4081", "#FFD740"]


# USER INPUT

SRC = 1        # source node
DST = 14       # destination node
K = 3          # k variable


# FUNCTIONS

def build_adj():
    adj = {}
    for u, v, w in EDGES:
        adj.setdefault(u, {})[v] = w
        adj.setdefault(v, {})[u] = w
    return adj


def dijkstra(adj, src, dst, fn=None, fe=None):
    fn, fe = fn or set(), fe or set()
    dist, prev, pq = {src: 0}, {src: None}, [(0, src)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float('inf')):
            continue
        if u == dst:
            break

        for v, w in adj.get(u, {}).items():
            if v in fn or (u, v) in fe or (v, u) in fe:
                continue

            nd = d + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    if dst not in dist:
        return None, float('inf')

    path, cur = [], dst
    while cur is not None:
        path.append(cur)
        cur = prev[cur]

    return path[::-1], dist[dst]


def path_edges(path):
    return {(min(path[i], path[i+1]), max(path[i], path[i+1]))
            for i in range(len(path) - 1)}


def yen_link_disjoint(adj, src, dst, K=3):
    results = []
    forbidden_edges = set()

    for _ in range(K):
        path, cost = dijkstra(adj, src, dst, fe=forbidden_edges)
        if path is None:
            break

        results.append((path, cost))
        forbidden_edges |= path_edges(path)

    return results


# PLOT

def make_graph():
    G = nx.Graph()
    for n in NODES:
        G.add_node(n)
    for u, v, w in EDGES:
        G.add_edge(u, v, weight=w)
    return G


def plot_path(path, cost, rank, src, dst, total_paths, all_paths):
    G = make_graph()
    fig, ax = plt.subplots(figsize=(13, 8))
    fig.patch.set_facecolor("#262626")
    ax.set_facecolor("#262626")

    other_path_edges = set()
    for i, (p, _) in enumerate(all_paths):
        if i != rank:
            other_path_edges |= path_edges(p)

    cur_edges  = path_edges(path)
    path_edge_list = list(zip(path[:-1], path[1:]))

    other_edge_list = [(u, v) for u, v in G.edges()
                       if (min(u,v), max(u,v)) in other_path_edges
                       and (min(u,v), max(u,v)) not in cur_edges]

    used = cur_edges | other_path_edges
    non_path = [(u, v) for u, v in G.edges() 
                if (min(u,v), max(u,v)) not in used]

    col = COLORS[rank % len(COLORS)]

    nx.draw_networkx_edges(G, POS, edgelist= G.edges(), ax=ax, 
                           edge_color="#FFFFFF", width=1.3, alpha=0.35, style="solid")
    
    for i, (p, _) in enumerate(all_paths):
        if i == rank:
            continue
        oel = list(zip(p[:-1], p[1:]))
        nx.draw_networkx_edges(G, POS, edgelist=oel, ax=ax,
                               edge_color=COLORS[i % len(COLORS)],
                               width=7.0, alpha=0.35)

    nx.draw_networkx_edges(G, POS, edgelist=path_edge_list, ax=ax,
                           edge_color=col, width=7.0, alpha=1.0)

    nx.draw_networkx_nodes(G, POS, ax=ax, node_color="#111111",
                           node_size=820, edgecolors="#EEEEEE")

    nx.draw_networkx_labels(G, POS, ax=ax,
                           font_color="white")

    route = " -> ".join(str(n) for n in path)

    ax.set_title(
        f"Path {rank+1}  |  Node {src} → Node {dst}\n"
        f"Route: {route}   |   Cost: {cost}",
        color="white",
        fontsize=11,
        fontweight="bold",
        pad=12
    )

    legend_handles = [
        mpatches.Patch(color=col, label=f"Active Path {rank+1}"),
        mpatches.Patch(color="#444444", label="Unused edges"),
    ]

    for i, (p, c) in enumerate(all_paths):
        if i != rank:
            legend_handles.append(
                mpatches.Patch(
                    color=COLORS[i % len(COLORS)],
                    label=f"Path {i+1} (other)"
                )
            )

    ax.legend(
        handles=legend_handles,
        loc="lower left",
        fontsize=9,
        frameon=True,
        facecolor="#1A1A1A",
        edgecolor="#555555",
        labelcolor="white"
    )

    ax.axis("off")
    
    plt.tight_layout()
    plt.savefig(f"path_{rank+1}.png", dpi=150, facecolor=fig.get_facecolor())
    plt.show()
    plt.close()

    print(f"  Path {rank+1}  |  {route}  |  cost={cost:,}")


# OUTPUT FILE

def write_txt(adj, K=3, filename="ksp.txt"):
    with open(filename, "w") as f:
        for src in sorted(NODES.keys()):
            for dst in sorted(NODES.keys()):
                if src >= dst:
                    continue

                paths = yen_link_disjoint(adj, src, dst, K)
                f.write(f"{src} -> {dst}\n")

                if not paths:
                    f.write(" No path found.\n\n")
                else:
                    for i, (path, cost) in enumerate(paths):
                        f.write(f" Path {i+1}: {path} cost={cost}\n")
                    f.write("\n")


# MAIN

if __name__ == "__main__":
    adj = build_adj()

    print("\n\t\t Path Diagrams: Node 1 -> Node 14\n")
    paths = yen_link_disjoint(adj, SRC, DST, K)

    if not paths:
        print("No paths found.")
    else:
        for i, (path, cost) in enumerate(paths):
            plot_path(path, cost, i, SRC, DST, len(paths), paths)

    write_txt(adj, K)