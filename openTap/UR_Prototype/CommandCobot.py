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
        add_attribute(OpenTap.Display("Cobot", "Resources"))
    #file_path will grab the location of the chosen .txt file. 
    file_path = property(String, "")\
        .add_attribute(FilePath(FilePathAttribute.BehaviorChoice.Open, ".txt"))\
        .add_attribute(Display("File Path", "Gets File Path filled with UR commands", "UR Script", -1, True))

    def __init__(self):
        super(CommandCobot, self).__init__()
        self.Logging = OpenTap.Enabled[String]()

    # This is what is executed when you press "Run Test Plan" on GUI. 
    def Run(self):
        super().Run()
        
        #Sends and records response from UR Bot
        response_received = self.UR3e_cobot.send_request_movement(self.file_path)

        if response_received == True:
            self.log.Info("URScript received by cobot controller.\n")
            self.UpgradeVerdict(OpenTap.Verdict.Pass)
        else:
            self.log.Info(
                "URScript command not received by cobot controller\n")
            self.UpgradeVerdict(OpenTap.Verdict.Fail)