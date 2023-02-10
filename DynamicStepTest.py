"""
Dynamic Test Step in Python
"""
from System import Type, String
from opentap import *
import OpenTap
from OpenTap import ITestStep, TestStep, IDynamicStep, DisplayAttribute

@attribute(DisplayAttribute, "DynamicTestStepPython", "A dynamic test step in Python.")
class DynamicTestStepPython(TestStep, IDynamicStep):
    NewData = property(String, "")
    NewData2 = property(String, "")

    def __init__(self, data=""):
        super(DynamicTestStepPython, self).__init__() # The base class initializer must be invoked
        self.NewData = "Hello"
        if (data != ""):
            self.NewData2 = self.NewData + data
    
    @method(Type)
    def GetStepFactoryType(self):
        return Type.GetType("DynamicTestStepPython")
    
    @method(ITestStep)
    def GetStep(self):
        return DynamicTestStepPython(self.NewData)
    
    @method()
    def Run(self):
        print("DynamicTestStepPython.Run() -> NewData: %s, NewData2: %s" % (self.NewData, self.NewData2))
        