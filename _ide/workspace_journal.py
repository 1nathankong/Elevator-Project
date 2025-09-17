# 2025-09-17T08:34:12.172666200
import vitis

client = vitis.create_client()
client.set_workspace(path="Elevator-Project")

comp = client.create_hls_component(name = "elevator_hls_test",cfg_file = ["hls_config.cfg"],template = "empty_hls_component")

comp = client.get_component(name="elevator_hls_test")
comp.run(operation="C_SIMULATION")

