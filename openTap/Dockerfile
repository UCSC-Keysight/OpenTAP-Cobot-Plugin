FROM opentapio/opentap:9.19.5-bionic-slim

ARG OUTPUT
ARG FILES
ARG GUI

RUN echo "Creating working directory..."
WORKDIR /environment/

RUN echo "Installing necessary dependencies..."
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    vim

RUN echo "Installing OpenTAP packages..."
RUN tap package install Python

# COPY ./openTapPlugin /opt/tap/Packages/UR3e/
# COPY ./.resources/Settings/* /opt/tap/Settings/Bench/Default/
# COPY ./scripts/* /environment/scripts/
#COPY ./.resources/*.TapPlan /environment/testPlans/
CMD ["/bin/bash"]