import meshtastic
import meshtastic.serial_interface
from meshtastic import BROADCAST_NUM
import time

def main():
    interface = meshtastic.serial_interface.SerialInterface()
    
    # On attend que l'interface soit connectée et que le nodedb soit disponible
    while not interface.nodes:
        print("En attente des nœuds...")
        time.sleep(1)

    # Supposons que node_id soit la destination souhaitée (exemple : "!435a7150")
    node_id = "!435a7150"
    print(f"Demande de télémétrie pour le nœud {node_id}...")
    
    
    print(interface.sendTelemetry(destinationId=node_id, wantResponse=True, telemetryType="environment_metrics"))

    print("En attente de la réponse de télémétrie...")
    time.sleep(10)
    
    interface.close()

if __name__ == '__main__':
    main()
