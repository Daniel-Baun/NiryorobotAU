import os
import sys
import math
import copy
import random
import time
import yaml
from threading import Lock, Thread
from pyniryo import *
from poses import *

#setup
workspace_storage = 'STORAGE_WS'
conf_file_name = "saved_joints_poses.yaml"

# robot 1
robot1_ip_address = "169.254.200.201"  

# robot 2
robot0_ip_address = "169.254.200.200"  

# define the height offset of the workspace used by the vision pick method
z_offset = 0.002
sleep_joints = [0.0, 0.55, -1.2, 0.0, 0.0, 0.0]
brightness_level = 1.5  # value between 0.5 and 2 to determine how bright the camera vision is
contrast_level = 0.8 #vaule of the contrast in the camera

# conveyor
conveyor_id = ConveyorID.ID_1  # define the id of the conveyor connected to the front Ned
conveyor_speed = 50  # speed of the conveyor between 0 and 100
conveyor_place_interval = 1.5  # minimal interval between conveyor places  (in seconds)

class RobotsMains:
    def __init__(self, robot1, robot0, workspace, saved_joints_poses):
        self.saved_joints_poses = saved_joints_poses

        self.client1 = robot1
        self.client2 = robot0

        self.client1.set_brightness(brightness_level)

        self.conveyor_lock = Lock()

        self.workspace = workspace
        self.conveyor_id = conveyor_id
        self.conveyor_move_time = 0

    def conveyor_controller(self, speed: int):
        self.client1.control_conveyor(conveyor_id, True, speed, ConveyorDirection.FORWARD)
        
    # starting a thread of each robot
    def run(self):
        self.conveyor_id = self.client1.set_conveyor()

        robot1_thread = Robot1(self.client1, self, self.workspace)
        robot0_thread = Robot0(self.client2, self)
        robot1_thread.start()
        robot0_thread.start()

# this class correpond to a robot, this class is run on a separate thread
# and permit multiple robots to move simultaneously
class RobotLoop(Thread):
    def __init__(self, client, parent):
        self.parent = parent
        self.saved_joints_poses = self.parent.saved_joints_poses
        self.client = client
        self.conveyor_lock = self.parent.conveyor_lock
        Thread.__init__(self)  # init this class has a thread

    def run(self):
        self.client.move_joints(*sleep_joints)
        self.robot_loop()

    def robot_loop(self):
        pass
    def stop_robot(self):
        pass

    

class Robot1(RobotLoop):
    def __init__(self, client, parent, workspace):
        super().__init__(client, parent)

        self.workspace = workspace

    def robot_loop(self):
        #Robot1 needs to start connected conveyor belt and starts to look after possible pickups
        print("Robot1 loop start")
        self.client.update_tool()
        self.client.release_with_tool()
        self.client.move_joints(*self.saved_joints_poses["client1_observation_pose"])
        while True:
            while True:
                obj_found, *_ = self.client.vision_pick(workspace_storage, z_offset, shape=ObjectShape.ANY,
                                                        color=ObjectColor.ANY)
                if obj_found:
                    break
                self.client.wait(2)

            print("Robot1 | going over Conveyor ")
            self.client.move_joints(*self.saved_joints_poses["client1_intermediate_pos"])
            print("Robot1 | dropping pawn ")
            self.client.move_joints(*self.saved_joints_poses["drop_positions_of_client1"])  # drop
            self.client.release_with_tool()
            print("locked robot1 ", {self.conveyor_lock.locked()})    
            self.conveyor_lock.acquire() # locks use of conveyorbelt for others
            print("is locked robot1 ", {self.conveyor_lock.locked()})

            self.parent.conveyor_controller(100) # start conveyor belt

            self.conveyor_lock.release() # unlocks use of conveyor for others
            print("unlocked robot1 ", {self.conveyor_lock.locked()})
            self.client.wait(8)    
            self.client.move_joints(*self.saved_joints_poses["client1_observation_pose"])

            self.client.wait(0.2)
    
    def wait_obj(self): # old
        self.client.move_joints(*self.saved_joints_poses["client1_observation_pose"])  # observation
        obj_found, pos, shape, color = self.client.detect_object(workspace_storage, shape=ObjectShape.ANY,
                                                                 color=ObjectColor.ANY)
        if obj_found and pos[0] < 0.90:
            return

class Robot0(RobotLoop):
    def __init__(self, client, parent):
        super().__init__(client, parent)



    def robot_loop(self):
    
        print("Back Ned loop start")
        self.client.update_tool()
        self.client.release_with_tool()
        sensor_pin_id = PinID.DI5
        while True:
            while self.client.digital_read(sensor_pin_id) == PinState.HIGH:
                self.client.wait(0.2)
            print("locked robot0 ", {self.conveyor_lock.locked()})    
            self.conveyor_lock.acquire()
            print("is locked robot0 ", {self.conveyor_lock.locked()})
            self.parent.conveyor_controller(0)
            self.client.move_joints(*self.saved_joints_poses["pick_positions_of_client2"])
            self.client.grasp_with_tool()
            self.client.move_joints(self.saved_joints_poses["client2_intermediate_pos"])
            self.client.move_joints(self.saved_joints_poses["drop_positions_of_client2"])
            self.client.release_with_tool()

            self.conveyor_lock.release()
            print("unlocked robot0 ", {self.conveyor_lock.locked()})    
            self.client.wait(0.2)
            self.client.move_joints(self.saved_joints_poses["client2_intermediate_pos"])
        #self.client.move_joints(*self.saved_joints_poses["client0_observation_pose"])
        

        
        #
        #while True:
        #    self.client.move_joints(*self.saved_joints_poses["pick_positions_of_client2"])  # observation
        #    obj_found, pos, shape, color = self.client.detect_object(workspace_storage, shape=ObjectShape.ANY,
        #                                                         color=ObjectColor.ANY)
        #    if obj_found and pos[0] < 0.90:
        #        self.client.control_conveyor(self.parent.conveyor_id, False, 0, ConveyorDirection.FORWARD)
        #        self.client.move_joints(*self.saved_joints_poses["pick_positions_of_client2"])  # grab
        #        self.client.grasp_with_tool()
        #        self.client.move_joints(*self.saved_joints_poses["client2_intermediate_pos"])
        #        self.client.move_joints(*self.saved_joints_poses["drop_positions_of_client2"])
        #        self.client.release_with_tool()


# - Initialize positions
def ask_position():
    joints_pose_dict = {}

    client1.move_joints(*sleep_joints)
    client2.move_joints(*sleep_joints)
    client1.set_learning_mode(True)
    client2.set_learning_mode(True)

    # the text displayed for each ask
    questions = ["ROBOT1 | Set the observation pose so the 4 landmarks are detected",
                 "ROBOT1 | A position of a few centimeters above the slope (at the top of the slope) ...",
                 "ROBOT1 | The position from which Ned can drop the pawn on the slope ...",
                 "ROBOT0 | The position from which Ned can grab the pawn at the bottom of the slope ...",
                 "ROBOT0 | A position a few centimeters above the previous position ...",
                 "ROBOT0 | A position at the back of the Conveyor Belt where Ned can drop the pawn ..."]

    # name of the position (cannot contain spaces)
    names = ["client1_observation_pose",
             "client1_intermediate_pos",
             "drop_positions_of_client1",
             "pick_positions_of_client2",
             "client2_intermediate_pos",
             "drop_positions_of_client2"]

    # function execute when position is given [function, args...]
    function = [[nothing],
                [nothing],
                [client1.release_with_tool],
                [client2.grasp_with_tool],
                [nothing],
                [client2.release_with_tool]]

    # client from which the position is taken
    client = [client1, client1, client1, client2, client2, client2]

    for question_index in range(len(questions)):
        input(questions[question_index])
        print('data joint : ', client[question_index].get_joints())
        joints_pose_dict[names[question_index]] = client[question_index].get_joints()
        function[question_index][0]()
        client[question_index].set_learning_mode(True)

    client1.move_joints(*sleep_joints)
    client2.move_joints(*sleep_joints)
    client2.set_learning_mode(True)
    client1.set_learning_mode(True)

    return joints_pose_dict

# - Useful functions

def create_new_workspace():
    print('Setting a new workspace : ')
    points = []
    id_point = 1

    for id_point in range(4):  # Iterating over 4 markers
        input("Press enter when on point".format(id_point + 1))
        # Getting pose
        points.append(client1.get_pose())
    input("Equip the operating tool")

    # Creating workspace
    client1.save_workspace_from_robot_poses(workspace_storage, *points)


# load all the robots pose or ask for new ones
def load_saved_joint_poses():
    file_path = os.path.join(os.getcwd(), conf_file_name)

    saved_joints_poses = load_yaml(file_path)
    if saved_joints_poses:
        print('setup positions retrieved from {} file'.format(conf_file_name))
    else:
        print('{} file not found ... asking for new setup positions'.format(conf_file_name))
        saved_joints_poses = ask_position()  # ask for new pose
        save_yaml(file_path, saved_joints_poses)
    return saved_joints_poses


# save dictionary in yaml
def save_yaml(path_, dict_):
    with open(path_, 'w') as f:
        yaml.dump(dict_, f, default_flow_style=False)


# load dictionary from yaml
def load_yaml(path_):
    if os.path.exists(path_):  # check if file exists
        if os.stat(path_).st_size == 0:  # check if file not empty
            saved_items = {}
        else:
            with open(path_, 'r') as f:
                saved_items = yaml.safe_load(f)
        return saved_items
    else:
        print("Empty or missing file: {}".format(path_))
        return {}

def main():
    print("I get here 1")
    saved_joint_poses = load_saved_joint_poses()  # load all the robots poses
    print("I get here 2")
    client1.release_with_tool()
    client2.release_with_tool()

    ws_list = client1.get_workspace_list()
    if workspace_storage not in ws_list:
        print('Error : ', workspace_storage, 'not found in robot1 workspace list..')
        create_new_workspace()

    main_loops = RobotsMains(client1, client2, workspace_storage, saved_joint_poses)
    main_loops.run()

def nothing():
    pass


# - Start Flag

def reset():  # delete saved pose
    print("reset saved positions ...")
    if conf_file_name in os.listdir("."):
        os.remove(conf_file_name)


flags = {
    "--reset": reset
}

if __name__ == '__main__':

    # argument parsing
    for av in sys.argv[1:]:
        if av in flags:
            flags[av]()
        else:
            print("unknown flag: ", av)

    client1 = NiryoRobot(robot1_ip_address)
    client2 = NiryoRobot(robot0_ip_address)

    calib_thread_r1 = Thread(target=client1.calibrate, args=[CalibrateMode.AUTO, ])
    calib_thread_r2 = Thread(target=client2.calibrate, args=[CalibrateMode.AUTO, ])
    calib_thread_r1.start()
    calib_thread_r2.start()
    calib_thread_r1.join()
    calib_thread_r2.join()


    client1.update_tool()
    client2.update_tool()
    print("I get here 0")
    main()

    
## Connect to robot & calibrate
#robot1 = NiryoRobot(robot1_ip_address)
#robot0 = NiryoRobot(robot0_ip_address)
#
#robot1.set_brightness(brightness_level)
#robot1.set_contrast(contrast_level)
#
#robot1.calibrate_auto()
#robot0.calibrate_auto()
## Move joints
##robot.move_joints(0.0, 0.151, -0.487, 0.047, 0.000, -0.129)
#robot1.move_joints(position_storage_observer_robot1)
#robot1.wait(3)
#print(robot1.get_workspace_list())
#obj_found, shape_ret, color_ret = robot1.vision_pick('STORAGE_WORKSPACE_NEW',
#                                                    height_offset=0.0,
#                                                    shape=ObjectShape.ANY,
#                                                    color=ObjectColor.ANY)
#
#robot1.move_joints(position_over_con1_robot1)
#robot1.release_with_tool()
#robot1.grasp_with_tool()
##start conveyer belt 1
#conveyor_id_1 = robot1.set_conveyor()
#robot1.run_conveyor(conveyor_id_1, speed=100, direction=ConveyorDirection.FORWARD)
#
#robot1.wait(7.5)
#robot1.stop_conveyor(conveyor_id_1)
#
#robot0.move_joints(position_con1_pickup_robot0)
#robot0.grasp_with_tool()
#robot0.execute_registered_trajectory('con1_to_unload')
#robot0.move_joints(position_unload_robot0)
#robot0.release_with_tool()
#robot0.execute_registered_trajectory('unload_to_con1')
#
#robot0.move_to_home_pose()
#robot1.move_to_home_pose()
## Stop TCP connection
#robot1.close_connection()
#robot0.close_connection()


#Note to myself

#self.client1.control_conveyor #ændre client1 til parameter
#best possible vision settings when starting
#add gracefull killer
#optimize time to pickup between robots
#randomize placearea 