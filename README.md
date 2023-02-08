# OpenTAP-Cobot-Plugin

#### Overview

- This file provides technical documentation related to UCSC-Keysight's software development project that seeks to create OpenTAP plugins to control Universal Robots' UR3e cobot.

## Usage

The following demonstration controls the cobot with OpenTAP using Keysight's Pathwave editor. The cobot moves to the specified location using the test step's URScript field at the execution of the test plan.

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
3. Open a commandline, navigate to the installed `../OpenTap` root directory then run the following commands:

   ```Console
   tap package install "Editor CE"
   tap package install Python
   tap package install SDK
   ```

4. Navigate to `../OpenTap/Packages` then clone the repository.
   ```Console
   git clone https://github.com/UCSC-Keysight/OpenTAP-Cobot-Plugin.git
   ```
5. Navigate back to the `../OpenTap` root directory then open the editor with the following command:

   ```Console
   tap editor
   ```

6. Setup and configure the test plan within the GUI with the following actions:
   
   <kbd>![setup2](https://user-images.githubusercontent.com/80125540/217393507-60ff4c8d-f3f6-4d1b-ad6c-fcbdd60e667c.gif)</kbd>
   
## Technical Details

### OpenTAP Infrastructure

OpenTAP implements an object hierarchy that plays a critical role in their software architecture.
  
<kbd>![hierarchy](https://doc.opentap.io/assets/img/ObjectHierarchy.0307a24d.png)</kbd>

The primary purpose of the hierarchy is to enforce modularization that'll encapsulate logic categorically which is used to control, manage and separate responsibilities within their software.  

