import OpenTap
from .UR3e import UR3e
from System.Xml.Serialization import XmlIgnore
import System.Xml
from System import Array, Double, Byte, Int32, String, Boolean
import System
from OpenTap import Log, DisplayAttribute, Display, Output, Unit, OutputAttribute, UnitAttribute, AvailableValues, EnabledIfAttribute
import math
from opentap import *
from System.Collections.Generic import List
import sys
import opentap
import clr
clr.AddReference("System.Collections")

@attribute(OpenTap.Display("Get Joint State", "Gets the current joint positions of the UR3e", "UR_Prototype"))
class GetState(TestStep):

    ur3e_cobot = property(UR3e, None).\
        add_attribute(OpenTap.Display(
            "Instrument", "The instrument to use in the step.", "Resources"))
    command = "get_actual_joint_positions()"

    def __init__(self):
        super(GetState, self).__init__()
        self.Logging = OpenTap.Enabled[String]()

    # This is what is executed when you press "Run Test Plan" on GUI. 
    def Run(self):
        super().Run()

        # Begin recieving data from UR3e
        response_received = self.ur3e_cobot.get_joint_state()

        if response_received != False:
            self.log.Info("Joint positions: " + str(response_received))
            self.UpgradeVerdict(OpenTap.Verdict.Pass)
        else:
            self.log.Info("No joint data was obtained.\n")
            self.UpgradeVerdict(OpenTap.Verdict.Fail)
