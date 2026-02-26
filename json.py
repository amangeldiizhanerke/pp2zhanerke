import json 
#open the JSON file and load its content
with open("sample-data.json", "r") as f:
    data = json.load(f)

# print table header
print("Interface Status")
print("=" * 80)
print(f"{'DN':<55} {'Description'}")
print("-" * 80)

#loop through each item inside "imdata"
for item in data["imdata"]:
    
    #access nested dictionary: l1PhysIf → attributes
    attributes = item["l1PhysIf"]["attributes"]

    #get DN and description values
    #.get() prevents error if key is missing
    dn = attributes.get("dn", "")
    descr = attributes.get("descr", "")

    #print formatted output
    print(f"{dn:<55} {descr}")