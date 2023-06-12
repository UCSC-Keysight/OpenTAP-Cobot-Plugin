from opentap import *
from System import Double, String
import OpenTap
import socket
from .package import *


@attribute(OpenTap.Display("UR3e", "UR3e driver.", "UR_Prototype"))
class UR3e(Instrument):
    ip_address = property(String, "192.168.56.101")\
        .add_attribute(OpenTap.Display("IP Address", "The static IP address of the UR3e cobot."))
    def __init__(self):
        super(UR3e, self).__init__()
        self.Name = "UR3e"

    def connect_to_cobot(self) -> socket.socket:
        """
        Connects to the UR3e2 cobot using its IP address and port number.

        Returns:
            socket.socket: A socket object representing the connection to the cobot, or None if the connection failed.
        """
        HOST = self.ip_address
        PORT = 30002
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.settimeout(4)
            self.log.Info(f"Connecting with {self.ip_address}:{PORT}")
            connection.connect((HOST, PORT))
            return connection
        except (socket.timeout, socket.error) as e:
            self.log.Error(f"Could not connect to {HOST}:{PORT}. Error: {e}")
            return None
    @method(Double)
    
    # DESCRIPTION:    Open socket, connect to cobot, send move command and wait until 
    #                 cobot response indicates target position has been reached. 
    # RETURNS:        The response package from the cobot on successful completion. 
    #                 None if there was no response from the cobot. 
    def send_request_movement(self, command):

        HOST = self.ip_address
        PORT = 30002

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(4)

            self.log.Info("Connecting with {}:{}".format(self.ip_address, PORT))
            try:
                client_socket.connect((HOST, PORT))
            except socket.timeout as e:
                self.log.Error("Timeout error: {}".format(e))
                return None
            except socket.error as e:
                self.log.Error("Could not connect to {}:{} Error: {}".format(HOST, PORT, e))
                return None
            try:
                # get target joint positions
                target_pos_list = command.split("[")[1]
                target_pos_list = target_pos_list.split("]")[0]
                target_pos_list = target_pos_list.split(",")
                target_pos_list = [round(float(i), (5)) for i in target_pos_list]
                
                # send commnad
                command = command + '\n'
                self.log.Info(f"Sending command {command!r}")
                client_socket.sendall(command.encode())  

                # read joint positions until they equal target joint positions
                while True:
                    new_message = client_socket.recv(4096)
                    if not new_message:
                        self.log.Error("Failed to receive message. Error: {}".format(socket.error))
                        break
                    new_package = Package(new_message)
                    # check if robot entered protective stop mode
                    robot_mode_data = new_package.get_subpackage("Robot Mode Data")
                    if robot_mode_data is not None:
                        protective_stop = robot_mode_data.subpackage_variables.isProtectiveStopped
                        if protective_stop:
                            self.log.Error("ERROR: UR3e entered protective stop mode")
                            return None
                    # compare target position with current position
                    joint_data = new_package.get_subpackage("Joint Data")
                    if joint_data is not None:
                        actual_pos_list = [
                            joint_data.subpackage_variables.Joint1_q_actual,
                            joint_data.subpackage_variables.Joint2_q_actual,
                            joint_data.subpackage_variables.Joint3_q_actual,
                            joint_data.subpackage_variables.Joint4_q_actual,
                            joint_data.subpackage_variables.Joint5_q_actual,
                            joint_data.subpackage_variables.Joint6_q_actual
                        ]
                        actual_pos_list = [round(i, 5) for i in actual_pos_list]
                        if actual_pos_list == target_pos_list:
                            self.log.Info("Target position " + str(target_pos_list) + " reached")
                            break

            except socket.error as e:
                self.log.Error("Send command failed. Error: {}".format(e))
                return None

        if new_package:
            client_socket.close()
            return new_package
        else:
            self.log.Error("No response message received.")
            client_socket.close()
            return None


    # DESCRIPTION:    Open socket, connect to cobot, open file, send move commands from each
    #                 line of file to the cobot. Move onto the next move command when target 
    #                 position is reached.
    # RETURNS:        True if response from cobot indicates successful completion. False if 
    #                 no response. 
    def send_request_from_file(self, file_path):

        HOST = self.ip_address
        PORT = 30002

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(4)

            self.log.Info("Connecting with {}:{}".format(self.ip_address, PORT))
            try:
                client_socket.connect((HOST, PORT))
            except socket.timeout as e:
                self.log.Error("Timeout error: {}".format(e))
                return False
            except socket.error as e:
                self.log.Error("Could not connect to {}:{} Error: {}".format(HOST, PORT, e))
                return False
            try:
                self.log.Debug(file_path)
                #Open and parse file
                f = open(file_path, "r")
                all_commands = f.readlines()
                for cur_command in all_commands:
                    # get target joint positions
                    target_pos_list = cur_command.split("[")[1]
                    target_pos_list = target_pos_list.split("]")[0]
                    target_pos_list = target_pos_list.split(",")
                    target_pos_list = [round(float(i), (5)) for i in target_pos_list]

                    # send command
                    if (cur_command[-1] != '\n'):
                        cur_command = cur_command + '\n'
                    self.log.Info(f"Sending command {cur_command!r}")
                    client_socket.sendall(cur_command.encode())

                    # read joint positions until they equal target joint positions
                    while True:
                        new_message = client_socket.recv(4096)
                        if not new_message:
                            self.log.Error("Failed to receive message. Error: {}".format(socket.error))
                            break
                        new_package = Package(new_message)
                        # check if robot entered protective stop mode
                        robot_mode_data = new_package.get_subpackage("Robot Mode Data")
                        if robot_mode_data is not None:
                            protective_stop = robot_mode_data.subpackage_variables.isProtectiveStopped
                            if protective_stop:
                                self.log.Error("ERROR: UR3e entered protective stop mode")
                                return False
                        # compare target position with current position
                        joint_data = new_package.get_subpackage("Joint Data")
                        if joint_data is not None:
                            actual_pos_list = [
                                joint_data.subpackage_variables.Joint1_q_actual,
                                joint_data.subpackage_variables.Joint2_q_actual,
                                joint_data.subpackage_variables.Joint3_q_actual,
                                joint_data.subpackage_variables.Joint4_q_actual,
                                joint_data.subpackage_variables.Joint5_q_actual,
                                joint_data.subpackage_variables.Joint6_q_actual
                            ]
                            actual_pos_list = [round(i, 5) for i in actual_pos_list]
                            if actual_pos_list == target_pos_list:
                                self.log.Info("Target position " + str(target_pos_list) + " reached")
                                break

            except socket.error as e:
                self.log.Error("Send command failed. Error: {}".format(e))
                return False

        if new_message:
            client_socket.close()
            return True
        else:
            self.log.Error("No response message received.")
            client_socket.close()
            return False
        

    # DESCRIPTION:    Open socket, connect to cobot, read message stream from cobot
    #                 until it recieves joint state data.
    # RETURNS:        List of joint state data
    def get_joint_state(self):
        HOST = self.ip_address
        PORT = 30002

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(4)

            self.log.Info("Connecting with {}:{}".format(self.ip_address, PORT))
            try:
                client_socket.connect((HOST, PORT))
            except socket.timeout as e:
                self.log.Error("Timeout error: {}".format(e))
                return False
            except socket.error as e:
                self.log.Error("Could not connect to {}:{} Error: {}".format(HOST, PORT, e))
                return False
            
            # read messages from UR3e until we recieve joint state
            while True:
                new_message = client_socket.recv(4096)
                if not new_message:
                    self.log.Error("Failed to receive message. Error: {}".format(socket.error))
                    break
                new_package = Package(new_message)
                joint_data = new_package.get_subpackage("Joint Data")
                if joint_data is not None:
                    actual_pos_list = [
                        joint_data.subpackage_variables.Joint1_q_actual,
                        joint_data.subpackage_variables.Joint2_q_actual,
                        joint_data.subpackage_variables.Joint3_q_actual,
                        joint_data.subpackage_variables.Joint4_q_actual,
                        joint_data.subpackage_variables.Joint5_q_actual,
                        joint_data.subpackage_variables.Joint6_q_actual
                    ]
                    actual_pos_list = [round(i, 5) for i in actual_pos_list]
                    return actual_pos_list
                
            return False
            

    def Open(self):
        """Called by TAP when the test plan starts."""
        self.log.Info("UR3e Instrument Opened")

    def Close(self):
        """Called by TAP when the test plan ends."""
        self.log.Info("UR3e Instrument Closed")
