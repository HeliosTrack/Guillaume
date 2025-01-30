import meshtastic
import meshtastic.serial_interface
import meshtastic.mesh_interface
import meshtastic.version
import meshtastic.remote_hardware

# Print the version of the meshtastic distribution
print(f"Hi ! This software run on  : {meshtastic.version.version('meshtastic')} meshtastic version")

# Create an instance of MeshInterface
mesh_interface_instance = meshtastic.mesh_interface.meshtastic.serial_interface.SerialInterface()

print(mesh_interface_instance.showInfo())

# Create an instance of RemoteHardwareClient
remote_hardware_instance = RemoteHardwareClient()

node_info = mesh_interface_instance.getMyNodeInfo()
nodeid = node_info["user"]["id"]  # Extract the actual node ID
mask = 0x76  # Mask for IO16 and IO17

print(remote_hardware_instance.readGPIOs(nodeid=nodeid, mask=mask))