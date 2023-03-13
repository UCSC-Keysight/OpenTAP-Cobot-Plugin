from opentap import *
from System import Double, String
import OpenTap
import socket

@attribute(OpenTap.Display("UR3e", "UR3e driver.", "UR_Prototype"))
class UR3e(Instrument):
<<<<<<<< HEAD:UR_Prototype/UR3e.py
    ip_address = property(String, "10.0.0.133")\
========
    IpAddress = property(String, "192.168.56.101")\
>>>>>>>> dockerized:openTap/openTapPlugin/UR3e.py
        .add_attribute(OpenTap.Display("IP Address", "The static IP address of the UR3e cobot."))
    def __init__(self):
        super(UR3e, self).__init__()
        self.Name = "UR3e"

    # DESCRIPTION:    Opens socket, connects to cobot, sends request message with URScript payload,
    #                 receives response message then closes socket.
    # PRE-CONDITION:  Argv `command` must be a single line of URScript code that ends with `\n`.
    # POST-CONDITION: Moves cobot to location specified by `command`; afterwards, receives cobot
    #                 response.
    @method(Double)
    def send_request_movement(self, file_path):

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
                    cur_command + '\n'
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
