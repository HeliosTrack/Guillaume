import meshtastic
import meshtastic.serial_interface


def on_receive(packet, interface):
    print("Packet reçu :", packet)

interface = meshtastic.serial_interface.SerialInterface()
interface.onReceive = on_receive

input("Appuyez sur Entrée pour quitter...\n")  # Garde le script en écoute
interface.close()
