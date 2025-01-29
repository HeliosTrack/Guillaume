import meshtastic
import meshtastic.serial_interface
import meshtastic.mesh_interface
import meshtastic.version

# Print the version of the meshtastic distribution
print(f"Hi ! This software run on  : {meshtastic.version.version("meshtastic")} meshtastic version")

# Create an instance of MeshInterface
mesh_interface_instance = meshtastic.mesh_interface.meshtastic.serial_interface.SerialInterface()

print(mesh_interface_instance.getLongName())

print(mesh_interface_instance.showInfo())