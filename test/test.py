# Iterate through all nodes in the mesh

import meshtastic
from meshtastic.serial_interface import SerialInterface

# Connect to the Meshtastic device
interface = SerialInterface()  # Automatically finds the device

for node_id, node in interface.nodes.items():
    user = node.get('user', {})
    position = node.get('position', {})

    long_name = user.get('longName', 'Unknown')
    short_name = user.get('shortName', 'Unknown')
    latitude = position.get('latitude', 'N/A')
    longitude = position.get('longitude', 'N/A')
    altitude = position.get('altitude', 'N/A')

    print(f"Node ID: {node_id}")
    print(f"Long Name: {long_name}")
    print(f"Short Name: {short_name}")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    print(f"Altitude: {altitude}")
    print("-" * 20)
