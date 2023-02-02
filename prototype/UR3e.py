from opentap import *
from System import Double, String
import OpenTap
import socket

@attribute(OpenTap.Display("UR3e", "UR3e driver.", "UR_Prototype"))
class UR3e(Instrument):
    IpAddress = property(String, "10.0.0.133")\
        .add_attribute(OpenTap.Display("IP Address", "The static IP address of the UR3e cobot."))
    def __init__(self):
        super(UR3e, self).__init__()
        self.Name = "UR3e"
         
    @method(Double)
    def send_request_movement(self):

        HOST = self.IpAddress
        PORT = 30002

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            
            client_socket.settimeout(4)

            try:
                client_socket.connect((HOST, PORT))
            except socket.timeout:
                return False
            except socket.error:
                return False

            urscript = b"movej([0, 0, 0, 0, 0, 0], a=1.2, v=1.05)\n"

            try:
                client_socket.sendall(urscript)
            except socket.error:
                return False
                
            response = client_socket.recv(1024)

        return True

    def Open(self):
        """Called by TAP when the test plan starts."""
        self.log.Info("UR3e Instrument Opened")

    def Close(self):
        """Called by TAP when the test plan ends."""
        self.log.Info("UR3e Instrument Closed")


