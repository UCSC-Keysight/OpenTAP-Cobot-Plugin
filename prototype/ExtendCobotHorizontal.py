import sys
import opentap
import clr
clr.AddReference("System.Collections")
from System.Collections.Generic import List
from opentap import *

import OpenTap 
import math
from OpenTap import Log, AvailableValues, EnabledIfAttribute

## Import necessary .net APIs
import System
from System import Array, Double, Byte, Int32, String, Boolean
import System.Xml
from System.Xml.Serialization import XmlIgnore

from .UR3e import UR3e

@attribute(OpenTap.Display("Extend Cobot Horizontal", "Moves UR3e cobot to a low horizontal position.", "UR_Prototype"))

class ExtendCobotHorizontal(TestStep): 
    
    UR3e_cobot = property(UR3e, None).\
    add_attribute(OpenTap.Display("Instrument", "The instrument to use in the step.", "Resources"))

    def __init__(self):
        super(ExtendCobotHorizontal, self).__init__()
        
        self.Logging = OpenTap.Enabled[String]()

    def Run(self):
        super().Run()

        response_received = self.UR3e_cobot.send_request_movement()

        if response_received == True:
            self.log.Info("URScript received by cobot controller.\n")
            self.UpgradeVerdict(OpenTap.Verdict.Pass)
        else:
            self.log.Info("URScript command not received by cobot controller\n")
            self.UpgradeVerdict(OpenTap.Verdict.Fail)