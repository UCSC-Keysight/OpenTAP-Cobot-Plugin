# Docker Setup Steps

1. simply ./runall.sh

This builds all necessary dependencies and sets up the containers through the docker-compose.yaml which will take a few minutes.
 - *For now the computer architecture must be x86_64 as docker expects that tag when building the image in compose.*

Once complete an interactive shell should open with access to the OpenTap container.
 - To access the editor run the command: tap tui
 - Set the UR3e's IP to: 192.168.56.101 under instruments and add it to the testplan.
 - Press F2 to add a test step and add a move cobot plan to the test steps.
 - Press F5 to run.

 In the background another container connected to the same subnet will handle calls to the UR Sim.
  - To access the simulator go to: http://localhost:6080
  - Click on: vnc_auto.html
