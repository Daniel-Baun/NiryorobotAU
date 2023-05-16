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
from main import match_table_ref_to_robots
from settings import * 
from DB_functions import *
from time_func import *

conveyor_id = ConveyorID.ID_1

class RobotsMains:
    def __init__(self, robot1, robot0, workspace, saved_joints_poses, DB_conn):
        self.saved_joints_poses = saved_joints_poses

        self.client1 = robot1
        self.client2 = robot0

        self.client1.set_brightness(brightness_level)

        self.conveyor_lock = Lock()

        self.workspace = workspace
        self.conveyor_id = conveyor_id
        self.DB_conn = DB_conn
        self.cursor = DB_conn.cursor()

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
        print("Robot1 loop start")
        self.client.update_tool() 
        self.client.release_with_tool()
       
        self.client.move_joints(*self.saved_joints_poses["client1_observation_pose"])
        while True:
            self.client.wait(0.2)
            if (is_order_waiting(self.parent.cursor)):
                data = pop_queue(self.parent.cursor)
                print(data, type(data))
                if not(data == None):
                    self.client.wait(0.5) #delay to get database queue
                    local_shape, local_color = match_table_ref_to_robots(data[1])
                    update_order_status(self.parent.cursor, self.parent.DB_conn, int(data[0]), "PROCESSING")


                    #Robot1 needs to start connected conveyor belt and starts to look after possible pickups        
                    self.client.vision_pick(workspace_storage, z_offset, shape=local_shape,
                                                                color=local_color)
                    write_time_to_csv(csvfilename)
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
                    self.client.wait(10)    
                    self.client.move_joints(*self.saved_joints_poses["client1_observation_pose"])

                    self.client.wait(0.2)
                self.client.wait(1)

class Robot0(RobotLoop):
    def __init__(self, client, parent):
        super().__init__(client, parent)
        placement_counter = 0
        self.placement_counter = placement_counter


    def modulo_place_pos(self):
        # iterate over the 9 possible positions using modulo and incrementing the placement_counter
        if self.placement_counter%9 == 0:
            self.placement_counter = 0
        self.client.move_joints(self.saved_joints_poses[f"drop_position_{self.placement_counter}_robot0"])
        self.placement_counter += 1

    def robot_loop(self):
        print("Back Ned loop start")
        self.client.update_tool()
        self.client.release_with_tool()
        sensor_pin_id = PinID.DI5
        while True:
            if (is_order_processing(self.parent.cursor)):
                data = finished_order(self.parent.cursor)
                if not(data == None):
                    while self.client.digital_read(sensor_pin_id) == PinState.HIGH:
                        self.client.wait(0.2)
                    self.client.wait(0.8)
                    print("Counter is: ", self.placement_counter)
                    print("locked robot0 ", {self.conveyor_lock.locked()})    
                    self.conveyor_lock.acquire()
                    print("is locked robot0 ", {self.conveyor_lock.locked()})
                    self.parent.conveyor_controller(0)
                    self.client.move_joints(*self.saved_joints_poses["pick_positions_of_client2"])
                    self.client.grasp_with_tool()
                    self.client.move_joints(self.saved_joints_poses["client2_intermediate_pos"])
                    self.modulo_place_pos()
                    self.client.release_with_tool()

                    self.conveyor_lock.release()
                    print("unlocked robot0 ", {self.conveyor_lock.locked()})    
                    print(data, type(data))
                    update_order_status(self.parent.cursor, self.parent.DB_conn, int(data[0]), "DONE")
                    write_time_to_csv(csvfilename)
                    self.client.wait(0.2)
                    self.client.move_joints(self.saved_joints_poses["client2_intermediate_pos"])
        
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

def main_robot():
    print("I get here 1")
    saved_joint_poses = load_saved_joint_poses()  # load all the robots poses
    print("I get here 2")
    client1.release_with_tool()
    client2.release_with_tool()
    DB_conn = psycopg2.connect(database = "main_db", user = "au682915", password = "admin", host = "localhost", port = "5432")
    ws_list = client1.get_workspace_list()
    if workspace_storage not in ws_list:
        print('Error : ', workspace_storage, 'not found in robot1 workspace list..')
        create_new_workspace()

    main_loops = RobotsMains(client1, client2, workspace_storage, saved_joint_poses, DB_conn)
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
    main_robot()

#Note to myself

#self.client1.control_conveyor #ændre client1 til parameter
#best possible vision settings when starting
#add gracefull killer
#optimize time to pickup between robots
#Add antal orderer, så vi bruger no_product til fetch funktionen
#Turn and use height ?

#Done
#Rette pick position for robot0 på con1
#randomize placearea - placearea is now in a 3x3 box
#add check connetion robotloop1 med kun connection og ikke credentials på login