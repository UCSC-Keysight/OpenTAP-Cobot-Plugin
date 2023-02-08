#!/bin/bash
docker build -t ucsc-keysight/urhandler:$(uname -m) . > /dev/null
