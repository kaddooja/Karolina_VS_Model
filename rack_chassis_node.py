import pandas as pd
import json

# ------------------- READ EXCEL -------------------
df = pd.read_excel("Racks.xlsx", sheet_name="Rack1")

# ---- Rack info ----
rack_name = df.loc[0, "Name"]
rack_desc = df.loc[0, "description"]
rack_width = df.loc[0, "Width (m)"]
rack_height = df.loc[0, "Height (m)"]
rack_depth = df.loc[0, "Depth (m)"]

# ------------------- CHASSIS SETUP -------------------
num_chassis = df["Chassis ID"].dropna().shape[0]
chassis_height = rack_height / num_chassis
y_spacing = chassis_height
start_y = -rack_height / 2 + chassis_height / 2

# Node layout inside chassis (2x2)

node_cols = 2
node_rows = 2
node_width = rack_width / node_cols
node_depth = rack_depth / node_rows
node_height = chassis_height / node_rows  # divide height if stacking

# ------------------- CREATE NODE.JSON -------------------
node_data = {
    "name": "NodeA",
    "description": "NodeA",
    "properties": {
        "type": "compute node",
        "dimensions_m": {
            "width": node_width,
            "height": node_height,
            "depth": node_depth
        }
    }
    
}

with open("Node.json", "w") as f:
    json.dump(node_data, f, indent=4)

print("Node.json generated")

# ------------------- CREATE CHASSIS.JSON -------------------
node_children = {}

for row in range(node_rows):
    for col in range(node_cols):
        node_name = f"Node{row*node_cols + col +1}"
        # x along width, y along chassis height, z along depth
        x = -rack_width/2 + node_width/2 + col * node_width
        y = -chassis_height/2 + node_height/2 + row * node_height
        z = 0  # front/back center
        node_children[node_name] = {
            "file": "Node.json",
            "position_m": {"x": x, "y": y, "z": z}
        }

chassis_json = {
    "name": "Chassis",
    "properties": {
        "type": "Chassis",
        "dimensions_m": {
            "width": rack_width,
            "height": chassis_height,
            "depth": rack_depth
        }
    },
    "children": node_children
}

with open("Chassis1.1.json", "w") as f:
    json.dump(chassis_json, f, indent=4)

print("Chassis.json generated")

# ------------------- CREATE RACK.JSON -------------------
rack_children = {}
current_index = 0
for _, row in df.iterrows():
    chassis_id = row.get("Chassis ID")
    if pd.notna(chassis_id):
        y_pos = start_y + current_index * y_spacing
        rack_children[chassis_id] = {
            "file": "Chassis.json",
            "position_m": {"x": 0, "y": y_pos, "z": 0}
        }
        current_index += 1

rack_json = {
    "name": rack_name,
    "description": rack_desc,
    "properties": {
        "type": "Rack",
        "dimensions_m": {
            "width": rack_width,
            "height": rack_height,
            "depth": rack_depth
        }
    },
    "children": rack_children
}

with open("Rack1.1.json", "w") as f:
    json.dump(rack_json, f, indent=4)

print("Rack.json generated")