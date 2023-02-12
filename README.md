# OpenTAP-Cobot-Plugin

### Overview

- This file provides technical documentation related to UCSC-Keysight's software development project that seeks to create OpenTAP plugins to control Universal Robots' _(UR)_ cobot model UR3e.
- These plugins are loosely being designed to potentially extend to other cobots in the future.
- The immediate purpose of these plugins will tentatively be used in 6G testing as described [here](https://gist.github.com/Shawn-Armstrong/8018e24419fa095ff15e1e2458042c8a).

## Usage

The following demonstration controls the cobot with OpenTAP using Keysight's Pathwave editor. The cobot moves to the specified location using the test step's URScript field at the execution of the test plan. 

- Clicking on the image will increase the resolution.

<kbd>![demonstration1](https://user-images.githubusercontent.com/80125540/217394032-08fd0b76-ed92-4a0b-8130-967558308db0.gif)</kbd>

## Setup

### Requirements

- [Python3](https://www.python.org/downloads/)
- [OpenTAP](https://opentap.io/downloads)
- [Git](https://git-scm.com/downloads)
- [UR Simulator](https://gist.github.com/Shawn-Armstrong/bbb2615abd917efc958c7fce714b0d46#ur-simulator-setup)

### Instructions

1. Start the UR simulator, create a UR3e instance then activate the cobot.

   <kbd>![setup1](https://user-images.githubusercontent.com/80125540/217388958-6d24335a-eda0-4a0d-95fa-1f553773d3dc.gif)</kbd>

2. [Download](https://opentap.io/downloads) and install OpenTAP for your system.
3. Perform the following version control actions within a new directory on your Desktop.

   ```Console
   git clone https://github.com/UCSC-Keysight/OpenTAP-Cobot-Plugin.git
   cd OpenTAP-Cobot-Plugin
   git fetch origin
   git checkout -b fix/refactor-project origin/fix/refactor-project
   ```

4. Perform the following build procedure inside the new directory:

   ````Console
   dotnet build
   bin\tap.exe editor
   ````

5. Setup and configure the test plan within the GUI with the following actions:
   
   <kbd>![setup2](https://user-images.githubusercontent.com/80125540/217393507-60ff4c8d-f3f6-4d1b-ad6c-fcbdd60e667c.gif)</kbd>

### Package Deployment
This plugin can be compressed into a package after setup, if desired, with the following steps:
  
```
bin\tap.exe package create 
./package.xml
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

The prototype only uses an instrument named `URe3` and a test step `MoveCobot`.

#### `URe3`
- A tool responsible for performing a conditioning action to the DUT; namely, modifying its location via the cobot arm. 
- Object strictly encapsulates logic related to this responsibility.
  - Implements `send_move_request()` which is used to modify the state of the cobot given an **arbitrary** move command. 
  - Implements logic used to display it's information on the GUI.
  
#### `MoveCobot`
- Instantiates a `URe3` object
- Implements logic used to collect URScript input from the end-user stored in `command`.
- Invokes the `URe3` function `send_move_request(command)`

#### `send_request_movement()`
- Creates a TCP socket connection.
- Sends requests to URe3 internal server.
- Receives response back from URe3 internal server.

## Bugs / Project Concerns

- [ ] [`send_request_movement()` prompts safety conflict.](https://user-images.githubusercontent.com/80125540/217407574-28cf2437-9097-4cba-8775-604fce77fcfb.gif)
- [ ] [Response is serialized.](https://user-images.githubusercontent.com/80125540/217407909-2838d182-68f7-482d-81b1-037fc5f79d53.png)
- [X] [UR ROS2 Driver's simulator fails.](https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver/issues/588)
- [ ] Optimize `bin` directory so that build generated files do not clutter tree object during version control commits. 
