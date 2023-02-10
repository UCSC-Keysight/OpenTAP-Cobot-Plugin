import OpenTap
from .UR3e import UR3e
from System.Xml.Serialization import XmlIgnore
import System.Xml
from System import Array, Double, Byte, Int32, String, Boolean
import System
import System.IO
from System.Text import StringBuilder
from OpenTap import Log, DisplayAttribute, Display, Output, Unit, OutputAttribute, UnitAttribute, AvailableValues, EnabledIfAttribute, FilePathAttribute, FilePath
import math
from opentap import *
from System.Collections.Generic import List
import sys
import opentap
import clr



clr.AddReference("System.Collections")

@attribute(OpenTap.Display("Command From File", "UR_Prototype"))
class CommandCobot(TestStep):
    UR3e_cobot = property(UR3e, None).\
        add_attribute(OpenTap.Display(
<<<<<<< HEAD
            "Cobot", "Resources"))
    FilePath = property(String, "")\
        .add_attribute(FilePath(FilePathAttribute.BehaviorChoice.Open, ".txt"))\
        .add_attribute(Display("File Path", "Gets File Path filled with UR commands", "UR Script", -1, True))

    # file = open(FilePath, "r")
    # listCommands = file.readlines()
    # for line in listCommands:
    #     Command = property(String, line)\
    #         .add_attribute(Display("Command", "This command gets sent to the UR Cobot", "UR Script", -1, True))

    def __init__(self):
        super(CommandCobot, self).__init__()
        # Converts the given File Path object into a string
        # self.sb = StringBuilder()

=======
            "Instrument", "The instrument to use in the step.", "Resources"))

 #   FilePath = property(String, "")\
 #       .add_attribute(FilePath(FilePathAttribute.BehaviorChoice.Open, ".txt"))\
 #       .add_attribute(Display("File", "Gets file contents and sends it to the UR Cobot", "UR Script", -1, True))

    # will have to replace this with the FilePath type that OpenTAP uses.
    file = open("D:\\Program Files\\OpenTAP\\Packages\\OpenTAP-Cobot-Plugin\\test.txt", "r")
    listCommands = file.readlines()
    CommandsArray = []
    #make an array of commands from the file
    for line in listCommands:
        CommandsArray.append(property(String, line)\
            .add_attribute(Display("Command", "This command gets sent to the UR Cobot", "UR Script", -1, True)))
    
    def __init__(self):
        super(CommandCobot, self).__init__()
>>>>>>> af44205ca70544fcf9d55c1642ce1290bc28fa9f
        self.Logging = OpenTap.Enabled[String]()

    # This is what is executed when you press "Run Test Plan" on GUI. 
    def Run(self):
        super().Run()
<<<<<<< HEAD
        # Command = property(String, self.FilePath)\
        #     .add_attribute(Display("Command", "This command gets sent to the UR Cobot", "UR Script", -1, True))
        # This sends the command to UR3e Instrument abstraction.
        response_received = self.UR3e_cobot.send_request_movement(self.FilePath)
    
=======

        #loop through the command array
        for curCommand in self.CommandsArray:
            response_received = self.UR3e_cobot.send_request_movement(self.curCommand)

        # This sends the command to UR3e Instrument abstraction.
        #response_received = self.UR3e_cobot.send_request_movement(self.Command)

>>>>>>> af44205ca70544fcf9d55c1642ce1290bc28fa9f
        if response_received == True:
            self.log.Info("URScript received by cobot controller.\n")
            self.UpgradeVerdict(OpenTap.Verdict.Pass)
        else:
            self.log.Info(
                "URScript command not received by cobot controller\n")
            self.UpgradeVerdict(OpenTap.Verdict.Fail)
