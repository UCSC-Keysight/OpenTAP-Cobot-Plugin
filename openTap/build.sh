#!/bin/bash
docker build -t ucsc-keysight/opentap:$(uname -m) . > /dev/null
