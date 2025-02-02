import meshtastic
import meshtastic.serial_interface
from meshtastic import BROADCAST_NUM
import time
import sys
import io
import json

interface = meshtastic.serial_interface.SerialInterface()

def get_temp_humidity_pression(node_id):
    """Send a telemetry request of environement to a node and return the response.
    But it's shady because the response is printed in the console and not returned.
    So I have to capture the output of the console and return it... I know it's not clean but it works. #TODO: Never fix this.
    """
    

    while not interface.nodes:
        print("En attente des nœuds...")
        time.sleep(1)

    
    print(f"Demande de télémétrie pour le nœud {node_id}...")

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    interface.sendTelemetry(destinationId=node_id, wantResponse=True, telemetryType="environment_metrics", channelIndex=0)
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout

    
    
    print("Captured Output:", output)
    return {"temp": output[55:60], "humidity": output[81:89], "pression": output[112:121]}
# interface.sendText("Test message", destinationId="!435a7150")


nodes = interface.nodes  # Il s'agit d'un dictionnaire : clés = identifiants des nœuds, valeurs = infos associées

# Affichage formaté de chaque nœud
for node_id, node_info in nodes.items():
    print(f"Node ID: {node_id}")
    print(json.dumps(node_info, indent=2))
    print("-" * 40)
    print(get_temp_humidity_pression(str(node_id)))
    print("-" * 40)

interface.close()