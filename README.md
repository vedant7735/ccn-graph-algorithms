# Graph Algorithms on Network Topologies

## Overview
This project implements two fundamental graph algorithms on mesh network topologies using Python and NetworkX:

1. Link-Disjoint K-Shortest Paths (NSFNET topology)
2. Minimum Spanning Tree using Kruskal’s Algorithm

---

## Problem Statement

1. Design a K-shortest path algorithm for a mesh network:
   - Input: Network graph (NSFNET topology)
   - Output: K shortest link-disjoint paths for every node pair
   - Store results in a text file

2. Design a Minimum Spanning Tree (MST):
   - Input: Weighted mesh network (≥ 7 nodes)
   - Output: MST edges, weights, and total cost

---

## Approach

### 1. K-Shortest Paths (Link-Disjoint)
- Based on Yen’s Algorithm
- Modified to enforce link-disjointness
- Uses Dijkstra’s algorithm for shortest path computation
- Outputs all valid paths and their costs to a text file

### 2. Minimum Spanning Tree
- Implemented using Kruskal’s Algorithm
- Uses Union-Find (Disjoint Set)
- Greedy selection of edges based on weight
- Avoids cycles while building MST

---

## Project Structure

- `algorithm1/kshortestpath` → K-shortest path implementation (NSFNET)
- `algorithm2/minimum_spanning_tree` → MST implementation (Kruskal)
- `algorithm1/ksp.txt` → Output file (k-shortest-path)
- `algorithm2/mst_process.txt` → Output file (mst)

---

## Tools & Technologies

- Python 3.11
- NetworkX
- Matplotlib

---

## Output

- Text files containing:
  - K-shortest paths for all node pairs
  - MST edges and total cost
- Graph visualizations of:
  - NSFNET topology with paths
  - MST highlighted over original graph

---

## Notes

- K-shortest paths are strictly link-disjoint
- NSFNET topology is used as a standard reference network
- MST ensures minimum total edge weight while connecting all nodes

---

## Reference

This repository is linked in the project report for accessing full outputs and implementation details.
