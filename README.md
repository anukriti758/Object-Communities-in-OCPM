# Object-Communities-in-OCPM

# Object-to-Object (O2O) Relationship Discovery from OCEL using Graph-Based Analysis

This repository provides a complete pipeline for discovering and analyzing Object-to-Object (O2O) relationships from an Object-Centric Event Log (OCEL). The pipeline is divided into three main phases:

---

## 📌 Phase 1: Extracting Object Pairs and Their O2O Relationships

In this phase, we:

- Load the OCEL file using `pm4py`.
- Generate all combinations of object type pairs.
- For each object type pair:
  - Filter the OCEL to keep only those object types.
  - Count:
    - **Direct relationships** (from the `"relationships"` attribute in the OCEL).
    - **Event co-participation** relationships (two objects appearing in the same event).
- Save results into two lists: `relation` and `event_relation`.

### Key Output
A table of object type pairs and their corresponding relationship weights.

---

## 📌 Phase 2: Normalizing and Converting to Single Weighted Graph

This phase transforms raw relationship counts into a normalized graph:

- Normalize both `relation` and `event_relation` to the range [0, 1].
- Combine them into a single weighted graph using a tunable alpha (default `alpha = 0.5`).
  - `combined_weight = alpha * norm_relation + (1 - alpha) * norm_event_relation`
- Create and visualize a **NetworkX** graph with:
  - Edge thickness representing combined weights.
  - Node labels for object types.

### Key Output
A normalized and visually interpretable graph of object type relationships.

---

## 📌 Phase 3: Dynamic Thresholding Using Conductance-Based Community Detection

This final phase identifies clusters (strongly connected groups) of object types:

- A dynamic threshold is applied based on local max-weight edges.
- For each threshold from 0.01 to 0.99:
  - Build communities where edge weights exceed the local threshold.
  - Calculate **graph conductance** for each community.
  - Select the threshold with the **lowest average conductance**.
- Visualize and print:
  - The best threshold.
  - Conductance score.
  - Strongly connected communities.

### Key Output
A graph showing clustered object types with meaningful connections based on graph-theoretic metrics.

---

## 🛠 Requirements

Install the required libraries:

```bash
pip install pm4py
pip install -U ortools
