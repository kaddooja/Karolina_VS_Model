# Karolina Cluster JSON Generation

## Overview
This project automates the generation of a hierarchical JSON representation of the **Karolina cluster hardware layout** using Python. The system reads rack and component specifications from an Excel file and converts them into structured JSON files describing racks, chassis, compute nodes, switches, and cooling units.

The goal is to create a **machine-readable layout of the cluster** that can be used for visualization, system modeling, infrastructure management, or simulation.

---

# Workflow Summary

1. Read rack and component information from an Excel file.
2. Extract rack dimensions and metadata.
3. Calculate chassis spacing and placement inside the rack.
4. Derive node dimensions from chassis dimensions.
5. Calculate node positions inside each chassis.
6. Generate JSON files for racks, chassis, nodes, and infrastructure components.
7. Maintain a hierarchical structure:
   
---

# Input Data

The script reads the Excel file:

### Sheets Used
- `karolina` → System level rack information
- `Rack1` → Detailed rack structure

### Extracted Data
From the Excel file the script reads:

- System name
- System description
- Rack ID
- Rack dimensions:
  - Width
  - Height
  - Depth
- Chassis IDs
- Chassis types (CN, CDU, Switch, etc.)

Each row represents a component inside the rack.

---

# System-Level JSON Generation

The first script reads the **cluster sheet** and generates a system-level JSON describing rack placement.

### Rack Placement Logic

Racks are positioned in 3D space using a constant spacing value.

