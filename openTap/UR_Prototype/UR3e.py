from System import String, Double
from opentap import *
import OpenTap
from OpenTap import Display, Output, Input
import socket
import time
import tkinter as tk
from .package import *
from threading import Thread


@attribute(OpenTap.Display("UR3e", "UR3e driver.", "UR_Prototype"))
class UR3e(Instrument):
    """
    UR3e is a class representing a driver for the UR3e collaborative robot.
    """
    
    ip_address = property(String, "192.168.56.101")\
        .add_attribute(OpenTap.Display("IP Address", "The static IP address of the UR3e cobot."))

    def __init__(self):
        super(UR3e, self).__init__()
        self.Name = "UR3e"

        self._connection = None
        self.joint_values = []
        self.target_position_command = ""
        self.initial_position_command = ""
        self.InputValue = Input[String]()


    def connect_to_cobot(self) -> socket.socket:
        """
        Connects to the UR3e2 cobot using its IP address and port number.

        Returns:
            socket.socket: A socket object representing the connection to the cobot, or None if the connection failed.
        """

        HOST = self.ip_address
        PORT = 30002

        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.settimeout(4)
            self.log.Info(f"Connecting with {self.ip_address}:{PORT}")
            connection.connect((HOST, PORT))
            return connection
        except (socket.timeout, socket.error) as e:
            self.log.Error(f"Could not connect to {HOST}:{PORT}. Error: {e}")
            return None


    # I think Python is prematurely closing the connection made in constructor.
    def is_connected(self) -> bool:
        """
        Checks if the instrument is connected to the cobot and attempts to reconnect if not.

        Returns:
            bool: True if the connection is established, False otherwise.
        """

        if self._connection is None:
            self._connection = self.connect_to_cobot()
            if self._connection is None:
                self.log.Error("Reconnection failed. Aborting command.")
                return False


    def allclose(self, a, b, atol=0.00001) -> bool:
        """
        Checks if all elements in two lists are approximately equal within a given tolerance.

        Args:
            a (list): First list of values.
            b (list): Second list of values.
            atol (float, optional): Absolute tolerance for comparing elements. Defaults to 0.00001.

        Returns:
            bool: True if all elements in the two lists are approximately equal, False otherwise.
        """
        return all(abs(x - y) <= atol for x, y in zip(a, b))


    def send_request_movement(self, command) -> Package:
        """
        Sends a movement command to the cobot and waits for the movement to complete.

        Args:
            command (str): A string containing the movement command.

        Returns:
            Package: A Package object containing the robot state information.
        """

        if self.is_connected() == False:
            return None

        try:

            # Sends command to cobot.
            command += '\n'
            self.log.Info(f"Sending command {command!r}")
            self._connection.sendall(command.encode())

            # Usage in send_request_movement:
            is_finished = False
            while is_finished == False:
                target_position = self.get_target_position()
                current_position = self.get_current_position()
                print(f"target: {target_position}, current: {current_position}")
                if self.allclose(target_position, current_position):
                    is_finished = True

            # Return robot state information for data acquisition.
            robot_state = 16
            new_package = self.receive_package(robot_state)
            return new_package

        except socket.error as e:
            self.log.Error(f"Send command failed. Error: {e}")
            return None
    

    def receive_package(self, target_package_type) -> Package:
        """
        Receives a package from the cobot matching the specified package type.

        Args:
            target_package_type (int): The package type to receive.

        Returns:
            Package: A Package object containing the deserialized data.
        """

        while True:
            new_message = self._connection.recv(2048)
            new_package = Package(new_message)

            if new_package.type == target_package_type:
                return new_package


    def get_current_position(self) -> list:
        """
        Retrieves the current position of the cobot.

        Returns:
            list: A list of joint positions.
        """

        if self.is_connected() == False:
            return None
        
        robot_state = 16
        new_package = self.receive_package(robot_state)
        joint_data = new_package.get_subpackage("Joint Data")

        q_actual_list = []
        for i in range(1, 7):
            q_actual = getattr(joint_data.subpackage_variables, f"Joint{i}_q_actual")
            q_actual_list.append(round(q_actual, 5))
        
        return q_actual_list
    

    def get_target_position(self) -> list:
        """
        Retrieves the target position of the cobot.

        Returns:
            list: A list of target joint positions.
        """

        if self.is_connected() == False:
            return None
        
        robot_state = 16
        new_package = self.receive_package(robot_state)
        joint_data = new_package.get_subpackage("Joint Data")

        q_target_list = []
        for i in range(1, 7):
            q_target = getattr(joint_data.subpackage_variables, f"Joint{i}_q_target")
            q_target_list.append(round(q_target, 5))
        
        return q_target_list


    def seek_target_position(self) -> str:
        """
        Launches a GUI for the user to manually adjust the cobot's joint positions and capture the 
        target position. Once completed, the robot will return to it's initial position before 
        function was called.

        Details:
            Every button press modifies related joint value, dynamically generates URScript
            source code using joint values then send the command to the robot.

        Returns:
            str: A string containing the target position URScript command.
        """
        
        self.joint_values = self.get_current_position()
        self.initial_position = self.get_current_position()

        # Create the main window
        root = tk.Tk()
        root.title("Modify Joint Values")
        root.geometry("400x300")
        root.resizable(True, True)

        # Create a frame to hold the buttons
        button_frame = tk.Frame(root)
        button_frame.pack(expand=True, fill=tk.BOTH)

        # Define button appearance settings
        button_bg = "light gray"
        button_fg = "black"
        button_relief = "raised"

        # Joint names
        joint_names = ["Base", "Shoulder", "Elbow", "Wrist 1", "Wrist 2", "Wrist 3"]

        # Create the joint value controls
        self.joint_entries = []  # To keep track of the entries

        # Create the joint value controls
        for idx, joint_name in enumerate(joint_names):
            label = tk.Label(button_frame, text=joint_name)
            label.grid(row=idx, column=0, padx=(10, 0), pady=(10, 0), sticky='w')

            minus_button = tk.Button(button_frame, text="-", command=lambda idx=idx: self.decrement_joint(idx), width=5, height=1, bg=button_bg, fg=button_fg, relief=button_relief)
            minus_button.grid(row=idx, column=1, padx=(10, 5), pady=(10, 0))

            plus_button = tk.Button(button_frame, text="+", command=lambda idx=idx: self.increment_joint(idx), width=5, height=1, bg=button_bg, fg=button_fg, relief=button_relief)
            plus_button.grid(row=idx, column=2, padx=(5, 10), pady=(10, 0))

            # Add an Entry to input the state of the joint, input formatted to 6 sigfigs
            formatted_joint_value = "{:.6f}".format(self.joint_values[idx])
            state_entry = tk.Entry(button_frame)
            state_entry.insert(0, formatted_joint_value)  # Insert the initial value
            state_entry.grid(row=idx, column=3, padx=(10, 0), pady=(10, 0), sticky='w')

            # Bind a function to the <Return> event
            state_entry.bind('<Return>', lambda event, idx=idx: self.update_joint_from_entry(idx))

            self.joint_entries.append(state_entry)  # Store the entry

        # Create the Capture button
        capture_button = tk.Button(button_frame, text="Capture", command=lambda: self.capture(root), width=10, height=2, bg=button_bg, fg=button_fg, relief=button_relief)
        capture_button.grid(row=6, column=1, padx=10, pady=20)

        root.mainloop()
        return self.target_position_command


    def increment_joint(self, index):
        """
        Increments the joint value at the given index and sends the updated joint positions to the cobot.
        Generate programmatically generate a URScript command with joints then send it.

        Args:
            index (int): The index of the joint value to increment.
        """

        self.joint_values[index] += 0.1
        seek_command = f"movej({self.joint_values}, v=1.0, a=1.0)\n"
        print(seek_command)
        self.send_request_movement(seek_command)

        # Update the entry for this joint
        formatted_joint_value = "{:.6f}".format(self.joint_values[index])
        self.joint_entries[index].delete(0, tk.END) 
        self.joint_entries[index].insert(0, formatted_joint_value) 



    def decrement_joint(self, index):
        """
        Decrements the joint value at the given index and sends the updated joint positions to the cobot.

        Args:
            index (int): The index of the joint value to decrement.
        """

        self.joint_values[index] -= 0.1
        print(self.joint_values)
        seek_command = f"movej({self.joint_values}, v=1.0, a=1.0)\n"
        print(seek_command)
        self.send_request_movement(seek_command)

        # Update the entry for this joint
        formatted_joint_value = "{:.6f}".format(self.joint_values[index])
        self.joint_entries[index].delete(0, tk.END)  
        self.joint_entries[index].insert(0, formatted_joint_value)  

    def update_joint_from_entry(self, index):
        """
        Updates the joint value at the given index with the value entered in the corresponding Entry widget and sends the updated joint positions to the cobot.

        Args:
            index (int): The index of the joint value to update.
        """

        # Get the text from the Entry widget and convert it to a float
        try:
            new_value = float(self.joint_entries[index].get())
        except ValueError:
            print(f"Invalid input: {self.joint_entries[index].get()}")
            return

        self.joint_values[index] = new_value
        seek_command = f"movej({self.joint_values}, v=1.0, a=1.0)\n"
        print(seek_command)
        self.send_request_movement(seek_command)



    def capture(self, root):
        """
        Captures the target position command and sends the initial position command to the cobot.

        Args:
            root (tk.Tk): The root Tkinter window.
            initial (list): The initial position of the cobot.
        """

        self.target_position_command = f"movej({self.joint_values}, v=1.0, a=1.0)\n"
        initial_position_command = f"movej({self.initial_position}, v=1.0, a=1.0)\n"
        print(f"Initial: {initial_position_command}, target:{self.target_position_command}")

        # Potential bug:
        # Caller goes out of scope before callee can finish.
        # This needs to be handled better.
        self.send_request_movement(initial_position_command)
        time.sleep(5)

        root.destroy()
        

        
        
