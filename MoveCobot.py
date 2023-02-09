import OpenTap
from .UR3e import UR3e
from System.Xml.Serialization import XmlIgnore
import System.Xml
from System import Array, Double, Byte, Int32, String, Boolean
import System
from OpenTap import Log, DisplayAttribute, Display, Output, Unit, OutputAttribute, UnitAttribute, AvailableValues, EnabledIfAttribute, FilePath, FilePathAttribute
import math
from opentap import *
from System.Collections.Generic import List
import sys
import opentap
import clr
clr.AddReference("System.Collections")

@attribute(OpenTap.Display("Move Cobot", "Moves UR3e cobot to the specified location", "UR_Prototype"))
class MoveCobot(TestStep):

    UR3e_cobot = property(UR3e, None).\
        add_attribute(OpenTap.Display(
            "Instrument", "The instrument to use in the step.", "Resources"))
    Command = property(String, "movej([0, 0, 0, 0, 0, 0], a=1.2, v=1.05)")\
        .add_attribute(Display("Command", "This move command gets sent to the UR Cobot", "UR Script", -1, True))
    Command2 = property(String, "")\
        .add_attribute(FilePath(FilePathAttribute.BehaviorChoice.Open, ".txt"))\
        .add_attribute(Display("File", "Gets file contents and sends it to the UR Cobot", "UR Script", -1, True))
        
    

    def __init__(self):
        super(MoveCobot, self).__init__()

        self.Logging = OpenTap.Enabled[String]()

    # This is what is executed when you press "Run Test Plan" on GUI. 
    def Run(self):
        super().Run()

        # This sends the command to UR3e Instrument abstraction.
        # response_received = self.UR3e_cobot.send_request_movement(self.Command)
        response_received = self.UR3e_cobot.send_request_movement(self.Command2)

        if response_received == True:
            self.log.Info("URScript received by cobot controller.\n")
            self.UpgradeVerdict(OpenTap.Verdict.Pass)
        else:
            self.log.Info(
                "URScript command not received by cobot controller\n")
            self.UpgradeVerdict(OpenTap.Verdict.Fail)
