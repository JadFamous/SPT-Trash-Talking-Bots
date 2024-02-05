import json

file_path = r'pmcchatresponse.json'

# Get user inputs for the desired values for "victim"
new_response_chance_percent_victim = int(input("Enter the new responseChancePercent value for 'victim': "))
new_positive_weight_victim = int(input("Enter the new positive weight for 'victim': "))
new_negative_weight_victim = int(input("Enter the new negative weight for 'victim': "))
new_plead_weight_victim = int(input("Enter the new plead weight for 'victim': "))
new_strip_cap_chance_victim = int(input("Enter the new stripCapitalisationChancePercent for 'victim': "))
new_all_caps_chance_victim = int(input("Enter the new allCapsChancePercent for 'victim': "))
new_append_bro_chance_victim = int(input("Enter the new appendBroToMessageEndChancePercent for 'victim': "))

# Get user inputs for the desired values for "killer"
new_response_chance_percent_killer = int(input("Enter the new responseChancePercent value for 'killer': "))
new_positive_weight_killer = int(input("Enter the new positive weight for 'killer': "))
new_negative_weight_killer = int(input("Enter the new negative weight for 'killer': "))
new_plead_weight_killer = int(input("Enter the new plead weight for 'killer': "))
new_strip_cap_chance_killer = int(input("Enter the new stripCapitalisationChancePercent for 'killer': "))
new_all_caps_chance_killer = int(input("Enter the new allCapsChancePercent for 'killer': "))
new_append_bro_chance_killer = int(input("Enter the new appendBroToMessageEndChancePercent for 'killer': "))

# Load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Update values for "victim"
if "victim" in data:
    data["victim"]["responseChancePercent"] = new_response_chance_percent_victim
    data["victim"]["responseTypeWeights"]["positive"] = new_positive_weight_victim
    data["victim"]["responseTypeWeights"]["negative"] = new_negative_weight_victim
    data["victim"]["responseTypeWeights"]["plead"] = new_plead_weight_victim
    data["victim"]["stripCapitalisationChancePercent"] = new_strip_cap_chance_victim
    data["victim"]["allCapsChancePercent"] = new_all_caps_chance_victim
    data["victim"]["appendBroToMessageEndChancePercent"] = new_append_bro_chance_victim

# Update values for "killer"
if "killer" in data:
    data["killer"]["responseChancePercent"] = new_response_chance_percent_killer
    data["killer"]["responseTypeWeights"]["positive"] = new_positive_weight_killer
    data["killer"]["responseTypeWeights"]["negative"] = new_negative_weight_killer
    data["killer"]["responseTypeWeights"]["plead"] = new_plead_weight_killer
    data["killer"]["stripCapitalisationChancePercent"] = new_strip_cap_chance_killer
    data["killer"]["allCapsChancePercent"] = new_all_caps_chance_killer
    data["killer"]["appendBroToMessageEndChancePercent"] = new_append_bro_chance_killer

# Save the modified data back to the JSON file
with open(file_path, 'w') as file:
    json.dump(data, file, indent=2)

print("Update successful.")
