#!/bin/bash
cd openTap && ./build.sh
cd ../urHandler && ./build.sh
cd .. && docker-compose run --rm openTapController
