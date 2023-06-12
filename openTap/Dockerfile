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
    vim \
    python3-tk
RUN pip install tabulate

RUN echo "Installing OpenTAP packages..."
RUN tap package install Python

CMD ["/bin/bash"]
