# OpenTAP-Cobot-Plugin

### Overview

- This file provides technical documentation related to UCSC-Keysight's software development project that seeks to create OpenTAP plugins to control Universal Robots' _(UR)_ cobot model UR3e.
- These plugins are loosely being designed to potentially extend to other cobots in the future.
- The immediate purpose of these plugins will tentatively be used in 6G testing as described [here](https://gist.github.com/Shawn-Armstrong/8018e24419fa095ff15e1e2458042c8a).

## Usage
- End-user uses OpenTAP plugin to send move commands to the cobot. 
    
 <kbd>![usage](https://user-images.githubusercontent.com/80125540/224439881-c21aa793-5173-42e4-9a26-bb517041b3e3.gif)</kbd>

## Setup

### Requirements

- [Python3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
- [.NET SDK](https://aka.ms/dotnet-download)
- [Google Chrome](https://www.google.com/chrome/)

### Docker Setup (runall.sh)
<pre>

runall.sh script manual page

runall.sh [bigl:d:f:o:] (Automation script for setting up OpenTAP/UR Sim/ROS2 (TBD))
    -b force builds containers instead of pulling from Docker Hub
    -i Opens an interactive shell to the opentap container
    -g Opens editor GUI within the opentap container hosted on a VNC webserver (Also includes environment dir with testplans and scripts)
    -l `@\<license-server-ip\>` Creates an env variable for the LM_LICENSE_FILE
    -f `<file1> <file2> <fileN>` Transfers 1 or more testplan files to the container to be automatically run (Unless -i or -g is set)
    -d `<dir>` Moves all testplan files within directory to the container be automatically run (Unless -i or -g is set)
    -o set output directory for test data and testplan logs (to be implemented)

By default runall.sh pulls images from Docker Hub on the ucsckeysight account. 
Including the -d or -f flags with the interactive shell or gui does not automatically run any testplans, 
but instead imports them to the environment directory to prevent override in stdout.

Initial build time will average from 2-4 minutes, 
after the initial build all further use is cached and instant. 
All environmental variables and imported code is stored via volume mounts and do not interfere with the image itself, but store persistent state.
</pre>

### Instructions

1. Start the UR3e simulator container by opening a console and running the following commands:
     
   ```Console
   docker network create --subnet=192.168.56.0/24 ursim_net
   docker run -it -e ROBOT_MODEL=UR3e --net ursim_net --ip 192.168.56.101 -p 30002:30002 -p 30004:30004 -p 6080:6080 --name ur3e_container universalrobots/ursim_e-series
   ``` 
2. Start the cobot by visiting http://localhost:6080/vnc_auto.html using Google Chrome and performing the following actions:
     
   <kbd>![start_cobot](https://user-images.githubusercontent.com/80125540/224440933-3e993623-81e5-48c1-9858-8629fe25f684.gif)</kbd>

3. Clone this repository in a directory of your choosing then navigate inside its root directory with the following commands:
     
   ```Console
   git clone https://github.com/UCSC-Keysight/OpenTAP-Cobot-Plugin.git
   cd OpenTAP-Cobot-Plugin
   ```
4. Perform the following build procedure inside the root directory; this will create the plugin using the current implementation files and open the editor for testing.
   ````Console
   dotnet build
   bin\tap editor
   ````
5. Test the built plugin using the editor with the following actions:
   - In the OpenTAP editor, click the + icon to add a new test step.
   - In the Pop-up test step window, select UR Prototype > Move Cobot > Add.
   - At the bottom of the window, right click the UR3e instrument, click Configure, and set the IP address as your host network's IPv4 address.
     - As an example, this can be identified on a Windows machine using a console running the command `ipconfig`; it should look something like this:
         
       ![image](https://user-images.githubusercontent.com/80125540/224469661-a78df69b-9ec3-408f-9578-e0a206b92601.png)
   - Click the green play button to run the test plan, and watch the UR3e move.
     
   <kbd>![step4](https://user-images.githubusercontent.com/80125540/224439495-be4a2be1-a2d2-48fb-b36e-d018a18b1af1.gif)</kbd>

### Setup Summary
- This setup is intended to provide a developing environment for plugin developers using OpenTAP's boilerplate for Python projects.
- The `bin` directory is a standalone OpenTAP installation used for streamlined testing. 
- The setup intends for developers to make changes to the implementation files then run `dotnet build` to apply the changes then `bin\tap` to test them in the editor. 
- This setup is preferred because the `.csproj` and `.sln` files assist in managing dependencies during the build process.
- This setup is not intended to be used by customers. Instead, developers will use it to produce a `.TapPackage` outlined in the Packaging section of the document. This package will one day be added to Keysight's package manager so a customer may access it by using `tap package install ur3e`
   
## Packaging

### Creating Package
- This plugin can be compressed into a package after build, if desired, by running the following command:
    
    ```
    bin\tap package create ./package.xml
    ``` 
### Installing Package Manually
- The `.TapPackage` can be installed into an actual OpenTAP installation by navigating to the OpenTAP root directory inside a console and running the following command:
    
     ```Console
     tap package install <path-to-.TapPackage-file>
     ```

### Installing Package with Package Manager
- **In the future**, a package will be added to Keysight's package manager which can be installed by navigating to the OpenTAP root directory inside a console and running the following command:
    
  ```Console
  tap package install ur3e
  ```
  
## Technical Details

### OpenTAP Infrastructure

OpenTAP implements an object hierarchy that plays a critical role in their software architecture.

<kbd>![hierarchy](https://doc.opentap.io/assets/img/ObjectHierarchy.0307a24d.png)</kbd>

The primary purpose of the hierarchy is to enforce modularization that'll encapsulate logic categorically which is used to control, manage and separate responsibilities within their software. There are four main categories that you should be aware of:

1. The **`DeviceUnderTest`** (DUT) class encapsulates logic strictly related to the object we're interested in collecting data about.
2. The **`Instrument`** class encapsulates logic that strictly relates to a physical tool. In general, this logic would implement some functionality that seeks to condition, expose or otherwise measure a parameter related to the DUT.
3. The **`TestStep`** class is the fundamental unit of work; essentially, it is used to tie everything together. OpenTAPs best practices recommend that it performs a single step
4. The **`ResultListener`** class is used to arbitrate the collection and management of data produced by test steps.

### Prototype Implementation

The prototype only uses an instrument named `UR3e` and a test step `MoveCobot`.

#### `UR3e`
- A tool responsible for performing a conditioning action to the DUT; namely, modifying its location via the cobot arm. 
- Object strictly encapsulates logic related to this responsibility.
  - Implements `send_request_movement()` which is used to modify the state of the cobot given an **arbitrary** move command. 
  - Implements logic used to display its information on the GUI.
  
#### `MoveCobot`
- Instantiates a `UR3e` object
- Implements logic used to collect URScript input from the end-user stored in `command`.
- Invokes the `UR3e` function `send_request_movement(command)`

#### `send_request_movement()`
- Creates a TCP socket connection.
- Sends requests to UR3e simulator's internal server.
- Receives response back from UR3e simulator's internal server.
