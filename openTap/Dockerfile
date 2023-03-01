FROM opentapio/opentap:9.19.5-bionic-slim

ARG OUTPUT
ARG FILES
ARG GUI

RUN echo "Creating working directory..."
WORKDIR /environment/
COPY ./openTapPlugin /opt/tap/Packages/UR3e/

RUN echo "Installing necessary dependencies..."
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    vim

RUN echo "Installing OpenTAP packages..."
RUN tap package install TUI
RUN tap package install Python
RUN tap package install "Editor X"

RUN echo "Optional Flags..."
COPY ./.resources/*.TapPlan /environment/testPlans/
COPY ./.resources/Settings/* /opt/tap/Settings/Bench/Default/
COPY ./scripts/* /environment/scripts/

#VNC Section
ENV VNC_PASSWD=keysight
# for the VNC connection
EXPOSE 5900
# for the browser VNC client
EXPOSE 5901

RUN git clone --branch v1.2.0 --single-branch https://github.com/novnc/noVNC.git /opt/noVNC
RUN git clone --branch v0.9.0 --single-branch https://github.com/novnc/websockify.git /opt/noVNC/utils/websockify
RUN ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html
RUN apt-get install -y novnc python3-websockify tigervnc-standalone-server x11vnc xvfb net-tools python python-numpy fluxbox
RUN useradd -m -s /bin/bash keysight
RUN echo keysight:keysight | chpasswd
RUN usermod -a -G sudo keysight
USER root

COPY --chown=keysight:users container_startup.sh /opt/container_startup.sh
COPY --chown=keysight:users x11vnc_entrypoint.sh /opt/x11vnc_entrypoint.sh

CMD ["/bin/bash"]