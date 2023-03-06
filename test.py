from pyniryo import *
from poses import *

robot_ip_address = "169.254.200.201"

# Connect to robot & calibrate
robot1 = NiryoRobot(robot_ip_address)
robot1.calibrate_auto()
# Move joints
#robot.move_joints(0.0, 0.151, -0.487, 0.047, 0.000, -0.129)
robot1.move_joints(storage_observer)
print(robot1.get_workspace_list())
obj_found, shape_ret, color_ret = robot1.vision_pick('STORAGE_1_WORKSPACE',
                                                    height_offset=0.0,
                                                    shape=ObjectShape.SQUARE,
                                                    color=ObjectColor.RED)
robot1.wait(3)

robot1.move_to_home_pose()
# Turn learning mode ON
robot1.set_learning_mode(True)
# Stop TCP connection
robot1.close_connection()