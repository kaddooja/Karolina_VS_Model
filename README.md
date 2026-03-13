# Karolina Cluster JSON Generation

## Overview
This project automates the generation of a hierarchical JSON representation of the **Karolina cluster hardware layout** using Python. The system reads rack and component specifications from an Excel file and converts them into structured JSON files describing racks, chassis, compute nodes, switches, and cooling units.

---

# Workflow Summary

1. Read rack and component information from an Excel file.
2. Extract rack dimensions and adata.
3. Calculate chassis spacing and placement inside the rack.
4. Derive node dimensions from chassis dimensions.
5. Calculate node positions inside each chassis.
6. Generate JSON files for racks, chassis, nodes, and infrastructure components.
7. Maintain a hierarchical structure:
   
System
└── Rack
└── Chassis
└── Nodes / Switches / Cooling Units

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
---
Racks are positioned in 3D space using a constant spacing value.
Each rack position is calculated as:
z_position = z_start + rack_index * x_spacing
---
This ensures that racks are evenly spaced along the **z-axis**.

# Rack-Level JSON Generation

The second script reads the Rack1 sheet and generates a detailed rack structure.
Rack Properties
The rack JSON contains:
   -Rack name
   -Description
   -Type
   -Dimensions
### Chassis Dimension Calculation
The rack height is divided equally among all chassis inside the rack
chassis_height = rack_height / number_of_chassis
This ensures that all chassis fit perfectly within the rack without overlapping.
Vertical Spacing
y_spacing = chassis_height
Starting Position

The coordinate system assumes the center of the rack as origin.

start_y = -rack_height / 2 + chassis_height / 2

Each chassis position is calculated using:

y_position = start_y + index * y_spacing

This stacks chassis from bottom to top inside the rack.
Chassis JSON Structure
Each chassis contains references to its internal components.
### Node Dimension Calculation
Nodes are placed inside each chassis.
Their dimensions are derived from the rack and chassis dimensions.
node_width  = rack_width
node_height = chassis_height / 2
node_depth  = rack_depth / 2
This allows nodes to fit correctly within the chassis.
### Node Layout Inside Chassis
Nodes are arranged in a 2 × 2 grid inside the chassis.
### Switch Layout
Switches are placed inside the chassis vertically.
### Switch Height
switch_height = chassis_height / 2
Switch Positions
Switch1 → y = -switch_height / 2
Switch2 → y =  switch_height / 2

This allows stacking of two switches inside the chassis.

### Generated Output Files

Running the scripts generates the following JSON files:
output.json
Rack1.1.json
Chassis1.1.json
Node.json
Switch.json
switch_dim.json
CDU.json
IBL.json
