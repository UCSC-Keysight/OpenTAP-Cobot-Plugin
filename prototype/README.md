<img src="https://user-images.githubusercontent.com/80125540/211405062-43230a2a-3bdf-41a4-92a3-a0f597187d7b.jpg" align="right">

# OpenTAP_UR_plugin_prototype.md<p></p>

## Overview

- This file provides a technical overview for an OpenTAP plugin prototype used to control a Universal Robot (UR) cobot, model UR3e.
- The primary purpose of this plugin is to demonstrate fundamental software integration aspects; namely, communication between OpenTAP software and Universal Robot's software interface, PolyScope.
- This plugin explores a transmission control protocol (TCP) socket method for establishing a communication layer.

## Usage

<kbd>![prototype_plugin1](https://user-images.githubusercontent.com/80125540/216204712-dafe7ea6-66d4-4154-8ee4-50a126fe13d2.gif)</kbd>

## Design

Critical points:
  - Prototype uses OpenTAP's [class heirarchy](https://doc.opentap.io/Developer%20Guide/Development%20Essentials/#opentap-plugin-object-hierarchy) to instantiate a UR3e instrument object. 
  - A test step object is used to invoke the UR3e instrument object's `send_request_movement()` function.
  - The `send_request_movement()` function establishes TCP client socket connection between OpenTAP and the UR3e's PolyScope.
  - The `send_request_movement()` function sends a request message whose payload contains a URScript[^1] command to move the robot. 
  - The UR3e simulator then sends a response message, presumably an acknowledgment, in what appears to be a serialized format.
 
## Implementation
drafting...

## Whats Next?

- Additional software integration testing needs to be conducted to identify any compatibility issues or inconsistencies in functionality. This will require a closer examination of URScript, it's hardware and any network limitations / vulnerabilities related to OpenTAP. 
- We need to draft a design that'll leverage ROS2 middleware so the system can potentially extrapolate to other cobots.
- We need to draft a design for the plugin's OpenTAP GUI interface that can be later scaled to any cobot.  

## Final Remarks

- The response message sent back from the controller appears to be a formatted byte string that has been serialized. I have been unable to identify an internal UR application protocol interface for deserializing the response which likely contains data related to the sate of the cobot. This could be valuable for future implementations to improve fault tolerance. 

[^1]: URScript is a proprietary language developed by Universal Robots designed to run on their cobot's onboard controller. URScript provides a high-level interface for implementing algorithms as well as controlling the robot's movements, inputs, and outputs. The languages specifications and application protocol interface are documented in the e-series [script manual](https://s3-eu-west-1.amazonaws.com/ur-support-site/115824/scriptManual_SW5.11.pdf). 

