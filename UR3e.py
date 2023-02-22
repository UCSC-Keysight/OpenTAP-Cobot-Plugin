from opentap import *
from System import Double, String
import OpenTap
import time
from pymodbus.client import ModbusTcpClient
import socket

@attribute(OpenTap.Display("UR3e", "UR3e driver.", "UR_Prototype"))
class UR3e(Instrument):
    IpAddress = property(String, "10.0.0.133")\
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
    def send_request_movement(self, FilePath):
         # Connect to the MODBUS server on the cobot
        client = ModbusTcpClient(self.IpAddress)
        try:
            client.connect()
            #print("Connection Success")
        except Exception as e:
            self.log.Error("Could not connect to cobot. Error: {}".format(e))
            #print("Connection Failed")
            return False
        try:
            # Open and parse file
            f = open(FilePath, "r")
            allCommands = f.readlines()
            for curCommand in allCommands:
                curCommand + '\n'
                self.log.Info(f"Sending command {curCommand!r}")
                # Send the command to the cobot using Modbus function code 6 (write single register)
                register_address = 0
                register_value = curCommand.encode()
                result = client.write_register(address=register_address, value=register_value, unit=0)
                if result.isError():
                    self.log.Error("Error writing register: {}".format(result))
                    #print(curCommand + " command not received")
                    return False
                else:
                    self.log.Info(f"Received Command")
                    print(curCommand + " received command ")
                # Wait for the cobot to process the command
                time.sleep(0.1)
                # Read the response from the cobot using Modbus function code 3 (read holding registers)
                register_address = 1
                register_count = 1
                result = client.read_holding_registers(address=register_address, count=register_count, unit=0)
                if result.isError():
                    self.log.Error("Error reading register: {}".format(result))
                    return False
                response = result.registers[0].to_bytes(2, byteorder='big').decode('utf-8')
                self.log.Info(f"Client received: {response!r}")
        except Exception as e:
            self.log.Error("Error sending command. Error: {}".format(e))
            return False

        client.close()
        return True

    def Open(self):
        """Called by TAP when the test plan starts."""
        self.log.Info("UR3e Instrument Opened")

    def Close(self):
        """Called by TAP when the test plan ends."""
        self.log.Info("UR3e Instrument Closed")
