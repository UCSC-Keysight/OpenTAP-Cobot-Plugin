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
    python3-pip

RUN echo "Installing OpenTAP packages..."
RUN tap package install TUI
RUN tap package install Python

RUN echo "Optional Flags..."
COPY ./.resources/*.TapPlan /environment/testPlans/
COPY ./.resources/Settings/* /opt/tap/Settings/Bench/Default/
COPY ./scripts/* /environment/scripts/

CMD ["/bin/bash"]

