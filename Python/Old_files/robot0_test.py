from pyniryo import *
from Python.Old_files.poses import *

#Constants

robot0_ip_address = "169.254.200.200"

z_offset_height = 0.002


# Connect to robot & calibrate
robot0 = NiryoRobot(robot0_ip_address)
robot0.calibrate_auto()
# Move joints
robot0.get_connected_conveyors_id()
conveyor_id_1 = robot0.set_conveyor()

# -- Setting variables
sensor_pin_id = PinID.DI5

# Run conveyor and wait until the IR sensor detects an object
robot0.run_conveyor(conveyor_id_1)
robot0.stop_conveyor(conveyor_id_1)
while robot0.digital_read(sensor_pin_id) == PinState.HIGH:
    robot0.wait(0.1)

#conveyor_id = robot0.set_conveyor()
#robot0.get_connected_conveyors_id()
##robot0.run_conveyor(conveyor_id,speed=50, direction=ConveyorDirection.FORWARD)
#robot0.control_conveyor(conveyor_id, True, 50, ConveyorDirection.FORWARD)
#print(robot0.get_saved_trajectory_list())
#print(robot0.get_saved_pose_list()[0])
#robot0.wait(10)
robot0.stop_conveyor(conveyor_id_1)
#robot0.move_joints(position_con1_pickup_robot0)
#robot0.grasp_with_tool()
#robot0.execute_registered_trajectory('con1_to_unload')
#robot0.move_joints(position_unload_robot0)
#robot0.release_with_tool()
#robot0.execute_registered_trajectory('unload_to_con1')

#robot0.move_joints()

robot0.move_to_home_pose()
# Stop TCP connection
robot0.close_connection()