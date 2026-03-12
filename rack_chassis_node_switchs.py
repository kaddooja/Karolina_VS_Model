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

# Node layout inside chassis (2x2 grid)

node_width = rack_width
node_depth = rack_depth / 2
node_height = chassis_height / 2
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
node_positions = {
    "Node1": (0, -node_height/2, -node_depth/2),
    "Node2": (0, -node_height/2,  node_depth/2),
    "Node3": (0,  node_height/2, -node_depth/2),
    "Node4": (0,  node_height/2,  node_depth/2)
}

for node, pos in node_positions.items():

    x, y, z = pos

    node_children[node] = {
        "file": "Node.json",
        "position_m": {
            "x": x,
            "y": y,
            "z": z
        }
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
current_index = 23

for _, row in df.iterrows():
    chassis_id = row.get("Chassis ID")
    chassis_type = row.get("Chassis Type")  # Column in Excel that tells type, e.g., CN, CDU

    if pd.notna(chassis_id):

        # Compute vertical position in rack
        y_pos = start_y + current_index * y_spacing

        # Choose file based on chassis type
        if chassis_type == "CN":
            file_name = "Chassis.json"
        elif pd.notna(chassis_type):
            # For other types, assume a JSON file with the type name, e.g., "CDU.json"
            file_name = f"{chassis_type}.json"
        else:
            # Default fallback
            file_name = "Chassis.json"

        rack_children[chassis_id] = {
            "file": file_name,
            "position_m": {"x": 0, "y": y_pos, "z": 0}
        }

        current_index -= 1

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

# ------------------- CREATE CDU.JSON -------------------
CDU_json = {
    "name": "CDU",
    "description": "Chassis_type",
    "properties": {
        "type": "Cooling",
        "dimensions_m": {
            "width": rack_width,
            "height": chassis_height,
            "depth": rack_depth
        }
    }
    
}
with open("CDU.json", "w") as f:
    json.dump(CDU_json, f, indent=4)
print("CDU.json generated")

# ------------------- CREATE switch.JSON -------------------
switch_json = {
    "name": "switch",
    "description": "Chassis_type",
    "properties": {
        "type": "switch",
        "dimensions_m": {
            "width": rack_width,
            "height": chassis_height,
            "depth": rack_depth
        }
    },
    
}
with open("Switch.json", "w") as f:
    json.dump(switch_json, f, indent=4)
print("Switch.json generated")

# ------------------- CREATE switch.JSON -------------------
IBL_json = {
    "name": "IBL",
    "description": "Chassis_type",
    "properties": {
        "type": "Cooling",
        "dimensions_m": {
            "width": rack_width,
            "height": chassis_height,
            "depth": rack_depth
        }
    }
    
}
with open("IBL.json", "w") as f:
    json.dump(IBL_json, f, indent=4)
print("IBL.json generated")
