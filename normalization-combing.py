"""
build_weighted_graph.py

This module normalizes object pair weights (from structural and event-based metrics)
and combines them into a unified weighted graph for analysis.
"""

import networkx as nx
import numpy as np

def normalize_weights(weights):
    min_w, max_w = min(weights), max(weights)
    return [(w - min_w) / (max_w - min_w) if max_w != min_w else 0 for w in weights]

def convert_to_single_graph(obj_pairs, relation, event_relation, alpha=0.5):
    norm_rel = normalize_weights(relation)
    norm_ev_rel = normalize_weights(event_relation)

    G = nx.Graph()
    for i, (v1, v2) in enumerate(obj_pairs):
        w1, w2 = norm_rel[i], norm_ev_rel[i]
        combined = alpha * w1 + (1 - alpha) * w2
        if combined > 0:
            G.add_edge(v1, v2, weight=combined, norm_relation=w1, norm_event_relation=w2)
    return G

def print_combined_edge_table(G):
    print(f"{'V1':<5} {'V2':<5} {'Norm Relation':<15} {'Norm Event Relation':<20} {'Combined Weight':<15}")
    print("-" * 70)
    for u, v, data in G.edges(data=True):
        print(f"{u:<5} {v:<5} {data['norm_relation']:.2f}          {data['norm_event_relation']:.2f}                {data['weight']:.2f}")
