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

    @method(Double)
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
                    subpackage = new_package.get_subpackage("Joint Data")
                    if subpackage is not None:
                        actual_pos_list = [
                            subpackage.subpackage_variables.Joint1_q_actual,
                            subpackage.subpackage_variables.Joint2_q_actual,
                            subpackage.subpackage_variables.Joint3_q_actual,
                            subpackage.subpackage_variables.Joint4_q_actual,
                            subpackage.subpackage_variables.Joint5_q_actual,
                            subpackage.subpackage_variables.Joint6_q_actual
                        ]
                        actual_pos_list = [round(i, 5) for i in actual_pos_list]
                        if actual_pos_list == target_pos_list:
                            self.log.Info("Target position " + str(target_pos_list) + " reached")
                            break

            except socket.error as e:
                self.log.Error("Send command failed. Error: {}".format(e))
                return None

        if new_message:
            client_socket.close()
            return True
        else:
            self.log.Error("No response message received.")
            client_socket.close()
            return False

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
                        subpackage = new_package.get_subpackage("Joint Data")
                        if subpackage is not None:
                            actual_pos_list = [
                                subpackage.subpackage_variables.Joint1_q_actual,
                                subpackage.subpackage_variables.Joint2_q_actual,
                                subpackage.subpackage_variables.Joint3_q_actual,
                                subpackage.subpackage_variables.Joint4_q_actual,
                                subpackage.subpackage_variables.Joint5_q_actual,
                                subpackage.subpackage_variables.Joint6_q_actual
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
    #                 until it recieves joint state data or 3 seconds have passed.
    # RETURNS:        List of joint state data if recieved, False if no joint data was
    #                 recieved after 3 seconds. 
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
                subpackage = new_package.get_subpackage("Joint Data")
                if subpackage is not None:
                    actual_pos_list = [
                        subpackage.subpackage_variables.Joint1_q_actual,
                        subpackage.subpackage_variables.Joint2_q_actual,
                        subpackage.subpackage_variables.Joint3_q_actual,
                        subpackage.subpackage_variables.Joint4_q_actual,
                        subpackage.subpackage_variables.Joint5_q_actual,
                        subpackage.subpackage_variables.Joint6_q_actual
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
