FROM opentapio/opentap:9.19.5-bionic-slim

RUN echo "Creating working directory..."
WORKDIR /opt/tap
COPY ./openTapPlugin /opt/tap/Packages/UR3e/

RUN echo "Installing necessary dependencies..."
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN echo "Installing OpenTAP packages..."
RUN tap package install TUI
RUN tap package install Python
CMD ["/bin/bash"]

