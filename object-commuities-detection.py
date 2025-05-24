"""
community_detection.py

This module identifies strongly connected object communities using a dynamic 
thresholding mechanism based on conductance to find the most meaningful structure.
"""

import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.cuts import conductance

def find_strongly_connected_groups(G, threshold):
    communities, visited = [], set()

    def neighbors_above_threshold(node):
        neighbors = []
        node_threshold = threshold * max([G[node][n]['weight'] for n in G.neighbors(node)])
        for neighbor in G.neighbors(node):
            edge_w = G[node][neighbor]['weight']
            neighbor_thresh = threshold * max([G[neighbor][n]['weight'] for n in G.neighbors(neighbor)])
            if edge_w >= node_threshold and edge_w >= neighbor_thresh:
                neighbors.append(neighbor)
        return neighbors

    for node in G.nodes():
        if node not in visited:
            community = {node}
            stack = [node]
            visited.add(node)
            while stack:
                current = stack.pop()
                for neighbor in neighbors_above_threshold(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        community.add(neighbor)
                        stack.append(neighbor)
            communities.append(list(community))
    return communities

def find_best_threshold(G, min_t=0.01, max_t=0.99, step=0.01):
    best_t, best_cond, best_comms = None, float('inf'), []
    for t in np.arange(min_t, max_t + step, step):
        comms = find_strongly_connected_groups(G, t)
        conds = []
        for c in comms:
            if len(c) > 1:
                try:
                    conds.append(conductance(G, set(c)))
                except:
                    continue
        if conds:
            avg = np.mean(conds)
            if avg < best_cond:
                best_t, best_cond, best_comms = t, avg, comms
    return best_t, best_cond, best_comms

def plot_graph_with_clusters(G, communities):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
    color_map = {node: colors[i % len(colors)] for i, group in enumerate(communities) for node in group}

    nx.draw_networkx_nodes(G, pos, node_size=500, node_color=[color_map[n] for n in G.nodes()])
    edge_weights = [data['weight'] * 5 for _, _, data in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, width=edge_weights, edge_color='purple', alpha=0.7)
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}, font_size=10)
    plt.title("Strong Object Communities Based on Dynamic Threshold")
    plt.show()
