# 2025-09-16T22:08:51.138892300
import vitis

client = vitis.create_client()
client.set_workspace(path="Elevator-Project")

comp = client.create_hls_component(name = "hls_component",cfg_file = ["hls_config.cfg"],template = "empty_hls_component")

comp = client.get_component(name="hls_component")
comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

client.delete_component(name="hls_component")

client.delete_component(name="componentName")

client.delete_component(name="componentName")

client.delete_component(name="componentName")

comp = client.create_hls_component(name = "hls_component",cfg_file = ["hls_config.cfg"],template = "empty_hls_component")

comp.run(operation="C_SIMULATION")

client.delete_component(name="hls_component")

client.delete_component(name="componentName")

client.delete_component(name="componentName")

client.delete_component(name="componentName")

comp = client.create_hls_component(name = "hls_component",cfg_file = ["hls_config.cfg"],template = "empty_hls_component")

comp.run(operation="C_SIMULATION")

client.delete_component(name="hls_component")

client.delete_component(name="componentName")

client.delete_component(name="componentName")

client.delete_component(name="componentName")

comp = client.create_hls_component(name = "elevator_controller",cfg_file = ["hls_config.cfg"],template = "empty_hls_component")

comp = client.get_component(name="elevator_controller")
comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

client.delete_component(name="elevator_controller")

client.delete_component(name="componentName")

client.delete_component(name="componentName")

client.delete_component(name="componentName")

client.delete_component(name="componentName")

client.delete_component(name="componentName")

client.delete_component(name="componentName")

comp = client.create_hls_component(name = "elevator_controller",cfg_file = ["hls_config.cfg"],template = "empty_hls_component")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="C_SIMULATION")

comp.run(operation="SYNTHESIS")

vitis.dispose()

