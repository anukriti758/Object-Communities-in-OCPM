from extract_o2o_relations import load_ocel, get_object_type_pairs, compute_o2o_relations
from build_weighted_graph import convert_to_single_graph, print_combined_edge_table
from community_detection import find_best_threshold, plot_graph_with_clusters

# Load and prepare
ocel = load_ocel("./drive/MyDrive/order-management.json")
obj_pairs = get_object_type_pairs(ocel)
relation, event_relation = compute_o2o_relations(ocel, obj_pairs)

# Build combined weighted graph
single_graph = convert_to_single_graph(obj_pairs, relation, event_relation, alpha=0.5)
print_combined_edge_table(single_graph)

# Detect strong object communities
best_t, best_c, best_communities = find_best_threshold(single_graph)
print(f"\nBest Threshold: {best_t:.2f}, Best Conductance: {best_c:.4f}")
for i, comm in enumerate(best_communities): print(f"Group {i+1}: {comm}")

# Plot
plot_graph_with_clusters(single_graph, best_communities)
