import OpenTap
from OpenTap import Log, DisplayAttribute, Display, Output, Unit, OutputAttribute, UnitAttribute, AvailableValues, EnabledIfAttribute
from opentap import *
from .UR3e import UR3e
from System import String, Array, IConvertible, Int32
from System.Collections.Generic import List
import clr
from enum import Enum

clr.AddReference("System.Collections")

@attribute(OpenTap.Display("Move Cobot", "Moves UR3e cobot to the specified location", "UR_Prototype"))
class MoveCobot(TestStep):

    ur3e_cobot = property(UR3e, None).\
        add_attribute(OpenTap.Display("Instrument", "The instrument to use in the step.", "Resources"))
    command = property(String, "movej([0, 0, 0, 0, 0, 0], a=1.2, v=1.05)")\
        .add_attribute(Display("command", "This move command gets sent to the UR Cobot", "UR Script", -1, True))
    
    Mode = property(String, "Seek Mode")\
        .add_attribute(OpenTap.AvailableValues("Available"))\
        .add_attribute(OpenTap.Display("Mode", "Values from Available Values can be selected here.", "Mode"))
    Available = property(List[String], None)\
        .add_attribute(OpenTap.Display("Available Values", "Select which values are available for 'Mode'.", "Mode"))
    C_Choice = property(String, "Joint")\
        .add_attribute(OpenTap.AvailableValues("Commands"))\
        .add_attribute(OpenTap.Display("Movement Choices", "Values from Command choices can be selected here.", "Movement Choices"))
    Commands = property(List[String], None)\
        .add_attribute(OpenTap.Display("Movements", "Select how you want to move the cobot.", "Movements"))


    def __init__(self):
        super(MoveCobot, self).__init__()
        self.Logging = OpenTap.Enabled[String]()
        self.Available = List[String]()
        self.Available.Add("Seek Mode")
        self.Available.Add("URScript Mode")
        self.Commands = List[String]()
        self.Commands.Add("Joint")
        self.Commands.Add("Linear")
        self.Commands.Add("Circular")
        self.Commands.Add("Blend")

    def Run(self):
        super().Run()
        
        if self.Mode == "Seek Mode":
            if self.C_Choice == "Linear":
                self.ur3e_cobot.set_command("movel")
            elif self.C_Choice == "Circular":
                self.ur3e_cobot.set_command("movec")
            elif self.C_Choice == "Blend":
                self.ur3e_cobot.set_command("movep")
            self.command = self.ur3e_cobot.seek_target_position()

        # Sends move command to cobot.
        response_package = self.ur3e_cobot.send_request_movement(self.command)
        if response_package is None:    
            self.UpgradeVerdict(OpenTap.Verdict.Fail)
            return

        robot_state_message = 16
        if response_package.type == robot_state_message:
            self.PublishResult("UR3e", response_package)
            self.UpgradeVerdict(OpenTap.Verdict.Pass)
        else:
            self.log.Info("URScript command not received by cobot.\n")
            self.UpgradeVerdict(OpenTap.Verdict.Fail)


    def PublishResult(self, tableName, package):
        """
            Summary:
                Overrides parent class PublishResult
                Publishes the results of a package to a table with the specified name.

            Details:
                This method takes a package containing subpackages and extracts the
                field names and values from each subpackage. The field names and values
                are then published to a table with the given name.

            Args:
                tableName (str): The name of the table to publish the results to.
                package: The package containing subpackages with field names and
                        values to be published.

            Note:
                The field values are converted to strings and stored as
                System.IConvertible elements in the all_field_values array before
                publishing due to .NET framework constraints. 
        """

        all_field_names = List[String]()
        total_field_values_count = sum(len(subpackage.subpackage_variables) for subpackage in package.subpackage_list)
        all_field_values = Array[IConvertible](total_field_values_count)

        current_index = 0
        for subpackage in package.subpackage_list:
            
            subpackage_field_names = list(subpackage.subpackage_variables._fields)
            for name in subpackage_field_names:
                all_field_names.Add(name)

            # Convert all elements in subpackage_field_values to strings
            subpackage_field_values = list(subpackage.subpackage_variables)
            subpackage_field_values = [str(value) for value in subpackage_field_values]

            for value in subpackage_field_values:
                all_field_values[current_index] = String(value)
                current_index += 1

        self.Results.Publish(tableName, all_field_names, all_field_values)
        
    
