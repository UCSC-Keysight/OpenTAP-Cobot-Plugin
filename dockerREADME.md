# Docker Setup Steps

Added files in changelog:
    docker-compose.yaml
    runall.sh
    openTap/
        .resources/
            fluxbox/
                apps (formats editor x to full screen and applies startup)
                startup (starts editor x and begins flux)
            Settings/ (Handles default settings for Editor/TUI)
                Connections.xml
                DUTs.xml
                Instruments.xml (Defaults UR3e instrument on bench with IP: 192.168.56.101)
        scripts/
            container_startup.sh (Sets up VNC Server and calls x11vnc_entrypoint.sh)
            runTestPlans.sh (Reads through the /environment/testPlans/ folder and runs each testplan iteratively outputting logs)
            x11vnc_entrpoiny.sh (Links vnc to fluxbox in /usr/bin/fluxbox including additional setup)
        build.sh (Builds the opentap base image)
        Dockerfile (Setup steps for opentap base image)
        DockerfileVNC (Setup steps for opentap flux extension image)
    urHandler/ (Builds the basic urHandler image)

runall.sh script manual page

runall.sh [bigl:d:f:o:] (Automation script for setting up OpenTAP/UR Sim/ROS2 (TBD))
    -b force builds containers instead of pulling from Docker Hub
    -i Opens an interactive shell to the opentap container
    -g Opens editor GUI within the opentap container hosted on a VNC webserver (Also includes environment dir with testplans and scripts)
    -l @<license-server-ip> Creates an env variable for the LM_LICENSE_FILE
    -f <file1> <file2> <fileN> Transfers 1 or more testplan files to the container to be automatically run (Unless -i or -g is set)
    -d <dir> Moves all testplan files within directory to the container be automatically run (Unless -i or -g is set)
    -o set output directory for test data and testplan logs (to be implemented)

By default runall.sh pulls images from Docker Hub on the ucsckeysight account, including -d or -f with the interactive shell or gui does not automatically run the testplans, but instead imports them to the environment directory to prevent override in stdout.


