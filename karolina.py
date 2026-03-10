import pandas as pd
import json
import os # this is to check if a file exists or not

#df = pd.read_excel("Karolina_System.xlsx")
df = pd.read_excel("Racks.xlsx", sheet_name="karolina")

# extract the system info from first row
system_name = df.loc[0, 'System Name']
system_description = df.loc[0, 'System Description']

# starting positions
x_start = 0.0
y_start = 0.0
z_start = 0.0
x_spacing = 55.0

children = {}
for i, row in df.iterrows():
    rack_id = row['Rack ID']
    

    position = {
        "x": x_start,
        "y": y_start,
        "z": z_start + i * x_spacing
}
    children[rack_id]={
        
        "file": f"{rack_id}.json",
        "position_m": position
        
    }

# --- STEP 2: Prepare JSON structure ---
final_json = {
    "systemName": system_name,
    "systemDescription": system_description,
    "children": children
    
    
}

with open("output.json", "w") as f:
    json.dump(final_json, f, indent = 4)

print("json created")