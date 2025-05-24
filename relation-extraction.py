"""
extract_o2o_relations.py

This module extracts pairwise object types from an OCEL log and computes their 
direct relationships and event-based co-participation counts (Object-to-Object relations).
"""

import pm4py
import inflect
import itertools
import json

# Read OCEL log
def load_ocel(filepath):
    return pm4py.read_ocel2_json(filepath)

# Generate all unique object type pairs
def get_object_type_pairs(ocel):
    all_obj = ocel.objects["ocel:type"].unique()
    return [list(pair) for pair in itertools.combinations(all_obj, 2)]

# Compute O2O relationships and co-participation counts
def compute_o2o_relations(ocel, obj_pairs, output_path="filtered_ocel.jsonocel"):
    p = inflect.engine()
    relation, event_relation = [], []

    for pair in obj_pairs:
        filtered_ocel = pm4py.filtering.filter_ocel_object_types(ocel, pair)
        pm4py.write.write_ocel2_json(filtered_ocel, output_path)

        with open(output_path, 'r') as file:
            data = json.load(file)

        omap = {obj["id"]: obj["type"] for obj in data.get("objects", [])}
        rel_count = sum(len(obj.get("relationships", [])) for obj in data["objects"])

        ev_rel_count = 0
        for event in data["events"]:
            num_A = sum(1 for r in event["relationships"] if omap[r["objectId"]] == pair[0])
            num_B = sum(1 for r in event["relationships"] if omap[r["objectId"]] == pair[1])
            ev_rel_count += num_A * num_B

        relation.append(rel_count)
        event_relation.append(ev_rel_count)
        print(f"{pair}, {rel_count}, {ev_rel_count}")

    return relation, event_relation
