from pyniryo import *
from poses import *

#Constants

robot1_ip_address = "169.254.200.201"
robot0_ip_address = "169.254.200.200"

z_offset_height = 0.002


# Connect to robot & calibrate
robot1 = NiryoRobot(robot1_ip_address)
robot1.calibrate_auto()
# Move joints
#robot.move_joints(0.0, 0.151, -0.487, 0.047, 0.000, -0.129)
robot1.move_joints(position_storage_observer_robot1)
robot1.wait(3)
print(robot1.get_workspace_list())
obj_found, shape_ret, color_ret = robot1.vision_pick('STORAGE_1_WORKSPACE',
                                                    height_offset=0.0,
                                                    shape=ObjectShape.CIRCLE,
                                                    color=ObjectColor.RED)

robot1.move_joints(position_over_con1_robot1)
robot1.release_with_tool()
robot1.grasp_with_tool()
#start conveyer belt 1
conveyor_id_1 = robot1.set_conveyor()
robot1.run_conveyor(conveyor_id_1, speed=100, direction=ConveyorDirection.FORWARD)

robot1.wait(7.5)
robot1.stop_conveyor(conveyor_id_1)


robot1.move_to_home_pose()
# Stop TCP connection
robot1.close_connection()