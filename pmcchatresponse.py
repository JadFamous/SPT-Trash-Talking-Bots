import json

file_path = r'pmcchatresponse.json'

def update_value(data, key, new_value, message):
    if key in data:
        try:
            data[key] = new_value
            print(f"Update successful: {message}")
        except Exception as e:
            print(f"Update failed for {message}. Error: {e}")

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
update_value(data["victim"], "responseChancePercent", new_response_chance_percent_victim, "responseChancePercent for 'victim'")
update_value(data["victim"]["responseTypeWeights"], "positive", new_positive_weight_victim, "positive weight for 'victim'")
update_value(data["victim"]["responseTypeWeights"], "negative", new_negative_weight_victim, "negative weight for 'victim'")
update_value(data["victim"]["responseTypeWeights"], "plead", new_plead_weight_victim, "plead weight for 'victim'")
update_value(data["victim"], "stripCapitalisationChancePercent", new_strip_cap_chance_victim, "stripCapitalisationChancePercent for 'victim'")
update_value(data["victim"], "allCapsChancePercent", new_all_caps_chance_victim, "allCapsChancePercent for 'victim'")
update_value(data["victim"], "appendBroToMessageEndChancePercent", new_append_bro_chance_victim, "appendBroToMessageEndChancePercent for 'victim'")

# Update values for "killer"
update_value(data["killer"], "responseChancePercent", new_response_chance_percent_killer, "responseChancePercent for 'killer'")
update_value(data["killer"]["responseTypeWeights"], "positive", new_positive_weight_killer, "positive weight for 'killer'")
update_value(data["killer"]["responseTypeWeights"], "negative", new_negative_weight_killer, "negative weight for 'killer'")
update_value(data["killer"]["responseTypeWeights"], "plead", new_plead_weight_killer, "plead weight for 'killer'")
update_value(data["killer"], "stripCapitalisationChancePercent", new_strip_cap_chance_killer, "stripCapitalisationChancePercent for 'killer'")
update_value(data["killer"], "allCapsChancePercent", new_all_caps_chance_killer, "allCapsChancePercent for 'killer'")
update_value(data["killer"], "appendBroToMessageEndChancePercent", new_append_bro_chance_killer, "appendBroToMessageEndChancePercent for 'killer'")

# Save the modified data back to the JSON file
with open(file_path, 'w') as file:
    json.dump(data, file, indent=2)

print("All updates completed.")
