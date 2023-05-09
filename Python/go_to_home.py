from pyniryo import *
from poses import *

# robot 1
robot1_ip_address = "169.254.200.201"  

# robot 0
robot0_ip_address = "169.254.200.200" 
robot0 = NiryoRobot(robot0_ip_address)
robot1 = NiryoRobot(robot1_ip_address)

if not (len(robot1.get_connected_conveyors_id()) == 0 ):
    print("Stopped conveyor 1")
    conveyor_id_1 = robot1.set_conveyor()
    robot1.stop_conveyor(conveyor_id_1)

if not (len(robot0.get_connected_conveyors_id()) == 0 ):
    print("Stopped conveyor 0")
    conveyor_id_0 = robot0.set_conveyor()
    robot0.stop_conveyor(conveyor_id_0)

robot1.move_to_home_pose()
robot0.move_to_home_pose()

robot0.close_connection()
robot1.close_connection()
