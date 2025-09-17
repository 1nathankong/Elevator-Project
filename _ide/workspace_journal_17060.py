# 2025-09-17T07:41:09.171072800
import vitis

client = vitis.create_client()
client.set_workspace(path="Elevator-Project")

comp = client.get_component(name="elevator_controller")
comp.run(operation="C_SIMULATION")

comp.run(operation="SYNTHESIS")

comp.run(operation="C_SIMULATION")

comp.run(operation="SYNTHESIS")

comp.run(operation="CO_SIMULATION")

comp.run(operation="C_SIMULATION")

