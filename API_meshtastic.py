import meshtastic
import meshtastic.serial_interface
from meshtastic import BROADCAST_NUM
import time
import sys
import io
import json

interface = meshtastic.serial_interface.SerialInterface()

def get_temp_humidity_pression(node_id):

    print(f"Demande de télémétrie pour le nœud {node_id}...")

    data = dict(interface.sendTelemetry(destinationId=node_id, wantResponse=True, telemetryType="environment_metrics", channelIndex=0))
    print(data)
    return [data["time"], data['environmentMetrics']['temperature'], data['environmentMetrics']['relativeHumidity'], data['environmentMetrics']['barometricPressure']]



def get_device(debug=False):
    nodes = interface.nodes
    for node_id, node_info in nodes.items():
        if debug:
            print(f"Node ID: {node_id}")
            print(json.dumps(node_info, indent=2))
            print("-" * 40)
    return nodes


def close_interface(): interface.close()
