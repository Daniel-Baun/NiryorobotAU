
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
brightness_level = 2  # value between 0.5 and 2 to determine how bright the camera vision is
contrast_level = 0.8 #vaule of the contrast in the camera

# conveyor
conveyor_speed = 50  # speed of the conveyor between 0 and 100
conveyor_place_interval = 1.5  # minimal interval between conveyor places  (in seconds)

