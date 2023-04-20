from opentap import *
from System import Double, String
import OpenTap
import socket
import time
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
                command = command + '\n'

                # get target joint positions
                target_pos_list = command.split("[")[1]
                target_pos_list = target_pos_list.split("]")[0]
                target_pos_list = target_pos_list.split(",")
                target_pos_list = [round(float(i), (5)) for i in target_pos_list]
                
                # send command
                self.log.Info(f"Sending command {command!r}")
                client_socket.sendall(command.encode())

                # read joint positions until they equal target joint positions
                start = time.time()
                while True:
                    new_message = client_socket.recv(4096)
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


                    if (time.time() - start) > 10: # allow 10 seconds before timeout
                        self.log.Info("Request timed out")
                        break        
                
            except socket.error as e:
                self.log.Error("Send command failed. Error: {}".format(e))
                return None

        if new_message:
            client_socket.close()
            return new_package
        else:
            self.log.Error("No response message received.")
            client_socket.close()
            return None

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
                    if (cur_command[-1] != '\n'):
                        cur_command = cur_command + '\n'
                    self.log.Info(f"Sending command {cur_command!r}")
                    client_socket.sendall(cur_command.encode())
                    response = client_socket.recv(1024)
                    self.log.Info(f"Client received: {response!r}")      

            except socket.error as e:
                self.log.Error("Send command failed. Error: {}".format(e))
                return False

        if response:
            # Not sure how to deserialize response.
            # Nothing in documentation about its encoding.
            # https://forum.universal-robots.com/t/how-do-i-deserialize-response-messages-from-the-controller/26537
            self.log.Warning("This response is serialized.")
            client_socket.close()
            return True
        else:
            self.log.Error("No response message received.")
            client_socket.close()
            return False


    def Open(self):
        """Called by TAP when the test plan starts."""
        self.log.Info("UR3e Instrument Opened")

    def Close(self):
        """Called by TAP when the test plan ends."""
        self.log.Info("UR3e Instrument Closed")
